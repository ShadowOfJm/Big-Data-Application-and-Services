import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- 配置参数 ---
num_records = 200  # 生成的记录数
filename = "house_sales.csv"

# --- 模拟数据池 ---
districts = ['朝阳', '海淀', '西城', '东城', '丰台', '石景山', '昌平', '大兴', '通州', '房山']
communities = [
    '某某小区A区', '某某小区B区', '阳光花园', '绿城百合', '万科城市花园', '金地自在城',
    '保利花园', '中海紫御华府', '富力城', '首开国风上观', '育慧里一区', '芍药居北里',
    '安贞西里', '三里屯南区', '双桥中路小区', '亦庄金茂府', '回龙观东大街', '天通苑北一区'
]
# 包含一些不规范的户型描述
layouts_raw = [
    '2室0厅', '3室2厅', '3室1厅', '2室2厅', '2室1厅',
    '2室2厅1卫', '5室3厅4卫', '1室1厅1卫', '3室3厅2卫', '2室0厅1卫',
    '2房间1卫', '3房间2厅', '1房间0厅', '4房2卫', '5房3厅4卫'
]
orientations = ['朝南', '朝北', '朝东', '朝西', '南北通透', '东西向']
floors = ['低楼层', '中楼层', '高楼层', '顶层', '底层']
decorations = ['精装修', '简装修', '毛坯', '中等装修', '豪华装修']
elevators = ['有', '无'] # 用字符串表示，方便后续处理空值

# --- 生成数据 ---
data = {
    '市区': np.random.choice(districts, num_records),
    '小区': np.random.choice(communities, num_records),
    '户型': np.random.choice(layouts_raw, num_records),
    '朝向': np.random.choice(orientations, num_records),
    '楼层': np.random.choice(floors, num_records),
    '装修情况': np.random.choice(decorations, num_records),
    '电梯': np.random.choice(elevators + [''], p=[0.45, 0.45, 0.1], size=num_records), # 10% 概率为空
    '面积(㎡)': np.round(np.random.uniform(40, 200, num_records), 2),
    '价格(万元)': np.round(np.random.uniform(150, 1500, num_records), 2),
    '年份': np.random.randint(2000, 2025, num_records)
}

df = pd.DataFrame(data)

# --- 插入一些异常或空值用于练习清洗 ---
# 1. 随机设置一些面积为空或为0
nan_area_indices = np.random.choice(df.index, size=int(0.02 * num_records), replace=False)
df.loc[nan_area_indices[:len(nan_area_indices)//2], '面积(㎡)'] = np.nan
df.loc[nan_area_indices[len(nan_area_indices)//2:], '面积(㎡)'] = 0

# 2. 随机设置一些价格为空
nan_price_indices = np.random.choice(df.index, size=int(0.03 * num_records), replace=False)
df.loc[nan_price_indices, '价格(万元)'] = np.nan

# 3. 随机设置一些面积小于20
small_area_indices = np.random.choice(df.index, size=int(0.02 * num_records), replace=False)
df.loc[small_area_indices, '面积(㎡)'] = np.round(np.random.uniform(5, 19, len(small_area_indices)), 2)

# --- 保存到 CSV ---
df.to_csv(filename, index=False, encoding='utf-8-sig') # utf-8-sig 有助于在 Excel 中正确显示中文

print(f"已生成包含 {num_records} 条记录的 '{filename}' 文件。")
print("数据预览 (前10行):")
print(df.head(10))

