import pandas as pd
import random
import numpy as np


def generate_tree_survey_data(filename='tree_survey.csv', num_rows=200):
    """
    生成模拟的城市树木调查数据 tree_survey.csv
    """

    # 1. 定义基础数据字典
    regions = ['南山区', '福田区', '罗湖区', '宝安区', '龙岗区']
    plots = ['中央公园', '滨河绿地', '市民广场', '中山公园', '莲花山公园', '东湖公园', '梧桐山风景区', '深圳湾公园']

    # 树种：包含一些需要标准化的非标准名称，用于测试清洗任务
    tree_species_raw = [
        '香樟', '二球悬铃木', '法桐', '悬铃木', '大王椰子', '小叶榕', '高山榕',
        '桃花心木', '秋枫', '盆架子', '木棉', '荷花玉兰', '广玉兰'
    ]

    growth_status = ['健康', '一般', '较差']
    age_groups = ['幼龄', '中龄', '成熟', '老龄']
    maintenance = ['定期养护', '偶尔养护', '无人养护', '近期修剪']
    is_ancient = ['是', '否']
    years = [2023, 2024, 2025]

    data = []

    for i in range(1, num_rows + 1):
        region = random.choice(regions)
        plot = f"{region}-{random.choice(plots)}"

        # 随机选择树种
        species = random.choice(tree_species_raw)

        status = random.choice(growth_status)
        age = random.choice(age_groups)
        maintain = random.choice(maintenance)
        ancient = random.choice(is_ancient)
        year = random.choice(years)

        # 生成胸径 (cm)，大部分在 20-100 之间，少量异常
        if random.random() < 0.05:
            diameter = 0  # 异常值：胸径为0，用于清洗任务1
        elif random.random() < 0.05:
            diameter = round(random.uniform(5, 19), 2)  # 较小树木，用于清洗任务5
        else:
            diameter = round(random.uniform(20, 120), 2)

        # 生成估值 (元)，通常与胸径正相关，但加入随机性
        # 基准估值：胸径 * 50 + 随机波动
        base_value = diameter * 50 + random.randint(-500, 500)
        if base_value < 0: base_value = 100

        # 制造一些极端高估值，用于清洗任务2
        if random.random() < 0.03:
            value = base_value * 4  # 超过平均值3倍
        else:
            value = int(base_value)

        # 制造缺失值 (NaN)
        if random.random() < 0.02:
            diameter = np.nan
        if random.random() < 0.02:
            value = np.nan
        if random.random() < 0.02:
            ancient = ''  # 空字符串，用于清洗任务4

        data.append({
            '区域': region,
            '地块名称': plot,
            '树种': species,
            '生长状况': status,
            '树龄段': age,
            '养护情况': maintain,
            '是否古树名木': ancient,
            '胸径(cm)': diameter,
            '估值(元)': value,
            '调查年份': year
        })

    # 创建 DataFrame
    df = pd.DataFrame(data)

    # 保存为 CSV
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"成功生成文件: {filename}")
    print(f"数据行数: {len(df)}")
    print("-" * 30)
    print("前10行数据预览:")
    print(df.head(10))


if __name__ == '__main__':
    generate_tree_survey_data()