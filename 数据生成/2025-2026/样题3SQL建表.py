import pandas as pd
import random
from datetime import date, timedelta

# 设置随机种子以确保结果可重现
random.seed(42)

# =================配置参数=================
NUM_WEATHER = 400   # weather 表的观测记录数
# =========================================

# 题目要求插入到 new_weather 表中的三条记录
NEW_WEATHER_ROWS = [
    (1016, '三亚', 572000, 2, '热带海洋性季风气候'),
    (1026, '上海', 200000, 1, '亚热带季风气候'),
    (1032, '乌鲁木齐', 830000, 2, '中温带半干旱大陆性气候')
]

# 省份：province_info 表
PROVINCES = [
    (1016, '海南省'),
    (1026, '上海市'),
    (1032, '新疆维吾尔自治区'),
    (1011, '北京市'),
    (1013, '广东省'),
    (1018, '江苏省'),
    (1021, '浙江省')
]
PROVINCE_CLIMATE = {
    1016: '热带海洋性季风气候',
    1026: '亚热带季风气候',
    1032: '中温带半干旱大陆性气候',
    1011: '温带季风气候',
    1013: '亚热带季风气候',
    1018: '亚热带季风气候',
    1021: '亚热带季风气候'
}

# 城市：city_info 表。每项为（城市ID、省份ID、城市名称、邮编、城市等级、气候条件）
CITIES = [
    (1, 1011, '北京', 100000, 1, '温带季风气候'),
    (2, 1013, '广州', 510000, 1, '亚热带季风气候'),
    (3, 1013, '深圳', 518000, 1, '亚热带季风气候'),
    (4, 1026, '上海', 200000, 1, '亚热带季风气候'),
    (5, 1018, '南京', 210000, 2, '亚热带季风气候'),
    (6, 1021, '杭州', 310000, 2, '亚热带季风气候'),
    (7, 1032, '乌鲁木齐', 830000, 2, '中温带半干旱大陆性气候'),
    (8, 1032, '阿克苏', 843000, 3, '温带大陆性干旱气候'),
    (9, 1016, '三亚', 572000, 2, '热带海洋性季风气候'),
    (10, 1016, '海口', 570000, 2, '热带海洋性季风气候'),
    (11, 1018, '苏州', 215000, 2, '亚热带季风气候'),
    (12, 1021, '宁波', 315000, 2, '亚热带季风气候')
]

WEATHER_CONDITIONS = ['晴', '多云', '阴', '小雨', '中雨', '大雨', '雷阵雨']


def generate_city_info():
    """
    生成 city_info 表的数据（题目中该表由给定 sql 文件导入，此脚本用于重建）。
    字段：city_id、province_id、city_name、zip_code、levels、climate
    """
    print("正在生成 city_info.csv 数据...")
    data = []
    for city_id, province_id, city_name, zip_code, levels, climate in CITIES:
        data.append({
            'city_id': city_id,
            'province_id': province_id,
            'city_name': city_name,
            'zip_code': zip_code,
            'levels': levels,
            'climate': climate
        })

    df = pd.DataFrame(data)
    df.to_csv('city_info.csv', index=False, encoding='utf-8-sig')
    print(f"city_info.csv 已生成，包含 {len(df)} 条记录。")
    return df


def generate_province_info():
    """
    生成 province_info 表的数据（题目中该表由给定 sql 文件导入，此脚本用于重建）。
    字段：province_id、province_name
    """
    print("正在生成 province_info.csv 数据...")
    data = [{'province_id': province_id, 'province_name': province_name}
            for province_id, province_name in PROVINCES]

    df = pd.DataFrame(data)
    df.to_csv('province_info.csv', index=False, encoding='utf-8-sig')
    print(f"province_info.csv 已生成，包含 {len(df)} 条记录。")
    return df


def generate_new_weather():
    """
    生成 new_weather 表的数据。
    字段：id、province_id、city_name、zip_code、levels、climate
    内容为题目要求插入的三条记录，id 自增。
    """
    print("正在生成 new_weather.csv 数据...")
    data = []
    for index, (province_id, city_name, zip_code, levels, climate) in enumerate(NEW_WEATHER_ROWS, start=1):
        data.append({
            'id': index,
            'province_id': province_id,
            'city_name': city_name,
            'zip_code': zip_code,
            'levels': levels,
            'climate': climate
        })

    df = pd.DataFrame(data)
    df.to_csv('new_weather.csv', index=False, encoding='utf-8-sig')
    print(f"new_weather.csv 已生成，包含 {len(df)} 条记录。")
    return df


def generate_weather():
    """
    生成 weather 表的数据。
    字段：id、city_id、city_name、climate、weather_condition、max_temp、wind_level、weather_date
    其中 climate、wind_level、max_temp 供题目中的四条查询使用。
    """
    print("正在生成 weather.csv 数据...")
    data = []

    for record_id in range(1, NUM_WEATHER + 1):
        city_id, province_id, city_name, zip_code, levels, climate = random.choice(CITIES)

        # 观测日期集中在 2025 年内
        weather_date = date(2025, 1, 1) + timedelta(days=random.randint(0, 364))

        weather_condition = random.choices(
            WEATHER_CONDITIONS,
            weights=[25, 22, 13, 15, 8, 5, 12],
            k=1
        )[0]

        # 最高气温：按气候带给出合理区间
        if '热带' in climate:
            max_temp = round(random.uniform(24, 36), 1)
        elif '干旱' in climate or '大陆性' in climate:
            max_temp = round(random.uniform(5, 38), 1)
        elif '温带季风' in climate and city_name == '北京':
            max_temp = round(random.uniform(-5, 35), 1)
        else:
            max_temp = round(random.uniform(12, 34), 1)

        # 风力等级 1-6 级
        wind_level = random.randint(1, 6)

        data.append({
            'id': record_id,
            'city_id': city_id,
            'city_name': city_name,
            'climate': climate,
            'weather_condition': weather_condition,
            'max_temp': max_temp,
            'wind_level': wind_level,
            'weather_date': weather_date
        })

    df = pd.DataFrame(data)
    df.to_csv('weather.csv', index=False, encoding='utf-8-sig')
    print(f"weather.csv 已生成，包含 {len(df)} 条记录。")
    return df


if __name__ == "__main__":
    # new_weather 为建表后手工插入的固定三条记录，其余三张表为题目给定的导入文件
    new_weather_df = generate_new_weather()
    city_info_df = generate_city_info()
    province_info_df = generate_province_info()
    weather_df = generate_weather()

    print("\n数据生成完成！")
    print("- new_weather.csv")
    print("- city_info.csv")
    print("- province_info.csv")
    print("- weather.csv")
