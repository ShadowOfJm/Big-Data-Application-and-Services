import pandas as pd

travel_order_data = pd.read_csv("travel_order_data.csv")
#打印数据集前 10 行（项目二 任务一 子任务一：数据获取，需截图）
print(travel_order_data.head(10))

#删除天气状况为空或为无效值的记录，并将结果存储为 `cleaned_data_c1_N.csv`，N 为删除的数据条数；
#第 (1) 步：题目要求“为空或为无效值”，无效值在本数据集中表现为 N/A、null 这类占位文本，
#所以除了 isna()，还要把去掉空格后等于 N/A / null 的记录一并算作无效
clean1 = travel_order_data["天气状况"].isna() | travel_order_data["天气状况"].astype(str).str.strip().isin(["N/A", "null"])
clean1_data = travel_order_data[~clean1]
N1 = clean1.sum()
filename1 = f"cleaned_data_c1_{N1}.csv"
clean1_data.to_csv(filename1,index=False)

#删除出行时长异常（超过 12 小时或小于 0.1 小时）的记录，并将结果存储为 `cleaned_data_c2_N.csv`，N 为删除的数据条数；
#第 (2) 步：时长过短或过长都属于异常，两个条件取“或”
clean2_copy = clean1_data.copy()
clean2 = (clean2_copy["出行时长(小时)"] < 0.1) | (clean2_copy["出行时长(小时)"] > 12)
N2 = clean2.sum()
clean2_data = clean2_copy[~clean2]
filename2 = f"cleaned_data_c2_{N2}.csv"
clean2_data.to_csv(filename2,index=False)

#将出行方式为空的记录填充为“未知”，并存储为 `cleaned_data_c3_N.csv`，N 为修改的数据条数；
#第 (3) 步：本步是“填充”不是删除，N 取被填充的条数，用填充前的 isna 标记统计
clean3_copy = clean2_data.copy()
mark = clean3_copy["出行方式"].isna()
clean3_copy["出行方式"] = clean3_copy["出行方式"].fillna("未知")
N3 = mark.sum()
filename3 = f"cleaned_data_c3_{N3}.csv"
clean3_copy.to_csv(filename3,index=False)

#将服务评分超出范围（1-5 分）的记录删除，并将结果存储为 `cleaned_data_c4_N.csv`，N 为删除的数据条数；
#第 (4) 步：评分小于 1 或大于 5 都判为超出范围
clean4_copy = clean3_copy.copy()
clean4 = (clean4_copy["服务评分"] > 5) | (clean4_copy["服务评分"] < 1)
clean4_data = clean4_copy[~clean4]
N4 = clean4.sum()
filename4 = f"cleaned_data_c4_{N4}.csv"
clean4_data.to_csv(filename4,index=False)

#将订单金额明显异常（超过该出行方式平均订单金额 5 倍）的记录删除， 将结果存储为 `cleaned_data_c5_N.csv`，N 为删除的数据条数。
#第 (5) 步：题目要求对比的是“该出行方式”的平均订单金额，所以必须按出行方式分组求均值，不能用全表均值
clean5_copy = clean4_data.copy()
#transform 把每种出行方式的均值按行广播回原表，长度与 clean5_copy 一致，便于逐行比较
avg = clean5_copy.groupby("出行方式")["订单金额(元)"].transform("mean")
clean5 = clean5_copy["订单金额(元)"] > avg * 5
N5 = clean5.sum()
filename5 = f"cleaned_data_c5_{N5}.csv"
clean5_data = clean5_copy[~clean5]
clean5_data.to_csv(filename5,index=False)
