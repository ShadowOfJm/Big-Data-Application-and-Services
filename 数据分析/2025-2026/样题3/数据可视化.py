import pandas as pd
import glob
import os
from pyecharts.charts import HeatMap
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pyecharts.charts import Scatter
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

#读取清洗后的最终数据（文件名带 N，按通配符取，避免写死数字）
f = max(glob.glob('cleaned_weather_c5_*.csv'), key=os.path.getmtime)
data = pd.read_csv(f)
print(f"读取文件：{f}，共 {len(data)} 行")

#把时间戳转成时间类型，热力图要按星期/小时取数，玫瑰图要按月份筛季度
data['观测时间戳'] = pd.to_datetime(data['观测时间戳'])
data['小时'] = data['观测时间戳'].dt.hour
data['星期'] = data['观测时间戳'].dt.weekday
data['月份'] = data['观测时间戳'].dt.month

#第 (1) 问：时间热力图展示一周内各时段（小时）的温度分布
#横轴为星期一至星期日，纵轴为 0-23 时，颜色冷暖表示温度高低
week = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
hours = [f'{h}时' for h in range(24)]
#按“星期 × 小时”分组求平均气温，得到热力图的每个格子值
t = data.groupby(['星期', '小时'])['气温(℃)'].mean().round(2)
#pyecharts 热力图的数据格式是 [x下标, y下标, 值]，所以按星期、小时两层循环拼出来
heat_data = []
for w in range(7):
    for h in range(24):
        v = t.get((w, h))
        #该时刻没有观测就留空（None），避免 0℃ 被误画成低温
        heat_data.append([w, h, None if pd.isna(v) else float(v)])
#色阶上下限直接取全期最低/最高气温，保证冷暖色贴合实际数据范围
vmin = data['气温(℃)'].min()
vmax = data['气温(℃)'].max()
heatmap = (
    HeatMap()
    .add_xaxis(week)
    .add_yaxis(
        '平均气温(℃)',
        hours,
        heat_data,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title='一周内各时段气温分布热力图'),
        xaxis_opts=opts.AxisOpts(name='星期', type_='category'),
        yaxis_opts=opts.AxisOpts(name='小时', type_='category'),
        visualmap_opts=opts.VisualMapOpts(
            min_=float(vmin), max_=float(vmax),
            is_calculable=True, orient='horizontal', pos_left='center', pos_bottom='0%'
        )
    )
)
heatmap.render('1.html')

#第 (2) 问：多系列折线图展示一年中（按月份）的温度变化趋势
#三条折线：平均气温、历史同期最高气温、历史同期最低气温
m = data.groupby('月份')['气温(℃)'].agg(['mean', 'max', 'min']).round(2)
#x 轴用“1月-12月”的中文月份标签，保证点位顺序与月份一致
months = [f'{i}月' for i in m.index.tolist()]
line = (
    Line()
    .add_xaxis(months)
    .add_yaxis('平均气温', m['mean'].tolist(), is_smooth=True)
    .add_yaxis('历史同期最高气温', m['max'].tolist(), is_smooth=True)
    .add_yaxis('历史同期最低气温', m['min'].tolist(), is_smooth=True)
    .set_global_opts(
        title_opts=opts.TitleOpts(title='一年中各月份气温变化趋势'),
        xaxis_opts=opts.AxisOpts(name='月份', type_='category'),
        yaxis_opts=opts.AxisOpts(name='气温(℃)'),
        tooltip_opts=opts.TooltipOpts(trigger='axis'),
        legend_opts=opts.LegendOpts(pos_top='5%')
    )
)
line.render('2.html')

#第 (3) 问：风向玫瑰图，展示特定区域在特定时期内的风向频率分布
#取第一季度（1-3 月）做示例，对应题目“如一个季度”的要求
q = data[data['月份'].isin([1, 2, 3])]
#统计各风向出现次数，玫瑰图的半径长度表示该风向出现的频率
wd = q['风向'].value_counts()
rose_data = [[str(k), int(v)] for k, v in wd.items()]
pie = (
    Pie()
    .add(
        '风向频率',
        rose_data,
        radius=['15%', '75%'],
        #rosetype='radius' 即玫瑰图：扇区半径随数值变化
        rosetype='radius',
        label_opts=opts.LabelOpts(formatter='{b}: {d}%')
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title='第一季度风向频率分布玫瑰图'),
        legend_opts=opts.LegendOpts(pos_top='5%'),
        tooltip_opts=opts.TooltipOpts(formatter='{b}<br/>出现次数：{c}<br/>占比：{d}%')
    )
)
pie.render('3.html')

#第 (4) 问：散点图分析温度与相对湿度的关系
#横轴温度、纵轴相对湿度，点的大小表示观测时的风速，颜色表示天气现象
#气温列表同时作为 x 轴数据传入（x 轴设为 value 型，ECharts 按数据点自身的坐标定位）
temps = data['气温(℃)'].tolist()
#把风速线性映射成点的直径：最小 6px、最大 22px，避免风速差异过大导致点看不清
v_min = data['风速(m/s)'].min()
v_max = data['风速(m/s)'].max()
def dot_size(v):
    if v_max == v_min:
        return 12
    return float(6 + (v - v_min) / (v_max - v_min) * 16)

#按天气现象分组，每种天气现象一个系列，颜色随系列自动区分，图例即可筛选
scatter = Scatter()
scatter.add_xaxis(temps)
for w, grp in data.groupby('天气现象'):
    #每个点用 [温度, 相对湿度] 表示坐标，避免 x/y 各自成列导致点错位
    pts = [[float(r['气温(℃)']), float(r['相对湿度(%)'])] for _, r in grp.iterrows()]
    #同系列内每个点大小不同，用 symbol_size 列表逐点指定
    sizes = [dot_size(float(r['风速(m/s)'])) for _, r in grp.iterrows()]
    scatter.add_yaxis(
        str(w),
        pts,
        symbol_size=sizes,
        label_opts=opts.LabelOpts(is_show=False)
    )
scatter.set_global_opts(
    title_opts=opts.TitleOpts(title='温度与相对湿度关系散点图（点大小=风速，颜色=天气现象）'),
    xaxis_opts=opts.AxisOpts(name='温度(℃)', type_='value'),
    yaxis_opts=opts.AxisOpts(name='相对湿度(%)', type_='value', min_=0, max_=100),
    legend_opts=opts.LegendOpts(pos_top='5%'),
    #数据是 [温度, 湿度] 两维数组，用 value[0]/value[1] 取对应值显示；formatter 写 JS 函数必须用 JsCode 包起来
    tooltip_opts=opts.TooltipOpts(
        formatter=JsCode('function(p){return "温度：" + p.value[0] + "℃<br/>相对湿度：" + p.value[1] + "%";}')
    )
)
scatter.render('4.html')
