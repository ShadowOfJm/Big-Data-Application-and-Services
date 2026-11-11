import pandas as pd
import numpy as np
import random

# --- 配置参数 ---
num_records = 5000

# 定义基础数据池
scenic_spots = ['西湖', '故宫', '长城', '黄山', '九寨沟', '张家界', '桂林山水', '鼓浪屿', '三亚', '丽江古城']
origins = ['北京', '上海', '广州', '深圳', '成都', '杭州', '西安', '南京', '武汉', '重庆', '天津', '青岛', '大连', '厦门', '昆明', '', '未知']
# 为前15个城市/地区设定一个基础概率
base_probs = [0.06, 0.08, 0.07, 0.06, 0.07, 0.08, 0.07, 0.05, 0.05, 0.05, 0.03, 0.03, 0.02, 0.03, 0.02]
# 计算剩余概率 (给空值''和'未知')
remaining_prob = 1.0 - sum(base_probs)
# 将剩余概率平均分配给空值和'未知'
# 或者可以自定义分配，比如空值占0.08，未知占0.04
prob_for_empty = 0.08
prob_for_unknown = remaining_prob - prob_for_empty
origins_probs = base_probs + [prob_for_empty, prob_for_unknown]

age_groups = ['18-25', '26-35', '36-45', '46-55', '55+']
transportations = ['自驾', '高铁/火车', '飞机', '大巴', '骑行/徒步']
weathers = ['晴', '多云', '阴', '小雨', '中雨', '大雨', '雪', '雾']

# --- 关键：再次验证概率总和 ---
# 使用 assert 确保万无一失
assert len(origins) == len(origins_probs), "Origins list and probabilities list must have the same length."
assert abs(sum(origins_probs) - 1.0) < 1e-9, f"Origins probabilities do not sum to 1: {sum(origins_probs):.10f}"

# --- 生成基础数据 ---
data = {
    '景区名称': np.random.choice(scenic_spots, size=num_records),
    '日期': pd.date_range(start='2024-01-01', end='2024-12-31', freq='D').to_series().sample(n=num_records, replace=True).reset_index(drop=True).dt.strftime('%Y-%m-%d'),
    '游客来源地': np.random.choice(origins, size=num_records, p=origins_probs),
    '游客年龄段': np.random.choice(age_groups, size=num_records),
    '停留时长（小时）': np.round(np.random.lognormal(mean=1.5, sigma=0.8, size=num_records), 2),
    '消费金额（元）': np.round(np.random.lognormal(mean=6, sigma=1, size=num_records), 2),
    '满意度评分': np.round(np.random.uniform(0, 6, size=num_records), 1),
    '出行方式': np.random.choice(transportations, size=num_records),
    '天气状况': np.random.choice(weathers + [''], size=num_records, p=[0.12, 0.15, 0.15, 0.12, 0.08, 0.05, 0.03, 0.02, 0.28])
}

# 验证天气概率总和
weather_probs = [0.12, 0.15, 0.15, 0.12, 0.08, 0.05, 0.03, 0.02, 0.28]
assert abs(sum(weather_probs) - 1.0) < 1e-9, f"Weather probabilities do not sum to 1: {sum(weather_probs):.10f}"

df = pd.DataFrame(data)

# --- 添加特定的异常值以供清洗 ---
# 1. 异常停留时长 (超过24小时或小于0.1小时)
num_abnormal_stay = int(num_records * 0.02)
abnormal_stay_indices = np.random.choice(df.index, size=num_abnormal_stay, replace=False)
for idx in abnormal_stay_indices:
     if random.random() > 0.5:
         df.loc[idx, '停留时长（小时）'] = round(random.uniform(24.1, 48), 2)
     else:
         df.loc[idx, '停留时长（小时）'] = round(random.uniform(0, 0.09), 2)

# 2. 超出范围的满意度评分 (>5)
num_abnormal_satisfaction = int(num_records * 0.01)
abnormal_satisfaction_indices = np.random.choice(df.index, size=num_abnormal_satisfaction, replace=False)
df.loc[abnormal_satisfaction_indices, '满意度评分'] = np.round(np.random.uniform(5.1, 7, size=num_abnormal_satisfaction), 1)

# 3. 异常高的消费金额
global_avg_spending = df['消费金额（元）'].mean()
num_extreme_spending = int(num_records * 0.005)
extreme_spending_indices = np.random.choice(df.index, size=num_extreme_spending, replace=False)
df.loc[extreme_spending_indices, '消费金额（元）'] = np.round(np.random.uniform(global_avg_spending * 6, global_avg_spending * 20, size=num_extreme_spending), 2)

# --- 保存到 CSV ---
filename = 'tourist_data.csv'
df.to_csv(filename, index=False, encoding='utf-8-sig')

print(f"已生成包含 {num_records} 条记录的 '{filename}' 文件。")
print("该文件已包含用于后续数据清洗任务的模拟异常数据。")

# --- 可选：打印前10行以供检查 ---
print("\n生成的 CSV 文件前10行内容预览:")
print(df.head(10))
