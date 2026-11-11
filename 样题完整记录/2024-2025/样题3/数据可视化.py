import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#读取清洗后的数据。说明：清洗步骤(4)输出的文件名是 cleaned_data_c5_N.csv（跳过 c4，没有 c4），
#目录中实际文件为 cleaned_data_c5_19.csv，原脚本读取的 cleaned_data_c4_19.csv 不存在，此处修正
data = pd.read_csv("cleaned_data_c5_19.csv")
#设置中文字体，避免图中的中文显示为方块
plt.rcParams['font.family'] = 'SimHei'
#解决负号显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False
#统一把开始时间转为时间类型，并取出小时、日期、星期（0=周一 … 6=周日）
data["开始时间"] = pd.to_datetime(data["开始时间"])
data['时间'] = data['开始时间'].dt.hour
data['日期'] = data['开始时间'].dt.date
data['星期'] = data['开始时间'].dt.dayofweek

#【第(1)问】创建时间热力图展示一周内各时段的骑行量分布
#横轴为星期（周一至周日），纵轴为小时（0-23时），颜色深浅表示骑行量的多少
#按星期和小时分组统计骑行次数，生成 星期×(0-23小时) 的矩阵
data['星期'] = data['星期'].astype(int)  # 转成整数，保证和 0-6 的星期刻度一一对应
heat_data = data.groupby(['星期', '时间']).size().unstack(fill_value=0)
#补齐 0-23 全部小时列，避免某些小时没有记录时矩阵错位
heat_data = heat_data.reindex(index=range(7), columns=range(24), fill_value=0)
week_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

plt.figure(figsize=(20,8),dpi=80)
#使用 imshow 绘制热力图，cmap='YlOrRd' 表示骑行量越大颜色越深
#把 imshow 返回的 mappable 对象保存下来，颜色条直接绑定这个对象，避免 matplotlib
#在当前轴上找不到可映射对象时报 "Unable to determine Axes to steal space for Colorbar"
heatmap = plt.imshow(heat_data.values, cmap='YlOrRd', aspect='auto')
#设置坐标轴刻度：横轴为星期，纵轴为小时
plt.xticks(range(7), week_names)
plt.yticks(range(24), range(24))
plt.xlabel("星期")
plt.ylabel("小时")
plt.title("一周内各时段骑行量热力图")
#添加颜色条，说明颜色深浅与骑行量的对应关系
plt.colorbar(heatmap, label='骑行量')
plt.show()

#【第(2)问】使用折线图展示一天24小时内的骑行量变化趋势
#图中包含工作日和周末两条折线，以便对比不同类型日期的使用模式差异
#按周末标记（0=工作日，1=周末）和小时分组统计骑行次数
line_data = data.groupby(['周末标记', '时间']).size().unstack(fill_value=0)
#补齐 0-23 全部小时列
line_data = line_data.reindex(columns=range(24), fill_value=0)
#取出工作日与周末两条序列
workday_line = line_data.loc[0] if 0 in line_data.index else pd.Series(0, index=range(24))
weekend_line = line_data.loc[1] if 1 in line_data.index else pd.Series(0, index=range(24))

plt.figure(figsize=(20,8),dpi=80)
plt.plot(range(24), workday_line.values, marker='o', label='工作日')
plt.plot(range(24), weekend_line.values, marker='s', label='周末')
plt.xticks(range(24), range(24))
plt.xlabel("小时")
plt.ylabel("骑行量")
plt.title("一天24小时骑行量变化趋势（工作日 vs 周末）")
plt.legend()
plt.show()

#【第(3)问】区域流向图：展示不同区域间的骑行流量，箭头粗细表示流量大小，颜色表示平均骑行时长
#简化说明：原始数据只有起止区域名称，没有经纬度坐标，无法在真实地图上绘制，
#因此这里把区域按环形均匀排布作为“相对位置”，用带箭头的注释（annotate）画流向：
#箭头由起始区域指向结束区域，箭头粗细（线宽）对应两区域间的骑行流量，箭头颜色对应这段行程的平均骑行时长。
#同时只保留总流量最高的若干区域，否则 18 个区域两两组合会让图形无法阅读。
flow = data[data["起始位置"] != data["结束位置"]].groupby(
    ["起始位置", "结束位置"]).agg(
    流量=('骑行ID', 'size'),
    平均时长=('骑行时长(分钟)', 'mean')
).reset_index()
#按区域总流量（上车次数+下车次数）排序，只取流量最大的前 10 个区域
area_total = pd.concat([
    data["起始位置"].value_counts(),
    data["结束位置"].value_counts()
], axis=1).fillna(0).sum(axis=1).sort_values(ascending=False)
top_areas = list(area_total.head(10).index)
#只保留两端都属于热门区域的流向
flow = flow[flow["起始位置"].isin(top_areas) & flow["结束位置"].isin(top_areas)]
#再取流量最大的前 30 条流向，避免箭头过密
flow = flow.sort_values(by="流量", ascending=False).head(30)
#把 10 个区域均匀分布在一个圆周上，作为绘图用的“相对坐标”
pos = {}
for i, name in enumerate(top_areas):
    angle = 2 * np.pi * i / len(top_areas)
    pos[name] = (np.cos(angle), np.sin(angle))
#准备箭头绘制所需的元素：每条流向的流量比例(width_ratio)和平均骑行时长(colors)
width_ratio, colors = [], []
for _, row in flow.iterrows():
    #箭头粗细与流量成正比，做归一化到 0~1，保证小流量也能看清
    width_ratio.append(row["流量"] / flow["流量"].max())
    colors.append(row["平均时长"])

plt.figure(figsize=(20,8),dpi=80)
#逐条绘制流向箭头：plt.quiver 的 width 只能设统一值，无法让每条箭头粗细不同，
#因此这里改用 annotate 的 arrowprops，把 linewidth 设为与该条流量成正比，从而实现“箭头粗细=流量大小”。
#颜色使用 coolwarm 色带映射平均骑行时长，并给每条箭头标注流量数字。
cmap = plt.cm.coolwarm
norm = plt.Normalize(min(colors), max(colors)) if colors else None
for i, (_, row) in enumerate(flow.iterrows()):
    x0, y0 = pos[row["起始位置"]]
    x1, y1 = pos[row["结束位置"]]
    plt.annotate('', xy=(x1, y1), xytext=(x0, y0),
                 arrowprops=dict(arrowstyle='-|>', color=cmap(norm(colors[i])),
                                 lw=1 + 6 * width_ratio[i], alpha=0.8), zorder=2)
#用散点标出各区域所在的节点位置
plt.scatter([pos[n][0] for n in top_areas], [pos[n][1] for n in top_areas],
            s=160, c='white', edgecolors='k', zorder=3)
#在每个区域的位置标注区域名称
for name, (px, py) in pos.items():
    plt.text(px * 1.12, py * 1.12, name, ha='center', va='center', fontsize=11, zorder=4)
#颜色条对应箭头颜色（平均骑行时长）
#ScalarMappable 只是颜色映射器，不属于任何 Axes，matplotlib 无法自动判断把颜色条放在哪，
#所以显式用当前 Axes 作为 ax 参数传入
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.colorbar(sm, ax=plt.gca(), label='平均骑行时长(分钟)')
#去掉坐标轴刻度，因为圆周位置只是相对示意，不代表真实经纬度
plt.xticks([])
plt.yticks([])
plt.title("区域间骑行流向图（箭头粗细=骑行流量，颜色=平均骑行时长；环形布局为简化示意）")
plt.show()

#【第(4)问】散点图：气温 vs 日骑行量，点大小表示平均骑行时长，颜色表示天气状况
#先按日期聚合：日骑行量=当天骑行次数，气温取当天平均温度，平均骑行时长取当天均值，
#天气状况取当天出现次数最多的天气
day_data = data.groupby('日期').agg(
    日骑行量=('骑行ID', 'size'),
    平均气温=('温度', 'mean'),
    平均骑行时长=('骑行时长(分钟)', 'mean'),
    天气状况=('天气状况', lambda x: x.value_counts().idxmax())
).reset_index()
#把天气状况映射成颜色编号，并记录图例标签
weather_list = list(day_data["天气状况"].unique())
weather_color = {w: i for i, w in enumerate(weather_list)}
day_data["天气颜色"] = day_data["天气状况"].map(weather_color)
#点大小与平均骑行时长成正比，做缩放并设置最小值，保证点可见
sizes = 40 + 260 * (day_data["平均骑行时长"] - day_data["平均骑行时长"].min()) / \
        (day_data["平均骑行时长"].max() - day_data["平均骑行时长"].min() + 1e-9)

plt.figure(figsize=(20,8),dpi=80)
sc = plt.scatter(day_data["平均气温"], day_data["日骑行量"], s=sizes,
                 c=day_data["天气颜色"], cmap='tab10', alpha=0.75, edgecolors='k')
plt.xlabel("平均气温(℃)")
plt.ylabel("日骑行量(次)")
plt.title("气温与日骑行量关系（点大小=平均骑行时长，颜色=天气状况）")
#按天气状况生成图例
for w in weather_list:
    plt.scatter([], [], c=[plt.cm.tab10(weather_color[w])], label=w, s=60, edgecolors='k')
plt.legend(title="天气状况", loc='upper right')
plt.show()
