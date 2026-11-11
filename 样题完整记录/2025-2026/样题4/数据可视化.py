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

#把交易日期转成时间类型，堆叠面积图要按月份取数
data['交易日期'] = pd.to_datetime(data['交易日期'])
data['月份'] = data['交易日期'].dt.month

#第 (1) 问：玫瑰图展示各小区年度交易总量占比
#统计各小区成交套数，扇区半径表示交易量大小，颜色深浅由数值自动分级
a = data['小区名称'].value_counts()
rose_data = [[str(k), int(v)] for k, v in a.items()]
pie = (
    Pie()
    .add(
        '交易量',
        rose_data,
        radius=['15%', '75%'],
        #rosetype='radius' 即玫瑰图：半径长度随交易量变化
        rosetype='radius',
        label_opts=opts.LabelOpts(formatter='{b}: {c}套（{d}%）')
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title='各小区年度交易总量占比玫瑰图'),
        legend_opts=opts.LegendOpts(pos_top='5%'),
        #鼠标悬停显示小区名、套数和占比
        tooltip_opts=opts.TooltipOpts(formatter='{b}<br/>成交套数：{c}<br/>占比：{d}%')
    )
)
pie.render('1.html')

#第 (2) 问：气泡图分析小区特征
#横轴=平均成交总价，纵轴=月均交易量，气泡大小=平均建筑面积，颜色=小区等级
b = data.groupby('小区名称').agg(
    平均成交总价=('成交总价（万元）', 'mean'),
    平均建筑面积=('建筑面积（㎡）', 'mean'),
    交易套数=('成交总价（万元）', 'size')
).round(2)
#月均交易量 = 该小区总套数 / 有交易的月份数，避免不同小区覆盖月份不同造成的偏差
months_cnt = data.groupby('小区名称')['月份'].nunique()
b['月均交易量'] = (b['交易套数'] / months_cnt).round(2)
#小区等级按平均成交总价的三分位切成高/中/低三档，用于气泡配色
q1 = b['平均成交总价'].quantile(1 / 3)
q2 = b['平均成交总价'].quantile(2 / 3)
def grade(p):
    if p > q2:
        return '高档小区'
    elif p > q1:
        return '中档小区'
    else:
        return '普通小区'
b['小区等级'] = b['平均成交总价'].apply(grade)

#气泡大小按平均建筑面积线性映射到 15-50px，面积差异才看得出来
s_min = b['平均建筑面积'].min()
s_max = b['平均建筑面积'].max()
def bubble_size(v):
    if s_max == s_min:
        return 25
    return float(15 + (v - s_min) / (s_max - s_min) * 35)

#x 轴用各小区的平均成交总价，一个小区对应一个气泡
scatter = Scatter()
scatter.add_xaxis(b['平均成交总价'].tolist())
#按小区等级分系列，图例即可筛选不同等级
for g, grp in b.groupby('小区等级'):
    #每个点用 [x, y] 表示坐标（均价, 月均交易量），并在名称里带上小区名便于悬停查看
    pts = [[float(r['平均成交总价']), float(r['月均交易量'])] for _, r in grp.iterrows()]
    sizes = [bubble_size(float(r['平均建筑面积'])) for _, r in grp.iterrows()]
    scatter.add_yaxis(
        str(g),
        pts,
        symbol_size=sizes,
        label_opts=opts.LabelOpts(is_show=False)
    )
scatter.set_global_opts(
    title_opts=opts.TitleOpts(title='各小区特征气泡图（大小=平均建筑面积，颜色=小区等级）'),
    xaxis_opts=opts.AxisOpts(name='平均成交总价(万元)', type_='value'),
    yaxis_opts=opts.AxisOpts(name='月均交易量(套)', type_='value'),
    legend_opts=opts.LegendOpts(pos_top='5%'),
    #开启缩放，便于查看密集区域的气泡
    datazoom_opts=[opts.DataZoomOpts(type_='inside'), opts.DataZoomOpts(type_='slider')],
    #气泡数据是 [均价, 月均交易量] 两维数组，用 value[0]/value[1] 取值；formatter 写 JS 函数必须用 JsCode 包起来
    tooltip_opts=opts.TooltipOpts(
        formatter=JsCode('function(p){return "均价：" + p.value[0] + "万元<br/>月均交易量：" + p.value[1] + "套";}')
    )
)
scatter.render('2.html')

#第 (3) 问：堆叠面积图展示一年内各主要户型交易量的变化趋势
#先算“月份×户型”的交易套数，行是月份、列是户型；unstack 把户型展开成列
c = data.groupby(['月份', '房源户型']).size().unstack(fill_value=0)
#只保留套数最多的前 4 个户型作为“主要户型”，避免图例过多导致堆叠面积图看不清
top_house = data['房源户型'].value_counts().head(4).index.tolist()
c = c[top_house]
#补齐没有交易的月份（值为 0），保证 x 轴 1-12 月连续
c = c.reindex(range(1, 13), fill_value=0)
months = [f'{i}月' for i in c.index.tolist()]
line = Line()
line.add_xaxis(months)
#每个户型一个系列，stack 参数相同即堆叠成面积图
for h in top_house:
    line.add_yaxis(
        str(h),
        c[h].astype(int).tolist(),
        stack='总量',
        is_smooth=True,
        #堆叠面积图靠 areaStyle 填充出面积效果
        areastyle_opts=opts.AreaStyleOpts(opacity=0.7),
        label_opts=opts.LabelOpts(is_show=False)
    )
line.set_global_opts(
    title_opts=opts.TitleOpts(title='一年内各主要户型交易量变化趋势（堆叠面积图）'),
    xaxis_opts=opts.AxisOpts(name='月份', type_='category', boundary_gap=False),
    yaxis_opts=opts.AxisOpts(name='交易量(套)'),
    tooltip_opts=opts.TooltipOpts(trigger='axis'),
    legend_opts=opts.LegendOpts(pos_top='5%'),
    #开启区域缩放，支持对某段时间高亮查看
    datazoom_opts=[opts.DataZoomOpts(type_='slider'), opts.DataZoomOpts(type_='inside')]
)
line.render('3.html')

#第 (4) 问：雷达图对比不同建筑年代房源的交易特征
#维度：成交总价、建筑面积、楼层、朝向评分、配套设施，先把每个维度换算成 0-100 的可比分数
d = data.copy()
#楼层从“25层”这类文本里取出数字
d['楼层数'] = d['楼层'].astype(str).str.extract(r'(\d+)').astype(float)
#朝向评分：南/南北最好给 100，东/东南/西南次之给 80，西/北给 60，未知给 40
def face_score(x):
    x = str(x)
    if x in ('南', '南北'):
        return 100
    elif x in ('东南', '西南', '东'):
        return 80
    elif x in ('西', '北'):
        return 60
    else:
        return 40
d['朝向评分'] = d['朝向'].apply(face_score)
#配套设施评分：统计“配套设施”里逗号分隔的项目个数，再按满分 5 项折算成百分制
d['配套评分'] = (d['配套设施'].astype(str).str.count(',') + 1).clip(upper=5) / 5 * 100
#按建筑年代分组求各维度均值，作为雷达图的一个“房源群体”
g = d.groupby('建筑年代').agg(
    成交总价=('成交总价（万元）', 'mean'),
    建筑面积=('建筑面积（㎡）', 'mean'),
    楼层=('楼层数', 'mean'),
    朝向评分=('朝向评分', 'mean'),
    配套设施=('配套评分', 'mean')
).round(2)
#各个量纲差别很大，统一除以该列最大值再乘 100，转成 0-100 的相对得分才能画在同一张雷达图上
k = (g / g.max() * 100).round(1)

#取年代最新的 4 个群体做对比，年代太少雷达图会看不清
k = k.tail(4)
indicators = [
    opts.RadarIndicatorItem(name='成交总价', max_=100),
    opts.RadarIndicatorItem(name='建筑面积', max_=100),
    opts.RadarIndicatorItem(name='楼层', max_=100),
    opts.RadarIndicatorItem(name='朝向评分', max_=100),
    opts.RadarIndicatorItem(name='配套设施', max_=100)
]
radar = Radar()
radar.add_schema(schema=indicators, splitline_opt=opts.SplitLineOpts(is_show=True))
#每个建筑年代一个系列，即雷达图上的一个闭合多边形
for year, row in k.iterrows():
    radar.add(
        series_name=f'{int(year)}年',
        data=[row.tolist()],
        #显示数据标签，符合题目“添加数据标签”的要求
        label_opts=opts.LabelOpts(is_show=True, font_size=10)
    )
radar.set_global_opts(
    title_opts=opts.TitleOpts(title='不同建筑年代房源交易特征雷达图（各维度相对得分）'),
    legend_opts=opts.LegendOpts(pos_top='5%')
)
radar.render('4.html')
