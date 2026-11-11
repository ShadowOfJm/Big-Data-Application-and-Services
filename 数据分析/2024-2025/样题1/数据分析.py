import pandas as pd
data = pd.read_csv("cleaned_data_c5_3.csv")

#（1）分析不同市区的二手房销售量：每个市区出现的房源条数就是该市区的销售数量
#value_counts() 默认就是按数量倒序，这里再显式 sort_values(ascending=False) 一次，保证是题目要求的"倒序排序"
a = data["市区"].value_counts().sort_values(ascending=False)
print("\n")
#head(3) 取倒序后的前三名市区
print(f"不同市区的二手房销售量{a.head(3)}")

#（2）计算各户型的平均售价：先按"户型"分组对"价格(万元)"求均值
#groupby().mean() 默认按分组键（户型）的字典序排列，必须补 sort_values(ascending=False) 才是"按平均售价倒序"
b = data.groupby("户型")['价格(万元)'].mean().sort_values(ascending=False)
print("\n")
#head(3) 取均价最高的前三种户型
print(f"各户型的平均售价{b.head(3)}")


#（3）计算每个市区的平均售价：同样先分组求均值，再按平均售价倒序排序
c = data.groupby("市区")['价格(万元)'].mean().sort_values(ascending=False)
print("\n")
#head(3) 取均价最高的前三名市区
print(f"每个市区的平均售价{c.head(3)}")


#（4）统计不同装修情况的房源数量：value_counts 统计每种装修情况的条数
#ascending=True 表示正序（数量从小到大），与题目"正序排序展示"一致
d = data["装修情况"].value_counts(ascending=True)
print("\n")
#题目只要求正序展示、没有规定取前几名，所以这里把全部装修情况都打印出来
print(f"不同装修情况的房源数量{d}")


#（5）筛选出售价在平均售价以下且面积超过平均面积的房源，并统计这些房源的数量
#先算出整体的平均售价和平均面积，作为筛选的两个阈值
avg_price = data['价格(万元)'].mean()
avg_area = data['面积(㎡)'].mean()
#用布尔索引同时满足两个条件：价格低于均价、面积高于均面积
e = ((data['价格(万元)'] < avg_price) & (data['面积(㎡)'] > avg_area))
#按布尔条件取出符合条件的房源明细
f = data[e]
#符合条件的房源条数
count = len(f)
print("\n")
print(f"出售价在平均售价{avg_price:.2f}以下且面积超过平均面积{avg_area:.2f}的房源\n{count}")
