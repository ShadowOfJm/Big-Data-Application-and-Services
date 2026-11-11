import pandas as pd
import glob
import os

#读取清洗后的最终数据（文件名带 N，按通配符取，避免写死数字）
f = max(glob.glob('cleaned_data_c5_*.csv'), key=os.path.getmtime)
data = pd.read_csv(f)
print(f"读取文件：{f}，共 {len(data)} 行")

#把交易日期转成时间类型，后面按日统计和判断节假日都要用
data['交易日期'] = pd.to_datetime(data['交易日期'])

#========== 1. 基础指标分析 ==========

#（1）交易量指标分析 —— 日均交易量：计算每日交易总数的算术平均值
a = data.groupby('交易日期').size()
avg_day = a.mean()
print(f"（1）日均交易量：{avg_day:.2f} 套/日")
#交易量波动系数：标准差 / 平均值，值越大说明交易量越不稳定
cv = a.std() / avg_day
print(f"（1）交易量波动系数（标准差/平均值）：{cv:.4f}")

#节假日交易量比：节假日期间日均交易量 / 普通日期日均交易量
#说明：题目未提供节假日名单，数据集也只有 2023-2025 年且不含法定节假日字段，
#这里用“固定日期法”近似标记：元旦(1/1)、春节(1/28-2/4)、清明(4/4-4/6)、劳动节(5/1-5/5)、
#端午(5/31-6/2)、中秋(10/6)、国庆(10/1-10/7)，跨年份统一套用，属口径近似，报告中需注明
def is_holiday(d):
    md = d.strftime('%m-%d')
    if md == '01-01':
        return True
    if '01-28' <= md <= '02-04':
        return True
    if '04-04' <= md <= '04-06':
        return True
    if '05-01' <= md <= '05-05':
        return True
    if '05-31' <= md <= '06-02':
        return True
    if md == '10-06':
        return True
    if '10-01' <= md <= '10-07':
        return True
    return False

data['是否节假日'] = data['交易日期'].apply(is_holiday)
#分别算节假日、普通日期的日均交易量（按“每日总套数”再求均值）
b = data.groupby(['交易日期', '是否节假日']).size().reset_index(name='套数')
h_avg = b[b['是否节假日']]['套数'].mean()
n_avg = b[~b['是否节假日']]['套数'].mean()
print(f"（1）节假日日均交易量：{h_avg:.2f} 套/日，普通日期日均交易量：{n_avg:.2f} 套/日")
if n_avg and not pd.isna(n_avg):
    print(f"（1）节假日交易量比（节假日/普通日期）：{h_avg / n_avg:.4f}")
else:
    print("（1）普通日期样本为空，无法计算节假日交易量比")
print("\n")

#（2）价格行为分析 —— 套均总价：交易总金额 / 总交易套数
total_price = data['成交总价（万元）'].sum()
total_cnt = len(data)
print(f"（2）套均总价：{total_price / total_cnt:.2f} 万元/套（总金额 {total_price:.2f} 万元 / {total_cnt} 套）")
#不同群体价格差异：按建筑年代和户型分组计算平均成交总价
c = data.groupby(['建筑年代', '房源户型'])['成交总价（万元）'].mean().round(2)
print(f"（2）不同建筑年代与户型的平均成交总价：\n{c}")
print("\n")

#（3）房源竞争力评估 —— 房源特征评分：5 分制，计算所有有效特征（楼层、朝向、装修）的加权平均值
#先把三个文本特征折算成 1-5 分，再按权重加总
d = data.copy()
#楼层分：先取出楼层数字，楼层越高采光越好，按 30 层封顶给分
_floor = d['楼层'].astype(str).str.extract(r'(\d+)').astype(float)[0]
d['楼层分'] = (1 + _floor.clip(upper=30) / 30 * 4).round(2)
#朝向分：南/南北 5 分，东南/西南/东 4 分，西/北 3 分，未知 2 分
def face_score(x):
    x = str(x)
    if x in ('南', '南北'):
        return 5
    elif x in ('东南', '西南', '东'):
        return 4
    elif x in ('西', '北'):
        return 3
    else:
        return 2
d['朝向分'] = d['朝向'].apply(face_score)
#装修分：豪装 5 分，精装 4 分，简装 3 分，毛坯 2 分
def fit_score(x):
    x = str(x)
    if x == '豪装':
        return 5
    elif x == '精装':
        return 4
    elif x == '简装':
        return 3
    else:
        return 2
d['装修分'] = d['装修情况'].apply(fit_score)
#加权平均：朝向权重 0.4（采光影响最大）、装修权重 0.35、楼层权重 0.25，三者合计为 1
w_face, w_fit, w_floor = 0.4, 0.35, 0.25
d['房源特征评分'] = (d['朝向分'] * w_face + d['装修分'] * w_fit + d['楼层分'] * w_floor).round(2)
score = d['房源特征评分'].mean()
print(f"（3）房源特征评分（5 分制，朝向 0.4 / 装修 0.35 / 楼层 0.25 加权）：{score:.2f} 分")
#再分项看看哪个特征拉低了整体分数，供运营建议引用
print(f"（3）分项平均分：朝向 {d['朝向分'].mean():.2f}，装修 {d['装修分'].mean():.2f}，楼层 {d['楼层分'].mean():.2f}")
print(f"（3）各小区房源特征评分：\n{d.groupby('小区名称')['房源特征评分'].mean().round(2)}")
print("\n")
