import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ==========================================
# 配置参数
# ==========================================
NUM_RECORDS = 2000  # 生成记录总数
OUTPUT_FILE = 'user_study_log.csv'

# 定义符合赛题业务场景的枚举值
COURSE_CATEGORIES = ['编程开发', '数据科学', '语言学习', '设计创意', '职场技能']
CONTENT_FORMS = ['视频', '图文', '直播', '互动课']
DEVICES = ['智能手机', '平板电脑', '桌面电脑', '网页端']
COURSE_NAMES = [
    'Python零基础入门', 'Java企业级开发', '前端Vue3实战', '数据分析与可视化',
    '雅思口语冲刺', '商务英语写作', 'UI/UX设计原理', 'Blender三维建模',
    'Excel高效办公', '项目管理PMP', '人工智能导论', '短视频运营实战'
]

print(f"正在生成 {NUM_RECORDS} 条在线教育平台学习行为模拟数据...")

# ==========================================
# 1. 生成基础合规数据
# ==========================================
np.random.seed(42)
random.seed(42)

data = {
    '学员ID': [f'U{str(i).zfill(5)}' for i in np.random.randint(1, 600, NUM_RECORDS)],
    '课程ID': [f'C{str(i).zfill(3)}' for i in np.random.randint(1, 50, NUM_RECORDS)],
    '课程名称': np.random.choice(COURSE_NAMES, NUM_RECORDS),
    '课程类别': np.random.choice(COURSE_CATEGORIES, NUM_RECORDS),
    '内容形式': np.random.choice(CONTENT_FORMS, NUM_RECORDS),
    '学习时长(分钟)': np.random.randint(10, 180, NUM_RECORDS),
    '章节完成率': np.round(np.random.uniform(0.05, 0.95, NUM_RECORDS), 2),
    '测试得分': np.random.randint(20, 95, NUM_RECORDS),
    '提问次数': np.random.randint(0, 8, NUM_RECORDS),
    '登录设备': np.random.choice(DEVICES, NUM_RECORDS),
    '学习时间段': np.random.randint(0, 24, NUM_RECORDS),
    # 生成最近60天内的日期，故意混用多种格式以测试清洗任务
    '最近学习日期': []
}

# 故意制造日期格式混乱 (YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY)
formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y']
for _ in range(NUM_RECORDS):
    dt = datetime.now() - timedelta(days=np.random.randint(0, 60))
    fmt = random.choice(formats)
    data['最近学习日期'].append(dt.strftime(fmt))

df = pd.DataFrame(data)

# ==========================================
# 2. 注入"脏数据" (对应清洗任务的5个步骤)
# ==========================================

# (1) 注入学习时长为空或<=5分钟的记录 (约3%)
mask_c1 = np.random.choice(df.index, size=int(NUM_RECORDS * 0.03), replace=False)
df.loc[mask_c1[:len(mask_c1)//2], '学习时长(分钟)'] = np.nan
df.loc[mask_c1[len(mask_c1)//2:], '学习时长(分钟)'] = np.random.randint(0, 5, len(mask_c1) - len(mask_c1)//2)

# (2) 注入测试得分超出[0,100]范围的记录 (约2%)
mask_c2 = np.random.choice(df.index, size=int(NUM_RECORDS * 0.02), replace=False)
df.loc[mask_c2[:len(mask_c2)//2], '测试得分'] = np.random.randint(-20, -1, len(mask_c2)//2)
df.loc[mask_c2[len(mask_c2)//2:], '测试得分'] = np.random.randint(101, 150, len(mask_c2) - len(mask_c2)//2)

# (4) 注入章节完成率异常 (>100% 或 <0%) 的记录 (约2%)
mask_c4 = np.random.choice(df.index, size=int(NUM_RECORDS * 0.02), replace=False)
df.loc[mask_c4[:len(mask_c4)//2], '章节完成率'] = np.round(np.random.uniform(1.01, 1.5, len(mask_c4)//2), 2)
df.loc[mask_c4[len(mask_c4)//2:], '章节完成率'] = np.round(np.random.uniform(-0.5, -0.01, len(mask_c4) - len(mask_c4)//2), 2)

# (5) 注入完全重复的记录 (约3%)
dup_indices = np.random.choice(df.index, size=int(NUM_RECORDS * 0.03), replace=False)
duplicates = df.loc[dup_indices].copy()
df = pd.concat([df, duplicates], ignore_index=True)

# 打乱顺序，使脏数据分布更真实
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# ==========================================
# 3. 导出CSV
# ==========================================
df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

print(f"✅ 数据生成完成！")
print(f"   文件路径: {OUTPUT_FILE}")
print(f"   总记录数: {len(df)}")
print(f"   包含字段: {list(df.columns)}")
print(f"\n📊 数据预览:")
print(df.head(10).to_string())
print(f"\n⚠️ 已注入的脏数据统计:")
print(f"   - 学习时长异常(空/≤5): ~{int(NUM_RECORDS * 0.03)} 条")
print(f"   - 测试得分越界(<0/>100): ~{int(NUM_RECORDS * 0.02)} 条")
print(f"   - 日期格式不统一: 全部({NUM_RECORDS}条)")
print(f"   - 章节完成率异常: ~{int(NUM_RECORDS * 0.02)} 条")
print(f"   - 完全重复记录: ~{int(NUM_RECORDS * 0.03)} 条")