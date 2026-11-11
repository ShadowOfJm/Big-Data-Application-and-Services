import pandas as pd
#读取清洗后的数据。说明：题目清洗步骤(4)要求的输出文件名为 cleaned_data_c5_N.csv（跳过 c4，没有 c4），
#目录中实际存在的文件是 cleaned_data_c5_19.csv，原脚本读取的 cleaned_data_c4_19.csv 并不存在，此处修正为 c5
data = pd.read_csv("cleaned_data_c5_19.csv")
#统一把开始时间转为时间类型，后续按小时、按星期统计都依赖它
data["开始时间"] = pd.to_datetime(data["开始时间"])
#取出小时、日期、星期，供各问复用（星期：0=周一 … 6=周日）
data['时间'] = data['开始时间'].dt.hour
data['日期'] = data['开始时间'].dt.date
data['星期'] = data['开始时间'].dt.dayofweek

#【第(1)问】按开始时间统计每个小时的平均骑行量，进行倒序排序展示前三个高峰时段
#平均骑行量 = 该小时的总骑行次数 / 该小时跨越的不同日期数量，避免统计天数不同导致的小小时之间不可比
#注意：分母要按“日期”去重，若直接对开始时间戳去重会把同一天的每条记录都算成一天，导致结果恒接近 1
hourly_stats = data.groupby('时间').agg(
    total_rides=('时间','size'),  # 计算每个小时的总骑行次数
    unique_dates=('日期', 'nunique')  # 计算每个小时跨越的不同日期数量
)
#计算每个小时的平均骑行量
hourly_stats['平均骑行量'] = hourly_stats['total_rides'] / hourly_stats['unique_dates']
#按平均骑行量进行降序排序
sorted_hourly_avg = hourly_stats[['平均骑行量']].sort_values(by='平均骑行量', ascending=False)
#选取前三个高峰时段
top_3_peak_hours = sorted_hourly_avg.head(3)
#打印结果
print(f"按平均骑行量排序的前三个高峰时段:\n{top_3_peak_hours}")
print("\n")

#【第(2)问】计算不同天气状况下的平均骑行时长和平均骑行距离
#同时统计每种天气的骑行次数，便于判断样本量是否足以支撑结论
tem = data.groupby("天气状况").agg({
    "骑行时长(分钟)":"mean",
    "骑行距离(km)":"mean",
    "骑行ID":"size"
}).rename(columns={"骑行ID":"骑行次数"})
print(f"不同天气状况下的平均骑行时长和平均骑行距离\n{tem.round(2)}")
print("\n")

#【第(3)问】分析工作日和周末的骑行模式差异，计算两者的平均骑行量、平均骑行时长和平均骑行距离
#平均骑行时长和平均骑行距离：按周末标记（0=工作日，1=周末）分组求均值
avg_1 = data.groupby("周末标记").agg({
    "骑行时长(分钟)":"mean",
    "骑行距离(km)":"mean"
})
#平均骑行量：用总骑行次数除以该类型（工作日/周末）覆盖的不同日期数，
#得到“每个工作日/每个周末日的平均骑行量”，两者天数不同也能公平对比
ride_count = data.groupby("周末标记").size()
day_count = data.groupby("周末标记")["日期"].nunique()
avg_1["平均骑行量"] = ride_count / day_count
#把 0/1 标记换成中文，便于阅读
avg_1.index = avg_1.index.map({0:"工作日", 1:"周末"})
print(f"工作日与周末的骑行模式对比（平均骑行量、平均骑行时长、平均骑行距离）\n{avg_1.round(2)}")
print("\n")

#【第(4)问】统计每个区域的起始和结束骑行次数，识别最热门的上车区域和下车区域
#统计每个起始位置的出现次数，即各区域的上车（借车）次数
area_start = data.groupby("起始位置").size().to_frame(name='起始次数')
#统计每个结束位置的出现次数，即各区域的下车（还车）次数
area_final = data.groupby("结束位置").size().to_frame(name='结束次数')
#按次数降序排列，第一行就是最热门区域
area_start = area_start.sort_values(by='起始次数', ascending=False)
area_final = area_final.sort_values(by='结束次数', ascending=False)
print(f"各区域起始骑行次数（降序）：\n{area_start}")
print("\n")
print(f"各区域结束骑行次数（降序）：\n{area_final}")
print("\n")
#最热门的上车区域与下车区域
print(f"最热门上车区域：{area_start.index[0]}，起始次数 {area_start['起始次数'].iloc[0]}")
print(f"最热门下车区域：{area_final.index[0]}，结束次数 {area_final['结束次数'].iloc[0]}")
print("\n")

#【第(5)问】分析温度对骑行量的影响，计算不同温度区间（0-10℃、10-20℃、20-30℃、30℃以上）的平均骑行量
#先按题目给定的区间切分温度；数据中还存在 0℃ 以下的记录，单独划为“0℃以下”，避免这部分数据被丢弃
#right=False 表示区间左闭右开（0-10℃ 即 [0,10)），与题目写的区间含义一致
bins = [-100, 0, 10, 20, 30, 100]
labels = ['0℃以下', '0-10℃', '10-20℃', '20-30℃', '30℃以上']
data['温度区间'] = pd.cut(data['温度'], bins=bins, labels=labels, right=False)
#平均骑行量 = 该温度区间的总骑行次数 / 该区间覆盖的不同日期数
temp_count = data.groupby('温度区间', observed=False).size()
temp_days = data.groupby('温度区间', observed=False)['日期'].nunique()
#先用 replace 把 0 天换成 NaN，避免没有记录的空区间出现除零得到 inf
temp_avg = (temp_count / temp_days.replace(0, pd.NA)).to_frame(name='平均骑行量')
#把每个区间的骑行次数与天数一并输出，便于判断样本是否充足
temp_avg["骑行次数"] = temp_count
temp_avg["覆盖天数"] = temp_days
print(f"不同温度区间的平均骑行量\n{temp_avg.round(2)}")
print("\n")
