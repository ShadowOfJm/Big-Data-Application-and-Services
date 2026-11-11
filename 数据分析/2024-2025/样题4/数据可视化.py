import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import Pie, Scatter, Line, Radar
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

#读取清洗后的数据，并把“日期”转成月份，供趋势图和分组统计使用（题目要求 date 列转月份）
data = pd.read_csv("cleaned_data_c5_54.csv")
data["月份"] = pd.to_datetime(data["日期"]).dt.month

#原始数据里没有“景区等级”字段，这里按各景区平均消费金额的三分位反推等级，仅用于图的颜色和图例分组
#规则：平均消费排名前1/3记为5A，中间1/3记为4A，后1/3记为3A（数据里无真实等级，属代理指标）
level_data = data.groupby("景区名称")["消费金额（元）"].mean().sort_values(ascending=False)
n_level = max(1, len(level_data) // 3)
level_map = {}
for i, name in enumerate(level_data.index):
    if i < n_level:
        level_map[name] = "5A"
    elif i < n_level * 2:
        level_map[name] = "4A"
    else:
        level_map[name] = "3A"
#等级对应的颜色，用于玫瑰图的颜色深浅和气泡图的系列颜色
level_color = {"5A": "#c23531", "4A": "#d48265", "3A": "#91c7ae"}


#（1）玫瑰图：各景区游客量分布
#扇形半径=游客量（rosetype="radius"），颜色深浅=景区等级（5A最深、4A次之、3A最浅），带图例和标题，鼠标悬停显示明细
count_data = data.groupby("景区名称").size().sort_values(ascending=False)
rose = Pie(init_opts=opts.InitOpts(width="1000px", height="600px", theme=ThemeType.LIGHT))
rose.add(
    "游客量",
    [list(z) for z in zip(count_data.index.tolist(), [int(v) for v in count_data.values])],
    radius=["20%", "75%"],
    center=["50%", "55%"],
    rosetype="radius",
    itemstyle_opts=opts.ItemStyleOpts(border_radius=6, border_color="#fff", border_width=1),
)
#按景区等级依次上色，形成“颜色深浅=级别”的视觉效果（5A最深、3A最浅）
rose.set_colors([level_color[v] for v in count_data.index.map(level_map)])
rose.set_series_opts(
    #扇形上标注景区名和游客量，鼠标悬停时高亮该扇区并显示占比
    label_opts=opts.LabelOpts(formatter="{b}\n{c}人次"),
    tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}<br/>游客量：{c}人次<br/>占比：{d}%"),
)
rose.set_global_opts(
    title_opts=opts.TitleOpts(title="各景区游客量分布玫瑰图", subtitle="扇形半径=游客量，颜色深浅=景区等级：5A(深红)/4A(橙)/3A(绿)"),
    legend_opts=opts.LegendOpts(is_show=True, orient="vertical", pos_left="2%", pos_top="15%"),
)
rose.render("rose_chart.html")


#（2）气泡图：景区特征对比
#横轴=平均消费金额，纵轴=日均游客量，气泡大小=满意度评分，颜色=景区等级；支持图例筛选和缩放
sc = data.groupby("景区名称").agg(
    平均消费=("消费金额（元）", "mean"),
    游客量=("景区名称", "count"),
    天数=("日期", "nunique"),
    满意度=("满意度评分", "mean"),
).reset_index()
#日均游客量=该景区总游客量/有记录的天数，避免各景区天数不同带来偏差
sc["日均游客量"] = (sc["游客量"] / sc["天数"]).round(2)
sc["平均消费"] = sc["平均消费"].round(2)
sc["满意度"] = sc["满意度"].round(2)
sc["等级"] = sc["景区名称"].map(level_map)

bubble = Scatter(init_opts=opts.InitOpts(width="1000px", height="600px", theme=ThemeType.LIGHT))
#x轴设为数值轴，真正的横纵坐标由每条数据的 [x, y] 决定（pyecharts 气泡图官方写法）
bubble.add_xaxis([r["平均消费"] for _, r in sc.iterrows()])
#按景区等级分系列添加，这样点击图例就能按等级筛选显示/隐藏
for lv in ["5A", "4A", "3A"]:
    part = sc[sc["等级"] == lv]
    if len(part) == 0:
        continue
    bubble.add_yaxis(
        lv,
        #每个点 = [平均消费, 日均游客量, 满意度, 景区名称]，后两项给气泡大小和悬停提示用
        [[r["平均消费"], r["日均游客量"], r["满意度"], r["景区名称"]] for _, r in part.iterrows()],
        #气泡大小由满意度换算，满意度越高气泡越大
        symbol_size=JsCode("function (p) {return p.value[2] * 8;}"),
        label_opts=opts.LabelOpts(
            is_show=True,
            position="right",
            formatter=JsCode("function (p) {return p.value[3];}"),
        ),
        itemstyle_opts=opts.ItemStyleOpts(color=level_color[lv], opacity=0.75),
    )
bubble.set_global_opts(
    title_opts=opts.TitleOpts(title="景区特征气泡图", subtitle="横轴=平均消费，纵轴=日均游客量，气泡大小=满意度，颜色=景区等级"),
    xaxis_opts=opts.AxisOpts(type_="value", name="平均消费（元）", splitline_opts=opts.SplitLineOpts(is_show=True)),
    yaxis_opts=opts.AxisOpts(type_="value", name="日均游客量（人次）", splitline_opts=opts.SplitLineOpts(is_show=True)),
    #鼠标悬停时显示景区名、平均消费、日均游客量和满意度
    tooltip_opts=opts.TooltipOpts(
        trigger="item",
        formatter=JsCode(
            "function (p) {return p.value[3] + '<br/>平均消费：' + p.value[0] + ' 元<br/>日均游客量：'"
            " + p.value[1] + ' 人次<br/>满意度：' + p.value[2];}"
        ),
    ),
    #数据缩放：鼠标滚轮缩放 + 底部滑块缩放（题目要求的“缩放”能力）
    datazoom_opts=[opts.DataZoomOpts(type_="inside"), opts.DataZoomOpts(type_="slider")],
    legend_opts=opts.LegendOpts(is_show=True, pos_top="8%"),
)
bubble.render("bubble_chart.html")


#（3）堆叠面积图：游客来源地变化趋势
#取游客量前6的客源地（排除“未知”），按月统计游客量，堆叠成面积图看一年内的变化
top_src = data[data["游客来源地"] != "未知"]["游客来源地"].value_counts().head(6).index.tolist()
months = sorted(data["月份"].unique())
area = Line(init_opts=opts.InitOpts(width="1000px", height="600px", theme=ThemeType.LIGHT))
area.add_xaxis([f"{m}月" for m in months])
for src in top_src:
    #该客源地每个月的游客量，个别月份没数据就补0，保证12个数据点对齐
    s = data[data["游客来源地"] == src].groupby("月份").size().reindex(months, fill_value=0)
    area.add_yaxis(
        src,
        [int(v) for v in s.values],
        stack="总量",
        is_smooth=True,
        #显示每个月的月度数据点，鼠标悬停可查看具体数值
        is_symbol_show=True,
        symbol_size=6,
        label_opts=opts.LabelOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(opacity=0.6),
    )
area.set_global_opts(
    title_opts=opts.TitleOpts(title="主要客源地游客量月度变化（堆叠面积图）", subtitle="数据区间：2024年1-12月"),
    xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False, name="月份"),
    yaxis_opts=opts.AxisOpts(type_="value", name="游客量（人次）"),
    #阴影指示器：鼠标移到某个月份时，用阴影带高亮该月这一段区域（区域高亮）
    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
    legend_opts=opts.LegendOpts(is_show=True, pos_top="8%"),
    datazoom_opts=[opts.DataZoomOpts(type_="inside")],
)
area.render("area_chart.html")


#（4）雷达图：不同游客群体（年龄段）特征对比
#消费金额、停留时长、满意度评分 直接取自原始数据；
#重游率、景点打卡数 原始数据没有，用可解释的代理指标：重游率=满意度>=4分的游客占比，打卡数=人均停留时长/1.5小时折算
g = data.groupby("游客年龄段").agg(
    消费=("消费金额（元）", "mean"),
    停留=("停留时长（小时）", "mean"),
    满意度=("满意度评分", "mean"),
)
g["重游率"] = data[data["满意度评分"] >= 4].groupby("游客年龄段").size().reindex(g.index, fill_value=0) / data.groupby("游客年龄段").size() * 100
g["打卡数"] = g["停留"] / 1.5
#各维度量纲差别大，统一按最大值换算成0-100的相对值，才能画在同一张雷达图上
dims = ["消费金额", "停留时长", "满意度评分", "重游率", "景点打卡数"]
vals = {
    "消费金额": g["消费"],
    "停留时长": g["停留"],
    "满意度评分": g["满意度"],
    "重游率": g["重游率"],
    "景点打卡数": g["打卡数"],
}
norm = {k: (v / v.max() * 100).round(1) for k, v in vals.items()}

radar = Radar(init_opts=opts.InitOpts(width="1000px", height="600px", theme=ThemeType.LIGHT))
radar.add_schema(
    #每个维度的最大值写进指标名，说明100分对应多少实际值
    schema=[opts.RadarIndicatorItem(name=f"{d}（满值{vals[d].max():.1f}）", max_=100) for d in dims],
    shape="polygon",
    splitarea_opt=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=0.15)),
)
for age in g.index:
    radar.add(
        age,
        [[norm[d][age] for d in dims]],
        #半透明填充，多个年龄段叠在一起也能对比
        areastyle_opts=opts.AreaStyleOpts(opacity=0.25),
        label_opts=opts.LabelOpts(is_show=False),
    )
radar.set_series_opts(tooltip_opts=opts.TooltipOpts(trigger="item"))
radar.set_global_opts(
    title_opts=opts.TitleOpts(title="不同年龄段游客群体特征对比雷达图", subtitle="各维度已归一化为0-100"),
    legend_opts=opts.LegendOpts(is_show=True, pos_top="8%"),
)
radar.render("radar_chart.html")
