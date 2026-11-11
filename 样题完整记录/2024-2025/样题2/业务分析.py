import pandas as pd
#读取清洗后的数据（清洗脚本最终产物为 cleaned_data_c5_0.csv）
data = pd.read_csv("cleaned_data_c5_0.csv")
#统一把“最后学习时间”转成时间类型，便于后续按时间维度统计
data["最后学习时间"] = pd.to_datetime(data["最后学习时间"], errors='coerce')

print("=" * 60)
print("在线学习平台 业务分析报告")
print("=" * 60)

#==================== 第一部分：三项专题分析 ====================

#【1. 课程参与度分析】
#参与度从三个角度看：覆盖规模（多少人学）、投入深度（学多久、多频繁）、完成情况（进度与完课率）
print("\n【1. 课程参与度分析】")
#总体参与规模
user_num = data["用户ID"].nunique()          # 覆盖用户数
course_num = data["课程名称"].nunique()      # 覆盖课程数
record_num = len(data)                       # 学习记录总数
print(f"参与用户数：{user_num} 人，覆盖课程：{course_num} 门，学习记录：{record_num} 条")
#人均指标，衡量单个用户的平均投入深度
per_user_times = record_num / user_num
per_user_duration = data["学习时长(分钟)"].sum() / user_num
print(f"人均学习次数：{per_user_times:.2f} 次，人均累计学习时长：{per_user_duration:.2f} 分钟")
#各类别参与度：用该类别学习人次占全部人次的比例衡量冷热程度
cat_count = data["课程类别"].value_counts()
cat_share = cat_count / record_num
print(f"各类别学习人次占比：\n{cat_share.apply(lambda x: f'{x:.2%}')}")
#完成情况：平均完成进度与整体完课率
avg_progress = data["完成进度"].mean()
finish_rate = (data["完成进度"] == 100).mean()
print(f"平均完成进度：{avg_progress:.2f}%，整体完课率（进度达100%的记录占比）：{finish_rate:.2%}")

#【2. 学习者行为分析】
#从学习时段、设备偏好、单次学习强度、互动活跃度四个维度刻画学习者习惯
print("\n【2. 学习者行为分析】")
#时段分布：看学习行为集中在一天中的哪个时间段
period_share = data["学习时段"].value_counts(normalize=True)
print(f"学习时段分布：\n{period_share.apply(lambda x: f'{x:.2%}')}")
#每个时段的平均单次学习时长，判断哪个时段学习更投入
period_duration = data.groupby("学习时段")["学习时长(分钟)"].mean().sort_values(ascending=False)
print(f"各时段平均单次学习时长：\n{period_duration.round(2)}")
#设备偏好：使用比例与各设备的平均单次学习时长
device_share = data["设备类型"].value_counts(normalize=True)
device_duration = data.groupby("设备类型")["学习时长(分钟)"].mean()
print(f"设备使用比例：\n{device_share.apply(lambda x: f'{x:.2%}')}")
print(f"各设备平均单次学习时长：\n{device_duration.round(2)}")
#单次学习强度与互动活跃度
avg_duration = data["学习时长(分钟)"].mean()
avg_interact = data["互动次数"].mean()
print(f"平均单次学习时长：{avg_duration:.2f} 分钟，平均互动次数：{avg_interact:.2f} 次")
#短时学习占比，反映碎片化学习程度
short_share = (data["学习时长(分钟)"] < 30).mean()
print(f"单次学习不足30分钟的碎片化记录占比：{short_share:.2%}")

#【3. 课程效果评估】
#用测验成绩、完成进度、完课率三个指标综合评估每门课程的教学效果
print("\n【3. 课程效果评估】")
course_eval = data.groupby("课程名称").agg(
    学习人次=('用户ID', 'size'),
    平均测验成绩=('测验成绩', 'mean'),
    平均完成进度=('完成进度', 'mean'),
    平均互动次数=('互动次数', 'mean')
)
#完课率单独按课程计算：该课程中进度达100%的记录数 / 该课程的记录数
course_finish = data.groupby("课程名称")["完成进度"].apply(lambda x: (x == 100).mean())
course_eval["完课率"] = course_finish
#按平均测验成绩降序，便于直接看出效果最好与最差的课程
course_eval = course_eval.sort_values(by="平均测验成绩", ascending=False)
print(f"各课程效果评估（按平均测验成绩降序）：\n{course_eval.round(2)}")
#效果最好的课程与最需要改进的课程
best_course = course_eval.index[0]
worst_course = course_eval.index[-1]
print(f"测验成绩最高的课程：{best_course}，平均 {course_eval.loc[best_course, '平均测验成绩']:.2f} 分")
print(f"测验成绩最低的课程：{worst_course}，平均 {course_eval.loc[worst_course, '平均测验成绩']:.2f} 分")
#完课率最低的课程，是最需要做内容与难度优化的对象
low_finish_course = course_eval["完课率"].idxmin()
print(f"完课率最低的课程：{low_finish_course}，完课率仅 {course_eval.loc[low_finish_course, '完课率']:.2%}")

#==================== 第二部分：平台运营现状概述 ====================

print("\n" + "=" * 60)
print("一、平台运营现状概述")
print("=" * 60)

#【总体运营指标】汇总规模、投入、完成、互动四类核心指标
print("\n（一）总体运营指标")
print(f"1. 用户规模：平台共有 {user_num} 名学习者产生 {record_num} 条有效学习记录，人均 {per_user_times:.2f} 次学习。")
print(f"2. 课程供给：覆盖 {course_num} 门课程、{data['课程类别'].nunique()} 个类别，课程类别分布为：\n{cat_count}")
print(f"3. 学习投入：人均累计学习 {per_user_duration:.2f} 分钟，平均单次学习 {avg_duration:.2f} 分钟，平均互动 {avg_interact:.2f} 次。")
print(f"4. 完成情况：平均完成进度 {avg_progress:.2f}%，整体完课率 {finish_rate:.2%}。")
print(f"5. 时间分布：学习时段占比最高的是 {period_share.idxmax()}（{period_share.max():.2%}）。")
print(f"6. 设备结构：使用最多的是 {device_share.idxmax()}（{device_share.max():.2%}）。")

#【主要问题识别】基于前面算出的指标，指出数据中暴露出的短板
print("\n（二）主要问题识别")
#问题一：完课率偏低，说明大量学习者中途流失
print(f"1. 完课率偏低：整体完课率仅 {finish_rate:.2%}，平均完成进度 {avg_progress:.2f}%，"
      f"说明多数学习者停留在课程中前期，学习过程存在明显中断。")
#问题二：课程之间效果差异明显
score_gap = course_eval["平均测验成绩"].max() - course_eval["平均测验成绩"].min()
print(f"2. 课程效果不均衡：最高与最低课程的平均测验成绩相差 {score_gap:.2f} 分，"
      f"“{worst_course}”明显落后，课程内容与难度需要针对性调整。")
#问题三：碎片化学习为主，深度投入不足
print(f"3. 碎片化学习突出：{short_share:.2%} 的学习记录单次不足 30 分钟，"
      f"且平均互动仅 {avg_interact:.2f} 次，学习的连贯性与深度不足。")
#问题四：完课率最低的课程拖累整体
print(f"4. 短板课程拖累整体：完课率最低的“{low_finish_course}”仅 {course_eval.loc[low_finish_course, '完课率']:.2%}，"
      f"是拉低平台整体完课率的主要来源。")

#【成功经验总结】把数据中表现好的方面提炼成可复制的经验
print("\n（三）成功经验总结")
print(f"1. 优势课程可复制：“{best_course}”平均测验成绩达 {course_eval.loc[best_course, '平均测验成绩']:.2f} 分，"
      f"其内容组织与难度梯度可作为其他课程的改造模板。")
print(f"2. 学习时段集中，便于精准运营：{period_share.idxmax()}是学习高峰（{period_share.max():.2%}），"
      f"在该时段推送提醒与直播课的到达率最高。")
print(f"3. 设备结构清晰：{device_share.idxmax()}占比最高（{device_share.max():.2%}），"
      f"说明用户已形成较稳定的终端使用习惯，产品优化可聚焦该终端。")
print(f"4. 用户覆盖较广：{user_num} 名用户在 {course_num} 门课程上产生了持续记录，"
      f"已具备按用户分层做精细化运营的数据基础。")

#==================== 第三部分：改进建议 ====================

print("\n" + "=" * 60)
print("二、改进建议")
print("=" * 60)

#【课程内容优化】针对完课率低、课程效果差异大、短板课程三类问题给出内容层面的建议
print("\n（一）课程内容优化")
print(f"1. 针对完课率仅 {finish_rate:.2%} 的问题，建议把长课程拆分为 15-20 分钟的知识点小节，"
      f"降低单次学习门槛，减少中途放弃。")
print(f"2. 针对“{worst_course}”成绩偏低，建议重做该课程的重点章节，补充例题与阶段小测，"
      f"并在关键节点设置检查点帮助学习者及时纠偏。")
print(f"3. 借鉴“{best_course}”的成功经验，统一各课程的难度梯度与章节结构，"
      f"缩小课程间 {score_gap:.2f} 分的成绩差距。")
print(f"4. 对完课率最低的“{low_finish_course}”单独做内容诊断，"
      f"优先补充案例与实操环节，提升学习的即时获得感。")

#【学习体验提升】围绕碎片化学习、互动少、设备使用习惯给出体验层面的建议
print("\n（二）学习体验提升")
print(f"1. 针对 {short_share:.2%} 的碎片化学习记录，建议提供可断点续学的短视频与知识卡片，"
      f"让短时段学习也能形成完整闭环。")
print(f"2. 针对平均互动仅 {avg_interact:.2f} 次的问题，建议在课程中嵌入随堂提问、弹幕讨论与学习打卡，"
      f"用轻量互动提升参与感。")
print(f"3. 围绕 {device_share.idxmax()} 这一主力终端（{device_share.max():.2%}）优先做体验优化，"
      f"保证页面加载、视频播放与作业提交的流畅度。")
print(f"4. 在 {period_share.idxmax()} 这一学习高峰时段安排答疑与直播，"
      f"把用户已有的学习习惯转化为更高的到场率与完成率。")

#【用户留存策略】从连续学习、分层运营、流失预警三方面给出留存建议
print("\n（三）用户留存策略")
print(f"1. 建立连续学习激励机制：以 7 天连续学习为周期设置成长任务与勋章，"
      f"把偶发学习转化为稳定习惯，直接提升学习黏性。")
print(f"2. 按学习行为分层运营：对高频高互动用户提供进阶课程与认证，"
      f"对低频用户推送其已学课程的下一章节，降低重新进入的门槛。")
print(f"3. 建立流失预警：对完成进度长期停滞（如低于 {avg_progress:.2f}% 的平均水平且长时间无新增记录）的用户"
      f"定向召回，配合限时学习提醒。")
print(f"4. 用课程口碑带动留存：优先推广“{best_course}”等高评价课程作为入口课，"
      f"以优质首课体验提升新用户的次日与次周留存。")

print("\n" + "=" * 60)
print("报告结束")
print("=" * 60)
