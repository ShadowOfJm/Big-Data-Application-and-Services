import pandas as pd

weather_observations = pd.read_csv("weather_observations.csv")
#打印数据集前 10 行（项目二 任务一 子任务一：数据获取，需截图）
print(weather_observations.head(10))

#删除“降水量”为空值且“天气现象”不为“雨”或“雪”的无效记录（即疑似缺失的记录），并将结果存储为 cleaned_weather_c1_N.csv，N 为删除的数据条数；
#第 (1) 步：只有“降水为空”并且“不是雨/雪”才算疑似缺失；雨雪天降水为空属正常留空，不删
precip_null = weather_observations["降水量(mm)"].isna()
weather_not_precip = ~weather_observations["天气现象"].astype(str).str.strip().isin(["雨", "雪"])
clean1_mark = precip_null & weather_not_precip
clean1_data = weather_observations[~clean1_mark].copy()
N1 = clean1_mark.sum()
filename1 = f"cleaned_weather_c1_{N1}.csv"
clean1_data.to_csv(filename1, index=False)

#识别并删除物理上不可能的异常记录（如：气温低于-50℃或高于 50℃， 气压低于 800hPa 或高于 1100hPa），将结果存储为 cleaned_weather_c2_N.csv，N 为删除的数据条数；
#第 (2) 步：气温、气压任一越界即判为物理不可能，两者取“或”合成一个删除标记
clean2 = clean1_data.copy()
air_temperature = (clean2["气温(℃)"] < -50) | (clean2["气温(℃)"] > 50)
air_pressure = (clean2["气压(hPa)"] < 800) | (clean2["气压(hPa)"] > 1100)
clean2_mark = air_pressure | air_temperature
N2 = clean2_mark.sum()
clean2_data = clean2[~clean2_mark].copy()
filename2 = f"cleaned_weather_c2_{N2}.csv"
clean2_data.to_csv(filename2, index=False)

#将“观测日期”和“观测时间”两列合并为标准的 YYYY-MM-DD HH:MM:SS 格式的“观测时间戳”列，并删除原两列，将结果存储为 cleaned_weather_c3_N.csv，N 为总记录条数（此项无需统计修改量，N 为处理后数据总行数）；
#第 (3) 步：先拼成“日期 时间”再统一转成 YYYY-MM-DD HH:MM:SS，最后删掉原来的两列
clean3 = clean2_data.copy()
clean3['观测时间戳'] = pd.to_datetime(clean3['观测日期'].astype(str) + ' ' + clean3['观测时间'].astype(str)).dt.strftime('%Y-%m-%d %H:%M:%S')
clean3.drop(columns=['观测日期', '观测时间'], inplace=True)
#题目明确本步 N 取“处理后数据总行数”，不是修改量
N3 = len(clean3)
filename3 = f'cleaned_weather_c3_{N3}.csv'
clean3.to_csv(filename3, index=False)

#删除所有字段完全相同的重复观测记录，并将结果存储为 cleaned_weather_c5_N.csv，N 为删除的数据条数；
#第 (4) 步：题目编号直接跳到 c5（没有 c4），N = 删除前的行数 - 去重后的行数
clean5 = clean3.copy()
clean5.drop_duplicates(inplace = True)
N5 = N3 - len(clean5)
filename5 = f'cleaned_weather_c5_{N5}.csv'
clean5.to_csv(filename5, index=False)
