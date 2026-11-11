import pandas as pd
#读取清洗脚本的最终产物 cleaned_tree_c5_7.csv，业务分析基于这份数据
data = pd.read_csv("cleaned_tree_c5_7.csv")

#（1）平均估值：计算数据集中所有树木记录的平均估值（元）
avg_value = data['估值(元)'].mean()
print(f"所有树木记录的平均估值:{avg_value:.2f}元")

#（2）最优势树种：根据记录数量，确定哪种树种的调查数量最多（即分布最广）
#先统计各树种的记录条数，再取数量最多的树种名和对应条数
sp = data["树种"].value_counts()
best_sp = sp.idxmax()
best_num = sp.max()
print(f"最优势树种:{best_sp},记录数量:{best_num}条")

#（3）高丰富度区域特征：识别树木记录数量在前25%的区域共有的特征（如估值范围、平均胸径、主要生长状况等）
#统计每个区域的树木记录条数，用 75% 分位数作为"记录数量靠前"的门槛
count_1 = data["区域"].value_counts()
top_25 = count_1.quantile(0.75)
#记录数量达到或超过该门槛的区域，即为前 25% 的区域
top_areas = count_1[count_1 >= top_25].index.tolist()
print("\n")
#前25%的区域名单
print(f"记录数量在前25%的区域{top_areas}")
#进入前25%的记录数量门槛
print(f"记录数量门槛(75%分位数){top_25}")

#把前 25% 区域内的树木记录筛出来，单独统计它们的估值、胸径和生长状况特征
top_tree = data[data["区域"].isin(top_areas)]

#估值范围：取最小值到最大值构成区间
value_range = top_tree["估值(元)"].min(),top_tree["估值(元)"].max()
#估值平均数
value_avg = top_tree['估值(元)'].mean()

#胸径范围：取最小值到最大值构成区间
dbh_range = top_tree["胸径(cm)"].min(),top_tree["胸径(cm)"].max()
#胸径平均数
dbh_avg = top_tree['胸径(cm)'].mean()

#主要生长状况：取出现次数最多的那种生长状况
main_status = top_tree["生长状况"].value_counts().idxmax()
print("\n")
print(f"估值范围{value_range[0]:.2f} ~ {value_range[1]:.2f}元")
print(f"平均估值{value_avg:.2f}元")
print(f"胸径范围{dbh_range[0]:.2f}(cm) ~ {dbh_range[1]:.2f}(cm)")
print(f"平均胸径{dbh_avg:.2f}(cm)")
print(f"主要生长状况{main_status}")

#（4）撰写针对城市林木资源管理、重点保护或生态规划的策略建议（至少两条），用 print 输出
#下面的建议来自前面三问的统计结果：整体均价水平、哪个树种分布最广、高记录数量区域有什么共性
print("\n")
print("城市林木资源管理与生态规划策略建议：")
#建议一：跟着优势树种走，把有限的养护资源优先投向分布最广的树种
print(f"1.聚焦优势树种养护：{best_sp}是调查数量最多的树种(共{best_num}条)，"
      f"分布最广、生态与景观作用最大，应优先保障其水肥、修剪与病虫害防治投入，"
      f"并以其为主要基调树种纳入城市绿地系统规划。")
#建议二：把资源向高记录数量区域集中，同时守住平均估值这条价值底线
print(f"2.按区域分级管理：记录数量在前25%的区域为{top_areas}，"
      f"其平均估值约{value_avg:.2f}元、平均胸径约{dbh_avg:.2f}cm，主要生长状况为{main_status}，"
      f"这些区域应作为重点养护片区，实行定期普查与动态建档，防止高价值林木流失。")
#建议三：围绕整体均价做价值分层，对低于均价但规格较大的树木重点保护
print(f"3.建立价值分层保护机制：全市平均估值为{avg_value:.2f}元，"
      f"对估值低于均价但胸径超过平均水平的林木，应重点核查其树龄与古树名木潜力，"
      f"符合标准的及时挂牌保护，避免因估值偏低在建设中遭到砍伐或移植。")
