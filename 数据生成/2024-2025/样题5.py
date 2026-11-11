# generate_hotel_data.py

import csv
import random
from datetime import datetime, timedelta

# 定义可能的城市和省份
cities_provinces = {
    '北京': '北京市', '上海': '上海市', '广州': '广东省', '深圳': '广东省',
    '杭州': '浙江省', '成都': '四川省', '西安': '陕西省', '南京': '江苏省',
    '武汉': '湖北省', '长沙': '湖南省'
}
cities = list(cities_provinces.keys())

# 定义可能的星级
levels = ['经济型', '舒适型', '高档型', '豪华型']

# 定义可能的房间类型
room_types = ['标准双人房', '大床房', '商务套房', '行政套房', '家庭房']

# 定义公司和出行住宿类型（用于填充额外字段）
companies = ['携程', '美团', '飞猪', '去哪儿', '同程', '艺龙', 'Agoda', 'Booking.com']
travel_types = ['商务出行', '休闲旅游', '家庭出游', '情侣度假']
campus_life_options = ['是', '否']

# 定义价格区间
price_ranges = {
    '经济型': (100, 300),
    '舒适型': (301, 600),
    '高档型': (601, 1200),
    '豪华型': (1201, 3000)
}


def generate_hotel_name(city, index):
    """生成酒店名称"""
    prefixes = [f"{city}", f"{city}市中心", f"{city}火车站", f"{city}机场", f"{city}商业区"]
    suffixes = ["大酒店", "宾馆", "酒店", "国际酒店", "商务酒店", "精品酒店", "快捷酒店", "度假村"]
    return f"{random.choice(prefixes)}{random.choice(suffixes)}{index}"


def generate_decorate_time():
    """生成装修时间，集中在近几年"""
    # 生成一个在过去 20 年内的随机日期
    end_date = datetime.now()
    start_date = end_date - timedelta(days=20 * 365)
    random_date = start_date + (end_date - start_date) * random.random()
    # 有一定概率为空
    if random.random() < 0.1:
        return ""
    return random_date.strftime("%Y-%m")


def main():
    """主函数，生成CSV文件"""
    filename = "hotel.csv"

    # CSV 文件的字段头 (基于PDF中的表结构和任务要求)
    # PDF中 hotel 表字段: id, hotel_name, city, province, level, room_num, score, commnet_num
    # 但任务中还提到了更多字段用于清洗等，所以我们包含这些额外字段
    fieldnames = [
        '酒店名称', '地区', '地址', '卫生评分', '服务评分', '设施评分', '位置评分',
        '评价数', '装修时间', '房间类型', '房价', '经度', '纬度', '公司', '出行住宿', '校园生活'
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 写入头部
        writer.writeheader()

        hotel_id = 1
        num_hotels = 200  # 生成200条数据

        for i in range(num_hotels):
            # 基本信息
            city = random.choice(cities)
            province = cities_provinces[city]
            hotel_name = generate_hotel_name(city, i + 1)

            # 地址 (模拟)
            districts = ["解放路", "中山路", "人民路", "建设路", "和平路", "青年路", "胜利路", "光明路"]
            address = f"{province}{city}{random.choice(districts)}{random.randint(1, 500)}号"

            # 评分 (0-5分)
            hygiene_score = round(random.uniform(3.0, 5.0), 1)
            service_score = round(random.uniform(3.0, 5.0), 1)
            facility_score = round(random.uniform(3.0, 5.0), 1)
            location_score = round(random.uniform(3.0, 5.0), 1)

            # 评价数
            comment_num = random.randint(0, 5000)

            # 装修时间
            decorate_time = generate_decorate_time()

            # 房间类型
            room_type = random.choice(room_types)

            # 房价 (基于星级和评分)
            # 简单逻辑：星级和评分越高，价格越高
            base_level = levels.index('舒适型')  # 默认舒适型
            if facility_score > 4.5:
                base_level = levels.index('豪华型')
            elif facility_score > 4.0:
                base_level = levels.index('高档型')
            elif facility_score < 3.5:
                base_level = levels.index('经济型')

            level = levels[base_level]
            price_min, price_max = price_ranges[level]
            price = random.randint(price_min, price_max)

            # 经纬度 (模拟北京中心附近)
            longitude = round(116.40 + random.uniform(-0.5, 0.5), 6)
            latitude = round(39.90 + random.uniform(-0.5, 0.5), 6)

            # 公司和出行类型
            company = random.choice(companies)
            travel_type = random.choice(travel_types)
            campus_life = random.choice(campus_life_options)

            # 以一定概率生成一些“脏数据”用于清洗任务
            if random.random() < 0.02:  # 2% 概率酒店名称为空
                hotel_name = ""
            if random.random() < 0.03:  # 3% 概率评分为空 (用字符串表示)
                if random.random() < 0.25:
                    hygiene_score = ""
                elif random.random() < 0.33:
                    service_score = ""
                elif random.random() < 0.5:
                    facility_score = ""
                else:
                    location_score = ""
            if random.random() < 0.02:  # 2% 概率评价数为0但评分不为0
                if comment_num == 0 and (
                        hygiene_score > 0 or service_score > 0 or facility_score > 0 or location_score > 0):
                    pass  # Already satisfied
                else:
                    comment_num = 0
            if random.random() < 0.02:  # 2% 概率地址为空
                address = ""
            if random.random() < 0.03:  # 3% 概率房价为0
                price = 0
            if random.random() < 0.02:  # 2% 概率房价为空
                price = ""
            if random.random() < 0.02:  # 2% 概率房间类型为"标准间"或"标准房"
                room_type = random.choice(["标准间", "标准房"])
            if random.random() < 0.03:  # 3% 概率所有评分都为0
                if random.random() < 0.5:
                    hygiene_score, service_score, facility_score, location_score = 0, 0, 0, 0
            if random.random() < 0.02:  # 2% 概率评分超过5分
                if random.random() < 0.25:
                    hygiene_score = random.uniform(5.1, 6.0)
                elif random.random() < 0.33:
                    service_score = random.uniform(5.1, 6.0)
                elif random.random() < 0.5:
                    facility_score = random.uniform(5.1, 6.0)
                else:
                    location_score = random.uniform(5.1, 6.0)
            # 重复数据在写入时处理更简单，这里不特意生成

            # 写入一行数据
            writer.writerow({
                '酒店名称': hotel_name,
                '地区': city,
                '地址': address,
                '卫生评分': hygiene_score,
                '服务评分': service_score,
                '设施评分': facility_score,
                '位置评分': location_score,
                '评价数': comment_num,
                '装修时间': decorate_time,
                '房间类型': room_type,
                '房价': price,
                '经度': longitude,
                '纬度': latitude,
                '公司': company,
                '出行住宿': travel_type,
                '校园生活': campus_life
            })

            hotel_id += 1

    print(f"已生成 {num_hotels} 条酒店数据到 {filename} 文件中。")


if __name__ == "__main__":
    main()