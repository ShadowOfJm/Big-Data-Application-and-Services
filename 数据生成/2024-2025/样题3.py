import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- 配置参数 ---
num_records = 10000  # 生成的记录数
start_date = datetime(2025, 1, 1, 0, 0, 0) # 开始日期
end_date = datetime(2025, 3, 31, 23, 59, 59) # 结束日期
# --- 配置参数 ---

# 预设数据
locations = [
    "朝阳区望京", "朝阳区大屯", "海淀区中关村", "海淀区五道口",
    "西城区西单", "东城区王府井", "丰台区方庄", "石景山区鲁谷",
    "通州区梨园", "昌平区回龙观", "大兴区亦庄", "顺义区新国展",
    "房山区良乡", "门头沟区石门营", "平谷区平谷镇", "怀柔区怀柔镇",
    "密云区密云镇", "延庆区延庆镇"
]
weather_conditions = ["晴", "多云", "阴", "小雨", "中雨", "大雨", "雪", "雾"]

# 生成基础数据
data = []

for i in range(num_records):
    ride_id = 1000 + i
    bike_id = f"B{random.randint(10000, 99999)}"
    user_id = f"U{random.randint(100000, 999999)}"

    # 随机生成开始时间
    random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
    start_time = start_date + timedelta(seconds=random_seconds)

    # 随机生成骑行时长 (分钟)
    ride_duration = random.randint(1, 24 * 60) # 1分钟到24小时

    # 计算结束时间
    end_time = start_time + timedelta(minutes=ride_duration)

    # 随机选择起始和结束位置
    start_location = random.choice(locations)
    end_location = random.choice(locations)

    # 基于时长模拟骑行距离 (假设平均速度 15 km/h)
    # 距离 = 速度 * 时间(小时) = 15 * (ride_duration / 60)
    ride_distance = round(15 * (ride_duration / 60.0), 2)
    # 添加一些随机性到距离
    ride_distance = max(0.1, round(np.random.normal(ride_distance, ride_distance * 0.2), 2))

    # 随机选择天气
    weather = random.choice(weather_conditions)

    # 随机生成温度
    temperature = round(random.uniform(-5, 35), 1)

    # 判断是否为周末 (周一=0, 周日=6)
    is_weekend = 1 if start_time.weekday() >= 5 else 0

    data.append([
        ride_id, bike_id, user_id, start_time.strftime("%Y-%m-%d %H:%M:%S"),
        end_time.strftime("%Y-%m-%d %H:%M:%S"), start_location, end_location,
        ride_distance, ride_duration, weather, temperature, is_weekend
    ])

# 创建DataFrame
columns = [
    "骑行ID", "单车编号", "用户ID", "开始时间", "结束时间",
    "起始位置", "结束位置", "骑行距离(km)", "骑行时长(分钟)",
    "天气状况", "温度", "周末标记"
]
df = pd.DataFrame(data, columns=columns)

# 引入少量空值和重复值以模拟真实数据（可选，但符合清洗任务）
# 1. 添加一些空的骑行距离和骑行时长
num_nulls = 50
null_indices_dist = np.random.choice(df.index, size=num_nulls//2, replace=False)
null_indices_dur = np.random.choice(df.index, size=num_nulls//2, replace=False)
df.loc[null_indices_dist[:len(null_indices_dist)//2], '骑行距离(km)'] = np.nan
df.loc[null_indices_dist[len(null_indices_dist)//2:], '骑行距离(km)'] = 0
df.loc[null_indices_dur[:len(null_indices_dur)//2], '骑行时长(分钟)'] = 0
df.loc[null_indices_dur[len(null_indices_dur)//2:], '骑行时长(分钟)'] = 25 * 60 # 超过24小时

# 2. 添加一些空的天气状况
num_null_weather = 30
null_weather_indices = np.random.choice(df.index, size=num_null_weather, replace=False)
df.loc[null_weather_indices, '天气状况'] = np.nan

# 3. 添加一些重复记录
num_duplicates = 20
duplicate_indices = np.random.choice(df.index[:-1], size=num_duplicates, replace=False) # 避免最后一行索引溢出
for idx in duplicate_indices:
     df.loc[len(df)] = df.loc[idx] # 添加重复行

# 保存到CSV文件
df.to_csv('bike_rides.csv', index=False, encoding='utf-8-sig') # utf-8-sig 通常在Windows上用Excel打开更好

print(f"已生成包含 {len(df)} 条记录的 bike_rides.csv 文件。")