import pandas as pd
#读取清洗后的数据。说明：清洗步骤(4)输出的文件名是 cleaned_data_c5_N.csv（跳过 c4，没有 c4），
#目录中实际文件为 cleaned_data_c5_19.csv，原脚本读取的 cleaned_data_c4_19.csv 不存在，此处修正
data = pd.read_csv("cleaned_data_c5_19.csv")
#统一把开始时间转为时间类型，并取出小时、日期、星期，供后续分析复用
data["开始时间"] = pd.to_datetime(data["开始时间"])
data['时间'] = data['开始时间'].dt.hour
data['日期'] = data['开始时间'].dt.date
data['星期'] = data['开始时间'].dt.dayofweek

print("=" * 60)
print("共享单车 业务分析报告")
print("=" * 60)

#【1. 单车周转率】
#周转率衡量单车被重复使用的效率：周转率 = 总骑行次数 / 投入运营的单车数。
#由于数据没有每天的车辆投放记录，这里用“观测期内每辆车的平均骑行次数”作为周转率指标，
#并额外给出日均周转率 = 周转率 / 覆盖天数，便于跨时间段比较。
print("\n【1. 单车周转率】")
total_rides = len(data)                       # 总骑行次数
bike_num = data["单车编号"].nunique()          # 出现的单车数量（近似投入运营车辆数）
day_num = data["日期"].nunique()               # 观测期覆盖天数
turnover = total_rides / bike_num              # 观测期内单车平均被骑行次数
daily_turnover = turnover / day_num            # 折算到每天的周转率
print(f"总骑行次数：{total_rides} 次，单车数量：{bike_num} 辆，覆盖天数：{day_num} 天")
print(f"单车周转率（观测期内每辆车平均骑行次数）：{turnover:.2f} 次/辆")
print(f"日均单车周转率：{daily_turnover:.4f} 次/辆/天")
#单车使用次数分布：观察是否存在少数车辆被高频使用、多数车辆闲置的情况
bike_count = data["单车编号"].value_counts()
print(f"单次骑行即闲置（只被骑1次）的单车数：{(bike_count == 1).sum()} 辆，"
      f"占比 {(bike_count == 1).mean():.2%}")
print(f"使用最频繁的单车：{bike_count.index[0]}，被骑行 {bike_count.iloc[0]} 次")
print(f"单车使用次数中位数：{bike_count.median():.0f} 次，均值：{bike_count.mean():.2f} 次")

#【2. 区域供需分析】
#把每个区域的上车次数视为“供给”（该区域有车可借），下车次数视为“需求”（该区域有人要还车），
#供需差 = 上车次数 - 下车次数。差值明显为正说明车辆堆积（供给过剩），为负说明车辆紧缺（需求旺盛）。
print("\n【2. 区域供需分析】")
start_count = data["起始位置"].value_counts()
end_count = data["结束位置"].value_counts()
area_supply = pd.concat([start_count, end_count], axis=1).fillna(0)
area_supply.columns = ["上车次数", "下车次数"]
#供需差与总流量
area_supply["供需差"] = area_supply["上车次数"] - area_supply["下车次数"]
area_supply["总流量"] = area_supply["上车次数"] + area_supply["下车次数"]
#按总流量降序，先看整体格局
area_supply = area_supply.sort_values(by="总流量", ascending=False).astype(int)
print(f"各区域供需情况（按总流量降序）：\n{area_supply}")
#车辆堆积最严重的区域（供需差最大，车多到没人骑走）
over_area = area_supply["供需差"].idxmax()
#车辆最紧缺的区域（供需差最小，还车需求远大于借车）
short_area = area_supply["供需差"].idxmin()
print(f"车辆堆积最严重的区域（供给过剩）：{over_area}，供需差 +{area_supply.loc[over_area, '供需差']} 次")
print(f"车辆最紧缺的区域（需求旺盛）：{short_area}，供需差 {area_supply.loc[short_area, '供需差']} 次")
print(f"总流量最高的区域：{area_supply.index[0]}，共 {area_supply['总流量'].iloc[0]} 次")
#跨区域骑行占比：反映调度压力，占比越高说明越需要跨区域调运车辆
cross_share = (data["起始位置"] != data["结束位置"]).mean()
print(f"跨区域骑行占比：{cross_share:.2%}（该部分行程会改变区域车辆分布，是调度压力的主要来源）")

#【3. 高峰期分析】
#从小时、星期两个维度找骑行高峰，并统计工作日与周末的差异，为车辆调度和人员排班提供依据
print("\n【3. 高峰期分析】")
#按小时统计总骑行次数与覆盖天数，算出每个小时的平均骑行量
hour_count = data.groupby("时间").size()
hour_days = data.groupby("时间")["日期"].nunique()
hour_avg = (hour_count / hour_days).sort_values(ascending=False)
print(f"平均骑行量最高的前三个小时：\n{hour_avg.head(3).round(2)}")
print(f"骑行量最高的时段是 {hour_avg.index[0]} 点，平均每小时 {hour_avg.iloc[0]:.2f} 次")
#按星期统计，找出最忙碌的一天（0=周一 … 6=周日）
week_count = data.groupby("星期").size()
week_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
print("各星期骑行次数：")
for i in range(7):
    if i in week_count.index:
        print(f"  {week_names[i]}：{week_count.loc[i]} 次")
print(f"骑行量最高的一天：{week_names[week_count.idxmax()]}，共 {week_count.max()} 次")
#工作日与周末对比：日均骑行量与平均骑行时长
workday_num = data[data["周末标记"] == 0]["日期"].nunique()
weekend_num = data[data["周末标记"] == 1]["日期"].nunique()
workday_rides = (data["周末标记"] == 0).sum()
weekend_rides = (data["周末标记"] == 1).sum()
print(f"工作日日均骑行量：{workday_rides / workday_num:.2f} 次/天"
      f"（{workday_num} 天，共 {workday_rides} 次）")
print(f"周末日均骑行量：{weekend_rides / weekend_num:.2f} 次/天"
      f"（{weekend_num} 天，共 {weekend_rides} 次）")
#工作日通勤特征：早高峰7-9点与晚高峰17-19点的骑行占比
commute_mask = ((data["时间"] >= 7) & (data["时间"] <= 9)) | ((data["时间"] >= 17) & (data["时间"] <= 19))
workday_commute_share = commute_mask[data["周末标记"] == 0].mean()
print(f"工作日早晚高峰（7-9点、17-19点）骑行占比：{workday_commute_share:.2%}，"
      f"体现明显的通勤潮汐特征")

#==================== 分析结论 ====================

print("\n" + "=" * 60)
print("分析结论")
print("=" * 60)

#结论一：周转率层面的判断
print("\n1. 单车周转率结论")
print(f"   观测期 {day_num} 天内，{bike_num} 辆单车共完成 {total_rides} 次骑行，"
      f"单车周转率为 {turnover:.2f} 次/辆，日均 {daily_turnover:.4f} 次/辆/天。")
print(f"   结合“{bike_count.index[0]}”被骑行 {bike_count.iloc[0]} 次、以及 "
      f"{(bike_count == 1).mean():.2%} 的单车仅被骑行 1 次来看，车辆使用极不均衡，"
      f"存在明显的调度优化空间。")

#结论二：区域供需层面的判断
print("\n2. 区域供需结论")
print(f"   “{over_area}”供给过剩（供需差 +{area_supply.loc[over_area, '供需差']} 次），"
      f"车辆容易堆积占用车位；")
print(f"   “{short_area}”供给不足（供需差 {area_supply.loc[short_area, '供需差']} 次），"
      f"高峰时段容易出现无车可借。")
print(f"   跨区域骑行占比 {cross_share:.2%}，说明多数行程会改变区域车辆分布，"
      f"需要按“{over_area} → {short_area}”的方向做主动调运。")

#结论三：高峰期层面的判断
print("\n3. 高峰期结论")
print(f"   骑行高峰集中在 {hour_avg.index[0]} 点（平均 {hour_avg.iloc[0]:.2f} 次/小时），"
      f"一周中最忙的是{week_names[week_count.idxmax()]}。")
print(f"   工作日日均 {workday_rides / workday_num:.2f} 次、周末日均 {weekend_rides / weekend_num:.2f} 次；"
      f"工作日早晚高峰骑行占比达 {workday_commute_share:.2%}，通勤属性突出。")
print(f"   建议在 {hour_avg.index[0]} 点前后提前完成车辆调度与人工巡检，"
      f"把可用车辆优先投向“{short_area}”等紧缺区域。")

print("\n" + "=" * 60)
print("报告结束")
print("=" * 60)
