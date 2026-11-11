import pandas as pd
import random
from datetime import datetime, timedelta

# 设置随机种子以确保结果可重现
random.seed(42)

# --- 配置 ---
NUM_HOTELS = 200  # 模拟200家酒店
NUM_COMMENTS = 800  # 模拟800条评论

# 城市与省份的对应关系（与样题5酒店数据集保持一致）
cities_provinces = {
    '北京': '北京市', '上海': '上海市', '广州': '广东省', '深圳': '广东省',
    '杭州': '浙江省', '成都': '四川省', '西安': '陕西省', '南京': '江苏省',
    '武汉': '湖北省', '长沙': '湖南省'
}
cities = list(cities_provinces.keys())

# hotel 表 level 字段为星级
levels = ['一星级', '二星级', '三星级', '四星级', '五星级']
level_weights = [5, 15, 30, 30, 20]
# 星级越高，评分基准越高，便于“按省份平均分上调0.5分”这类统计类操作体现差异
level_base_score = {'一星级': 3.4, '二星级': 3.7, '三星级': 4.0, '四星级': 4.3, '五星级': 4.6}

# 酒店名称的构词素材
areas = ['市中心', '火车站', '会展中心', '高新区', '老城区', '滨江路',
         '人民路', '步行街', '汽车站', '景区']
suffixes = ['大酒店', '国际酒店', '商务酒店', '精品酒店', '假日酒店',
            '宾馆', '酒店', '度假酒店', '温泉酒店', '公寓酒店']

# 评论人昵称素材
commentator_surnames = ['张', '王', '李', '赵', '陈', '刘', '杨', '黄', '周', '吴',
                        '徐', '孙', '马', '朱', '胡', '郭', '何', '高', '林', '罗']
commentator_nicks = ['旅行的猫', '爱睡懒觉', '出差达人', '小城故事', '一路向南',
                     '云端漫步', '背包客', '吃货日记', '周末去哪儿', '安静的树',
                     '南方姑娘', '北方汉子', '早起的鸟', '夜归人', '慢慢来',
                     '把酒言欢', '看海的人', '山路弯弯', '城市漫游者', '风吹麦浪']

# 评论内容（按评分区间区分好评、中评、差评），字段长度需满足 varchar(500)
positive_comments = [
    '位置很好，出行方便，房间干净整洁，服务态度也不错，下次还会再住。',
    '前台办理入住很快，房间隔音效果好，晚上休息得很踏实。',
    '性价比很高，早餐种类丰富，卫生做得到位，整体体验超出预期。',
    '酒店环境安静，设施比较新，离地铁站很近，适合出差和旅游。',
    '服务人员很热情，主动帮忙拿行李，房间采光好，住得很舒服。',
    '房间空间宽敞，床品干净，热水稳定，整体感觉满意。',
    '装修风格简洁大方，公共区域干净，周边餐饮选择多，很方便。',
    '入住体验不错，退房手续办理迅速，值得推荐给朋友。'
]
neutral_comments = [
    '整体中规中矩，位置还行，房间设施稍旧，价格合适的话可以考虑。',
    '服务态度一般，房间干净程度还可以，隔音效果有待提升。',
    '早餐比较简单，热水有时候不太稳定，其他方面问题不大。',
    '入住过程顺利，房间面积偏小，性价比一般般。',
    '设施有些老旧，但卫生做得还行，勉强可以接受。',
    '前台响应速度一般，房间空调声音略大，希望改进。'
]
negative_comments = [
    '房间卫生很差，床单上有污渍，前台态度冷淡，非常失望。',
    '隔音太差，一整晚都在听隔壁说话，根本没法休息。',
    '订的房间和实际入住的不一致，工作人员也没有给出合理解决。',
    '卫生间有异味，热水时冷时热，设施损坏也没人维修。',
    '退房时被多收了一笔费用，解释不清，体验极差。',
    '房间有很重的烟味，空调不制冷，投诉后无人处理。',
    '网上图片与实际差距太大，房间狭小潮湿，不建议入住。'
]


def generate_hotel_name(city, used_names):
    """生成不重复的酒店名称"""
    while True:
        name = f"{city}{random.choice(areas)}{random.choice(suffixes)}"
        if name not in used_names:
            used_names.add(name)
            return name


def generate_hotel_data():
    """
    生成 hotel 表的数据。
    字段：id、hotel_name、city、province、level、room_num、score、commnet_num
    """
    print("正在生成 hotel.csv 数据...")
    data = []
    used_names = set()

    for hotel_id in range(1, NUM_HOTELS + 1):
        city = random.choice(cities)
        province = cities_provinces[city]
        hotel_name = generate_hotel_name(city, used_names)

        level = random.choices(levels, weights=level_weights, k=1)[0]

        # 房间数 30-600 间
        room_num = random.randint(30, 600)

        # 评分以星级为基准上下浮动，保留一位小数，取值范围 2.5-5.0
        score = level_base_score[level] + random.uniform(-0.9, 0.4)
        score = round(min(5.0, max(2.5, score)), 1)

        # 评论数统一为 4 位数：commnet_num 在 hotel 表中为 varchar，
        # 位数一致可保证字符串比较结果与数值大小一致
        commnet_num = random.randint(1000, 9999)

        data.append({
            'id': hotel_id,
            'hotel_name': hotel_name,
            'city': city,
            'province': province,
            'level': level,
            'room_num': room_num,
            'score': score,
            'commnet_num': commnet_num
        })

    df = pd.DataFrame(data)
    df.to_csv('hotel.csv', index=False, encoding='utf-8-sig')
    print(f"hotel.csv 已生成，包含 {len(df)} 条记录。")
    return df


def generate_commentator_pool():
    """生成评论人昵称池"""
    pool = set()
    for surname in commentator_surnames:
        for nick in commentator_nicks:
            pool.add(f"{surname}{nick}")
    return sorted(pool)


def generate_comment_time():
    """生成 2024-01-01 至 2025-12-31 之间的评论时间"""
    start = datetime(2024, 1, 1)
    end = datetime(2025, 12, 31, 23, 59, 59)
    seconds = int((end - start).total_seconds())
    return (start + timedelta(seconds=random.randint(0, seconds))).strftime('%Y-%m-%d %H:%M:%S')


def build_comment(index, hotel_name, commentator, score):
    """按评分选择对应语气的评论内容，组装一条评论记录"""
    if score >= 4:
        content = random.choice(positive_comments)
    elif score == 3:
        content = random.choice(neutral_comments)
    else:
        content = random.choice(negative_comments)

    return {
        'id': index,
        'name': hotel_name,
        'commentator': commentator,
        'score': score,
        'comment_time': generate_comment_time(),
        'content': content
    }


def generate_comment_data(hotel_names_list):
    """
    生成 comment 表的数据。
    字段：id、name、commentator、score、comment_time、content
    其中 name 为酒店名称，取自 hotel 表，保证评论能对应到具体酒店。
    """
    print("正在生成 comment.csv 数据...")
    commentator_pool = generate_commentator_pool()

    # 指定一部分评论人专门发差评（每人 3-5 条、评分不超过 2 分），
    # 使“发表过 3 条及以上差评的评论人”这一统计有稳定的查询结果
    bad_reviewers = random.sample(commentator_pool, 8)
    data = []

    for commentator in bad_reviewers:
        count = random.randint(3, 5)
        for _ in range(count):
            data.append(build_comment(
                len(data) + 1,
                random.choice(hotel_names_list),
                commentator,
                random.choice([1, 2])
            ))

    # 其余评论按正常分布生成，评分越高越常见
    score_weights = [2, 5, 15, 38, 40]  # 对应 1-5 分
    while len(data) < NUM_COMMENTS:
        commentator = random.choice(commentator_pool)
        hotel_name = random.choice(hotel_names_list)
        score = random.choices([1, 2, 3, 4, 5], weights=score_weights, k=1)[0]
        data.append(build_comment(len(data) + 1, hotel_name, commentator, score))

    # 按评论时间重排 id，使评论编号与时间顺序一致
    data.sort(key=lambda row: row['comment_time'])
    for index, row in enumerate(data, start=1):
        row['id'] = index

    df = pd.DataFrame(data)
    df.to_csv('comment.csv', index=False, encoding='utf-8-sig')
    print(f"comment.csv 已生成，包含 {len(df)} 条记录。")

    # 统计差评（评分小于等于2分）达到3条及以上的评论人数量
    bad_count = df[df['score'] <= 2].groupby('commentator').size()
    bad_reviewer_num = int((bad_count >= 3).sum())
    print(f"其中发表过 3 条及以上差评的评论人共 {bad_reviewer_num} 名。")
    return df


if __name__ == "__main__":
    # 先生成 hotel 数据，comment 表的酒店名称从 hotel 表中选取
    hotel_df = generate_hotel_data()
    hotel_names = hotel_df['hotel_name'].tolist()

    # 基于酒店名称列表生成 comment 数据
    comment_df = generate_comment_data(hotel_names)

    print("\n数据生成完成！")
    print("- hotel.csv")
    print("- comment.csv")
