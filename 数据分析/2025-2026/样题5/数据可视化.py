import pandas as pd
import glob
import os
from pyecharts.charts import Pie
from pyecharts.charts import Scatter
from pyecharts.charts import Line
from pyecharts.charts import Radar
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

#读取清洗后的最终数据（文件名带 N，按通配符取，避免写死数字）
f = max(glob.glob('cleaned_data_c5_*.csv'), key=os.path.getmtime)
data = pd.read_csv(f)
print(f"读取文件：{f}，共 {len(data)} 行")

#把日期转成时间类型，堆叠面积图要按星期和小时取数
data['日期'] = pd.to_datetime(data['日期'])
data['星期'] = data['日期'].dt.weekday
data['周末标记'] = data['星期'].apply(lambda x: '周末' if x >= 5 else '工作日')
#出行时段是浮点小时（如 8.5），统一取整点小时
data['小时'] = data['出行时段(小时)'].apply(lambda v: int(v) % 24)

#第 (1) 问：玫瑰图展示各出行方式订单量分布
#统计各出行方式的订单量，扇区半径表示订单量大小，颜色深浅由数值自动分级
a = data['出行方式'].value_counts()
rose_data = [[str(k), int(v)] for k, v in a.items()]
pie = (
    Pie()
    .add(
        '订单量',
        rose_data,
        radius=['15%', '75%'],
        #rosetype='radius' 即玫瑰图：半径长度随订单量变化
        rosetype='radius',
        label_opts=opts.LabelOpts(formatter='{b}: {c}单（{d}%）')
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title='各出行方式订单量分布玫瑰图'),
        legend_opts=opts.LegendOpts(pos_top='5%'),
        #鼠标悬停显示出行方式、订单量和占比
        tooltip_opts=opts.TooltipOpts(formatter='{b}<br/>订单量：{c}<br/>占比：{d}%')
    )
)
pie.render('1.html')

#第 (2) 问：气泡图分析订单特征
#横轴=平均订单金额，纵轴=日均订单量，气泡大小=平均服务评分，颜色=出行方式
b = data.groupby('出行方式').agg(
    平均订单金额=('订单金额(元)', 'mean'),
    平均服务评分=('服务评分', 'mean'),
    订单量=('订单ID', 'size')
).round(2)
#日均订单量 = 该出行方式订单量 / 有订单的天数，避免不同方式覆盖天数不同造成偏差
days_cnt = data.groupby('出行方式')['日期'].nunique()
b['日均订单量'] = (b['订单量'] / days_cnt).round(2)

#气泡大小按平均服务评分映射到 15-50px；评分本身差距小，先按 min-max 拉开再放大
s_min = b['平均服务评分'].min()
s_max = b['平均服务评分'].max()
def bubble_size(v):
    if s_max == s_min:
        return 30
    return float(15 + (v - s_min) / (s_max - s_min) * 35)

#x 轴用各出行方式的平均订单金额，一种出行方式对应一个气泡
scatter = Scatter()
scatter.add_xaxis(b['平均订单金额'].tolist())
#每种出行方式单独一个系列，颜色自然区分，图例可筛选
for g, row in b.iterrows():
    #每个点用 [x, y] 表示坐标（均价, 日均订单量）
    scatter.add_yaxis(
        str(g),
        [[float(row['平均订单金额']), float(row['日均订单量'])]],
        symbol_size=bubble_size(float(row['平均服务评分'])),
        label_opts=opts.LabelOpts(is_show=True, formatter=str(g))
    )
scatter.set_global_opts(
    title_opts=opts.TitleOpts(title='各出行方式特征气泡图（大小=平均服务评分，颜色=出行方式）'),
    xaxis_opts=opts.AxisOpts(name='平均订单金额(元)', type_='value'),
    yaxis_opts=opts.AxisOpts(name='日均订单量(单)', type_='value'),
    legend_opts=opts.LegendOpts(pos_top='5%'),
    #开启缩放，便于查看密集区域
    datazoom_opts=[opts.DataZoomOpts(type_='inside'), opts.DataZoomOpts(type_='slider')],
    #气泡数据是 [均价, 日均订单量] 两维数组，用 value[0]/value[1] 取值；formatter 写 JS 函数必须用 JsCode 包起来
    tooltip_opts=opts.TooltipOpts(
        formatter=JsCode('function(p){return "平均订单金额：" + p.value[0] + "元<br/>日均订单量：" + p.value[1] + "单";}')
    )
)
scatter.render('2.html')

#第 (3) 问：堆叠面积图展示一周内各时段订单量变化趋势
#按题目要求以“工作日/周末”作为不同颜色，堆叠出各小时段的订单量
c = data.groupby(['小时', '周末标记']).size().unstack(fill_value=0)
#补齐 0-23 时，保证 x 轴 24 个小时连续
c = c.reindex(range(24), fill_value=0)
hours = [f'{h}时' for h in c.index.tolist()]
line = Line()
line.add_xaxis(hours)
#工作日、周末各一个系列，stack 相同即堆叠成面积图
for col in c.columns:
    line.add_yaxis(
        str(col),
        c[col].astype(int).tolist(),
        stack='订单量',
        is_smooth=True,
        #堆叠面积图靠 areaStyle 填充出面积效果
        areastyle_opts=opts.AreaStyleOpts(opacity=0.7),
        label_opts=opts.LabelOpts(is_show=False)
    )
line.set_global_opts(
    title_opts=opts.TitleOpts(title='一周内各时段订单量变化趋势（堆叠面积图）'),
    xaxis_opts=opts.AxisOpts(name='时段(小时)', type_='category', boundary_gap=False),
    yaxis_opts=opts.AxisOpts(name='订单量(单)'),
    tooltip_opts=opts.TooltipOpts(trigger='axis'),
    legend_opts=opts.LegendOpts(pos_top='5%'),
    #开启区域缩放，支持对某段时间高亮查看
    datazoom_opts=[opts.DataZoomOpts(type_='slider'), opts.DataZoomOpts(type_='inside')]
)
line.render('3.html')

#第 (4) 问：雷达图对比不同年龄段乘客的出行特征
#维度：订单金额、出行距离偏好、服务评分、出行频率、夜间订单比例，先按年龄段分组求各维度均值
d = data.copy()
#夜间订单标记：18 点至次日 6 点算夜间
d['是否夜间'] = d['小时'].apply(lambda h: 1 if (h >= 18 or h < 6) else 0)
g = d.groupby('乘客年龄段').agg(
    订单金额=('订单金额(元)', 'mean'),
    出行距离偏好=('出行时长(小时)', 'mean'),
    服务评分=('服务评分', 'mean'),
    出行频率=('订单ID', 'size'),
    夜间订单比例=('是否夜间', 'mean')
).round(4)
#夜间订单比例转成百分数便于阅读
g['夜间订单比例'] = (g['夜间订单比例'] * 100).round(2)
#各维度量纲差别大，统一除以该列最大值再乘 100，转成 0-100 的相对得分才能画在同一张雷达图上
k = (g / g.max() * 100).round(1)
indicators = [
    opts.RadarIndicatorItem(name='订单金额', max_=100),
    opts.RadarIndicatorItem(name='出行距离偏好', max_=100),
    opts.RadarIndicatorItem(name='服务评分', max_=100),
    opts.RadarIndicatorItem(name='出行频率', max_=100),
    opts.RadarIndicatorItem(name='夜间订单比例', max_=100)
]
radar = Radar()
radar.add_schema(schema=indicators, splitline_opt=opts.SplitLineOpts(is_show=True))
#每个年龄段一个系列，即雷达图上的一个闭合多边形
for age, row in k.iterrows():
    radar.add(
        series_name=str(age),
        data=[row.tolist()],
        #显示数据标签，符合题目“添加数据标签”的要求
        label_opts=opts.LabelOpts(is_show=True, font_size=10)
    )
radar.set_global_opts(
    title_opts=opts.TitleOpts(title='不同年龄段乘客出行特征雷达图（各维度相对得分）'),
    legend_opts=opts.LegendOpts(pos_top='5%')
)
radar.render('4.html')
