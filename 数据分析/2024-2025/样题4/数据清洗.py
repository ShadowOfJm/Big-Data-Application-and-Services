import pandas as pd
tourist_data = pd.read_csv("tourist_data.csv")
print(tourist_data.head(10))

#删除天气状况为空或为零的记录，并将结果存储为 cleaned_data_c1_N.csv，N 为删除的数据条数；
clean1 = (tourist_data["天气状况"].isna()) | (tourist_data["天气状况"] == 0)
N1 = clean1.sum()
filename_1 = f"cleaned_data_c1_{N1}.csv"
clean1_data = tourist_data[~clean1]
clean1_data.to_csv(filename_1,index=False)

#删除停留时长异常（超过24小时或小于0.1小时）的记录，并将结果存储为 cleaned_data_c2_N.csv，N 为删除的数据条数；
clean2_copy = clean1_data.copy()
clean2 = (clean2_copy["停留时长（小时）"] > 24 ) | (clean2_copy["停留时长（小时）"] < 0.1 )
N2 = clean2.sum()
filename_2 = f"cleaned_data_c2_{N2}.csv"
clean2_data = clean2_copy[~clean2]
clean2_data.to_csv(filename_2,index=False)

#将游客来源地为空的记录填充为"未知"，并存储为 cleaned_data_c3_N.csv，N 为修改的数据条数；
clean3_copy = clean2_data.copy()
#掩码：标记"游客来源地"为空的行，这些行才需要填充
clean3 = clean3_copy['游客来源地'].isna()
N3 = clean3.sum()
#修正：原写法是 clean3 = clean3.fillna("未知")，对布尔掩码调用 fillna 不起作用（布尔序列没有 NaN），
#导致后面 clean3_copy[~clean3] 把来源地为空的记录直接删掉而不是填充。
#这里改为直接对数据框的"游客来源地"列填充"未知"，行数保持不变
clean3_copy.loc[clean3, '游客来源地'] = "未知"
clean3_data = clean3_copy
filename_3 = f"cleaned_data_c3_{N3}.csv"
clean3_data.to_csv(filename_3,index=False)

#将满意度评分超出范围（0-5分）的记录删除，并将结果存储为 cleaned_data_c4_N.csv，N 为删除的数据条数；
clean4_copy = clean3_data.copy()
clean4 = (clean4_copy['满意度评分'] > 5) | (clean4_copy['满意度评分'] < 0)
N4 = clean4.sum()
filename_4 = f'cleaned_data_c4_{N4}.csv'
clean4_data = clean4_copy[~clean4]
clean4_data.to_csv(filename_4,index=False)

#将消费金额明显异常（超过该景区平均消费金额5倍）的记录删除，将结果存储为 cleaned_data_c5_N.csv，N 为删除的数据条数
clean5_copy = clean4_data.copy()
avg_price = clean5_copy['消费金额（元）'].mean()
print(avg_price * 5)
clean5 = clean5_copy['消费金额（元）'] > avg_price * 5
N5 = clean5.sum()
filename_5 = f'cleaned_data_c5_{N5}.csv'
clean5_data = clean5_copy[~clean5]
clean5_data.to_csv(filename_5,index=False)