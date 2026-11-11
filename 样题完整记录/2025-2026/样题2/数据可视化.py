import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams['font.family'] = 'SimHei'  # 替换为你选择的字体
data = pd.read_csv("cleaned_step5_55.csv")

#（1）绘制双轴组合图：主 Y 轴（柱状图）为各课程的平均学习时长，次 Y 轴（折线图，带标记点）为对应课程的近一年更新次数
#说明：原始数据没有“课程更新频率/近一年更新次数”和“学科领域”字段，
#这里用“课程类别”作为“学科领域”的分组依据（一个课程可能出现在多个类别下，取记录数最多的类别作为它的主学科领域），
#用“最近学习日期”的覆盖月份数作为“近一年更新次数”的替代指标（某课程在近一年内被持续更新的月份越多，说明更新越频繁）
#先算每门课程的平均学习时长（主 Y 轴柱子的高度）
course_dur = data.groupby("课程名称")["学习时长(分钟)"].mean()

#算每门课程在多少个不同月份有学习记录，作为“近一年更新次数”的替代
#先把日期转成 年-月 形式，再按课程统计去重后的月份数
data["年月"] = pd.to_datetime(data["最近学习日期"], errors="coerce").dt.to_period("M")
course_update = data.groupby("课程名称")["年月"].nunique()

#为每门课程确定它的主学科领域（即该课程记录数最多的那个课程类别），用于在 X 轴上分组标注
#按 课程+类别 统计人次后倒序排列，每门课程取第一条，就是它最主要的学科领域
cat_count = data.groupby(["课程名称", "课程类别"]).size().reset_index(name="人次")
cat_count = cat_count.sort_values("人次", ascending=False).drop_duplicates("课程名称")
course_cat = cat_count.set_index("课程名称")["课程类别"]

#按主学科领域把课程排序，让同一领域的课程在 X 轴上挨在一起，形成分组效果
order = course_cat.sort_values().index
course_dur = course_dur.reindex(order)
course_update = course_update.reindex(order)
course_cat = course_cat.reindex(order)

#X 轴刻度标签写成“课程名(学科领域)”，这样既能看出是哪些课程，也体现了分组
labels = [f"{n}({course_cat[n]})" for n in order]
#柱子的位置
x = list(range(len(labels)))

fig, ax1 = plt.subplots(figsize=(20,8),dpi=80)
#主 Y 轴：柱状图展示各课程的平均学习时长
ax1.bar(x, course_dur.values, width=0.5, label="平均学习时长(分钟)")
ax1.set_xlabel("课程（按学科领域分组）")
ax1.set_ylabel("平均学习时长(分钟)")
#柱子上标出具体数值，方便读图
for i, v in zip(x, course_dur.values):
    ax1.text(i, v + 0.5, f"{v:.1f}", ha="center", va="bottom", fontsize=9)

#次 Y 轴：折线图（带标记点）展示对应课程的近一年更新次数
ax2 = ax1.twinx()
ax2.plot(x, course_update.values, color="red", marker="o", label="近一年更新次数")
ax2.set_ylabel("近一年更新次数(有学习记录的月份数)")
#折线点上标出数值
for i, v in zip(x, course_update.values):
    ax2.text(i, v + 0.05, f"{int(v)}", ha="center", va="bottom", fontsize=9, color="red")

#X 轴刻度需要旋转，否则课程名过长会重叠
ax1.set_xticks(list(x))
ax1.set_xticklabels(labels, rotation=45, ha="right")
plt.title("课程更新频率与用户参与度（平均学习时长）关系")
#双轴图例需要把两个轴的图例合并显示
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper right")
#tight_layout 避免旋转后的刻度标签被裁掉
plt.tight_layout()
plt.show()


#（2）绘制热力图，呈现“用户学习时段”（按小时划分）与“常用设备类型”的共现关系
#X 轴为一天中的 24 个小时，Y 轴为主要的设备类型，单元格颜色深浅代表在该时段使用该设备的学习人次占比
#先构造 设备 x 小时 的交叉计数表：按 设备+时段 分组统计人次，再 unstack 把时段转成列
#fill_value=0 让没有记录的 设备/时段 组合补 0，避免出现空值
pivot = data.groupby(["登录设备", "学习时间段"]).size().unstack(fill_value=0)

#把列补齐成完整的 0-23 小时，保证 X 轴是整 24 小时，避免某些小时没数据导致轴不完整
pivot = pivot.reindex(columns=range(24), fill_value=0)

#把计数换算成占比：每个单元格除以全表总人次，得到“在该时段使用该设备的学习人次占比”
pivot_ratio = pivot / pivot.values.sum()

fig, ax = plt.subplots(figsize=(20,8),dpi=80)
#imshow 画热力图，cmap="YlOrRd" 用浅黄到深红表示占比由低到高
im = ax.imshow(pivot_ratio.values, aspect="auto", cmap="YlOrRd")
#设置 X 轴刻度为 24 个小时
ax.set_xticks(range(24))
ax.set_xticklabels([str(h) for h in range(24)])
#设置 Y 轴刻度为设备类型
ax.set_yticks(range(len(pivot_ratio.index)))
ax.set_yticklabels(pivot_ratio.index)
ax.set_xlabel("学习时段（小时）")
ax.set_ylabel("设备类型")
ax.set_title("用户学习时段与常用设备类型的共现关系（人次占比）")
#色标，说明颜色深浅对应的占比大小
plt.colorbar(im, ax=ax, label="学习人次占比")
#在每个单元格里标出占比数值，便于精确读数
for i in range(pivot_ratio.shape[0]):
    for j in range(pivot_ratio.shape[1]):
        ax.text(j, i, f"{pivot_ratio.values[i, j]:.3f}", ha="center", va="center", fontsize=7)
plt.tight_layout()
plt.show()
