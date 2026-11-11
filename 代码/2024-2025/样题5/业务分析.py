import pandas as pd

#读取样例5清洗完成后的数据（c10 为最终结果）
data = pd.read_csv("cleaned_data_c10_0.csv")

#（1）平均房价：计算数据集中所有酒店的平均房价。
#题目要求的是"整体平均房价"，所以直接对房价列求均值
avg_price = data["房价"].mean()
print(f"所有酒店的平均房价: {avg_price:.2f}")
print("\n")


#（2）最受欢迎的房间类型：根据评价数量，确定哪种房间类型最受欢迎
#按房间类型汇总评价数，评价数总和越大说明越受欢迎，倒序排序
best_room = data.groupby("房间类型")["评价数"].sum().sort_values(ascending=False)
print(best_room)
#取出排名第一的房间类型及其评价数
print(f"最受欢迎的房间类型: {best_room.index[0]}，评价数合计: {best_room.iloc[0]}")
print("\n")

#（3）高评分酒店特征：识别评分在前25%的酒店共有的特征（如房价范围、位置等）
#先算每家酒店的综和评分（四项评分的平均），作为筛选高评分酒店的依据
data['评分'] = (data["卫生评分"] + data["服务评分"] + data["设施评分"] + data["位置评分"] ) / 4
#取评分的 75% 分位数作为门槛，达到该分值即属于前25%
top_25 = data["评分"].quantile(0.75)
h_top_25 = data[data['评分'] >= top_25]
print(h_top_25)
print("\n")
#高评分酒店的房价特征：了解它们的价位区间
if "房价" in h_top_25.columns:
    avg_price_1 = h_top_25["房价"].mean()
    print(f"平均房价: {avg_price_1:.2f}")
    range_price_min = h_top_25["房价"].min()
    range_price_max = h_top_25["房价"].max()
    print(f"房价范围: {range_price_min} - {range_price_max}")
#高评分酒店的装修时间特征：看它们的装修新旧
if "装修时间" in h_top_25.columns:
    range_zx_min = h_top_25["装修时间"].min()
    range_zx_max = h_top_25["装修时间"].max()
    print(f"装修时间范围: {range_zx_min} - {range_zx_max}")
#高评分酒店在各地区的房间类型情况
if "地区" in h_top_25.columns:
    a = h_top_25.groupby("地区")["房间类型"].max()
    print(a)
#高评分酒店所属公司的分布：按酒店数统计，找出占比最多和最少的公司
if "公司" in h_top_25.columns:
    gs_count = h_top_25["公司"].value_counts()
    gs_max = gs_count.index[0]
    gs_min = gs_count.index[-1]
    print(f"最多的所属公司:{gs_max}（{gs_count.iloc[0]}家）")
    print(f"最少的所属公司:{gs_min}（{gs_count.iloc[-1]}家）")
