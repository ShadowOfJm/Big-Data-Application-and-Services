import pandas as pd
data = pd.read_csv("cleaned_data_c10_0.csv")

#分析各地区酒店的分布情况，统计每个地区的酒店数量，进行倒序排序展示前两名
a = data['地区'].value_counts() # 默认倒序
print(f"各地区酒店的分布情况{a.head(3)}")
print("\n")

#计算不同装修时间的酒店的平均设施评分
b = data.groupby("装修时间")["设施评分"].mean()
print(f"不同装修时间的酒店的平均设施评分{b}")
print("\n")


#计算每个地区的平均房价，进行倒序排序展示前三名
c = data.groupby("地区")["房价"].mean()
print(f"每个地区的平均房价{c.head(3)}")
print("\n")


#统计数据集中每种房间类型的出现频次，进行正序排序展示前两名
d = data["房间类型"].value_counts(ascending=True)
print(f"每种房间类型的出现频次{d.head(2)}")
print("\n")


#筛选出卫生评分和服务评分均高于4.5的酒店，并统计这些酒店的数量
e = ((data["卫生评分"] > 4.5) & (data["服务评分"] > 4.5)).sum()
print(f"卫生评分和服务评分均高于4.5的酒店{e}")
print("\n")