import pandas as pd
data = pd.read_csv("cleaned_data_c5_3.csv")

#分析不同市区的二手房销售量，统计每个市区的房源销售数量，并进行倒序排序展示前三名
a = data["市区"].value_counts()
print("\n")
print(f"不同市区的二手房销售量{a.head(3)}")

#计算各户型的平均售价，并进行倒序排序展示前三种户型
b = data.groupby("户型")['价格(万元)'].mean()
print("\n")
print(f"各户型的平均售价{b.head(3)}")


#计算每个市区的平均售价，进行倒序排序展示前三名
c = data.groupby("市区")['价格(万元)'].mean()
print("\n")
print(f"每个市区的平均售价{c.head(3)}")


#统计不同装修情况的房源数量，并进行正序排序展示
d = data["装修情况"].value_counts(ascending=True)
print("\n")
print(f"不同装修情况的房源数量{d.head(3)}")


#筛选出售价在平均售价以下且面积超过平均面积的房源，并统计这些房源的数量
avg_price = data['价格(万元)'].mean()
avg_area = data['面积(㎡)'].mean()
e = ((data['价格(万元)'] < avg_price) & (data['面积(㎡)'] > avg_area))
f = data[e]
count = len(f)
print("\n")
print(f"出售价在平均售价{avg_price:.2f}以下且面积超过平均面积{avg_area:.2f}的房源\n{count}")
