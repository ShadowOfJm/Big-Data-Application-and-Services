import pandas as pd

data = pd.read_csv("cleaned_data_c10_0.csv")

#平均房价：计算数据集中所有酒店的平均房价。
avg_price = data.groupby("酒店名称")["房价"].mean()
print(avg_price)
print("\n")


#最受欢迎的房间类型：根据评价数量，确定哪种房间类型最受欢迎
best_room = data.groupby("房间类型")["评价数"].sum().sort_values(ascending=False)
print(best_room)
print("\n")
#高评分酒店特征：识别评分在前25%的酒店共有的特征（如房价范围、位置等）
data['评分'] = (data["卫生评分"] + data["服务评分"] + data["设施评分"] + data["位置评分"] ) / 4
top_25 = data["评分"].quantile(0.75)
h_top_25 = data[data['评分'] >= top_25]
print(h_top_25)
if "房价" in h_top_25.columns:
    avg_price_1 = h_top_25["房价"].mean()
    print(f"平均房价: {avg_price_1:.2f}")
    range_price_min = h_top_25["房价"].min()
    range_price_max = h_top_25["房价"].max()
    print(f"房价范围: {range_price_min} - {range_price_max}")
if "装修时间" in h_top_25.columns:
    range_zx_min = h_top_25["装修时间"].min()
    range_zx_max = h_top_25["装修时间"].max()
    print(f"装修时间范围: {range_zx_min} - {range_zx_max}")
if "地区" in h_top_25.columns:
    a = h_top_25.groupby("地区")["房间类型"].max()
    print(a)
if "公司" in h_top_25.columns:
    gs_max = h_top_25["公司"].max()
    gs_min = h_top_25["公司"].min()
    print(f"最多的所属公司:{gs_max}")
    print(f"最少的所属公司:{gs_min}")
