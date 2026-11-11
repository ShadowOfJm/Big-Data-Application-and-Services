import pandas as pd
data = pd.read_csv("cleaned_data_c5_3.csv")

#（1）平均售价：计算数据集中所有房源的平均售价。
avg_price = data['价格(万元)'].mean()
print(f"所有房源的平均售价:{avg_price:.2f}万元")

#（2）最受欢迎的户型：根据销售量，确定哪种户型最受欢迎。
#先统计各户型的房源条数（即销售量），再取数量最多的户型名和对应销量
hx = data["户型"].value_counts()
best_hx = hx.idxmax()
best_num = hx.max()
print(f"最受欢迎的户型:{best_hx},销售量:{best_num}")

#（3）高销量市区特征：识别销售量在前25%的市区共有的特征（如售价范围、面积等）。
#统计每个市区的房源数量，用 75% 分位数作为"高销量"的门槛
count_1 = data["市区"].value_counts()
top_25 = count_1.quantile(0.75)
#销量达到或超过该门槛的市区即为前25%的高销量市区
top_cities = count_1[count_1 >= top_25].index.tolist()
print("\n")
#前25%的市区
print(top_cities)
#销售量阈值 (前25%)
print(top_25)

#把高销量市区的房源筛出来，单独统计它们的价格和面积特征
top_house = data[data["市区"].isin(top_cities)]

#价格范围：取最小值到最大值构成区间
price_range = top_house["价格(万元)"].min(),top_house["价格(万元)"].max()
#价格平均数
price_avg = top_house['价格(万元)'].mean()

#面积范围：取最小值到最大值构成区间
area_range = top_house["面积(㎡)"].min(),top_house["面积(㎡)"].max()
#面积平均数
area_avg = top_house['面积(㎡)'].mean()
print("\n")
print(f"价格范围{price_range[0]:.2f} ~ {price_range[1]:.2f}万元")
print(f"价格平均数{price_avg:.2f}万元")
print(f"面积范围{area_range[0]:.2f}(㎡) ~ {area_range[1]:.2f}(㎡)")
print(f"平均面积{area_avg:.2f}(㎡)")

#（4）撰写营销策略建议（至少两条），用 print 输出
#下面的建议来自前面三问的统计结果：高销量市区集中在哪、哪种户型卖得最多、均价与面积的关系
print("\n")
print("营销策略建议：")
#建议一：跟着销量走，把营销资源优先投到高销量市区
print(f"1.聚焦高销量市区：销量前25%的市区为{top_cities}，"
      f"这些市区房源均价约{price_avg:.2f}万元、平均面积约{area_avg:.2f}㎡，"
      f"应将房源主推与广告投放优先集中到这些区域，提高成交转化率。")
#建议二：主推畅销户型，备货和宣传向最受欢迎户型倾斜
print(f"2.主推畅销户型：{best_hx}是销量最高的户型(共{best_num}套)，"
      f"可将其作为主打房源重点包装，并据此调整收房与装修投入的结构。")
#建议三：围绕整体均价做分层定价，低总价+大面积房源作为卖点
print(f"3.围绕均价{avg_price:.2f}万元做分层定价："
      f"对低于均价且面积大于平均水平的房源，突出'低总价、大面积'的性价比卖点，"
      f"吸引对面积敏感的刚需客户。")
