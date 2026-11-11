import pandas as pd
#读取原始数据 learning_data.csv，查看前10行了解字段与数据形态
learning_data = pd.read_csv('learning_data.csv')
print(learning_data.head(10))

#【清洗步骤1】删除学习时长为空或为0的记录
#对应题目要求：剔除无效学习时长记录，结果存为 cleaned_data_c1_N.csv，N = 删除条数
clean1 = (learning_data["学习时长(分钟)"] == 0 ) | (learning_data["学习时长(分钟)"].isna())
#N1 为满足删除条件的记录条数（布尔序列求和即条数）
N1 = clean1.sum()
#用 ~ 取反，保留不符合删除条件的行
cleaned_data_c1 = learning_data[~clean1]
filename_1 = f"cleaned_data_c1_{N1}.csv"
cleaned_data_c1.to_csv(filename_1,index=False)

#【清洗步骤2】删除测验成绩异常（大于100分或小于0分）的记录
#对应题目要求：成绩不在 0~100 区间的记录视为异常，结果存为 cleaned_data_c2_N.csv，N = 删除条数
clean2 = (cleaned_data_c1["测验成绩"] < 0 ) | (cleaned_data_c1["测验成绩"] > 100 )
N2 = clean2.sum()
cleaned_data_c2 = cleaned_data_c1[~clean2]
filename_2 = f"cleaned_data_c2_{N2}.csv"
cleaned_data_c2.to_csv(filename_2,index=False)

#【清洗步骤3】将最后学习时间格式不规范的记录做标准化处理
#对应题目要求：用 pd.to_datetime 统一时间格式，errors='coerce' 让无法解析的值变为 NaT，
#结果存为 cleaned_data_c3_N.csv，N = 被改为 NaT（即原格式不规范）的条数
cleaned_data_c3 = cleaned_data_c2.copy()
cleaned_data_c3["最后学习时间"] = pd.to_datetime(cleaned_data_c3["最后学习时间"],errors='coerce')
#总条数减去能成功解析的条数，就是格式不规范（变成 NaT）的条数
N3 = len(cleaned_data_c3) - cleaned_data_c3["最后学习时间"].notna().sum()
filename_3 = f"cleaned_data_c3_{N3}.csv"
cleaned_data_c3.to_csv(filename_3,index=False)

#【清洗步骤4】将完成进度超过100%的记录修正为100%
#对应题目要求：完成进度是百分比，超过 100 属于越界值，结果存为 cleaned_data_c4_N.csv，N = 修改条数
cleaned_data_c4 = cleaned_data_c3.copy()
clean4 = cleaned_data_c4["完成进度"] > 100 #将大于100的数据放在clean4
N4 = clean4.sum()
cleaned_data_c4.loc[clean4,"完成进度"] = 100 #使用df.loc[行索引,列索引], =100是我们想要赋给选中单元格的新值
filename_4 = f"cleaned_data_c4_{N4}.csv"
cleaned_data_c4.to_csv(filename_4,index=False)

#【清洗步骤5】删除重复的学习记录
#对应题目要求：结果存为 cleaned_data_c5_N.csv，N = 删除的重复条数
cleaned_data_c5 = cleaned_data_c4.copy()
N5 = cleaned_data_c5.duplicated().sum()  #使用.duplicated()标记重复的记录
cleaned_data_c5 = cleaned_data_c4.drop_duplicates() #使用.drop_duplicates()删除重复记录
filename_5 = f"cleaned_data_c5_{N5}.csv"
cleaned_data_c5.to_csv(filename_5,index=False)
