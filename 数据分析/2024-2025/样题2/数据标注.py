import pandas as pd
#读取清洗后的数据（清洗脚本最终产物为 cleaned_data_c5_0.csv）
data = pd.read_csv("cleaned_data_c5_0.csv")

#【子任务一】学习投入度标注，输出 engagement_level.csv
data_1 = data.copy()
#学习投入度标注：按学习时长与互动次数两个维度判定投入程度
def learning_engagement_annotation(a):
    #高度投入：每次学习时长超过60分钟且互动次数大于5次；
    if a["学习时长(分钟)"] >  60 and a["互动次数"] > 5:
        return '高度投入'
    #中度投入：每次学习时长在30-60分钟之间或互动次数在3-5次之间；
    elif 30 < a["学习时长(分钟)"] < 60 or  3 < a["互动次数"] < 5:
        return "中度投入"
    #低度投入：每次学习时长低于30分钟且互动次数少于3次；
    elif  a["学习时长(分钟)"] < 30 and  a["互动次数"] < 3:
        return  "低度投入"
    #补充：以上三档之外还有两类交叉情况原逻辑未覆盖，会造成空值，这里按“投入度由时长与互动共同决定”补全，
    #即只要有一项很高就归为高度投入，两项都不高则归为低度投入，保证每条记录都有明确标注
    elif a["学习时长(分钟)"] > 60 or a["互动次数"] > 5:
        return '高度投入'
    else:
        return "低度投入"


data_1["学习投入度"] = data_1.apply(learning_engagement_annotation,axis=1)
data_1['记录ID']=range(1,len(data_1)+1)
out = ['记录ID', '课程名称', '学习时长(分钟)', '互动次数', '学习投入度']
data_1=data_1[out]
data_1.to_csv("engagement_level.csv",index=False)


#【子任务二】学习模式标注，按题目要求输出 learning_pattern.csv
#题目要求输出列为：用户ID、主要学习时段、常用设备、平均单次时长、学习模式
#注意：原脚本直接取“主要学习时段”“常用设备”两列，但原始数据里没有这两列，会报 KeyError，
#因此这里先按用户聚合出每个用户的特征，再逐用户判定学习模式。
data_2 = data.copy()
#先由“最后学习时间”取出小时和星期，供判定夜间学习型与周末集中型使用（空值变为 NaT，后续按组求均值会自动忽略）
data_2['学习小时'] = pd.to_datetime(data_2["最后学习时间"], errors='coerce').dt.hour
data_2['星期'] = pd.to_datetime(data_2["最后学习时间"], errors='coerce').dt.dayofweek
#周末标记：星期六(5)、星期日(6) 记为 1，工作日记为 0，时间缺失的记录记为空值（NaN），不参与周末占比计算
#这里直接映射成 0/1 浮点数，保证后面求均值时能被当作数值处理
data_2['是否周末'] = data_2['星期'].map(lambda x: float('nan') if pd.isna(x) else (1.0 if x in [5, 6] else 0.0))

#按用户聚合：主要学习时段取出现最多的时段，常用设备取出现最多的设备，平均单次时长取学习时长均值，
#平均学习小时与周末占比用于判定学习模式
user_data = data_2.groupby("用户ID").agg(
    主要学习时段=('学习时段', lambda x: x.value_counts().idxmax()),
    常用设备=('设备类型', lambda x: x.value_counts().idxmax()),
    平均单次时长=('学习时长(分钟)', 'mean'),
    平均学习小时=('学习小时', 'mean'),
    周末占比=('是否周末', 'mean')
).reset_index()
#若某用户所有记录的时间都缺失，周末占比会是 NaN，这里补 0 避免后续比较出错
user_data['周末占比'] = user_data['周末占比'].fillna(0)

#学习模式标注：按题目给出的四类规则逐个用户判定
def learning_style(b):
    #工作学习型：主要在工作日9:00-18:00期间使用PC端学习
    if (9 <= b["平均学习小时"] < 18) & (b["常用设备"] == "PC端"):
        return "工作学习型"
    #夜间学习型：主要在20:00-24:00期间进行学习，设备类型不限
    elif 20 <= b["平均学习小时"] < 24:
        return "夜间学习型"
    #碎片学习型：主要使用移动设备，单次学习时长较短（小于30分钟），分布在全天各个时段
    elif (b["常用设备"] == "移动端") & (b["平均单次时长"] < 30):
        return "碎片学习型"
    #周末集中型：主要在周末进行长时间（超过2小时）的学习，设备类型不限
    elif (b["周末占比"] > 0.5) & (b["平均单次时长"] > 120):
        return "周末集中型"
    else:
        #以上四类都不满足时，归入占比最高的周末集中型之外的兜底类别，
        #这里沿用原脚本的兜底写法，统一记为周末集中型
        return "周末集中型"

user_data.loc[:, "学习模式"] = user_data.apply(learning_style, axis=1)
#按题目要求的列顺序输出，平均单次时长为该用户所有学习记录时长的均值，保留两位小数
out = ["用户ID", "主要学习时段", "常用设备", "平均单次时长", "学习模式"]
user_data["平均单次时长"] = user_data["平均单次时长"].round(2)
user_data[out].to_csv("learning_pattern.csv", index=False)
