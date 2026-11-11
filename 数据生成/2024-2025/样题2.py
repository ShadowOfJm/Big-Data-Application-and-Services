import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# 初始化 Faker 库，用于生成模拟数据
fake = Faker()
# 可以设置本地化以生成更符合特定地区习惯的名字等，例如 fake = Faker('zh_CN')

# 定义一些可能的值用于随机选择
course_names_base = [
    "Python基础", "数据结构入门", "Web开发实战", "机器学习原理",
    "Java核心技术", "数据库设计", "UI/UX设计", "项目管理",
    "市场营销", "财务分析", "英语口语", "历史探秘"
]
categories = ["编程", "数据科学", "设计", "商业", "语言", "兴趣"]
levels = ["入门", "初级", "中级", "高级"]
device_types = ["PC端", "移动端", "平板端"]

def generate_learning_data(num_records=1000):
    """
    生成模拟在线教育平台学习数据。
    :param num_records: 要生成的记录数量
    :return: 包含模拟数据的 Pandas DataFrame
    """
    data = []
    # 假设有一个用户池和课程池
    user_ids = [fake.unique.random_int(min=1000, max=9999) for _ in range(200)]  # 生成200个唯一用户ID
    course_ids = list(range(1, len(course_names_base) + 1))  # 课程ID 1-12

    for _ in range(num_records):
        user_id = random.choice(user_ids)
        course_id = random.choice(course_ids)
        course_name = course_names_base[course_id - 1]  # 根据ID获取课程名
        category = random.choice(categories)
        level = random.choice(levels)

        # 学习时长 (分钟)
        study_duration = random.randint(0, 240)  # 可能为0

        # 完成进度 (0-120%)，允许超过100%
        completion_progress = round(random.uniform(0, 120), 2)

        # 最后学习时间 (过去一年内) - 先生成标准格式
        last_study_time_dt = fake.date_time_between(start_date='-1y', end_date='now')
        # 格式化为标准字符串
        last_study_time_standard_str = last_study_time_dt.strftime('%Y-%m-%d %H:%M:%S')

        # 测验成绩 (可能异常 -10 到 110)
        quiz_score = round(random.uniform(-10, 110), 2)

        # 互动次数
        interaction_count = random.randint(0, 20)

        # 设备类型
        device_type = random.choice(device_types)

        # 学习时段 (根据最后学习时间确定)
        hour = last_study_time_dt.hour
        if 6 <= hour < 12:
            study_period = "上午"
        elif 12 <= hour < 18:
            study_period = "下午"
        elif 18 <= hour < 24:
            study_period = "晚上"
        else:  # 0-6点
            study_period = "凌晨"

        data.append({
            "用户ID": user_id,
            "课程ID": course_id,
            "课程名称": course_name,
            "课程类别": category,
            "学习时长(分钟)": study_duration,
            "完成进度": completion_progress,
            # 先存入标准格式的字符串，后续再修改
            "最后学习时间": last_study_time_standard_str,
            "测验成绩": quiz_score,
            "互动次数": interaction_count,
            "设备类型": device_type,
            "学习时段": study_period
        })

    # 创建 DataFrame
    df = pd.DataFrame(data)

    # 为了更贴近实际数据和任务要求，可以引入一些“问题”数据
    # 例如：随机将一些学习时长设为空(NaN)
    nan_indices = random.sample(range(len(df)), k=int(0.02 * len(df)))  # 随机2%为空
    df.loc[nan_indices, '学习时长(分钟)'] = None

    # --- 新增：生成格式不规范的最后学习时间 ---
    # 随机选择一小部分索引 (例如 5%)
    bad_format_indices = random.sample(range(len(df)), k=max(1, int(0.05 * len(df)))) # 至少生成1个

    for idx in bad_format_indices:
        # 生成几种常见的错误格式
        error_type = random.choice(['invalid_string', 'wrong_separator', 'invalid_date', 'random_chars'])

        if error_type == 'invalid_string':
            # 完全无效的字符串
            df.loc[idx, '最后学习时间'] = "Not a valid date"
        elif error_type == 'wrong_separator':
            # 错误的分隔符 (例如用 / 代替 -)
            # 获取原始标准时间字符串
            original_time_str = df.loc[idx, '最后学习时间']
            if pd.notna(original_time_str): # 确保原始时间不是 NaN
                 # 尝试解析标准格式并重新格式化为错误格式
                 try:
                     parsed_dt = datetime.strptime(original_time_str, '%Y-%m-%d %H:%M:%S')
                     df.loc[idx, '最后学习时间'] = parsed_dt.strftime('%Y/%m/%d %H:%M:%S') # 改成 /
                     # 或者更极端的错误
                     # df.loc[idx, '最后学习时间'] = f"{parsed_dt.year}/{parsed_dt.month+10}/{parsed_dt.day+20} {parsed_dt.hour}:{parsed_dt.minute}:{parsed_dt.second}"
                 except ValueError:
                     # 如果解析失败（理论上不应该），则用一个明显的错误格式
                     df.loc[idx, '最后学习时间'] = "2023/99/99 99:99:99"
            else:
                 df.loc[idx, '最后学习时间'] = "2023/01/01 12:00:00" # 如果原始是空，给个默认错误的
        elif error_type == 'invalid_date':
            # 日期本身无效 (例如 2月30日, 13月)
            df.loc[idx, '最后学习时间'] = "2024-02-30 15:00:00" # 2月没有30日
            # 或者 "2023-13-01 10:00:00" # 13月
        elif error_type == 'random_chars':
            # 随机字符
            df.loc[idx, '最后学习时间'] = fake.password(length=15, special_chars=False) # 生成随机字母数字组合

    return df

# --- 主执行部分 ---
if __name__ == "__main__":
    # 生成 1000 条模拟数据
    df_learning_data = generate_learning_data(1000)

    # 保存到 CSV 文件
    output_filename = "learning_data.csv"
    # index=False 表示不保存行索引
    # encoding='utf-8-sig' 在Windows上用Excel打开中文不乱码
    df_learning_data.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"已生成 {len(df_learning_data)} 条记录并保存到 '{output_filename}'")

    # 打印前10行以供检查 (对应任务要求)
    print("\n--- learning_data.csv 前10行 ---")
    print(df_learning_data.head(10))

