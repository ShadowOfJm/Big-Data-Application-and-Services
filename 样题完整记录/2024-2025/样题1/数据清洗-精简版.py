import pandas as pd
house_sales = pd.read_csv("house_sales.csv")
print(house_sales.head(10))

#删除面积为空或为零的记录，并将结果存储为 cleaned_data_c1_N.csv，N 为删除的数据条数
clean1 = (house_sales["面积(㎡)"] == 0) | (house_sales["面积(㎡)"].isna())
N1 = clean1.sum()
filename_1 = f"cleaned_data_c1_{N1}.csv"
clean1_data = house_sales[~clean1]
clean1_data.to_csv(filename_1,index=False)


#删除“价格(万元)”为空或异常高（超过平均价格的3倍）的记录，并将结果存储为 cleaned_data_c2_N.csv，N 为删除的数据条数
clean2_copy = clean1_data.copy()
avg_price = clean2_copy["价格(万元)"].mean()
clean2 = (clean2_copy["价格(万元)"].isna()) | (clean2_copy["价格(万元)"] > avg_price *3)
N2 = clean2.sum()
filename_2 = f"cleaned_data_c2_{N2}.csv"
clean2_data = clean2_copy[~clean2]
clean2_data.to_csv(filename_2,index=False)


#对房型数据进行标准化，例如将不规范的房型描述（2房间2卫）转换为标准格式（2室0厅），并存储为 cleaned_data_c3_N.csv，N 为修改的数据条数
clean3_copy = clean2_data.copy()
cs =  len(clean3_copy)
clean3_copy["户型"] = clean3_copy["户型"].str.replace("2房间2卫","2室0厅")
N3 = len(clean3_copy) - cs
filename_3 = f"cleaned_data_c3_{N3}.csv"
clean3_copy.to_csv(filename_3,index=False)


#删除电梯字段为空白的记录，并将结果存储为 cleaned_data_c4_N.csv，N 为删除的数据条数；
clean4_copy = clean3_copy.copy()
clean4 = clean4_copy["电梯"].isna()
N4 = clean4.sum()
filename_4 = f"cleaned_data_c4_{N4}.csv"
clean4_data = clean4_copy[~clean4]
clean4_data.to_csv(filename_4,index=False)


#删除面积(㎡)小于20的记录，将结果存储为 cleaned_data_c5_N.csv，N 为删除的数据条数；
clean5_copy = clean4_data.copy()
clean5 = clean5_copy[clean5_copy["面积(㎡)"] >= 20]
N5 = len(clean5_copy) - len(clean5)
filename_5 = f"cleaned_data_c5_{N5}.csv"
clean5.to_csv(filename_5,index=False)