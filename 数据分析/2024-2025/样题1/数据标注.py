import pandas as pd

data = pd.read_csv("cleaned_data_c5_3.csv")

#1.子任务一：价格区间标注
#按每个市区自己的平均售价把该市区的房源分成"经济型/中档型/高端型"
#用 transform 把每个市区的平均售价广播回每一行，避免 groupby().apply() 在新版 pandas 里
#丢掉分组键、造成"市区"列错位成 NaN 的问题
city_avg = data.groupby("市区")["价格(万元)"].transform("mean")


def price_range_mark(row):
    #低于均价的70%记为经济型
    if row["价格(万元)"] < row["市区均价"] * 0.7:
        return "经济型"
    #高于均价的130%记为高端型
    elif row["价格(万元)"] > row["市区均价"] * 1.3:
        return "高端型"
    #均价的70%~130%之间（��边界）都记为中档型
    else:
        return "中档型"


#把每个市区的平均售价作为临时列"市区均价"参与逐行判断
data["市区均价"] = city_avg
#按题目要求新增一列"价格区间"（apply(axis=1) 表示逐行处理）
data.loc[:, "价格区间"] = data.apply(price_range_mark, axis=1)
#临时列用完即删，保持输出文件干净
data = data.drop(columns=["市区均价"])
#按题目要求的列顺序整理，并给每条记录加上从1开始的编号
data.insert(0, "编号", range(1, len(data) + 1))
#输出价格区间标注结果，文件名按题目要求
data.to_csv("price_range_mark.csv", index=False)


#2.子任务二：市区热门度标注
#计算每个市区的房源数量
area_counts = data["市区"].value_counts()
#计算全市平均房源数量，作为判断热门度的基准
avg_area = area_counts.mean()


def area_mark(area):
    # 每个市区的数量
    count = area_counts[area]
    #低于平均数量的80%为低热门
    if count < avg_area * 0.8:
        return "低热门"
    #高于平均数量的120%为高热门
    elif count > avg_area * 1.2:
        return "高热门"
    #平均数量的80%~120%之间记为中热门
    else:
        return "中热门"


# 使用map函数将'市区'列映射到'区域热门度'列
data["区域热门度"] = data["市区"].map(area_mark)
#输出热门度标注结果，文件名按题目要求
data.to_csv("area_popularity_mark.csv", index=False)
