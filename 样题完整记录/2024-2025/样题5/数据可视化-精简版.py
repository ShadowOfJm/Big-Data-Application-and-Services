import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Radar
from pyecharts.charts import Scatter
from pyecharts import options as opts
import random

from pyecharts.options import InitOpts

data = pd.read_csv("cleaned_data_c10_0.csv")


#使用柱状图展示各个地区的酒店数量，柱状图中的每个柱子代表一个地区， 高度代表该地区的酒店数量
num = data.groupby("地区").size().reset_index(name='酒店数量')
print(num)
bar = (
    Bar()
    .add_xaxis(num["地区"].tolist())
    .add_yaxis('酒店数量',num["酒店数量"].tolist())

)
bar.render("1.html")

#创建条形图比较不同地区酒店的平均卫生评分和服务评分，条形图中横轴表示评分，纵轴表示地区，每个地区有两个条形，分别表示卫生和服务评分
num1 = data.groupby('地区')[["卫生评分","服务评分"]].mean().round(2)
regions = num1.index.tolist()
avg_pf1 = num1["卫生评分"].tolist()
avg_pf2 = num1["服务评分"].tolist()
bar1 = (
    Bar()
    .add_xaxis(regions)
    .add_yaxis("卫生评分",avg_pf1)
    .add_yaxis("服务评分",avg_pf2)
    .reversal_axis()
)
bar1.render("2.html")

#使用雷达图展示任意一间酒店在卫生、服务、设施和位置评分的综合表现，雷达图中的每个轴代表一个评分指标（卫生、服务、设施、位置），每个酒店表现为雷达图上的一个闭合路径
sj = random.randint(0,len(data))
num2 = data.iloc[sj][['卫生评分', '服务评分', '设施评分', '位置评分']].tolist()
h_n = data.iloc[sj]['酒店名称']
num2 = [float(i) for  i in num2]
radar = (
    Radar()
    .add_schema(
        schema=[
            opts.RadarIndicatorItem(name='卫生',max_=10),
            opts.RadarIndicatorItem(name='服务',max_=10),
            opts.RadarIndicatorItem(name='设施',max_=10),
            opts.RadarIndicatorItem(name='位置',max_=10)
        ]
    )
    .add(
        series_name=h_n,
        data=[num2]
    )
)
radar.render("3.html")

#制作散点图探索房价与评价数量之间的关系，散点图中的横轴为房价，纵轴为评价数量，每个点代表一家酒店
s_fj = data['房价'].tolist()
# 把数据进行排序
s_fj.sort()
s_pjs = data['评价数'].tolist()
scatter = (
    Scatter(InitOpts(width='1200px',height='600px'))
    .add_xaxis(s_fj)
    .add_yaxis(series_name="酒店",y_axis=s_pjs)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(name='房价'),
        yaxis_opts=opts.AxisOpts(name='评价数量')
    )
)

scatter.render('4.html')