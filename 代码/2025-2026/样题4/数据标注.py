import pandas as pd
import glob
import os

#读取清洗后的最终结果：文件名里的 N 会随数据变化，所以按通配符取最新的 c5 文件，不写死数字
f = max(glob.glob('cleaned_data_c5_*.csv'), key=os.path.getmtime)
data = pd.read_csv(f)
print(f"读取文件：{f}，共 {len(data)} 行")

#子任务一：房源价值分类标注
#先算出全部房源的平均成交总价，作为高/中价值判断的基准线
avg = data['成交总价（万元）'].mean()
#按题目三条规则打标：高价值=总价>1.5倍且面积>120；中价值=总价0.5~1.5倍且面积80~120；其余为低价值
def value_type(row):
    p = row['成交总价（万元）']
    s = row['建筑面积（㎡）']
    if p > avg * 1.5 and s > 120:
        return '高价值房源'
    elif avg * 0.5 <= p <= avg * 1.5 and 80 <= s <= 120:
        return '中价值房源'
    else:
        return '低价值房源'

#新增“房源价值类型”列，并生成题目示例要求的“编号”列（从 1 开始）
data['房源价值类型'] = data.apply(value_type, axis=1)
data['编号'] = range(1, len(data) + 1)

#只保留题目示例要求的 5 列，输出 tourist_value_mark.csv
result1 = data[['编号', '小区名称', '成交总价（万元）', '建筑面积（㎡）', '房源价值类型']].copy()
#列名按题目示例改成半角括号形式（原文示例为“成交总价(万元)”“建筑面积(㎡)”）
result1.columns = ['编号', '小区名称', '成交总价(万元)', '建筑面积(㎡)', '房源价值类型']
print(result1.head(10))
print(f"高价值 {int((data['房源价值类型'] == '高价值房源').sum())} 套，"
      f"中价值 {int((data['房源价值类型'] == '中价值房源').sum())} 套，"
      f"低价值 {int((data['房源价值类型'] == '低价值房源').sum())} 套")
result1.to_csv('tourist_value_mark.csv', index=False)

#子任务二：交易热季标注
#先按“交易日期”取月份，再按月统计交易总量和平均成交总价
d = data.copy()
d['月份'] = pd.to_datetime(d['交易日期']).dt.month
g = d.groupby('月份').agg(
    交易总量=('小区名称', 'size'),
    平均成交总价=('成交总价（万元）', 'mean')
).round(2)

#年平均值是后面判断旺/平/淡季的基准：月均交易量、月均成交总价各算一个
avg_num = g['交易总量'].mean()
avg_price = g['平均成交总价'].mean()

#按题目三条规则给每个月打季节标签
def season_type(row):
    n = row['交易总量']
    p = row['平均成交总价']
    #旺季：量 > 年均 120% 且 均价 > 年均 110%
    if n > avg_num * 1.2 and p > avg_price * 1.1:
        return '旺季'
    #淡季：量 < 年均 80% 且 均价 < 年均 90%
    elif n < avg_num * 0.8 and p < avg_price * 0.9:
        return '淡季'
    #其余落在平季区间（量 80%-120% 或 均价 90%-110%）
    else:
        return '平季'

g['季节类型'] = g.apply(season_type, axis=1)

#“同比年平均”按题目示例取成交总价相对年均值的百分比（如 92%）
g['同比年平均'] = (g['平均成交总价'] / avg_price * 100).round(0).astype(int).astype(str) + '%'

#月份显示成“1月”这种格式，与题目示例一致
g['月份'] = [f'{i}月' for i in g.index]
#按题目示例的列顺序输出 season_mark.csv
result2 = g[['月份', '交易总量', '平均成交总价', '同比年平均', '季节类型']].reset_index(drop=True)
result2.columns = ['月份', '交易总量', '平均成交总价(万元)', '同比年平均', '季节类型']
print(result2)
result2.to_csv('season_mark.csv', index=False)
