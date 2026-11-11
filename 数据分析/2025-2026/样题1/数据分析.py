import pandas as pd
#读取清洗脚本的最终产物 cleaned_tree_c5_7.csv（161 条记录），后续分析都基于这份数据
data = pd.read_csv("cleaned_tree_c5_7.csv")

#（1）分析不同区域的树木调查数量：每个区域出现的记录条数就是该区域的调查数量
#value_counts() 默认就是按数量倒序，这里再显式 sort_values(ascending=False) 一次，保证是题目要求的"倒序排序"
a = data["区域"].value_counts().sort_values(ascending=False)
print("\n")
#head(3) 取倒序后的前三名区域
print(f"不同区域的树木调查数量{a.head(3)}")

#（2）计算各类树种的平均估值：先按"树种"分组对"估值(元)"求均值
#groupby().mean() 默认按树种名的字典序排列，必须补 sort_values(ascending=False) 才是"按平均估值倒序"
b = data.groupby("树种")["估值(元)"].mean().sort_values(ascending=False)
print("\n")
#head(3) 取平均估值最高的三种树种
print(f"各类树种的平均估值{b.head(3)}")

#（3）计算每个区域的平均估值：同样先按区域分组求均值，再按平均估值倒序排序
c = data.groupby("区域")["估值(元)"].mean().sort_values(ascending=False)
print("\n")
#head(3) 取均价最高的前三名区域
print(f"每个区域的平均估值{c.head(3)}")

#（4）统计不同生长状况（健康、一般、较差）的树木数量：value_counts 统计每种状况的条数
#ascending=True 表示正序（数量从小到大），与题目"正序排序展示"一致
d = data["生长状况"].value_counts(ascending=True)
print("\n")
#题目只要求正序展示、没有规定取前几名，所以这里把三种生长状况全部打印出来
print(f"不同生长状况的树木数量{d}")

#（5）筛选估值在平均估值以下但胸径(cm)超过平均胸径的树木记录，并统计数量
#先算出整体的平均估值和平均胸径，作为筛选的两个阈值
avg_value = data["估值(元)"].mean()
avg_dbh = data["胸径(cm)"].mean()
#用布尔索引同时满足两个条件：估值低于平均估值、胸径高于平均胸径
mask = (data["估值(元)"] < avg_value) & (data["胸径(cm)"] > avg_dbh)
#按布尔条件取出符合条件的树木记录明细
e = data[mask]
print("\n")
#统计符合条件的记录条数
print(f"估值低于平均估值{avg_value:.2f}元但胸径超过平均胸径{avg_dbh:.2f}cm的树木记录数量{len(e)}")
