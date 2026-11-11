import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Radar
from pyecharts.charts import Scatter
from pyecharts import options as opts
import random

from pyecharts.options import InitOpts

#读取样例5清洗完成后的数据（c10 为最终结果）
data = pd.read_csv("cleaned_data_c10_0.csv")


#（1）使用柱状图展示各个地区的酒店数量，柱状图中的每个柱子代表一个地区， 高度代表该地区的酒店数量
#groupby("地区").size() 统计每个地区的酒店条数，reset_index 把结果转成两列的表，方便取用
num = data.groupby("地区").size().reset_index(name='酒店数量')
print(num)
bar = (
    Bar()
    #x 轴放地区名，y 轴放对应的酒店数量
    .add_xaxis(num["地区"].tolist())
    .add_yaxis('酒店数量',num["酒店数量"].tolist())

)
bar.render("1.html")

#（2）创建条形图比较不同地区酒店的平均卫生评分和服务评分，条形图中横轴表示评分，纵轴表示地区，每个地区有两个条形，分别表示卫生和服务评分
#按地区分组，一次取出卫生评分和服务评分两列的均值，并保留两位小数
num1 = data.groupby('地区')[["卫生评分","服务评分"]].mean().round(2)
regions = num1.index.tolist()
avg_pf1 = num1["卫生评分"].tolist()
avg_pf2 = num1["服务评分"].tolist()
bar1 = (
    Bar()
    .add_xaxis(regions)
    #同一个 x 轴上添加两个 y 序列，就形成每个地区两根条形（卫生、服务）
    .add_yaxis("卫生评分",avg_pf1)
    .add_yaxis("服务评分",avg_pf2)
    #reversal_axis() 把柱子转成横向，使纵轴变成地区
    .reversal_axis()
)
bar1.render("2.html")

#（3）使用雷达图展示任意一间酒店在卫生、服务、设施和位置评分的综合表现，雷达图中的每个轴代表一个评分指标（卫生、服务、设施、位置），每个酒店表现为雷达图上的一个闭合路径
#随机抽一家酒店：索引范围是 0 ~ len(data)-1，所以要减 1，否则可能越界
sj = random.randint(0,len(data)-1)
#取出这家酒店的四项评分，并记录酒店名称用于图例
num2 = data.iloc[sj][['卫生评分', '服务评分', '设施评分', '位置评分']].tolist()
h_n = data.iloc[sj]['酒店名称']
#统一转成 float，避免读取时出现字符串导致画图失败
num2 = [float(i) for i in num2]
radar = (
    Radar()
    .add_schema(
        #四个维度对应四个评分指标，max_ 设为 5（评分满分）
        schema=[
            opts.RadarIndicatorItem(name='卫生',max_=5),
            opts.RadarIndicatorItem(name='服务',max_=5),
            opts.RadarIndicatorItem(name='设施',max_=5),
            opts.RadarIndicatorItem(name='位置',max_=5)
        ]
    )
    .add(
        series_name=h_n,
        #pyecharts 的 Radar 会自动把首尾相连成闭合路径，这里传入四个维度的值即可
        data=[num2]
    )
)
radar.render("3.html")

#（4）制作散点图探索房价与评价数量之间的关系，散点图中的横轴为房价，纵轴为评价数量，每个点代表一家酒店
# 把数据进行排序：房价与评价数必须一一对应，所以按整张表按房价排序，
# 再分别取出两列；原代码只对房价一列 sort()，会导致 x/y 错位
df_sort = data.sort_values('房价')
s_fj = df_sort['房价'].tolist()
s_pjs = df_sort['评价数'].tolist()
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
