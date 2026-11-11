import pandas as pd
import random
from datetime import date, timedelta

# 设置随机种子以确保结果可重现
random.seed(42)

# =================配置参数=================
NUM_COURSES = 30          # 课程信息表记录数
NUM_BEHAVIORS = 2000      # 学习行为表记录数
# =========================================

# course 表 subject 字段：所属学科
SUBJECTS = ['编程', '数学', '语言', '设计', '物理', '英语']

# difficulty 字段：难度级别枚举值
DIFFICULTIES = ['初级', '中级', '高级']

# 各学科下可用的课程名称词干
COURSE_TOPICS = {
    '编程': ['Python', 'Java', 'C++', 'Web 前端', '数据结构', '算法设计', 'Go 语言'],
    '数学': ['高等数学', '线性代数', '概率论', '离散数学', '数理统计'],
    '语言': ['普通话', '日语', '韩语', '德语', '法语'],
    '设计': ['UI 设计', '平面设计', '三维建模', '交互设计'],
    '物理': ['大学物理', '力学', '电磁学', '热力学'],
    '英语': ['英语语法', '英语口语', '雅思写作', '商务英语']
}

TEACHERS = ['张伟', '王芳', '李强', '刘洋', '陈静', '杨帆',
            '赵敏', '周涛', '吴磊', '徐丽', '孙鹏', '朱婷']

# 登录设备与学习时间段（用于学习行为表的真实感，非建表字段）
DEVICES = ['手机', '平板', '电脑']
TIME_SLOTS = ['上午', '下午', '晚上']


def generate_course_data():
    """
    生成 course 表的数据。
    字段：course_id、title、subject、difficulty、total_lessons、original_price、
          current_price、teacher_name、publish_date、total_students、avg_review_score
    """
    print("正在生成 course.csv 数据...")
    data = []

    # 主讲教师按轮转分配，保证每位教师名下至少有一门课程，
    # 使“每位主讲教师名下所有课程的总学习人次”这一查询不会漏掉教师
    teacher_cycle = TEACHERS[:]
    random.shuffle(teacher_cycle)

    for course_id in range(1, NUM_COURSES + 1):
        subject = random.choice(SUBJECTS)
        topic = random.choice(COURSE_TOPICS[subject])
        difficulty = random.choice(DIFFICULTIES)
        title = f"{topic}{difficulty}课程"

        total_lessons = random.randint(10, 120)

        # 原价与现价：现价不超过原价
        original_price = round(random.uniform(199, 2999), 2)
        current_price = round(original_price * random.uniform(0.5, 1.0), 2)

        teacher_name = teacher_cycle[(course_id - 1) % len(teacher_cycle)]
        # 上架日期在 2023-01-01 至 2025-12-31 之间
        publish_date = date(2023, 1, 1) + timedelta(days=random.randint(0, 1094))

        total_students = random.randint(50, 20000)

        # 平均好评率范围 0.0-5.0
        avg_review_score = round(random.uniform(2.5, 5.0), 1)

        data.append({
            'course_id': course_id,
            'title': title,
            'subject': subject,
            'difficulty': difficulty,
            'total_lessons': total_lessons,
            'original_price': original_price,
            'current_price': current_price,
            'teacher_name': teacher_name,
            'publish_date': publish_date,
            'total_students': total_students,
            'avg_review_score': avg_review_score
        })

    df = pd.DataFrame(data)
    df.to_csv('course.csv', index=False, encoding='utf-8-sig')
    print(f"course.csv 已生成，包含 {len(df)} 条记录。")
    return df


def generate_study_behavior_data(course_df):
    """
    生成 study_behavior 表的数据。
    字段：record_id、user_id、course_id、access_date、daily_study_minutes、
          finished_lessons、assignment_score、is_joined_discussion、note_count
    course_id 取自 course 表，保证外键有效。
    """
    print("正在生成 study_behavior.csv 数据...")
    course_ids = course_df['course_id'].tolist()
    lesson_map = dict(zip(course_df['course_id'], course_df['total_lessons']))

    data = []
    for record_id in range(1, NUM_BEHAVIORS + 1):
        course_id = random.choice(course_ids)
        user_id = random.randint(1, 500)

        # 学习日期在 2024-01-01 至 2025-12-31 之间
        access_date = date(2024, 1, 1) + timedelta(days=random.randint(0, 730))

        # 当日学习时长 5-180 分钟；作业得分 0-100；笔记条数 0-20
        daily_study_minutes = random.randint(5, 180)
        finished_lessons = random.randint(0, min(10, lesson_map[course_id]))
        assignment_score = round(random.uniform(0, 100), 1)
        is_joined_discussion = random.choices([1, 0], weights=[45, 55], k=1)[0]
        note_count = random.randint(0, 20)

        data.append({
            'record_id': record_id,
            'user_id': user_id,
            'course_id': course_id,
            'access_date': access_date,
            'daily_study_minutes': daily_study_minutes,
            'finished_lessons': finished_lessons,
            'assignment_score': assignment_score,
            'is_joined_discussion': is_joined_discussion,
            'note_count': note_count
        })

    df = pd.DataFrame(data)
    df.to_csv('study_behavior.csv', index=False, encoding='utf-8-sig')
    print(f"study_behavior.csv 已生成，包含 {len(df)} 条记录。")
    return df


if __name__ == "__main__":
    # 先生成课程数据，学习行为表的 course_id 取自课程表
    course_df = generate_course_data()
    study_behavior_df = generate_study_behavior_data(course_df)

    print("\n数据生成完成！")
    print("- course.csv")
    print("- study_behavior.csv")
