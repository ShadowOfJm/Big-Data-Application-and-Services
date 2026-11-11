import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 设置随机种子以保证结果可复现
np.random.seed(42)
random.seed(42)

# ================= 配置参数 =================
NUM_RECORDS = 200  # 生成记录数，可根据需要调整
STATION_IDS = [f"STATION_{str(i).zfill(3)}" for i in range(1, 6)]
WEATHER_PHENOMENA = ["晴", "多云", "阴", "雨", "雪", "雾"]
WIND_DIRECTIONS = ["东", "南", "西", "北", "东南", "东北", "西南", "西北"]

# ================= 数据生成逻辑 =================
records = []
start_date = datetime(2025, 1, 1)

for i in range(NUM_RECORDS):
    record_id = i + 1
    station_id = random.choice(STATION_IDS)

    # 随机生成观测日期和时间
    obs_date = start_date + timedelta(days=random.randint(0, 364))
    obs_hour = random.randint(0, 23)
    obs_minute = random.choice([0, 15, 30, 45])
    obs_time = f"{obs_hour:02d}:{obs_minute:02d}"

    # 生成气象要素（含正常值与少量异常值）
    temperature = round(np.random.normal(22, 10), 1)  # 均值22℃，标准差10
    humidity = round(np.random.uniform(30, 95), 1)
    precipitation = round(max(0, np.random.exponential(5)), 1)
    wind_speed = round(max(0, np.random.normal(3.5, 2)), 1)
    wind_dir = random.choice(WIND_DIRECTIONS)
    pressure = round(np.random.normal(1013, 15), 1)
    weather = random.choice(WEATHER_PHENOMENA)

    # === 注入异常/缺失数据以支持清洗任务 ===
    # 任务c1: 降水量为空且天气非雨雪
    if random.random() < 0.05:
        precipitation = np.nan
        weather = random.choice(["晴", "多云", "阴"])

    # 任务c2: 物理不可能的异常值
    if random.random() < 0.03:
        temperature = random.choice([-60, 55])
    if random.random() < 0.03:
        pressure = random.choice([750, 1150])

    # 任务c4: 完全重复记录
    if random.random() < 0.04 and len(records) > 0:
        records.append(records[-1].copy())
        continue

    records.append({
        "记录ID": record_id,
        "观测站ID": station_id,
        "观测日期": obs_date.strftime("%Y-%m-%d"),
        "观测时间": obs_time,
        "气温(℃)": temperature,
        "相对湿度(%)": humidity,
        "降水量(mm)": precipitation,
        "风速(m/s)": wind_speed,
        "风向": wind_dir,
        "气压(hPa)": pressure,
        "天气现象": weather
    })

# ================= 保存文件 =================
df = pd.DataFrame(records)
output_file = "weather_observations.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"✅ 数据生成完成！共 {len(df)} 条记录")
print(f"📁 文件已保存至: {output_file}")
print(f"\n前10行预览:")
print(df.head(10).to_string(index=False))