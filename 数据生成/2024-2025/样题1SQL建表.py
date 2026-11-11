import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 设置随机种子以确保结果可重现
np.random.seed(42)
random.seed(42)


def generate_house_info_data():
    """生成房源信息表数据"""
    house_ids = list(range(1, 1001))  # 1000条房源记录

    communities = [
        "阳光花园", "碧水湾", "绿城雅苑", "金桂园", "紫荆花城",
        "梧桐郡", "翡翠湖畔", "香榭丽舍", "锦绣江南", "龙湖天街",
        "万科城", "碧桂园", "恒大华府", "保利花园", "中海寰宇"
    ]

    districts = ["朝阳区", "海淀区", "丰台区", "西城区", "东城区",
                 "昌平区", "大兴区", "通州区", "顺义区", "房山区"]

    layouts = ["一室一厅", "两室一厅", "两室两厅", "三室一厅", "三室两厅",
               "四室两厅", "复式", "别墅"]

    orientations = ["南北通透", "朝南", "朝北", "朝东", "朝西", "东南", "西南"]

    data = []
    for i, house_id in enumerate(house_ids):
        community = random.choice(communities)
        district = random.choice(districts)
        layout = random.choice(layouts)
        area = round(random.uniform(40, 200), 2)
        price = round(area * random.uniform(5000, 15000), 2)
        floor_info = f"{random.randint(1, 30)}层/共{random.randint(20, 40)}层"
        orientation = random.choice(orientations)
        status = random.choice(['在售', '出售'])

        data.append({
            'house_id': house_id,
            'community': community,
            'district': district,
            'layout': layout,
            'area': area,
            'price': price,
            'floor_info': floor_info,
            'orientation': orientation,
            'status': status
        })

    return pd.DataFrame(data)


def generate_community_info_data():
    """生成小区信息表数据"""
    community_ids = list(range(1, 101))  # 100个小区

    community_names = [
        "阳光花园", "碧水湾", "绿城雅苑", "金桂园", "紫荆花城",
        "梧桐郡", "翡翠湖畔", "香榭丽舍", "锦绣江南", "龙湖天街",
        "万科城", "碧桂园", "恒大华府", "保利花园", "中海寰宇",
        "绿地国际", "华润置地", "融创壹号院", "世茂天际", "富力城",
        "远洋山水", "金地格林", "招商雍华府", "泰禾金尊府", "华夏幸福城",
        "新城控股", "龙湖春江", "绿地申花", "保利茉莉公馆", "中海云麓",
        "万科翡翠", "碧桂园凤凰", "恒大御景", "华润万象府", "招商蛇口",
        "远洋国际", "金地华府", "融创桃花源", "泰禾院子", "富力公主",
        "绿地海珀", "华润悦府", "保利天汇", "中海寰宇天下", "万科城市之光",
        "碧桂园森林", "恒大中央广场", "龙湖原著", "世茂海峡", "华夏四季",
        "新城吾悦", "龙湖春江郦城", "绿地理想城", "保利大国璟", "中海熙岸",
        "万科新里程", "碧桂园星作", "恒大金碧", "华润置地橡树湾", "招商雍容华府",
        "远洋万和城", "金地自在城", "融创壹号院", "泰禾北京院子", "富力桃园",
        "绿地海顿公馆", "华润置地幸福里", "保利香槟国际", "中海紫御", "万科翡翠公园",
        "碧桂园天玺", "恒大绿洲", "龙湖景粼天序", "世茂璀璨天城", "华夏四季公馆",
        "新城控股樾府", "龙湖春江彼岸", "绿地国际花都", "保利和光尘樾", "中海寰宇时代",
        "万科新里程", "碧桂园星作", "恒大金碧", "华润置地橡树湾", "招商雍容华府",
        "远洋万和城", "金地自在城", "融创壹号院", "泰禾北京院子", "富力桃园",
        "绿地海顿公馆", "华润置地幸福里", "保利香槟国际", "中海紫御", "万科翡翠公园",
        "碧桂园天玺", "恒大绿洲", "龙湖景粼天序", "世茂璀璨天城", "华夏四季公馆",
        "新城控股樾府", "龙湖春江彼岸", "绿地国际花都", "保利和光尘樾", "中海寰宇时代"
    ]

    districts = ["朝阳区", "海淀区", "丰台区", "西城区", "东城区",
                 "昌平区", "大兴区", "通州区", "顺义区", "房山区"]

    data = []
    for i, community_id in enumerate(community_ids):
        # 如果社区名称不够用，循环使用
        community_name_index = i % len(community_names)
        community_name = community_names[community_name_index]
        district = random.choice(districts)
        build_year = random.randint(1990, 2023)
        property_fee = round(random.uniform(2.0, 8.0), 2)
        subway_distance = random.randint(0, 5000)  # 米

        data.append({
            'community_id': community_id,
            'community_name': community_name,
            'district': district,
            'build_year': build_year,
            'property_fee': property_fee,
            'subway_distance': subway_distance
        })

    return pd.DataFrame(data)


def generate_transaction_records_data():
    """生成交易记录表数据"""
    record_ids = list(range(1, 801))  # 800条交易记录

    # 生成交易日期（过去5年内的随机日期）
    start_date = datetime.now() - timedelta(days=5 * 365)
    end_date = datetime.now()

    data = []
    for i, record_id in enumerate(record_ids):
        house_id = random.randint(1, 1000)  # 随机关联房源ID
        days_diff = random.randint(0, 5 * 365)
        transaction_date = start_date + timedelta(days=days_diff)
        transaction_price = round(random.uniform(1000000, 15000000), 2)  # 100万-1500万
        price_change = round(random.uniform(-100000, 100000), 2)  # 价格变动
        transaction_type = random.choice(['二手房', '新房', '法拍房', '共有产权房'])

        data.append({
            'record_id': record_id,
            'house_id': house_id,
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'transaction_price': transaction_price,
            'price_change': price_change,
            'transaction_type': transaction_type
        })

    return pd.DataFrame(data)


def main():
    print("正在生成房源信息表数据...")
    house_info_df = generate_house_info_data()
    house_info_df.to_csv('house_info.csv', index=False, encoding='utf-8')
    print(f"已生成 {len(house_info_df)} 条房源信息数据")

    print("正在生成小区信息表数据...")
    community_info_df = generate_community_info_data()
    community_info_df.to_csv('community_info.csv', index=False, encoding='utf-8')
    print(f"已生成 {len(community_info_df)} 条小区信息数据")

    print("正在生成交易记录表数据...")
    transaction_records_df = generate_transaction_records_data()
    transaction_records_df.to_csv('transaction_records.csv', index=False, encoding='utf-8')
    print(f"已生成 {len(transaction_records_df)} 条交易记录数据")

    print("\n数据文件已生成完成！")
    print("文件列表：")
    print("- house_info.csv")
    print("- community_info.csv")
    print("- transaction_records.csv")


if __name__ == "__main__":
    main()