import pandas as pd
#读取清洗后的数据（清洗脚本最终产物为 cleaned_data_c5_0.csv）
data = pd.read_csv("cleaned_data_c5_0.csv")

#【第(1)问】分析各类别课程的完课率，计算方法为：完成进度达到100%的学习者人数/课程报名总人数，
#并按完课率降序排列展示前三个类别
#计算每个类别的课程报名总人数
a = data.groupby("课程类别").size()
#计算每个类别中完成进度达到100%的学习者人数
b = data[data["完成进度"]==100].groupby("课程类别").size()
#用人数除以报名总人数得到完课率；reindex 保证没有满100%学员的类别也能对齐、不产生 NaN 缺失
c = b.reindex(a.index, fill_value=0)/a
d = c.to_frame(name="完课率")
sort = d.sort_values(by="完课率",ascending=False)
#展示完课率最高的前三个类别
print(f"完课率前三个类别：\n{sort.head(3)}")
print("\n")

#【第(2)问】计算每个时间段（上午：6:00-12:00、下午：12:00-18:00、晚上：18:00-24:00、凌晨：0:00-6:00）的平均学习时长，
#找出学习参与度最高的时间段
#说明：数据中已有“学习时段”列（取值 上午/下午/晚上/凌晨），该列完整无空值，直接分组即可；
#而“最后学习时间”列有 41 条空值，若用它推算小时，这些空值会被误归到“凌晨”，因此优先使用“学习时段”列。
avg_duration_per_period = data.groupby("学习时段")["学习时长(分钟)"].mean()
avg = pd.Series(avg_duration_per_period,name="平均学习时长")
avg_1 = avg.sort_values(ascending=False)
print(f"各时间段平均学习时长（降序）：\n{avg_1}")
#排在第一位的即学习参与度最高的时间段
print(f"学习参与度最高的时间段：{avg_1.index[0]}，平均学习时长 {avg_1.iloc[0]:.2f} 分钟")
print("\n")

#【第(4)问-前置】不同难度等级课程的平均测验成绩
#说明：原始数据没有“难度级别”字段，这里沿用按课程名称排序后依次映射 A、B、C…… 的方式作为难度等级。
sorted_unique_courses = data['课程名称'].drop_duplicates().sort_values()
num_courses = len(sorted_unique_courses)
course_levels = [chr(65 + i) for i in range(num_courses)]
course_to_level_map = dict(zip(sorted_unique_courses, course_levels))
data.loc[:,'等级'] = data['课程名称'].map(course_to_level_map)
#按课程名称和等级分组求平均测验成绩，观察难度梯度是否合理
pjcj = data.groupby(["课程名称","等级"])['测验成绩'].mean()
print(f"不同难度等级课程的平均测验成绩：\n{pjcj}")
print("\n")

#【第(4)问】统计每类设备（PC端、移动端、平板端）的使用比例和平均单次学习时长，分析用户的设备使用偏好
#使用比例 = 该类设备的记录数 / 全部记录数
all_p = data["用户ID"].count()
use_s = data.groupby("设备类型").size()
bili = use_s/all_p
print(f"各设备类型使用比例：\n{bili}")
#平均单次学习时长要按设备类型分别求均值，而不是对全表求一个总均值
one_s = data.groupby("设备类型")["学习时长(分钟)"].mean()
print(f"各设备类型平均单次学习时长：\n{one_s}")
#使用比例最高的设备即用户最偏好的设备
print(f"用户最偏好的设备类型：{bili.idxmax()}，占比 {bili.max():.2%}")
print("\n")

#【第(5)问】计算课程的学习黏性（连续学习天数大于7天的用户占比），找出最具吸引力的三门课程
#先用“最后学习时间”取出每条学习记录的日期（空值先丢掉，避免参与计算）
data['学习日期'] = pd.to_datetime(data["最后学习时间"], errors='coerce').dt.date

#计算每个用户出现过的不同学习日期，并去重排序
user_days = data.dropna(subset=['学习日期']).groupby("用户ID")["学习日期"].apply(lambda x: sorted(set(x)))

#定义一个函数，求某个用户最长连续学习天数
def max_continue_days(days):
    #没有学习日期则连续天数为0
    if len(days) == 0:
        return 0
    max_days = 1
    cur = 1
    #从第二天开始，逐日与前一天比较：相差1天则连续，否则连续中断重新计数
    for i in range(1, len(days)):
        if (days[i] - days[i-1]).days == 1:
            cur += 1
            max_days = max(max_days, cur)
        else:
            cur = 1
    return max_days

#对每个用户计算最长连续学习天数
user_continue = user_days.apply(max_continue_days)
#连续学习天数大于7天的用户为高黏性用户
sticky_users = user_continue[user_continue > 7]
#黏性用户占比 = 黏性用户数 / 全部用户数
sticky_rate = len(sticky_users)/len(user_continue)
print(f"连续学习天数大于7天的用户数：{len(sticky_users)}，总用户数：{len(user_continue)}")
print(f"课程学习黏性（连续学习天数>7天用户占比）：{sticky_rate:.2%}")
print("\n")

#计算参与课程吸引力排序的用户群体
if len(sticky_users) > 0:
    #有满足>7天的用户时，直接以高黏性用户的学习记录统计课程吸引力
    sticky_data = data[data["用户ID"].isin(sticky_users.index)]
    print("课程吸引力排序依据：连续学习天数大于7天的高黏性用户学习记录")
else:
    #说明：本数据集中每个用户的不同学习日期最多只有 3 天连续，没有任何用户满足“连续学习天数>7天”，
    #因此黏性占比为 0.00%。为保证第(5)问仍能给出课程吸引力结论，这里退化为
    #“连续学习天数最多的那批用户”作为相对高黏性群体，并在输出中如实标注该退化处理。
    max_continue = user_continue.max()
    sticky_data = data[data["用户ID"].isin(user_continue[user_continue == max_continue].index)]
    print(f"说明：数据中单个用户最长连续学习天数仅为 {max_continue} 天，无用户满足“大于7天”，故黏性占比为 0.00%；")
    print(f"下面退化为使用“连续学习天数达到最大值 {max_continue} 天”的相对高黏性用户来排序课程吸引力")

#找出最具吸引力的三门课程：在筛选出的用户群体中，统计各课程名称的出现次数并取前三
top_courses = sticky_data["课程名称"].value_counts().head(3)
print(f"最具吸引力的三门课程：\n{top_courses}")
print("\n")
