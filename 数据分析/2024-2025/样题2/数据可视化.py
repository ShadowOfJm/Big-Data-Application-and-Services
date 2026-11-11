import matplotlib.pyplot as plt
import pandas as pd
#读取清洗后的数据（清洗脚本最终产物为 cleaned_data_c5_0.csv）
data = pd.read_csv("cleaned_data_c5_0.csv")
#设置中文字体，避免图中的中文显示为方块
plt.rcParams['font.family'] = 'SimHei'
#解决保存/显示时负号变成方块的问题
plt.rcParams['axes.unicode_minus'] = False

#【第(1)问】创建多系列折线图展示一周内不同时段的学习人数变化趋势
#说明：数据没有“星期”字段，这里用“最后学习时间”的日期推出星期几，并把“学习时段”作为多条折线系列。
#先取出学习日期与星期序号（0=周一 … 6=周日），空值丢弃
data['学习日期'] = pd.to_datetime(data["最后学习时间"], errors='coerce').dt.date
data['星期'] = pd.to_datetime(data["最后学习时间"], errors='coerce').dt.dayofweek
week_data = data.dropna(subset=['学习日期', '星期'])
#固定星期与时间段的顺序，保证横轴和多条折线的顺序稳定
week_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
period_names = ['凌晨', '上午', '下午', '晚上']
#按星期和时间段分组统计学习人数，unstack 后行是星期、列是时间段
week_data['星期'] = week_data['星期'].astype(int)  # 含空值时星期是浮点型，转成整数才能和 0-6 的刻度对齐
week_count = week_data.groupby(['星期', '学习时段']).size().unstack(fill_value=0)
#按固定顺序重排，缺失的列补 0，保证每个时间段都有一条完整折线
week_count = week_count.reindex(index=range(7), columns=period_names, fill_value=0)

plt.figure(figsize=(20,8),dpi=80)
#每个时间段画一条折线，形成多系列折线图
for p in period_names:
    plt.plot(week_names, week_count[p], marker='o', label=p)
plt.xlabel("星期")
plt.ylabel("学习人数")
plt.title("一周内不同时段的学习人数变化趋势")
plt.legend()
plt.show()

#【第(2)问】构建堆叠柱状图比较各课程类别在不同难度级别的分布情况
#说明：原始数据没有“难度级别”字段，沿用按课程名称排序后依次映射 A、B、C…… 的方式作为难度等级。
sorted_unique_courses = data['课程名称'].drop_duplicates().sort_values()
num_courses = len(sorted_unique_courses)
course_levels = [chr(65 + i) for i in range(num_courses)]
course_to_level_map = dict(zip(sorted_unique_courses, course_levels))
data.loc[:,'等级'] = data['课程名称'].map(course_to_level_map)

#交叉表：行是课程类别，列是难度等级，值是记录数
stack_data = pd.crosstab(data["课程类别"], data["等级"])
plt.figure(figsize=(20,8),dpi=80)
#bottom 记录当前堆叠高度，逐层向上叠加，形成堆叠柱状图
bottom = pd.Series([0]*len(stack_data), index=stack_data.index)
for level in stack_data.columns:
    plt.bar(stack_data.index, stack_data[level], bottom=bottom, label=f"等级{level}")
    bottom = bottom + stack_data[level]
plt.legend()
plt.xlabel("课程类别")
plt.ylabel("课程数量")
plt.title("各课程类别在不同难度级别的分布情况")
plt.show()
