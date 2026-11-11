import pandas as pd
data = pd.read_csv("cleaned_data_c5_54.csv")

#把日期转成月份和星期，后面的客流、周末、月度分析都要用到
data["月份"] = pd.to_datetime(data["日期"]).dt.month
data["星期"] = pd.to_datetime(data["日期"]).dt.dayofweek


#一、基础指标分析
#（1）客流指标分析：总游客量、日均游客量、峰值月份、各景区客流排名、周末与工作日差异
print("========== 一、基础指标分析 ==========")
print("\n----- （1）客流指标分析 -----")
total = len(data)
days = data["日期"].nunique()
print(f"总游客量：{total} 人次")
print(f"统计天数：{days} 天，日均游客量：{total/days:.2f} 人次")
#月度客流：找出全年客流最高和最低的月份
m = data.groupby("月份").size()
print(f"客流最高月份：{m.idxmax()}月（{m.max()} 人次），最低月份：{m.idxmin()}月（{m.min()} 人次）")
#景区客流排行
print("各景区客流排名（人次）：")
for name, num in data.groupby("景区名称").size().sort_values(ascending=False).items():
    print(f"  {name}：{num}")
#周末与工作日的日均客流对比
weekend = data[data["星期"] >= 5]
workday = data[data["星期"] < 5]
weekend_avg = len(weekend) / weekend["日期"].nunique()
workday_avg = len(workday) / workday["日期"].nunique()
print(f"周末日均客流 {weekend_avg:.2f} 人次，工作日日均客流 {workday_avg:.2f} 人次，周末相对工作日增长 {(weekend_avg-workday_avg)/workday_avg*100:.2f}%")


#（3）游客体验评估：满意度评分为5分制，计算所有有效评分的加权平均值
#有效评分=0到5分之间的记录（清洗阶段已剔除超范围值，这里再确认一次），按各分值出现的次数加权
print("\n----- （3）游客体验评估 -----")
#只保留0-5分范围内的有效评分，超出范围的视为无效
valid = data[(data["满意度评分"] >= 0) & (data["满意度评分"] <= 5)]["满意度评分"]
#加权平均：每个分值 × 该分值出现次数，求和后除以有效评分总条数
score_count = valid.value_counts().sort_index()
#用 numpy 做「分值 × 次数」的加权求和：score_count.index 是分值，score_count.values 是各分值出现次数
weighted_avg = float((score_count.index.to_numpy() * score_count.to_numpy()).sum() / score_count.to_numpy().sum())
print(f"有效评分条数：{int(score_count.values.sum())} 条（总记录 {total} 条）")
print("各分值人数分布：")
for s, n in score_count.items():
    print(f"  {s}分：{n} 人")
print(f"满意度加权平均值：{weighted_avg:.2f} 分（5分制），得分率 {weighted_avg/5*100:.2f}%")
#分景区看体验差异，找出体验最好和最差的景区
by_scenic = data.groupby("景区名称")["满意度评分"].mean().sort_values(ascending=False)
print(f"满意度最高景区：{by_scenic.index[0]}（{by_scenic.iloc[0]:.2f} 分），最低景区：{by_scenic.index[-1]}（{by_scenic.iloc[-1]:.2f} 分）")


#二、运营建议
#基于上面的客流、消费、体验指标，输出结论和可执行的运营建议
print("\n========== 二、运营建议 ==========")
#先取几个结论要用的关键指标
avg_money = data["消费金额（元）"].mean()
avg_stay = data["停留时长（小时）"].mean()
top_age = data.groupby("游客年龄段")["消费金额（元）"].mean().idxmax()
top_src = data[data["游客来源地"] != "未知"]["游客来源地"].value_counts().idxmax()
top_way = data.groupby("出行方式")["消费金额（元）"].mean().idxmax()
peak_month = m.idxmax()
low_month = m.idxmin()

print("\n【分析结论】")
print(f"1. 全年共接待游客 {total} 人次，日均 {total/days:.2f} 人次，客流高峰在 {peak_month} 月、低谷在 {low_month} 月，淡旺季差异明显。")
print(f"2. 游客人均消费 {avg_money:.2f} 元、平均停留 {avg_stay:.2f} 小时，整体停留时间偏短，二次消费挖掘空间较大。")
print(f"3. 满意度加权平均仅 {weighted_avg:.2f} 分（5分制），得分率 {weighted_avg/5*100:.2f}%，游客体验整体偏低，是当前最突出的短板。")
print(f"4. {top_age} 年龄段人均消费最高，是最具消费潜力的群体；{top_src} 是第一大客源地；{top_way} 出行方式的游客消费能力最强。")
print(f"5. 周末日均客流比工作日高 {(weekend_avg-workday_avg)/workday_avg*100:.2f}%，客流明显向周末集中。")

print("\n【运营建议】")
print(f"1. 针对满意度短板做专项整改：当前加权平均仅 {weighted_avg:.2f} 分，建议对满意度最低的景区（{by_scenic.index[-1]}）开展服务流程排查，重点整治排队、导览、卫生等高频投诉环节，并建立月度满意度回访机制。")
print(f"2. 淡季引流 + 旺季限流：在 {low_month} 月等淡季推出门票折扣、套票和主题活动拉动客流；在 {peak_month} 月等旺季实行分时预约和限流，保障游览体验不因超载下滑。")
print(f"3. 围绕高消费群体做精准营销：针对 {top_age} 年龄段和 {top_src} 等主要客源地，设计深度游、夜游、文创和餐饮组合产品，把人均停留从 {avg_stay:.2f} 小时延长到半天以上，提升人均消费。")
print(f"4. 平抑周末客流峰谷：周末日均客流比工作日高 {(weekend_avg-workday_avg)/workday_avg*100:.2f}%，建议推出工作日专属优惠和错峰套餐，把部分周末客流引导到工作日，缓解景区承载压力。")
