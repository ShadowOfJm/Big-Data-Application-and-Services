import pandas as pd

tourist_data = pd.read_csv("tourist_data.csv")
#打印数据集前 10 行（项目二 任务一 子任务一：数据获取，需截图）
print(tourist_data.head(10))

#删除装修情况为空或为零的记录，并将结果存储为 cleaned_data_c1_N.csv， N 为删除的数据条数；
#第 (1) 步：空值(isna)和字符串"0"都算无效装修情况，两者取“或”后删除
clean1 = (tourist_data["装修情况"].isna()) | (tourist_data["装修情况"] == "0")
clean1_data = tourist_data[~clean1]
N1 = clean1.sum()
filename1 = f'cleaned_data_c1_{N1}.csv'
clean1_data.to_csv(filename1,index=False)

#删除建筑面积异常（超过 500 ㎡或小于 20 ㎡）的记录，并将结果存储为 cleaned_data_c2_N.csv，N 为删除的数据条数；
#第 (2) 步：面积过大或过小都属于异常，两个条件取“或”
clean2_copy = clean1_data.copy()
clean2 = (clean2_copy['建筑面积（㎡）'] > 500 )|(clean2_copy['建筑面积（㎡）'] < 20 )
clean2_data = clean2_copy[~clean2]
N2 = clean2.sum()
filename2 = f'cleaned_data_c2_{N2}.csv'
clean2_data.to_csv(filename2,index=False)

#将朝向为空的记录填充为"未知"，并存储为 cleaned_data_c3_N.csv，N 为修改的数据条数；
#第 (3) 步：本步是“填充”不是删除，所以 N 取被填充的条数，用填充前的 isna 标记统计
clean3_copy = clean2_data.copy()
mark = clean3_copy["朝向"].isna()
N3 = mark.sum()
clean3_copy['朝向'] = clean3_copy['朝向'].fillna("未知")
filename3 = f'cleaned_data_c3_{N3}.csv'
clean3_copy.to_csv(filename3,index=False)

#将成交单价超出范围（低于 5000 元/㎡或高于 200000 元/㎡）的记录删除， 并将结果存储为 cleaned_data_c4_N.csv，N 为删除的数据条数；
#第 (4) 步：上限是 200000 元/㎡（题目原文），不是 20000，写错会误删大量正常房源
clean4_copy = clean3_copy.copy()
clean4 = (clean4_copy["成交单价（元/㎡）"] < 5000) | (clean4_copy["成交单价（元/㎡）"] > 200000)
N4 = clean4.sum()
clean4_data = clean4_copy[~clean4]
filename4 = f'cleaned_data_c4_{N4}.csv'
clean4_data.to_csv(filename4,index=False)

#将成交总价明显异常（超过该小区平均成交总价 5 倍）的记录删除，将结果存储为 cleaned_data_c5_N.csv，N 为删除的数据条数。
#第 (5) 步：题目要求对比的是“该小区”的平均成交总价，所以必须按小区名称分组求均值，不能用全表均值
clean5_copy = clean4_data.copy()
#transform 把每个小区的均值按行广播回原表，长度与 clean5_copy 一致，便于逐行比较
avg = clean5_copy.groupby('小区名称')['成交总价（万元）'].transform('mean')
clean5 = clean5_copy["成交总价（万元）"] > avg * 5
N5 = clean5.sum()
clean5_data = clean5_copy[~clean5]
filename5 = f'cleaned_data_c5_{N5}.csv'
clean5_data.to_csv(filename5,index=False)
