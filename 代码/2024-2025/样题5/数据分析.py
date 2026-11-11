import pandas as pd
#读取样例5清洗完成后的数据（c10 为最终结果）
data = pd.read_csv("cleaned_data_c10_0.csv")

#（1）分析各地区酒店的分布情况，统计每个地区的酒店数量，进行倒序排序展示前两名
#value_counts() 默认就是按数量倒序，这里再显式排序一次，保证符合题目"倒序排序"的要求
a = data['地区'].value_counts().sort_values(ascending=False)
#head(2) 取数量最多的前两名地区
print(f"各地区酒店的分布情况{a.head(2)}")
print("\n")

#（2）计算不同装修时间的酒店的平均设施评分
#按装修时间分组，对设施评分求均值（装修时间为"年-月"，分组后天然按时间先后排列）
b = data.groupby("装修时间")["设施评分"].mean()
print(f"不同装修时间的酒店的平均设施评分{b}")
print("\n")


#（3）计算每个地区的平均房价，进行倒序排序展示前三名
#groupby().mean() 默认按地区名的字典序排，必须补 sort_values(ascending=False) 才是按平均房价倒序
c = data.groupby("地区")["房价"].mean().sort_values(ascending=False)
#head(3) 取平均房价最高的前三名地区
print(f"每个地区的平均房价{c.head(3)}")
print("\n")


#（4）统计数据集中每种房间类型的出现频次，进行正序排序展示前两名
#ascending=True 表示正序（频次从小到大），符合题目"正序排序"的要求
d = data["房间类型"].value_counts(ascending=True)
#head(2) 取频次最低的前两名房间类型
print(f"每种房间类型的出现频次{d.head(2)}")
print("\n")


#（5）筛选出卫生评分和服务评分均高于4.5的酒店，并统计这些酒店的数量
#两个条件用 & 连接，表示"均高于"，再 sum() 统计条数
e = ((data["卫生评分"] > 4.5) & (data["服务评分"] > 4.5)).sum()
print(f"卫生评分和服务评分均高于4.5的酒店{e}")
print("\n")
