import pandas as pd
data = pd.read_csv("cleaned_data_c5_3.csv")
# 1.价格区间标注
def avg_price(group):
    avg = group["价格(万元)"].mean()

    def price_range_mark(mark):
        if mark["价格(万元)"] < avg * 0.7:
            return "经济型"
        elif avg * 0.7 < mark["价格(万元)"] < avg * 1.3:
            return "中档型"
        elif mark["价格(万元)"] > avg * 1.3:
            return "高端型"

    group.loc[:,"价格区间"] = group.apply(price_range_mark,axis=1)
    return group

data = data.groupby("市区").apply(avg_price)
data.to_csv("price_range_mark.csv",index=False)

#2.市区热门度标注
#计算每个市区的房源数量
area_counts = data['市区'].value_counts()
#计算全市平均房源数量
avg_area = area_counts.mean()
def area_mark(area):
    # 每个市区的数量
    count = area_counts[area]
    if count < avg_area * 0.8:
        return "低热门"
    elif avg_area * 0.8 < count < avg_area * 1.2:
        return "中热门"
    elif count > avg_area * 1.2:
        return "高热门"
# 使用map函数将'市区'列映射到'区域热门度'列
data['区域热门度'] = data['市区'].map(area_mark)
data.to_csv("area_popularity_mark.csv",index=False)