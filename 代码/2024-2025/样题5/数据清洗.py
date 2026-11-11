import pandas as pd

#读取原始酒店数据
hotel = pd.read_csv("hotel.csv")
#先预览前10行，确认列名和脏数据情况
print(hotel.head(10))

#c1：删除酒店名称为空的记录，将结果存储为 cleaned_data_c1_N.csv，N为删除的数据条数。
#CSV 里的空白字段读入后就是 NaN，用 isna() 即可定位
clean1 = hotel["酒店名称"].isna()
#N1 = 被删除的条数
N1 = clean1.sum()
filename_1 = f'cleaned_data_c1_{N1}.csv'
#取反保留名称不为空的记录
clean1_data = hotel[~clean1]
clean1_data.to_csv(filename_1,index=False)

#c2：将评分数据中的空值替换为0分，包括卫生评分、服务评分、设施评分和位置评分，将结果存储为 cleaned_data_c2_N.csv，N为修改的数据条数
clean2_copy = clean1_data.copy()
#创建一个要处理数据的列表
cl = ["卫生评分","服务评分","设施评分","位置评分"]
#统计一共有多少空值  第一个.sum()是先按照列来求出有多少空值,第二个.sum()是对第一个的结果（一个包含各列空值数的 Series）再求和
N2 = clean2_copy[cl].isna().sum().sum()
filename_2 = f"cleaned_data_c2_{N2}.csv"
#将空值替换为0
clean2_data = clean2_copy.fillna(value={col:0 for col in cl})
clean2_data.to_csv(filename_2,index=False)


#c3：删除评价数为0但任一评分项不为0的矛盾记录，将结果存储为 cleaned_data_c3_N.csv，N为删除的数据条数。
clean3_copy = clean2_data.copy()
#找出评价数为0
clean3 = clean3_copy["评价数"] == 0
#找出任一评分项不为0（any(axis=1) 表示逐行判断，只要有一列为真就算真）
pf = (clean3_copy[cl] != 0).any(axis=1)
#统计出符合这两个条件的数据：评价数为0和任一评分项不为0
tj = pf & clean3
N3 = tj.sum()
filename_3 = f'cleaned_data_c3_{N3}.csv'
#取反删除这些矛盾记录
clean3_data =clean3_copy[~tj]
clean3_data.to_csv(filename_3,index=False)


#c4：将装修时间为空的记录设置为数据集中最常见的装修时间，将结果存储为 cleaned_data_c4_N.csv，N为修改的数据条数。
clean4_copy = clean3_data.copy()
#找出最常见的装修时间，dropna=True会自动排除null
most_time = clean4_copy["装修时间"].mode(dropna=True)
#取第一个最常见的值
most_full = most_time.iloc[0]
#装修时间为空的条数就是要修改的条数
clean4 = clean4_copy["装修时间"].isna()
N4 = clean4.sum()
filename_4 = f'cleaned_data_c4_{N4}.csv'
#用最常见的装修时间填充空值
clean4_copy.fillna({"装修时间":most_full},inplace=True)
clean4_copy.to_csv(filename_4,index=False)


#c5：删除地址字段完全为空的记录，将结果存储为 cleaned_data_c5_N.csv，N 为删除的数据条数
clean5_copy = clean4_copy.copy()
#地址为空即 NaN
clean5 = clean5_copy["地址"].isna()
N5 = clean5.sum()
filename_5 =  f"cleaned_data_c5_{N5}.csv"
#取反保留地址不为空的记录
clean5_data = clean5_copy[~clean5]
clean5_data.to_csv(filename_5,index=False)


#c6：将房价为0或空值的记录删除，将结果存储为 cleaned_data_c6_N.csv，N为删除的数据条数
clean6_copy = clean5_data.copy()
#房价为0 或 房价为空，两类都算异常
clean6 = (clean6_copy["房价"]==0) | (clean6_copy["房价"].isna())
N6 = clean6.sum()
filename_6 =f"cleaned_data_c6_{N6}.csv"
clean6_data = clean6_copy[~clean6]
clean6_data.to_csv(filename_6,index=False)


#c7：统一房间类型的表述，将"标准间"、"标准房"统一改为"标准双人房"，将结果存储为 cleaned_data_c7_N.csv，N为修改的数据条数
clean7_copy = clean6_data.copy()
#先统计"标准间"和"标准房"两种不规范写法共有多少条
clean7 = (clean7_copy["房间类型"] == "标准间") | (clean7_copy["房间类型"] == "标准房")
N7 = clean7.sum()
filename_7 = f"cleaned_data_c7_{N7}.csv"
#统一文本格式：df['列名'] = df['列名'].str.replace('旧格式', '新格式')
#注意：原写法 str.replace("标准间" or "标准房", ...) 里的 or 只会取到"标准间"，"标准房"永远替换不到
#所以这里拆成两次替换，两种写法都统一成"标准双人房"
clean7_copy["房间类型"] = clean7_copy["房间类型"].str.replace("标准间","标准双人房")
clean7_copy["房间类型"] = clean7_copy["房间类型"].str.replace("标准房","标准双人房")
clean7_copy.to_csv(filename_7,index=False)


#c8：删除四项评分（卫生评分、服务评分、设施评分、位置评分）均为0的记录，将结果存储为 cleaned_data_c8_N.csv，N为删除的数据条数。
clean8_copy = clean7_copy.copy()
#四项评分同时为0才算无效记录，所以用 & 连接四个条件
clean8 = (clean8_copy["卫生评分"] == 0) & (clean8_copy["服务评分"] == 0) & (clean8_copy["设施评分"] == 0) & (clean8_copy["位置评分"] == 0)
N8 = clean8.sum()
filename_8 = f"cleaned_data_c8_{N8}.csv"
clean8_data = clean8_copy[~clean8]
clean8_data.to_csv(filename_8,index=False)


#c9：将评分超过5分的无效值修正为5分，将结果存储为 cleaned_data_c9_N.csv，N为修改的数据条数
#直接沿用上一步的内存结果，不再从磁盘按固定文件名（带 N）反读，避免文件名一变就报错
clean9_copy = clean8_data.copy()
cl = ["卫生评分","服务评分","设施评分","位置评分"]
#先留一份改分前的副本，用于统计到底改了多少个格子
jl = clean9_copy[cl].copy()
#df.loc[df['列名'] > 上限, '列名'] = 上限
for i in cl:
    clean9_copy.loc[clean9_copy[i] > 5, i] = 5
#逐格比较改前改后是否不同，求和得到被修正的条数
change = jl !=  clean9_copy[cl]
N9 = change.sum().sum()
filename_9 = f"cleaned_data_c9_{N9}.csv"
clean9_copy.to_csv(filename_9,index=False)


#c10：识别并删除完全重复的记录（所有字段值都相同），将结果存储为 cleaned_data_c10_N.csv，N为删除的数据条数。
clean10_copy = clean9_copy.copy()
#keep="first" 表示重复记录保留第一条
clean10 = clean10_copy.drop_duplicates(keep="first")
#N10 = 去重前后条数差
N10 = len(clean10_copy) - len(clean10)
filename_10 = f"cleaned_data_c10_{N10}.csv"
clean10.to_csv(filename_10,index=False)
