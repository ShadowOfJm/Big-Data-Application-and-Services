import pandas as pd
data = pd.read_csv("cleaned_data_c10_0.csv")
data_1 = data.copy()
#1. 子任务一：酒店价格区间标注
def hotel_price_level(a):
    if a["房价"] <= 300:
        return "经济型"
    elif 301< a["房价"] <= 800:
        return "中端型"
    elif a["房价"] > 801:
        return "高端型"
out = ["酒店名称","地区","房价"]
data_1 = data_1[out]
data_1.loc[:,"价格类型"] = data_1.apply(hotel_price_level,axis=1)
data_1.to_csv("hotel_price_level.csv",index=False)


#2. 子任务二：酒店服务质量标注
data_2 = data.copy()
data_2['服务质量得分'] = (data_2["服务评分"]+data_2["卫生评分"]/2).round(2)
def hotel_service_level(b):
    #计算服务质量得分
    if b >= 4.5 :
        return"优质服务"
    elif 4.0 <= b <=4.4:
        return"良好服务"
    elif 3.5 <= b <= 3.9:
        return "标准服务"
    elif b < 3.5:
        return"需改进服务"
data_2["服务等级"] = data_2["服务质量得分"].apply(hotel_service_level)
out_1 = ["酒店名称","服务评分","卫生评分","服务质量得分","服务等级"]
data_2 = data_2[out_1]
data_2.to_csv("hotel_service_level.csv",index=False)
