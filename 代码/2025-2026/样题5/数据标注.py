import pandas as pd
import glob
import os

#读取清洗后的最终结果：文件名里的 N 会随数据变化，所以按通配符取最新的 c5 文件，不写死数字
f = max(glob.glob('cleaned_data_c5_*.csv'), key=os.path.getmtime)
data = pd.read_csv(f)
print(f"读取文件：{f}，共 {len(data)} 行")

#子任务一：乘客价值分类标注
#先算全部订单的平均金额，作为高/中价值判断的基准线
avg = data['订单金额(元)'].mean()

#出行时段是带小数的浮点数（如 8.5），先取出整点小时再判断落在哪个时段
def hour_of(v):
    #24 点按 0 点处理，避免边界值落到任何区间外
    h = int(v) % 24
    return h

#按题目三条规则打标：高价值=金额>1.5倍且高峰(07-09/17-19)；中价值=金额0.5~1.5倍且平峰(10-16)；其余为低价值
def passenger_type(row):
    p = row['订单金额(元)']
    h = hour_of(row['出行时段(小时)'])
    #高峰时段：7 点到 9 点之前、17 点到 19 点之前
    is_peak = (7 <= h < 9) or (17 <= h < 19)
    #平峰时段：10 点到 16 点（含 16 点这一小时）
    is_flat = 10 <= h <= 16
    if p > avg * 1.5 and is_peak:
        return '高价值乘客'
    elif avg * 0.5 <= p <= avg * 1.5 and is_flat:
        return '中价值乘客'
    else:
        return '低价值乘客'

#新增“乘客价值类型”列，并生成题目示例要求的“编号”列（从 1 开始）
data['乘客价值类型'] = data.apply(passenger_type, axis=1)
data['编号'] = range(1, len(data) + 1)

#只保留题目示例要求的 5 列，输出 passenger_value_mark.csv
result1 = data[['编号', '出行方式', '订单金额(元)', '出行时段(小时)', '乘客价值类型']].copy()
print(result1.head(10))
print(f"高价值 {int((data['乘客价值类型'] == '高价值乘客').sum())} 单，"
      f"中价值 {int((data['乘客价值类型'] == '中价值乘客').sum())} 单，"
      f"低价值 {int((data['乘客价值类型'] == '低价值乘客').sum())} 单")
result1.to_csv('passenger_value_mark.csv', index=False)

#子任务二：出行需求旺季标注
#先按“日期”取月份，再按月统计订单总量和平均订单金额
d = data.copy()
d['月份'] = pd.to_datetime(d['日期']).dt.month
g = d.groupby('月份').agg(
    订单总量=('订单ID', 'size'),
    平均订单金额=('订单金额(元)', 'mean')
).round(2)

#年平均值是后面判断旺/平/淡季的基准：月均订单量、月均订单金额各算一个
avg_num = g['订单总量'].mean()
avg_price = g['平均订单金额'].mean()

#按题目三条规则给每个月打需求季节标签
def season_type(row):
    n = row['订单总量']
    p = row['平均订单金额']
    #旺季：量 > 年均 120% 且 均价 > 年均 110%
    if n > avg_num * 1.2 and p > avg_price * 1.1:
        return '旺季'
    #淡季：量 < 年均 80% 且 均价 < 年均 90%
    elif n < avg_num * 0.8 and p < avg_price * 0.9:
        return '淡季'
    #其余落在平季区间（量 80%-120% 或 均价 90%-110%）
    else:
        return '平季'

g['需求季节类型'] = g.apply(season_type, axis=1)

#“同比年平均”按题目示例取平均订单金额相对年均值的百分比（如 85%）
g['同比年平均'] = (g['平均订单金额'] / avg_price * 100).round(0).astype(int).astype(str) + '%'

#月份显示成“1月”这种格式，与题目示例一致
g['月份'] = [f'{i}月' for i in g.index]
#按题目示例的列顺序输出 demand_season_mark.csv
result2 = g[['月份', '订单总量', '平均订单金额', '同比年平均', '需求季节类型']].reset_index(drop=True)
result2.columns = ['月份', '订单总量', '平均订单金额(元)', '同比年平均', '需求季节类型']
print(result2)
result2.to_csv('demand_season_mark.csv', index=False)
