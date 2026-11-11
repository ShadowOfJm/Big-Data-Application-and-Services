import pandas as pd
data = pd.read_csv("cleaned_data_c5_54.csv")

#1. 子任务一：游客价值分类标注
#先算出全部游客的平均消费金额，作为后面划分高/中/低价值的分界基准
avg_price = data["消费金额（元）"].mean()
def tourist_value_mark(a):
    #高价值游客：消费金额高于平均值的1.5倍且停留时长超过4小时
    if (a["消费金额（元）"] > avg_price * 1.5) & (a["停留时长（小时）"] > 4):
        return "高价值游客"
    #中价值游客：消费金额在平均值的0.5-1.5倍之间且停留时长在2-4小时之间
    elif (avg_price*0.5 < a["消费金额（元）"] < avg_price*1.5) & (2 < a["停留时长（小时）"] < 4):
        return "中价值游客"
    #低价值游客：不满足上述条件的游客
    else:
        return "低价值游客"

#按题目要求的列顺序整理数据，并给每条记录加上从1开始的编号
data["编号"]= range(1,len(data)+1)
data_list = ["编号","景区名称","消费金额（元）","停留时长（小时）"]
data = data[data_list].copy()
#逐行调用上面的判定函数，生成“游客价值类型”列（对应子任务一）
data.loc[:,"游客价值类型"] = data.apply(tourist_value_mark,axis=1)
#输出子任务一的结果文件：tourist_value_mark.csv
data.to_csv("tourist_value_mark.csv",index=False)


#2. 子任务二：旅游旺季标注
#子任务一把data的列裁剪过了，这里重新读一份清洗数据，保留“日期”列用于按月统计
data2 = pd.read_csv("cleaned_data_c5_54.csv")
#把“日期”转成月份：数据是2024年整年，取出1-12月
data2["月份"] = pd.to_datetime(data2["日期"]).dt.month
#按月分组统计：游客总量=当月记录条数，平均消费=当月消费金额的均值
month_data = data2.groupby("月份").agg(游客总量=("景区名称","count"), 平均消费=("消费金额（元）","mean")).reset_index()
#把聚合结果的列名改成带单位的“平均消费（元）”，方便和清洗数据里的列名对齐
month_data = month_data.rename(columns={"平均消费": "平均消费（元）"})
month_data["平均消费（元）"] = month_data["平均消费（元）"].round(2)
#计算年平均值：全年总游客量/12得到“年平均月游客量”，全年消费均值作为“年平均消费”
avg_count = len(data2) / 12
avg_money = data2["消费金额（元）"].mean()
#“同比年平均”：该月游客量、平均消费分别是全年平均水平的百分之多少，合成一列便于对照
month_data["同比年平均"] = [f"游客量{x/avg_count*100:.1f}% 消费{y/avg_money*100:.1f}%" for x,y in zip(month_data["游客总量"], month_data["平均消费（元）"])]
def season_mark(b):
    #旺季：月游客量超过年平均值的120 % 且月平均消费超过年平均值的110 %
    if (b["游客总量"] > avg_count * 1.2) & (b["平均消费（元）"] > avg_money * 1.1):
        return "旺季"
    #平季：月游客量在年平均值的80%-120%之间，或月平均消费在年平均值的90%-110%之间
    elif ((avg_count*0.8 <= b["游客总量"] <= avg_count*1.2) | (avg_money*0.9 <= b["平均消费（元）"] <= avg_money*1.1)):
        return "平季"
    #淡季：其余情况，即月游客量低于年平均值的80 % 且月平均消费低于年平均值的90 %（含一高一低的过渡月份）
    else:
        return "淡季"

#逐行判定每个月的季节类型（对应子任务二）
month_data["季节类型"] = month_data.apply(season_mark,axis=1)
#按题目要求的列顺序整理，输出子任务二的结果文件：season_mark.csv
month_data = month_data[["月份","游客总量","平均消费（元）","同比年平均","季节类型"]]
month_data.to_csv("season_mark.csv",index=False)
