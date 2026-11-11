import pandas as pd
#读取原始数据 bike_rides.csv，查看前10行了解字段与数据形态
bike_rides = pd.read_csv('bike_rides.csv')
print(bike_rides.head(10))

#【清洗步骤1】删除骑行距离为空或为0的记录
#对应题目要求：无效距离记录无分析价值，结果存为 cleaned_data_c1_N.csv，N = 删除条数
clean1 = (bike_rides["骑行距离(km)"] == 0) | (bike_rides["骑行距离(km)"].isna())
N1 = clean1.sum()
clean1_data = bike_rides[~clean1]
filename_1 = f"cleaned_data_c1_{N1}.csv"
clean1_data.to_csv(filename_1,index=False)

#【清洗步骤2】删除骑行时长小于1分钟或大于24小时的异常记录
#对应题目要求：1分钟以下视为误触，1440分钟（24小时）以上视为异常，结果存为 cleaned_data_c2_N.csv，N = 删除条数
clean2 = clean1_data.copy()
#布尔条件命名为 clean2_data 容易和 DataFrame 混淆，这里改名为 drop_mask 表示“待删除的行”
drop_mask_2 = (clean2["骑行时长(分钟)"] < 1) | (clean2["骑行时长(分钟)"] > 1440)
N2 = drop_mask_2.sum()
clean2_data = clean2[~drop_mask_2]
filename_2 = f"cleaned_data_c2_{N2}.csv"
clean2_data.to_csv(filename_2,index=False)

#【清洗步骤3】将天气状况中的空值替换为该时段最常见的天气状况
#对应题目要求：用众数填充缺失天气，结果存为 cleaned_data_c3_N.csv，N = 修改（被填充）的条数
clean3 = clean2_data.copy()
#找出天气状况为空的行，这些行才需要填充
na_mask_3 = clean3["天气状况"].isna()
N3 = na_mask_3.sum()
#取非空天气中出现次数最多的天气作为众数（不能直接对整个含空值的列取众数，避免空值干扰）
most_weather = clean3["天气状况"].mode()[0]
#只对空值位置填充众数，其余行保持原值不变
clean3.loc[na_mask_3, "天气状况"] = most_weather
#注意：这一步写出的是填充后的完整数据表，而不是布尔掩码
clean3_data = clean3
filename_3 = f"cleaned_data_c3_{N3}.csv"
clean3_data.to_csv(filename_3,index=False)


#【清洗步骤4】识别并删除重复的骑行记录
#对应题目要求：题目原文编号为(4)但输出文件名要求是 cleaned_data_c5_N.csv（跳过 c4，没有 c4），
#因此这里文件名用 c5，N = 删除的重复条数
#注意：本步从上一步清洗结果 clean3_data 继续，保证天气空值已填充，避免跳过第3步
clean4 = clean3_data.copy()
#识别并删除重复的骑行记录，keep='first' 保留第一次出现的记录
clean4_data = clean4.drop_duplicates(keep='first')
#删除前的行数减去删除后的行数，即被删除的重复条数
N4 = len(clean4) - len(clean4_data)
filename_4 = f"cleaned_data_c5_{N4}.csv"
clean4_data.to_csv(filename_4,index=False)
