import pandas as pd
import glob
import os

#读取清洗后的最终数据（文件名带 N，按通配符取，避免写死数字）
f = max(glob.glob('cleaned_data_c5_*.csv'), key=os.path.getmtime)
data = pd.read_csv(f)
print(f"读取文件：{f}，共 {len(data)} 行")

#把日期转成时间类型，后面按日统计和判断节假日都要用
data['日期'] = pd.to_datetime(data['日期'])

#========== 1. 基础指标分析 ==========

#（1）运力指标分析 —— 日均订单量：计算每日订单总数的算术平均值
a = data.groupby('日期').size()
avg_day = a.mean()
print(f"（1）日均订单量：{avg_day:.2f} 单/日")
#订单波动系数：标准差 / 平均值，值越大说明订单量越不稳定
cv = a.std() / avg_day
print(f"（1）订单波动系数（标准差/平均值）：{cv:.4f}")

#节假日订单比：节假日期间日均订单量 / 普通日期日均订单量
#说明：题目未提供节假日名单，数据集也不含节假日字段，这里用“固定日期法”按公历月日近似标记：
#元旦(1/1)、春节(1/28-2/4)、清明(4/4-4/6)、劳动节(5/1-5/5)、端午(5/31-6/2)、中秋(10/6)、国庆(10/1-10/7)
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

data['是否节假日'] = data['日期'].apply(is_holiday)
#分别算节假日、普通日期的日均订单量（按“每日订单数”再求均值）
b = data.groupby(['日期', '是否节假日']).size().reset_index(name='订单数')
h_avg = b[b['是否节假日']]['订单数'].mean()
n_avg = b[~b['是否节假日']]['订单数'].mean()
print(f"（1）节假日日均订单量：{h_avg:.2f} 单/日，普通日期日均订单量：{n_avg:.2f} 单/日")
if n_avg and not pd.isna(n_avg):
    print(f"（1）节假日订单比（节假日/普通日期）：{h_avg / n_avg:.4f}")
else:
    print("（1）普通日期样本为空，无法计算节假日订单比")
print("\n")

#（2）收益行为分析 —— 平均客单价：订单总金额 / 总订单数
total_amount = data['订单金额(元)'].sum()
total_cnt = len(data)
print(f"（2）平均客单价：{total_amount / total_cnt:.2f} 元/单（总金额 {total_amount:.2f} 元 / {total_cnt} 单）")
#不同群体消费差异：按年龄段和出行方式分组计算平均订单金额
c = data.groupby(['乘客年龄段', '出行方式'])['订单金额(元)'].mean().round(2)
print(f"（2）不同年龄段与出行方式的平均订单金额：\n{c}")
print("\n")

#（3）服务质量评估 —— 服务评分：5 分制，计算所有有效评分的加权平均值
#先看各评分的订单分布，作为加权平均的权重来源
d = data['服务评分'].value_counts().sort_index()
print(f"（3）各服务评分的订单分布：\n{d}")
#加权平均 = Σ(评分 × 该评分订单数) / Σ订单数，等价于直接用评分列求均值
w = (data['服务评分'] * 1).sum() / len(data)
print(f"（3）服务评分加权平均值（按订单量加权，5 分制）：{w:.2f} 分")
#再分出行方式看服务质量差异，供运营建议引用
print(f"（3）各出行方式的平均服务评分：\n{data.groupby('出行方式')['服务评分'].mean().round(2)}")
print("\n")
