import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(2026)
random.seed(2026)

n_samples = 300
order_ids = [f"ORD{str(i).zfill(6)}" for i in range(1, n_samples + 1)]
dates = [(datetime(2025, 1, 1) + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d") for _ in range(n_samples)]
age_groups = ["18-25岁", "26-35岁", "36-45岁", "46-55岁", "55岁以上"]
service_types = ["快车", "专车", "拼车", "豪华车"]
weather_pool = ["晴", "多云", "小雨", "大雨", "雪", "雾", None, "", "N/A"]  # 包含空值和无效值
road_pool = ["畅通", "缓行", "拥堵", "严重拥堵"]

# 生成基础数据
data = {
    "订单ID": order_ids,
    "日期": dates,
    "乘客年龄段": np.random.choice(age_groups, n_samples),
    "出行时长(小时)": np.round(np.random.uniform(0.3, 3.0, n_samples), 2),
    "订单金额(元)": np.round(np.random.uniform(15.0, 120.0, n_samples), 2),
    "服务评分": np.random.choice([1, 2, 3, 4, 5], n_samples),
    "出行方式": np.random.choice(service_types, n_samples),
    "天气状况": np.random.choice(weather_pool, n_samples, p=[0.25, 0.2, 0.15, 0.1, 0.05, 0.05, 0.08, 0.07, 0.05]),
    "道路状况": np.random.choice(road_pool, n_samples),
    "出行时段(小时)": np.round(np.random.uniform(0, 24, n_samples), 1)  # 标注任务必需字段
}

df = pd.DataFrame(data)

# ==================== 针对样题5清洗规则的精准脏数据注入 ====================

# 规则C1: 天气状况为空或无效值 (目标删除约20-30条)
invalid_weather_idx = random.sample(range(n_samples), 25)
for idx in invalid_weather_idx:
    df.loc[idx, "天气状况"] = random.choice([None, "", "N/A", "未知", "null"])

# 规则C2: 出行时长异常 (>12小时 或 <0.1小时) (目标删除约15-20条)
duration_outlier_idx = random.sample(list(set(range(n_samples)) - set(invalid_weather_idx)), 18)
for i, idx in enumerate(duration_outlier_idx):
    if i % 2 == 0:
        df.loc[idx, "出行时长(小时)"] = round(random.uniform(12.1, 24.0), 2)  # 超过12小时
    else:
        df.loc[idx, "出行时长(小时)"] = round(random.uniform(0.01, 0.09), 2)  # 小于0.1小时

# 规则C3: 出行方式为空 (目标修改约15-20条)
empty_service_idx = random.sample(list(set(range(n_samples)) - set(invalid_weather_idx) - set(duration_outlier_idx)), 18)
for idx in empty_service_idx:
    df.loc[idx, "出行方式"] = None

# 规则C4: 服务评分超出范围(1-5分) (目标删除约10-15条)
score_outlier_idx = random.sample(list(set(range(n_samples)) - set(invalid_weather_idx) - set(duration_outlier_idx)), 12)
for idx in score_outlier_idx:
    df.loc[idx, "服务评分"] = random.choice([0, -1, 6, 7, 10])

# 规则C5: 订单金额明显异常(超过该出行方式平均金额5倍) (目标删除约10条)
# 先计算各出行方式的基准均值，再注入极端值
mean_amounts = df.groupby("出行方式")["订单金额(元)"].mean().to_dict()
amount_outlier_candidates = list(set(range(n_samples)) - set(invalid_weather_idx) - set(duration_outlier_idx) - set(score_outlier_idx))
amount_outlier_idx = random.sample(amount_outlier_candidates, 10)
for idx in amount_outlier_idx:
    stype = df.loc[idx, "出行方式"]
    if pd.notna(stype) and stype in mean_amounts:
        df.loc[idx, "订单金额(元)"] = round(mean_amounts[stype] * random.uniform(5.5, 10.0), 2)

# 打乱顺序使脏数据分布自然
df = df.sample(frac=1, random_state=2026).reset_index(drop=True)

# 保存文件
output_path = "travel_order_data.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ 样题5专用数据集已生成: {output_path}")
print(f"📊 总记录数: {len(df)}")
print("\n前10行预览:")
print(df.head(10).to_string())