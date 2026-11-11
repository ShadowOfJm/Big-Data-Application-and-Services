import pandas as pd
import random
from datetime import date, timedelta

# 设置随机种子以确保结果可重现
random.seed(42)

# =================配置参数=================
NUM_DESTINATIONS = 20     # 目的地信息表记录数
NUM_TRAVEL_RECORDS = 2000  # 游客出行记录表记录数
# =========================================

# destination 表：目的地类型
DEST_TYPES = ['海滨', '山区', '城市', '古镇', '度假村']

# 目的地素材：（名称、国家、所属地区、类型、最佳旅游季节）
DESTINATION_POOL = [
    ('三亚', '中国', '亚洲', '海滨', '11月-次年3月'),
    ('厦门鼓浪屿', '中国', '亚洲', '海滨', '3-5月'),
    ('巴厘岛', '印度尼西亚', '东南亚', '海滨', '4-10月'),
    ('普吉岛', '泰国', '东南亚', '海滨', '11月-次年4月'),
    ('马尔代夫', '马尔代夫', '南亚', '度假村', '11月-次年4月'),
    ('东京', '日本', '亚洲', '城市', '3-5月'),
    ('巴黎', '法国', '欧洲', '城市', '4-6月'),
    ('罗马', '意大利', '欧洲', '城市', '4-6月'),
    ('因特拉肯', '瑞士', '欧洲', '山区', '6-9月'),
    ('张家界', '中国', '亚洲', '山区', '4-10月'),
    ('黄山', '中国', '亚洲', '山区', '3-5月'),
    ('丽江古城', '中国', '亚洲', '古镇', '3-5月'),
    ('乌镇', '中国', '亚洲', '古镇', '3-5月'),
    ('京都', '日本', '亚洲', '古镇', '3-4月'),
    ('新加坡', '新加坡', '东南亚', '城市', '全年'),
    ('悉尼', '澳大利亚', '大洋洲', '城市', '9-11月'),
    ('长滩岛', '菲律宾', '东南亚', '海滨', '11月-次年5月'),
    ('清迈', '泰国', '东南亚', '古镇', '11月-次年2月'),
    ('圣托里尼', '希腊', '欧洲', '海滨', '5-10月'),
    ('皇后镇', '新西兰', '大洋洲', '度假村', '12月-次年2月')
]

# 交通方式与用户ID（用于出行记录表的真实感）
TRANSPORT_MODES = ['飞机', '高铁', '自驾', '大巴', '邮轮']
# 目的地类型对应的日均消费区间（元/天），用于生成合理的预估费用与总花费
DAILY_COST_RANGE = {
    '海滨': (600, 1800),
    '山区': (400, 1200),
    '城市': (500, 1600),
    '古镇': (300, 900),
    '度假村': (1000, 3000)
}


def generate_destination_data():
    """
    生成 destination 表的数据。
    字段：dest_id、dest_name、country、region、dest_type、avg_rating、
          best_season、estimated_cost
    """
    print("正在生成 destination.csv 数据...")
    data = []

    # 从素材池中随机抽取，保证不重名
    selected = random.sample(DESTINATION_POOL, NUM_DESTINATIONS)

    for dest_id, (dest_name, country, region, dest_type, best_season) in enumerate(selected, start=1):
        # 平均用户评分范围 1.0-5.0
        avg_rating = round(random.uniform(3.5, 5.0), 2)

        # 人均预估费用按目的地类型的日均消费乘以建议出行天数估算
        low, high = DAILY_COST_RANGE[dest_type]
        estimated_cost = round(random.uniform(low, high) * random.randint(3, 7), 2)

        data.append({
            'dest_id': dest_id,
            'dest_name': dest_name,
            'country': country,
            'region': region,
            'dest_type': dest_type,
            'avg_rating': avg_rating,
            'best_season': best_season,
            'estimated_cost': estimated_cost
        })

    df = pd.DataFrame(data)
    df.to_csv('destination.csv', index=False, encoding='utf-8-sig')
    print(f"destination.csv 已生成，包含 {len(df)} 条记录。")
    return df


def generate_travel_record_data(destination_df):
    """
    生成 travel_record 表的数据。
    字段：record_id、user_id、dest_id、travel_date、travel_days、total_expense、
          transport_mode、is_group_tour、satisfaction
    dest_id 取自 destination 表，保证外键有效。
    """
    print("正在生成 travel_record.csv 数据...")
    dest_ids = destination_df['dest_id'].tolist()
    dest_cost_map = dict(zip(destination_df['dest_id'], destination_df['estimated_cost']))

    # 每个目的地给定一个固定的“实际/预估”费用比，再叠加逐条记录的随机波动。
    # 这样不同目的地的实际花费才有系统性差异：费用比高于 1.2 的目的地会在
    # “人均预估费用低于实际人均花费 20% 以上”的查询中命中，其余不命中
    dest_actual_ratio = {dest_id: random.uniform(0.85, 1.35) for dest_id in dest_ids}

    data = []
    for record_id in range(1, NUM_TRAVEL_RECORDS + 1):
        dest_id = random.choice(dest_ids)
        # 用户ID 脱敏处理，形如 U000123
        user_id = f"U{random.randint(1, 800):06d}"

        # 出行日期集中在 2024-2025 年，便于按年份和季度统计
        travel_date = date(2024, 1, 1) + timedelta(days=random.randint(0, 730))

        travel_days = random.randint(1, 10)

        # 总花费即该次出行的人均花费：预估费用 × 目的地费用比 × 记录级波动
        total_expense = round(
            dest_cost_map[dest_id] * dest_actual_ratio[dest_id] * random.uniform(0.85, 1.15), 2
        )

        transport_mode = random.choice(TRANSPORT_MODES)
        is_group_tour = random.choices([1, 0], weights=[40, 60], k=1)[0]
        satisfaction = random.choices([1, 2, 3, 4, 5], weights=[2, 5, 15, 38, 40], k=1)[0]

        data.append({
            'record_id': record_id,
            'user_id': user_id,
            'dest_id': dest_id,
            'travel_date': travel_date,
            'travel_days': travel_days,
            'total_expense': total_expense,
            'transport_mode': transport_mode,
            'is_group_tour': is_group_tour,
            'satisfaction': satisfaction
        })

    df = pd.DataFrame(data)
    df.to_csv('travel_record.csv', index=False, encoding='utf-8-sig')
    print(f"travel_record.csv 已生成，包含 {len(df)} 条记录。")
    return df


if __name__ == "__main__":
    # 先生成目的地数据，出行记录表的 dest_id 取自目的地表
    destination_df = generate_destination_data()
    travel_record_df = generate_travel_record_data(destination_df)

    print("\n数据生成完成！")
    print("- destination.csv")
    print("- travel_record.csv")
