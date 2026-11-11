import pandas as pd
import glob
import os

#读取清洗后的最终数据（文件名带 N，按通配符取，避免写死数字）
f = max(glob.glob('cleaned_data_c5_*.csv'), key=os.path.getmtime)
data = pd.read_csv(f)
print(f"读取文件：{f}，共 {len(data)} 行")

#把日期转成时间类型，周末/工作日判断和按月统计都要用
data['日期'] = pd.to_datetime(data['日期'])
data['月份'] = data['日期'].dt.month
#weekday：周一=0 …… 周日=6，>=5 即为周末
data['周末标记'] = data['日期'].dt.weekday.apply(lambda x: '周末' if x >= 5 else '工作日')

#第 (1) 问：分析各出行方式的订单分布，找出最主要的出行方式（占比超过 40%）
#统计各出行方式的订单量并换算成占比
a = data['出行方式'].value_counts().rename('订单量').to_frame()
a['占比(%)'] = (a['订单量'] / len(data) * 100).round(2)
print(f"（1）各出行方式的订单分布：\n{a}")
#只保留占比超过 40% 的出行方式，即平台的主要出行方式
b = a[a['占比(%)'] > 40]
if len(b) > 0:
    print(f"（1）最主要的出行方式（占比超过 40%）：\n{b}")
else:
    print("（1）没有占比超过 40% 的出行方式")
print("\n")

#第 (2) 问：计算不同年龄段乘客的平均订单金额和常用出行时段，发现最具消费潜力的乘客群体
#平均订单金额直接分组求均值
c = data.groupby('乘客年龄段')['订单金额(元)'].mean().round(2).rename('平均订单金额')
#常用出行时段取该年龄段出现次数最多的整点小时
_h = data['出行时段(小时)'].apply(lambda v: int(v) % 24)
data['小时'] = _h
#idxmax 取每个年龄段订单量最大的那个小时，即该群体的常用出行时段
d = data.groupby('乘客年龄段')['小时'].agg(lambda s: s.value_counts().idxmax()).rename('常用出行时段(时)')
e = pd.concat([c, d], axis=1)
#再补上订单量，避免只看均价忽略样本量
e['订单量'] = data.groupby('乘客年龄段').size()
print(f"（2）不同年龄段乘客的平均订单金额与常用出行时段：\n{e}")
#消费潜力用“平均订单金额”衡量，取最高者
print(f"（2）最具消费潜力的乘客群体（平均订单金额最高）：{e['平均订单金额'].idxmax()}，{e['平均订单金额'].max():.2f} 元")
print("\n")

#第 (3) 问：分析周末和工作日的订单量差异，计算周末订单量相对工作日的增长百分比
#先统计周末、工作日各自的订单量
k = data['周末标记'].value_counts()
print(f"（3）周末与工作日的订单量：\n{k}")
#增长百分比以工作日为基准：(周末 - 工作日) / 工作日 × 100%
if '工作日' in k.index and '周末' in k.index:
    grow = (k['周末'] - k['工作日']) / k['工作日'] * 100
    print(f"（3）周末订单量相对工作日的增长百分比：{grow:.2f}%")
else:
    print("（3）数据中缺少工作日或周末样本，无法计算增长百分比")
print("\n")

#第 (4) 问：统计不同天气状况下的订单比例，并根据平均订单金额对天气状况进行排序
#按天气状况统计订单量，占比 = 该天气订单量 / 总订单量
m = data['天气状况'].value_counts().rename('订单量').to_frame()
m['占比(%)'] = (m['订单量'] / len(data) * 100).round(2)
#再按天气状况求平均订单金额，并按金额降序排列，得到天气的价格排序
m['平均订单金额'] = data.groupby('天气状况')['订单金额(元)'].mean().round(2)
m = m.sort_values('平均订单金额', ascending=False)
print(f"（4）不同天气状况的订单比例及按平均订单金额排序：\n{m}")
print("\n")

#第 (5) 问：分析服务评分与订单金额的关系，计算相关系数
#用皮尔逊相关系数衡量线性相关程度，越接近 1 说明评分越高金额越大
r = data['服务评分'].corr(data['订单金额(元)'])
print(f"（5）服务评分与订单金额的相关系数：{r:.4f}")
print("\n")
