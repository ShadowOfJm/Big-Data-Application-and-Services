import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta, time

# 设置 Faker 实例，用于生成模拟数据
fake = Faker('zh_CN')

# --- 配置 ---
NUM_SPOTS = 50  # 模拟50个景点
NUM_RECORDS = 5000  # 模拟5000条游客流量记录


def generate_scenic_spots():
    """
    生成 scenic_spot 表的数据。
    """
    print("正在生成 scenic_spot.csv 数据...")
    data = []
    # 定义一些常见的景点类型和级别
    types = ['自然风光', '历史古迹', '现代建筑', '主题乐园', '宗教场所', '博物馆']
    levels = ['5A', '4A', '3A', '2A', '1A']
    cities = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '西安', '武汉', '重庆']

    for i in range(1, NUM_SPOTS + 1):
        spot_id = i
        # 生成一个有中国特色的景点名称
        suffixes = ['风景区', '公园', '山', '湖', '寺', '塔', '古城', '古镇', '乐园', '遗址']
        spot_name = fake.last_name() + random.choice(suffixes)

        city = random.choice(cities)
        level = random.choice(levels)
        type_ = random.choice(types)

        # 门票价格 0-300元
        ticket_price = round(random.uniform(0, 300), 2)

        # 开放时间 例如 08:00-18:00
        open_hour = random.randint(6, 10)
        close_hour = random.randint(17, 22)
        opening_hours = f"{open_hour:02d}:00-{close_hour:02d}:00"

        # 最大承载量 1000-50000人
        max_capacity = random.randint(1000, 50000)

        data.append({
            'spot_id': spot_id,
            'spot_name': spot_name,
            'city': city,
            'level': level,
            'type': type_,
            'ticket_price': ticket_price,
            'opening_hours': opening_hours,
            'max_capacity': max_capacity
        })

    df = pd.DataFrame(data)
    df.to_csv('scenic_spot.csv', index=False, encoding='utf-8-sig')
    print(f"scenic_spot.csv 已生成，包含 {len(df)} 条记录。")
    return df


def generate_visitor_flow(spot_ids_list):
    """
    生成 visitor_flow 表的数据。
    """
    print("正在生成 visitor_flow.csv 数据...")
    data = []
    # 生成过去一年中的随机日期
    start_date = datetime.today() - timedelta(days=365)

    weathers = ['晴', '多云', '阴', '小雨', '大雨', '雪', '雾']

    for i in range(1, NUM_RECORDS + 1):
        record_id = i

        # 从已生成的景点ID列表中随机选择一个
        spot_id = random.choice(spot_ids_list)

        # 随机生成访问日期
        random_days = random.randint(0, 365)
        visit_date = start_date + timedelta(days=random_days)

        # 游客数量，基于最大容量的一个百分比，但有一定随机性
        capacity_for_this_spot = next((item['max_capacity'] for item in scenic_spot_data if item['spot_id'] == spot_id),
                                      10000)
        base_visitor_count = int(capacity_for_this_spot * random.uniform(0.05, 0.95))
        visitor_count = max(100, base_visitor_count)  # 确保至少有100人

        # 高峰时段，假设在 9-18 点之间
        peak_hour = time(hour=random.randint(9, 18), minute=random.randint(0, 59))

        weather = random.choice(weathers)

        # 是否为节假日，简单地设置为20%概率是节假日
        is_holiday = random.choice([True, False])
        if is_holiday:
            # 如果是节假日，游客数量可能会更多
            visitor_count = int(visitor_count * random.uniform(1.1, 2.0))

        data.append({
            'record_id': record_id,
            'spot_id': spot_id,
            'visit_date': visit_date.strftime('%Y-%m-%d'),
            'visitor_count': visitor_count,
            'peak_hour': peak_hour.strftime('%H:%M:%S'),
            'weather': weather,
            'is_holiday': is_holiday
        })

    df = pd.DataFrame(data)
    df.to_csv('visitor_flow.csv', index=False, encoding='utf-8-sig')
    print(f"visitor_flow.csv 已生成，包含 {len(df)} 条记录。")
    return df


if __name__ == "__main__":
    # 为了在生成 visitor_flow 时能知道对应 spot_id 的 max_capacity，我们先生成并存储 scenic_spot 数据
    scenic_spot_df = generate_scenic_spots()
    scenic_spot_data = scenic_spot_df.to_dict('records')  # 转换为字典列表方便查找
    spot_ids = scenic_spot_df['spot_id'].tolist()

    # 基于景点ID列表生成 visitor_flow 数据
    visitor_flow_df = generate_visitor_flow(spot_ids)

    print("\n数据生成完成！")
    print("- scenic_spot.csv")
    print("- visitor_flow.csv")
