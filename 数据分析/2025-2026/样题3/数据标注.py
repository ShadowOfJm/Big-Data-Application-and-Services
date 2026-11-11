import pandas as pd
import glob
import os

#读取清洗后的最终结果：文件名里的 N 会随数据变化，所以按通配符取最新的 c5 文件，不写死数字
f = max(glob.glob('cleaned_weather_c5_*.csv'), key=os.path.getmtime)
data = pd.read_csv(f)
print(f"读取文件：{f}，共 {len(data)} 行")

#子任务一：气温等级标注
#先把“观测时间戳”拆回“观测日期”，再按题目要求用“观测日期”+“观测站ID”分组求日最高气温
d = data.copy()
d['观测日期'] = pd.to_datetime(d['观测时间戳']).dt.strftime('%Y-%m-%d')
day_max = d.groupby(['观测日期', '观测站ID'])['气温(℃)'].max().reset_index()
day_max.rename(columns={'气温(℃)': '日最高气温'}, inplace=True)

#按题目阈值分四级：<10 寒冷；10~20 凉爽；20~28 舒适；>=28 炎热
def temp_level(t):
    if t < 10:
        return '寒冷'
    elif t < 20:
        return '凉爽'
    elif t < 28:
        return '舒适'
    else:
        return '炎热'

#把分级结果写进新增的“气温等级”列
day_max['气温等级'] = day_max['日最高气温'].apply(temp_level)

#只保留题目示例要求的四列，输出 temperature_level.csv
result1 = day_max[['观测日期', '观测站ID', '日最高气温', '气温等级']]
print(result1.head(10))
result1.to_csv('temperature_level.csv', index=False)

#子任务二：降水强度标注
#依据“天气现象”+“降水量(mm)”分级；非雨雪天气一律记为“非降水”，所以先把缺失的降水量补 0 便于比较
p = data.copy()
p['降水量(mm)'] = p['降水量(mm)'].fillna(0)

#雨/雪按降水量分三档，并把“雨”“雪”分别拼进等级名（小雨/中雨/大雨、小雪/中雪/大雪）
def rain_level(row):
    w = str(row['天气现象']).strip()
    v = row['降水量(mm)']
    if w not in ('雨', '雪'):
        return '非降水'
    if v < 10:
        return f'小{w}'
    elif v < 25:
        return f'中{w}'
    else:
        return f'大{w}'

#给每条观测记录打上“降水强度”标签
p['降水强度'] = p.apply(rain_level, axis=1)

#按题目示例的列顺序输出，原始列名是“观测时间戳”，这里改成示例里的“观测时间”
result2 = p[['记录ID', '观测时间戳', '天气现象', '降水量(mm)', '降水强度']].copy()
result2.rename(columns={'观测时间戳': '观测时间'}, inplace=True)
print(result2.head(10))
result2.to_csv('precipitation_intensity.csv', index=False)
