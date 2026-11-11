import pandas as pd
#读取样题2清洗脚本的最终产物 cleaned_step5_55.csv，业务分析基于这份数据
data = pd.read_csv("cleaned_step5_55.csv")
#统一日期为日期类型，供统计活跃月份、学习天数使用
data["最近学习日期"] = pd.to_datetime(data["最近学习日期"], errors="coerce")

#========== 一、核心发现总结 ==========
#（1）用户活跃规律：找出最活跃的时段与最偏好的设备组合
#先按小时统计学习人次，人次最多的小时就是最活跃时段
hour_count = data["学习时间段"].astype(int).value_counts().sort_index()
best_hour = hour_count.idxmax()
print(f"最活跃学习小时:{best_hour}点（该小时学习人次{hour_count.max()}）")

#设备偏好：统计各设备的记录数，占比最高的即最偏好设备
device_count = data["登录设备"].value_counts()
print(f"最偏好设备:{device_count.idxmax()}（{device_count.max()}人次，占{device_count.max()/len(data):.1%}）")

#设备+时段的组合：把 设备 与 小时 组合起来统计，找出人次最多的组合，即最典型的用户学习场景
combo = data.groupby(["登录设备", "学习时间段"]).size().sort_values(ascending=False)
print(f"最典型的设备与时段组合:{combo.idxmax()}，共{combo.max()}人次")

#（2）课程内容表现：总结哪种内容形式、学科领域更受欢迎、更能促进完成与留存
#按内容形式比较平均学习时长、平均章节完成率、平均测试得分三个指标
form_stat = data.groupby("内容形式").agg(
    平均学习时长=("学习时长(分钟)", "mean"),
    平均完成率=("章节完成率", "mean"),
    平均得分=("测试得分", "mean"),
    学习人次=("学员ID", "size")
).sort_values("平均完成率", ascending=False)
print("\n")
print(f"不同内容形式的平均学习时长/完成率/得分\n{form_stat}")

#按课程类别比较完成率与得分，看哪个学科领域表现更好
cat_stat = data.groupby("课程类别").agg(
    平均完成率=("章节完成率", "mean"),
    平均得分=("测试得分", "mean"),
    学习人次=("学员ID", "size")
).sort_values("平均完成率", ascending=False)
print("\n")
print(f"不同课程类别的平均完成率/得分\n{cat_stat}")

#（3）潜在风险与机会：识别参与度偏低的课程类别与设备渠道
#平台整体完成率作为基准线，低于基准线的类别视为存在参与度下降风险
avg_all = data["章节完成率"].mean()
risk_cat = cat_stat[cat_stat["平均完成率"] < avg_all].index.tolist()
print("\n")
print(f"平台整体平均完成率{avg_all:.4f}")
print(f"完成率低于整体水平、存在参与度下降风险的课程类别{risk_cat}")

#设备渠道里平均学习时长最低的设备，说明用户在该渠道停留时间偏短，是需要优化的对象
device_dur = data.groupby("登录设备")["学习时长(分钟)"].mean().sort_values()
print(f"各设备平均学习时长{device_dur}")
print(f"平均学习时长最低、需重点优化的设备渠道{device_dur.idxmin()}")

#========== 二、数据驱动的优化建议 ==========
#下面的建议均对应上面算出的具体数字：最活跃时段/设备、表现最好的内容形式与类别、风险类别
print("\n")
print("在线教育平台运营优化建议：")

#建议一：内容与运营策略——把表现最好的内容形式做成可复制的模板
print(f"1.复制高完成率内容模板：{form_stat.index[0]}的平均章节完成率最高（{form_stat['平均完成率'].iloc[0]:.1%}），"
      f"应以此类形式为主力，把表现最好的{cat_stat.index[0]}类课程的课程设计（章节切分、互动节奏）沉淀为模板，"
      f"向完成率偏低的{risk_cat}等类别推广复用。")

#建议二：功能与体验优化——按最活跃时段和设备做个性化触达
print(f"2.按活跃时段与设备做个性化推送：用户在{best_hour}点最活跃、最常用{device_count.idxmax()}，"
      f"应把学习提醒与内容推送集中在{best_hour}点前后，并优先保证{device_count.idxmax()}端的页面加载与交互体验，"
      f"针对{device_dur.idxmin()}端平均学习时长偏低（{device_dur.min():.1f}分钟）的问题优化界面与内容加载速度。")

#建议三：资源分配建议——为课程更新与技术开发排优先级
print(f"3.资源分配优先级：课程更新优先投向{cat_stat.index[-1]}等完成率靠后的类别，"
      f"技术开发优先投入{device_count.idxmax()}端，"
      f"市场推广集中投放在{best_hour}点前后的活跃高峰时段，以最小成本提升整体参与度与留存。")
