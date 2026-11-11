import pandas as pd
data = pd.read_csv("cleaned_data_c5_3.csv")

#平均售价：计算数据集中所有房源的平均售价。
avg_price = data['价格(万元)'].mean()
print(f"所有房源的平均售价:{avg_price:.2f}万元")
#最受欢迎的户型：根据销售量，确定哪种户型最受欢迎。
best_hx = data["户型"].value_counts().idxmax()
best_num = data["户型"].value_counts().max()
print(f"最受人最受欢迎的户型:{best_hx},销售量:{best_num}")

# 高销量市区特征：识别销售量在前25%的市区共有的特征（如售价范围、面积等）。
count_1 = data["市区"].value_counts()
top_25 = count_1.quantile(0.75)
top_cities = count_1[count_1 >= top_25].index.tolist()
#前25%的市区
print(top_cities)
#销售量阈值 (前25%)
print(top_25)

top_house = data[data["市区"].isin(top_cities)]

price_range = top_house["价格(万元)"].min(),top_house["价格(万元)"].max()
price_avg = top_house['价格(万元)'].mean()

area_range = top_house["面积(㎡)"].min(),top_house["面积(㎡)"].max()
area_avg = top_house['面积(㎡)'].mean()
print(f"价格范围{price_range[0]:.2f} ~ {price_range[1]:.2f}万元")
print(f"价格平均数{price_avg:.2f}万元")
print(f"面积范围{area_range[0]:.2f}(㎡) ~ {area_range[1]:.2f}(㎡)")
print(f"平均面积{area_avg:.2f}(㎡)")