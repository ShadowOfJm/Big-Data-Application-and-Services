import pandas as pd
data = pd.read_csv("cleaned_data_c5_54.csv")

#分析各景区的游客来源地分布，找出每个景区最主要的客源地（占比超过 20%）
#按“景区名称+游客来源地”分组计数，再除以该景区的游客总数，得到各来源地的占比
a = data.groupby(["景区名称","游客来源地"]).size().reset_index(name="人数")
a["占比"] = a["人数"] / a.groupby("景区名称")["人数"].transform("sum")
print("=====（1）各景区客源地分布（占比超过20%的客源地）=====")
#实际数据里客源地很分散，先统计一下到底有没有占比超过20%的，避免这一问输出为空
over = a[a["占比"] > 0.2]
print(f"全年占比超过20%的“景区-客源地”组合共 {len(over)} 个")
for name, g in a.groupby("景区名称"):
    #占比降序排列，先按题目口径取超过20%的客源地
    g = g.sort_values("占比", ascending=False)
    main = g[g["占比"] > 0.2]
    if len(main) > 0:
        txt = "、".join(f"{r['游客来源地']}({r['占比']*100:.1f}%)" for _, r in main.iterrows())
        print(f"{name}：主要客源地 {txt}")
    else:
        #没有客源地超过20%时，补充输出该景区占比最高的前3个客源地，作为“最主要客源地”的参考
        top3 = g.head(3)
        txt = "、".join(f"{r['游客来源地']}({r['占比']*100:.1f}%)" for _, r in top3.iterrows())
        print(f"{name}：无客源地占比超20%，占比最高的前3位为 {txt}")


#不同年龄段游客的平均消费金额和平均停留时长，发现最具消费潜力的群体
#按年龄段分组，对消费金额和停留时长分别求均值
b = data.groupby("游客年龄段").agg(平均消费=("消费金额（元）","mean"), 平均停留=("停留时长（小时）","mean"), 人数=("景区名称","count"))
b = b.round(2).sort_values("平均消费", ascending=False)
print("\n=====（2）不同年龄段的平均消费与平均停留时长 =====")
print(b)
#平均消费最高的年龄段即为最具消费潜力的群体
print(f"最具消费潜力群体：{b.index[0]}（平均消费{b['平均消费'].iloc[0]:.2f}元，平均停留{b['平均停留'].iloc[0]:.2f}小时）")


#周末和工作日的游客量差异，计算周末相对工作日的增长百分比
#把日期转成星期：0-4为周一至周五（工作日），5-6为周六周日（周末）
data["星期"] = pd.to_datetime(data["日期"]).dt.dayofweek
weekend = data[data["星期"] >= 5]
workday = data[data["星期"] < 5]
#用日均游客量比较更公平：周末共约104天，工作日约261天
weekend_avg = len(weekend) / weekend["日期"].nunique()
workday_avg = len(workday) / workday["日期"].nunique()
growth = (weekend_avg - workday_avg) / workday_avg * 100
print("\n=====（3）周末与工作日游客量差异 =====")
print(f"周末游客总量：{len(weekend)} 人次，日均 {weekend_avg:.2f} 人次")
print(f"工作日游客总量：{len(workday)} 人次，日均 {workday_avg:.2f} 人次")
print(f"周末相对工作日日均增长：{growth:.2f}%")


#不同出行方式的游客比例，并按平均消费金额排序
#按出行方式分组计数求占比，同时算平均消费，最后按平均消费降序排列
c = data.groupby("出行方式").agg(人数=("景区名称","count"), 平均消费=("消费金额（元）","mean"))
c["比例"] = (c["人数"] / len(data) * 100).round(2)
c["平均消费"] = c["平均消费"].round(2)
c = c.sort_values("平均消费", ascending=False)
print("\n=====（4）不同出行方式占比（按平均消费降序） =====")
print(c)


#满意度评分与停留时长的相关系数
#用皮尔逊相关系数衡量两者线性相关程度，取值-1到1，绝对值越大相关性越强
r = data["满意度评分"].corr(data["停留时长（小时）"])
print("\n=====（5）满意度评分与停留时长的相关系数 =====")
print(f"相关系数 r = {r:.4f}")
