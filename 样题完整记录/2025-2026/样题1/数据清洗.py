import pandas as pd
#子任务一：数据获取——用 pandas 读取 tree_survey.csv，并打印前 10 行（题目要求截图终端输出）
tree_survey = pd.read_csv("tree_survey.csv")
print(tree_survey.head(10))

#子任务二-（1）：删除胸径(cm)为空或为零的记录，结果存为 cleaned_tree_c1_N.csv，N 为删除条数
#布尔条件：胸径等于 0，或胸径为空（NaN）都算异常记录
clean1 = (tree_survey["胸径(cm)"] == 0) | (tree_survey["胸径(cm)"].isna())
#取反得到保留下来的正常记录
clean1_data = tree_survey[~clean1]
#N 就是被删掉的条数，直接写进文件名
N1 = clean1.sum()
filename1 = f"cleaned_tree_c1_{N1}.csv"
clean1_data.to_csv(filename1,index=False)


#子任务二-（2）：删除估值(元)为空或异常高（超过平均估值的 3 倍）的记录，存为 cleaned_tree_c2_N.csv
#注意：这里是在上一步清洗后的 clean1_data 上继续做，均值也取这份数据的均值
clean2_copy = clean1_data.copy()
avg = clean2_copy["估值(元)"].mean()
#估值缺失，或估值大于均值的 3 倍，都判为异常
clean2 = (clean2_copy["估值(元)"].isna()) | (clean2_copy["估值(元)"] > avg * 3)
N2 = clean2.sum()
filename2 = f"cleaned_tree_c2_{N2}.csv"
#取反保留正常记录
clean2_data = clean2_copy[~clean2]
clean2_data.to_csv(filename2,index=False)


#子任务二-（3）：树种标准化，把“法桐”“悬铃木”统一转换成标准名“二球悬铃木”，存为 cleaned_tree_c3_N.csv
#N 是被修改的条数，不是删除条数，所以这一步的行数不变
clean3_copy = clean2_data.copy()
#先备份原始树种列，后面用它和新列比对，统计到底改了多少条
original = clean3_copy["树种"].copy()
species_mapping = {
    '法桐': '二球悬铃木',
    '悬铃木': '二球悬铃木',
}
#map 只替换字典里出现的名字，没命中的会变成 NaN，用 fillna 补回原来的树种名
clean3_copy["树种"] = clean3_copy["树种"].map(species_mapping).fillna(clean3_copy["树种"])
#原始树种与替换后不相同的记录，就是被修改的记录
mask = original != clean3_copy["树种"]
N3 = mask.sum()
filename3 = f"cleaned_tree_c3_{N3}.csv"
clean3_copy.to_csv(filename3,index=False)


#子任务二-（4）：删除是否古树名木字段为空白的记录，存为 cleaned_tree_c4_N.csv
#CSV 里该字段的空白会被 pandas 读成 NaN，用 isna 判断
clean4_copy = clean3_copy.copy()
clean4 = clean4_copy["是否古树名木"].isna()
N4 = clean4.sum()
filename4 = f"cleaned_tree_c4_{N4}.csv"
clean4_data = clean4_copy[~clean4]
clean4_data.to_csv(filename4,index=False)



#子任务二-（5）：删除胸径(cm)小于 20 的记录（树木过小，不符合统计标准），存为 cleaned_tree_c5_N.csv
clean5_copy = clean4_data.copy()
clean5 = clean5_copy["胸径(cm)"] < 20
N5 = clean5.sum()
filename5 =f"cleaned_tree_c5_{N5}.csv"
clean5_data = clean5_copy[~clean5]
#这份 cleaned_tree_c5_N.csv 是后面数据标注、数据分析、数据可视化的输入
clean5_data.to_csv(filename5,index=False)
