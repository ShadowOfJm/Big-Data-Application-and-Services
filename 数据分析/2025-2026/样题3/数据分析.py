import pandas as pd
import glob
import os

#读取清洗后的最终数据（文件名带 N，按通配符取，避免写死数字）
f = max(glob.glob('cleaned_weather_c5_*.csv'), key=os.path.getmtime)
data = pd.read_csv(f)
print(f"读取文件：{f}，共 {len(data)} 行")

#把“观测时间戳”转成时间类型，后面按小时、按星期、按季节统计都要用
data['观测时间戳'] = pd.to_datetime(data['观测时间戳'])
data['小时'] = data['观测时间戳'].dt.hour
data['月份'] = data['观测时间戳'].dt.month

#第 (1) 问：按观测时间统计一天中每个小时的平均温度、最高温度、最低温度，并找出日温差最大的三个时段
#按小时分组，一次算出平均/最高/最低气温，再用最高减最低得到该小时的日温差
a = data.groupby('小时')['气温(℃)'].agg(['mean', 'max', 'min']).round(2)
a.columns = ['平均温度', '最高温度', '最低温度']
a['日温差'] = (a['最高温度'] - a['最低温度']).round(2)
print(f"（1）每个小时的平均温度、最高温度和最低温度：\n{a}")
#按日温差倒序取前三个小时，即温差最大的三个时段
print(f"（1）日温差最大的三个时段：\n{a.sort_values('日温差', ascending=False).head(3)[['日温差']]}")
print("\n")

#第 (2) 问：计算不同天气现象（晴、雨、雪、阴、多云等）下的平均温度、平均降水量和平均风速
b = data.groupby('天气现象').agg({
    '气温(℃)': 'mean',
    '降水量(mm)': 'mean',
    '风速(m/s)': 'mean'
}).round(2)
b.columns = ['平均温度', '平均降水量', '平均风速']
print(f"（2）不同天气现象下的平均温度、平均降水量和平均风速：\n{b}")
print("\n")

#第 (3) 问：分析不同季节的温度与降水量模式差异，计算各季节的平均温度、总降水量
#春 3-5 月、夏 6-8 月、秋 9-11 月、冬 12/1/2 月，用月份映射成季节名
def season(m):
    if m in (3, 4, 5):
        return '春季'
    elif m in (6, 7, 8):
        return '夏季'
    elif m in (9, 10, 11):
        return '秋季'
    else:
        return '冬季'

data['季节'] = data['月份'].apply(season)
#平均温度用 mean，总降水量用 sum，两个指标口径不同所以要分开算
c = data.groupby('季节').agg(平均温度=('气温(℃)', 'mean'), 总降水量=('降水量(mm)', 'sum')).round(2)
#按春夏秋冬固定顺序输出，避免分组后顺序乱掉
c = c.reindex(['春季', '夏季', '秋季', '冬季'])
print(f"（3）各季节的平均温度和总降水量：\n{c}")
print("\n")

#第 (4) 问：统计各观测站的日最高气温极值和日最低气温极值，识别高温区域和低温区域
#先按“观测站+日期”求每日极值，再按观测站取全期极值，否则同一天多条记录会把极值算重复
d = data.copy()
d['日期'] = d['观测时间戳'].dt.strftime('%Y-%m-%d')
e = d.groupby(['观测站ID', '日期'])['气温(℃)'].agg(['max', 'min']).reset_index()
g = e.groupby('观测站ID').agg(日最高气温极值=('max', 'max'), 日最低气温极值=('min', 'min')).round(2)
print(f"（4）各观测站的日最高气温极值和日最低气温极值：\n{g}")
#极值最大的站判为高温区域，极值最小的站判为低温区域
print(f"（4）高温区域（日最高气温极值最高）：{g['日最高气温极值'].idxmax()}，{g['日最高气温极值'].max()}℃")
print(f"（4）低温区域（日最低气温极值最低）：{g['日最低气温极值'].idxmin()}，{g['日最低气温极值'].min()}℃")
print("\n")

#第 (5) 问：分析降水量等级（无降水 0mm、小雨 0-10mm、中雨 10-25mm、大雨 >25mm）与平均相对湿度、平均风速的关系
#按题目给的四个区间把降水量离散成等级，再统计各等级的平均湿度和平均风速
def rain_level(v):
    if v <= 0:
        return '无降水'
    elif v < 10:
        return '小雨'
    elif v < 25:
        return '中雨'
    else:
        return '大雨'

data['降水量等级'] = data['降水量(mm)'].fillna(0).apply(rain_level)
h = data.groupby('降水量等级').agg(平均相对湿度=('相对湿度(%)', 'mean'), 平均风速=('风速(m/s)', 'mean')).round(2)
#按降水由弱到强排序，便于看出湿度、风速随降水等级的变化趋势
h = h.reindex(['无降水', '小雨', '中雨', '大雨'])
print(f"（5）降水量等级与平均相对湿度、平均风速的关系：\n{h}")
print("\n")
