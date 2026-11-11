import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid

# 设置 Faker 实例，用于生成模拟数据
fake = Faker('zh_CN')  # 使用中文本地化数据

# --- 配置 ---
NUM_BIKES = 100  # 模拟100辆自行车
NUM_RECORDS = 1000  # 模拟1000条骑行记录
BIKE_ID_PREFIX = "B"
USER_ID_PREFIX = "U"


def generate_bike_status():
    """
    生成 bike_status 表的数据。
    """
    print("正在生成 bike_status 数据...")
    data = []
    for i in range(1, NUM_BIKES + 1):
        bike_id = f"{BIKE_ID_PREFIX}{i:05d}"  # B000001, B000002, ...

        # 随机选择状态 (可用或不可用)
        status = random.choice(['可用', '维修'])

        # 电池电量为 0-100 的整数
        battery_level = random.randint(0, 100)

        # 最后一次维护时间在最近一个月内
        days_since_maintenance = random.randint(0, 90)
        last_maintain_time = datetime.now() - timedelta(days=days_since_maintenance)

        # 当前位置使用 Faker 生成一个城市名
        current_location = fake.city()

        # 总里程为 0 到 5000 公里的浮点数
        total_mileage = round(random.uniform(0, 5000), 2)

        data.append({
            'bike_id': bike_id,
            'status': status,
            'battery_level': battery_level,
            'last_maintain_time': last_maintain_time.strftime('%Y-%m-%d %H:%M:%S'),
            'current_location': current_location,
            'total_mileage': total_mileage
        })

    df = pd.DataFrame(data)
    df.to_csv('bike_status.csv', index=False, encoding='utf-8-sig')
    print(f"bike_status.csv 已生成，包含 {len(df)} 条记录。")
    return df


def generate_ride_records(bike_ids_list):
    """
    生成 ride_records 表的数据。
    """
    print("正在生成 ride_records 数据...")
    data = []
    for _ in range(NUM_RECORDS):
        id_val = len(data) + 1

        # 从已生成的自行车ID列表中随机选择一个
        bike_id = random.choice(bike_ids_list)

        # 生成用户ID (例如 U000000001)
        user_id_num = random.randint(1, 10000)
        user_id = f"{USER_ID_PREFIX}{user_id_num:09d}"

        # 随机生成一个起始时间（过去一周内的某个时刻）
        start_time = datetime.now() - timedelta(days=random.randint(0, 7),
                                                hours=random.randint(0, 23),
                                                minutes=random.randint(0, 59))

        # 随机生成骑行时长（分钟），例如 5到120分钟
        ride_duration_minutes = random.randint(5, 120)
        ride_duration_seconds = ride_duration_minutes * 60
        end_time = start_time + timedelta(seconds=ride_duration_seconds)

        # 随机生成起点和终点位置
        start_location = fake.address()
        end_location = fake.address()

        # 随机生成骑行距离（公里），例如 0.5到20公里
        ride_distance = round(random.uniform(0.5, 20.0), 2)

        data.append({
            'id': id_val,
            'bike_id': bike_id,
            'user_id': user_id,
            'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'start_location': start_location,
            'end_location': end_location,
            'ride_distance': ride_distance,
            'ride_duration': ride_duration_minutes
        })

    df = pd.DataFrame(data)
    df.to_csv('ride_records.csv', index=False, encoding='utf-8-sig')
    print(f"ride_records.csv 已生成，包含 {len(df)} 条记录。")
    return df


if __name__ == "__main__":
    # 生成 bike_status 数据并获取自行车ID列表
    bike_status_df = generate_bike_status()
    bike_ids = bike_status_df['bike_id'].tolist()

    # 基于自行车ID列表生成 ride_records 数据
    ride_records_df = generate_ride_records(bike_ids)

    print("\n数据生成完成！")
    print("- ride_records.csv")
    print("- bike_status.csv")
