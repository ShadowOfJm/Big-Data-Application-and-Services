import pandas as pd
#读取原始房价数据
house_sales = pd.read_csv("house_sales.csv")
#先预览前10行，确认列名和脏数据情况
print(house_sales.head(10))

#c1：删除面积为空或为零的记录，并将结果存储为 cleaned_data_c1_N.csv，N 为删除的数据条数；
#布尔条件：面积等于0 或 面积为空值
clean1 = (house_sales["面积(㎡)"] == 0) | (house_sales["面积(㎡)"].isna())
#N1 = 被删除的条数，直接写进文件名
N1 = clean1.sum()
filename_1 = f"cleaned_data_c1_{N1}.csv"
#取反 ~clean1 保留符合条件的正常记录
clean1_data = house_sales[~clean1]
clean1_data.to_csv(filename_1,index=False)


#c2：删除"价格(万元)"为空或异常高（超过平均价格的3倍）的记录，并将结果存储为 cleaned_data_c2_N.csv，N 为删除的数据条数
#在 c1 结果的基础上继续清洗
clean2_copy = clean1_data.copy()
#以当前价格的平均值作为衡量"异常高"的基准
avg_price = clean2_copy["价格(万元)"].mean()
#布尔条件：价格为空 或 价格超过均价的3倍
clean2 = (clean2_copy["价格(万元)"].isna()) | (clean2_copy["价格(万元)"] > avg_price *3)
N2 = clean2.sum()
filename_2 = f"cleaned_data_c2_{N2}.csv"
#取反保留正常记录
clean2_data = clean2_copy[~clean2]
clean2_data.to_csv(filename_2,index=False)


#c3：对房型数据进行标准化，例如将不规范的房型描述（2房间2卫）转换为标准格式（2室0厅），并存储为 cleaned_data_c3_N.csv，N 为修改的数据条数
clean3_copy = clean2_data.copy()
#替换前先记录一次房型列，用于后面统计真正被改动过的条数
old_hx = clean3_copy["户型"].copy()
#把不规范的"2房间2卫"统一替换成"2室0厅"
clean3_copy["户型"] = clean3_copy["户型"].str.replace("2房间2卫","2室0厅")
#N3 = 户型真正发生变化（修改过）的条数
N3 = (clean3_copy["户型"] != old_hx).sum()
filename_3 = f"cleaned_data_c3_{N3}.csv"
clean3_copy.to_csv(filename_3,index=False)


#c4：删除电梯字段为空白的记录，并将结果存储为 cleaned_data_c4_N.csv，N 为删除的数据条数；
clean4_copy = clean3_copy.copy()
#电梯为空（CSV 中的空白读入后就是 NaN）
clean4 = clean4_copy["电梯"].isna()
N4 = clean4.sum()
filename_4 = f"cleaned_data_c4_{N4}.csv"
clean4_data = clean4_copy[~clean4]
clean4_data.to_csv(filename_4,index=False)


#c5：删除面积(㎡)小于20的记录，将结果存储为 cleaned_data_c5_N.csv，N 为删除的数据条数；
clean5_copy = clean4_data.copy()
#只保留面积大于等于20的房源
clean5_data = clean5_copy[clean5_copy["面积(㎡)"] >= 20]
#N5 = 清洗前后的条数差，即被删除的条数
N5 = len(clean5_copy)-len(clean5_data)
filename_5 = f"cleaned_data_c5_{N5}.csv"
clean5_data.to_csv(filename_5,index=False)
