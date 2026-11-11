import pandas as pd
#读取清洗后的数据。说明：清洗步骤(4)输出的文件名是 cleaned_data_c5_N.csv（跳过 c4，没有 c4），
#目录中实际文件为 cleaned_data_c5_19.csv，原脚本读取的 cleaned_data_c4_19.csv 不存在，此处修正
data = pd.read_csv("cleaned_data_c5_19.csv")
data_1 = data.copy()
#【子任务一】骑行距离分类标注，输出 ride_distance_mark.csv
def ride_distance_mark(a):
    #短途：骑行距离小于2公里；
    if a["骑行距离(km)"] < 2:
        return "短途"
    #中途：骑行距离在2公里至5公里之间
    elif 2 <= a["骑行距离(km)"] < 5:
        return "中途"
    #长途：骑行距离超过5公里
    #修正：原代码写成 > 2，会把已经判定为“中途”的区间重复覆盖，这里改为 >= 5
    elif a["骑行距离(km)"] >= 5:
        return "长途"
    #兜底：距离为空等异常情况，标为未知，避免产生空值
    else:
        return "未知"
#先按题目要求挑选输出列，再在挑选后的表上做标注，避免后续列名改动导致取列失败
list_out = ["骑行ID","开始时间","骑行距离(km)"]
data_1 = data_1[list_out]
data_1.loc[:,"距离分类"] = data_1.apply(ride_distance_mark,axis=1)
data_1.to_csv("ride_distance_mark.csv",index=False)

#【子任务二】时段热度标注，输出 time_period_mark.csv
def time_period_mark(b):
    time = pd.to_datetime(b["开始时间"])
    hour = time.hour
    if b["周末标记"] == 0:
        #高峰时段：工作日的7:00-9:00和17:00-19:00
        #修正：原代码 7 < hour < 9 实际只含 8 点，改为 7 <= hour <= 9，与题目区间一致
        if (7 <= hour <= 9) or (17 <= hour <= 19):
            return "高峰时段"
        #平峰时段：工作日的9:00-17:00和19:00-22:00
        #注意：上面的高峰已覆盖 9 点和 17~19 点，这里按顺序判断，先命中的分支优先
        elif (9 <= hour <= 17) or (19 <= hour < 22):
            return "平峰时段"
        #低峰时段：工作日的22:00-次日7:00
        elif (22 <= hour <= 23) or (0 <= hour <= 7):
            return "低峰时段"
        #兜底：理论上不会走到这里，返回低峰时段保证每条都有标注
        else:
            return "低峰时段"
    else:
        #低峰时段：周末全天
        return "低峰时段"
list_out_1 = ["骑行ID","开始时间","周末标记"]
data = data[list_out_1]
data.loc[:,"时段热度"] = data.apply(time_period_mark,axis=1)
data.to_csv("time_period_mark.csv",index=False)
