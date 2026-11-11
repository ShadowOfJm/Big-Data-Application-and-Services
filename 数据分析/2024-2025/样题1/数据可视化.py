import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams['font.family'] = 'SimHei'  # 替换为你选择的字体
data = pd.read_csv("cleaned_data_c5_3.csv")

#（1）使用柱状图展示各市区的二手房销售数量，柱状图中的每个柱子代表一个市区，高度代表该市区的房源销售数量
#value_counts() 统计每个市区的房源条数，即该市区的销售数量
count = data['市区'].value_counts()
plt.figure(figsize=(20,8),dpi=80)
#柱状图：x 轴为市区名，y 轴为对应的销售数量
plt.bar(count.index,count.values)
plt.title("各市区的二手房销售数量")
plt.xlabel("市区")
plt.ylabel("房源销售数量")
plt.show()

#（2）创建条形图比较不同户型的平均售价，条形图中横轴表示平均售价，纵轴表示户型
#先按户型分组对价格求均值，作为每个户型的平均售价
avg_price = data.groupby("户型")['价格(万元)'].mean()
plt.figure(figsize=(20,8),dpi=80)
#barh 是横向条形图：第一个参数是纵轴（户型），第二个参数是横轴（平均售价）
plt.barh(avg_price.index,avg_price.values)
plt.title("不同户型的平均售价")
plt.xlabel("平均售价")
plt.ylabel("户型")
plt.show()


#（3）使用折线图展示不同年份的二手房平均售价趋势
#按年份分组求平均售价，得到每年的均价序列（折线图的 y 值）
avg_price_2 = data.groupby("年份")['价格(万元)'].mean()
plt.figure(figsize=(20,8),dpi=80)
#折线图：x 轴为年份，y 轴为该年的平均售价
plt.plot(avg_price_2.index,avg_price_2.values)
plt.title("不同年份的二手房平均售价趋势")
plt.xlabel("年份")
#修正：原代码多写了一个单引号，ylabel 应为规范的"价格(万元)"
plt.ylabel("价格(万元)")
plt.show()


#（4）制作散点图探索售价与面积之间的关系，散点图中的横轴为售价，纵轴为面积，每个点代表一套房源
#散点图第一个参数是横轴（价格），第二个参数是纵轴（面积）
plt.figure(figsize=(20,8),dpi=80)
plt.scatter(data['价格(万元)'],data['面积(㎡)'])
plt.title("售价与面积之间的关系")
plt.xlabel("价格(万元)")
plt.ylabel("面积(㎡)")
plt.show()
