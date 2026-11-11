import pandas as pd
import random
import datetime

# 设置随机种子以确保结果可重现
random.seed(42)

# =================配置参数=================
NUM_TREES = 60        # 树木信息表记录数
NUM_GROWTH_RECORDS = 150  # 生长记录表记录数
# =========================================

# 区域与土壤类型、管护单位（region_info 表用于关联 tree_info 的 region 字段）
REGION_SOIL = {
    "南山区": ("壤土", "南山区城市管理局"),
    "福田区": ("壤土", "福田区园林绿化中心"),
    "罗湖区": ("红壤", "罗湖区市政养护所"),
    "宝安区": ("砂土", "宝安区绿化管理处"),
    "龙岗区": ("黄壤", "龙岗区公园管理中心"),
    "盐田区": ("砂土", "盐田区城市管理所")
}
REGIONS = list(REGION_SOIL.keys())

SPECIES_LIST = [
    "香樟", "二球悬铃木", "大王椰子", "榕树", "木棉",
    "荷花玉兰", "秋枫", "盆架子", "凤凰木", "宫粉羊蹄甲",
    "紫檀", "银杏", "水杉", "白蜡树"
]
HEALTH_STATUS_OPTIONS = ["健康", "一般", "较差"]


def generate_region_info():
    """
    生成 region_info 表的数据。
    字段：region_id、region_name、area_size、soil_type、manager
    """
    print("正在生成 region_info.csv 数据...")
    data = []

    for region_id, region_name in enumerate(REGIONS, start=1):
        soil_type, manager = REGION_SOIL[region_name]
        # 区域面积 100-5000 公顷
        area_size = round(random.uniform(100, 5000), 2)

        data.append({
            'region_id': region_id,
            'region_name': region_name,
            'area_size': area_size,
            'soil_type': soil_type,
            'manager': manager
        })

    df = pd.DataFrame(data)
    df.to_csv('region_info.csv', index=False, encoding='utf-8-sig')
    print(f"region_info.csv 已生成，包含 {len(df)} 条记录。")
    return df


def generate_tree_info():
    """
    生成 tree_info 表的数据。
    字段：tree_id、species、region、age、height、diameter、health_status、planting_date
    region 取自 region_info 表，保证两表可以关联查询。
    """
    print("正在生成 tree_info.csv 数据...")
    data = []

    for tree_id in range(1, NUM_TREES + 1):
        species = random.choice(SPECIES_LIST)
        region = random.choice(REGIONS)
        age = random.randint(1, 100)

        # 高度与胸径随树龄增长，加入随机波动
        height = round(max(1.5, age * random.uniform(0.1, 0.3) + random.uniform(-1, 2)), 2)
        diameter = round(max(5.0, age * random.uniform(0.2, 0.8) + random.uniform(-2, 5)), 2)

        # 健康状况加权随机，多数为健康
        health_status = random.choices(HEALTH_STATUS_OPTIONS, weights=[70, 20, 10], k=1)[0]

        # 种植日期按树龄倒推，保证与 age 一致
        current_year = 2026
        planting_year = max(1900, current_year - age + random.randint(0, 1))
        planting_date = datetime.date(planting_year, random.randint(1, 12), random.randint(1, 28))

        data.append({
            'tree_id': tree_id,
            'species': species,
            'region': region,
            'age': age,
            'height': height,
            'diameter': diameter,
            'health_status': health_status,
            'planting_date': planting_date
        })

    df = pd.DataFrame(data)
    df.to_csv('tree_info.csv', index=False, encoding='utf-8-sig')
    print(f"tree_info.csv 已生成，包含 {len(df)} 条记录。")
    return df


def generate_growth_records(tree_df):
    """
    生成 growth_records 表的数据。
    字段：record_id、tree_id、measure_date、new_height、health_update、note
    tree_id 取自 tree_info 表，保证外键有效。
    """
    print("正在生成 growth_records.csv 数据...")
    tree_ids = tree_df['tree_id'].tolist()
    tree_heights = dict(zip(tree_df['tree_id'], tree_df['height']))

    notes = ['生长正常', '已修剪枯枝', '发现虫害已处理', '施肥养护', '长势良好',
             '需持续观察', '根系加固', '枝叶稀疏待复壮', '']

    data = []
    for record_id in range(1, NUM_GROWTH_RECORDS + 1):
        tree_id = random.choice(tree_ids)

        # 测量日期集中在最近两年内，便于“最近一年内有生长记录”的查询
        days_ago = random.randint(0, 730)
        measure_date = datetime.date(2026, 1, 1) - datetime.timedelta(days=days_ago)

        # 新增高度：在基准高度上小幅增长
        new_height = round(max(0.1, tree_heights[tree_id] * random.uniform(0.01, 0.15)), 2)

        health_update = random.choices(HEALTH_STATUS_OPTIONS, weights=[65, 25, 10], k=1)[0]
        note = random.choice(notes)

        data.append({
            'record_id': record_id,
            'tree_id': tree_id,
            'measure_date': measure_date,
            'new_height': new_height,
            'health_update': health_update,
            'note': note
        })

    df = pd.DataFrame(data)
    df.to_csv('growth_records.csv', index=False, encoding='utf-8-sig')
    print(f"growth_records.csv 已生成，包含 {len(df)} 条记录。")
    return df


if __name__ == "__main__":
    # 先生成区域与树木数据，生长记录的 tree_id 取自树木表
    region_df = generate_region_info()
    tree_df = generate_tree_info()
    growth_df = generate_growth_records(tree_df)

    print("\n数据生成完成！")
    print("- region_info.csv")
    print("- tree_info.csv")
    print("- growth_records.csv")
