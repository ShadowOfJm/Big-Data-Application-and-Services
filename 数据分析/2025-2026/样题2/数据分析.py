import pandas as pd
#读取样题2清洗脚本的最终产物 cleaned_step5_55.csv（1900 条记录），五项分析都基于这份数据
data = pd.read_csv("cleaned_step5_55.csv")

#统一“最近学习日期”为日期类型，供第（5）问统计学习天数使用
#清洗脚本已把该列规范成 YYYY-MM-DD，这里再转一次日期类型是为了后续能按天去重、按区间筛选
#errors='coerce' 保证遇到个别无法解析的值时变成空值而不是直接报错
data["最近学习日期"] = pd.to_datetime(data["最近学习日期"], errors="coerce")

#（1）计算各“课程类别”的平均“最终通过率”，筛选出高于平台整体平均通过率的类别，按通过率从高到低排序
#说明：原始数据没有“最终通过率”字段，只有“章节完成率”（0~1 的小数，表示课程章节的完成比例），
#它是这批数据里唯一能反映“课程完成/通过程度”的指标，因此用“章节完成率”作为“最终通过率”的替代指标
a = data.groupby("课程类别")["章节完成率"].mean()
#平台整体平均通过率 = 所有记录章节完成率的均值，作为筛选达标的基准线
avg_pass = data["章节完成率"].mean()
#筛出高于整体平均的类别，再倒序排列
a_pass = a[a > avg_pass].sort_values(ascending=False)
print("\n")
print(f"平台整体平均通过率{avg_pass:.4f}")
print(f"高于平台整体平均通过率的课程类别{a_pass}")

#（2）将一天划分为四个学习区间，计算每个区间内发起学习会话的独立用户数，找出最活跃的学习区间
#区间划分：清晨 5:00-10:59、午间 11:00-16:59、傍晚 17:00-21:59、深夜 22:00-4:59
#“学习时间段”字段是 0-23 的整点小时数，直接按小时归入对应区间
def time_interval(h):
    if 5 <= h <= 10:
        return "清晨(5:00-10:59)"
    elif 11 <= h <= 16:
        return "午间(11:00-16:59)"
    elif 17 <= h <= 21:
        return "傍晚(17:00-21:59)"
    else:
        return "深夜(22:00-4:59)"


data["学习区间"] = data["学习时间段"].astype(int).apply(time_interval)
#按区间统计“独立用户数”：先对 区间+学员ID 去重，再数每个区间有多少个不同的学员
b = data.drop_duplicates(["学习区间", "学员ID"]).groupby("学习区间")["学员ID"].nunique()
#倒序排列，排在第一的就是最活跃区间
b = b.sort_values(ascending=False)
print("\n")
print(f"各学习区间的独立用户数{b}")
print(f"最活跃的学习区间{b.idxmax()}")

#（3）分析不同“内容形式”的平均“用户满意度评分”，识别最受欢迎的内容形式
#说明：原始数据没有“用户满意度评分”字段，用“测试得分”（0~100 分）作为满意度评分的替代指标，
#它反映用户学完之后掌握内容的效果，得分越高说明对该内容形式的接受度越好
c = data.groupby("内容形式")["测试得分"].mean().sort_values(ascending=False)
print("\n")
print(f"不同内容形式的平均满意度评分{c}")
print(f"最受欢迎的内容形式{c.idxmax()}")

#（4）统计各类“登录设备”下的平均“单次访问时长”和“页面访问深度”，分析不同设备的典型使用场景
#说明：原始数据没有“单次访问时长”“页面访问深度”字段，
#用“学习时长(分钟)”作为单次访问时长的替代指标，用“章节完成率”作为页面访问深度的替代指标
#（章节完成率越高，说明这次访问看得越深入、翻的页面越多）
d = data.groupby("登录设备").agg(
    平均单次访问时长=("学习时长(分钟)", "mean"),
    平均页面访问深度=("章节完成率", "mean"),
    记录数=("学员ID", "size")
).sort_values("平均单次访问时长", ascending=False)
print("\n")
print(f"各类登录设备的平均单次访问时长与平均页面访问深度\n{d}")

#（5）定义“高留存用户”为在最近 30 天内累计学习天数≥10 天的用户，计算各门课程的“高留存用户占比”，找出占比最高的三门课程
#取数据中最大的学习日期作为“今天”，往前推 29 天构成最近 30 天窗口
end_date = data["最近学习日期"].max()
start_date = end_date - pd.Timedelta(days=29)
#先筛出落在最近 30 天窗口内的记录
recent = data[(data["最近学习日期"] >= start_date) & (data["最近学习日期"] <= end_date)]
#按 学员ID 统计这段时间内的“去重学习天数”
days = recent.groupby("学员ID")["最近学习日期"].nunique()
#学习天数达到 10 天及以上的即为高留存用户
high_users = days[days >= 10].index
print("\n")
print(f"最近30天窗口{start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
print(f"窗口内活跃用户数{len(days)},高留存用户数(累计学习天数>=10){len(high_users)}")

#计算各门课程的高留存用户占比：分子是该课程下的高留存用户数，分母是该课程下的全部独立用户数
e = data.groupby("课程名称")["学员ID"].nunique()
e_high = data[data["学员ID"].isin(high_users)].groupby("课程名称")["学员ID"].nunique()
#用 reindex 补齐没有高留存用户的课程（补 0），避免相减时对不齐
e_high = e_high.reindex(e.index).fillna(0)
ratio = (e_high / e).sort_values(ascending=False)
print(f"各门课程的高留存用户占比\n{ratio.head(3)}")

#补充说明：按题目“最近30天累计学习天数>=10天”的原始口径筛选，本数据集里没有任何用户达标
#（每位用户在任意 30 天窗口内的去重学习天数最多只有 6 天，数据整体学习频次偏低），
#因此上面这张占比表全部为 0。为了让结论不至于完全空白，这里再按“>=3 天”的放宽口径给出参考排名
if len(high_users) == 0:
    print("\n")
    print("注意：按题目口径（最近30天学习天数>=10天）本数据集无用户达标，以下为放宽到>=3天的参考结果")
    high_users_2 = days[days >= 3].index
    e_high_2 = data[data["学员ID"].isin(high_users_2)].groupby("课程名称")["学员ID"].nunique()
    e_high_2 = e_high_2.reindex(e.index).fillna(0)
    ratio_2 = (e_high_2 / e).sort_values(ascending=False)
    print(f"放宽口径(>=3天)的高留存用户占比前三名\n{ratio_2.head(3)}")
