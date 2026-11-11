import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

n = 300  # 适当增加数据量以保证脏数据分布合理

communities = ['翡翠花园', '阳光城', '万科金域', '碧桂园', '恒大名都', '保利天悦', '中海锦城', '龙湖春江']
layouts = ['一室一厅', '两室一厅', '两室两厅', '三室一厅', '三室两厅', '四室两厅']
orientations = ['东', '南', '西', '北', '南北', '东南', '西南']
decorations = ['毛坯', '简装', '精装', '豪装']
facilities_list = ['地铁', '学校', '医院', '商场', '公园', '停车场', '电梯', '健身房']

data = []
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = (end_date - start_date).days

for i in range(n):
    community = random.choice(communities)

    # === 正常数据基准值 ===
    area = round(np.random.uniform(40, 180), 2)
    unit_price = int(np.random.uniform(8000, 65000))
    total_price = round(area * unit_price / 10000, 2)
    orientation = random.choice(orientations)
    decoration = random.choice(decorations)

    # === 注入脏数据 ===
    # 脏数据1: 装修情况为空或为零 (约5%)
    if random.random() < 0.05:
        decoration = random.choice(['', '0', None])

    # 脏数据2: 建筑面积异常 (约4%)
    if random.random() < 0.04:
        area = random.choice([round(np.random.uniform(5, 19), 2),
                              round(np.random.uniform(501, 800), 2)])
        total_price = round(area * unit_price / 10000, 2)  # 同步更新总价

    # 脏数据3: 朝向为空 (约5%)
    if random.random() < 0.05:
        orientation = ''

    # 脏数据4: 成交单价超出范围 (约4%)
    if random.random() < 0.04:
        unit_price = random.choice([int(np.random.uniform(1000, 4999)),
                                    int(np.random.uniform(200001, 350000))])
        total_price = round(area * unit_price / 10000, 2)

    # 脏数据5: 成交总价明显异常-超过该小区均值5倍 (约3%)
    # 注意: 这里直接制造一个极端高价，后续清洗时通过分组均值判断
    if random.random() < 0.03:
        total_price = round(total_price * np.random.uniform(6, 12), 2)

    facility_count = random.randint(2, 5)
    facilities = ','.join(random.sample(facilities_list, facility_count))
    trans_date = start_date + timedelta(days=random.randint(0, date_range))

    record = {
        '小区名称': community,
        '交易日期': trans_date.strftime('%Y-%m-%d'),
        '房源户型': random.choice(layouts),
        '建筑面积（㎡）': area,
        '成交总价（万元）': total_price,
        '成交单价（元/㎡）': unit_price,
        '楼层': f"{random.randint(1, 33)}层",
        '朝向': orientation,
        '装修情况': decoration,
        '建筑年代': random.randint(1990, 2024),
        '配套设施': facilities
    }
    data.append(record)

df = pd.DataFrame(data)
df.to_csv('tourist_data.csv', index=False, encoding='utf-8-sig')

# 打印脏数据统计摘要，方便验证
print(f"成功生成 tourist_data.csv，共 {len(df)} 条数据")
print(f"装修情况为空/零: {(df['装修情况'].isna() | df['装修情况'].isin(['', '0'])).sum()} 条")
print(f"建筑面积异常: {((df['建筑面积（㎡）'] > 500) | (df['建筑面积（㎡）'] < 20)).sum()} 条")
print(f"朝向为空: {(df['朝向'] == '').sum()} 条")
print(f"单价超范围: {((df['成交单价（元/㎡）'] < 5000) | (df['成交单价（元/㎡）'] > 200000)).sum()} 条")
print("注: 总价异常需在清洗阶段按小区分组均值判断")