import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams['font.family'] = 'SimHei'  # 替换为你选择的字体
data = pd.read_csv("cleaned_tree_c5_7.csv")

#（1）使用柱状图展示各区域的树木调查数量，柱状图中的每个柱子代表一个区域，高度代表该区域的树木记录数量
#value_counts() 统计每个区域的记录条数，即该区域的调查数量
count = data['区域'].value_counts()
plt.figure(figsize=(20,8),dpi=80)
#柱状图：x 轴为区域名，y 轴为对应的调查数量
plt.bar(count.index,count.values)
plt.title("各区域的树木调查数量")
plt.xlabel("区域")
plt.ylabel("树木调查数量")
plt.show()

#（2）创建条形图比较不同树种的平均估值(元)，条形图中横轴表示平均估值，纵轴表示树种
#先按树种分组对估值求均值，作为每个树种的平均估值；再倒序排列，让平均估值最高的树种排在最上面
avg_price = data.groupby("树种")['估值(元)'].mean().sort_values()
plt.figure(figsize=(20,8),dpi=80)
#barh 是横向条形图：第一个参数是纵轴（树种），第二个参数是横轴（平均估值）
plt.barh(avg_price.index,avg_price.values)
plt.title("不同树种的平均估值")
plt.xlabel("平均估值(元)")
plt.ylabel("树种")
plt.show()


#（3）使用折线图展示不同调查年份的树木平均估值趋势
#按调查年份分组求平均估值，得到每年的均价序列（折线图的 y 值），sort_index 保证年份是从小到大排列
avg_price_2 = data.groupby("调查年份")['估值(元)'].mean().sort_index()
plt.figure(figsize=(20,8),dpi=80)
#折线图：x 轴为调查年份，y 轴为该年的平均估值
plt.plot(avg_price_2.index,avg_price_2.values)
plt.title("不同调查年份的树木平均估值趋势")
plt.xlabel("调查年份")
plt.ylabel("平均估值(元)")
plt.show()


#（4）制作散点图探索树木估值(元)与胸径(cm)之间的关系，横轴为估值，纵轴为胸径，每个点代表一株被调查的树木
#散点图第一个参数是横轴（估值），第二个参数是纵轴（胸径）
plt.figure(figsize=(20,8),dpi=80)
plt.scatter(data['估值(元)'],data['胸径(cm)'])
plt.title("树木估值与胸径之间的关系")
plt.xlabel("估值(元)")
plt.ylabel("胸径(cm)")
plt.show()
