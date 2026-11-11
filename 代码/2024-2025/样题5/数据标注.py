import pandas as pd
#读取样例5清洗完成后的数据（c10 为最终结果）
data = pd.read_csv("cleaned_data_c10_0.csv")

#1. 子任务一：酒店价格区间标注
data_1 = data.copy()

#按房价高低把酒店分成经济型/中端型/高端型
def hotel_price_level(a):
    #300元及以下为经济型
    if a["房价"] <= 300:
        return "经济型"
    #301~800元为中端型（用 <=800 兜住边界，避免 800~801 之间漏标）
    elif a["房价"] <= 800:
        return "中端型"
    #800元以上为高端型
    else:
        return "高端型"

#只保留酒店名称、地区、房价三列作为标注结果
out = ["酒店名称","地区","房价"]
#用 .copy() 显式复制，避免切片后赋值报警告
data_1 = data_1[out].copy()
#逐行判断价格区间，写入新列"价格类型"
data_1.loc[:,"价格类型"] = data_1.apply(hotel_price_level,axis=1)
#输出价格区间标注结果，文件名按题目要求
data_1.to_csv("hotel_price_level.csv",index=False)


#2. 子任务二：酒店服务质量标注
data_2 = data.copy()
#计算服务质量得分：服务评分与卫生评分的平均值（注意必须加括号，
#原写法 服务评分 + 卫生评分/2 会先算除法，得分区间变成 1.5~7.5，和 4.5/4.0/3.5 的分档标准对不上）
data_2['服务质量得分'] = ((data_2["服务评分"] + data_2["卫生评分"]) / 2).round(2)

#根据服务质量得分划分服务等级
def hotel_service_level(b):
    #4.5分及以上为优质服务
    if b >= 4.5 :
        return"优质服务"
    #4.0~4.49分为良好服务
    elif 4.0 <= b < 4.5:
        return"良好服务"
    #3.5~3.99分为标准服务
    elif 3.5 <= b < 4.0:
        return "标准服务"
    #3.5分以下为需改进服务
    elif b < 3.5:
        return"需改进服务"

#逐行按得分打上服务等级
data_2["服务等级"] = data_2["服务质量得分"].apply(hotel_service_level)
#只保留输出需要的列
out_1 = ["酒店名称","服务评分","卫生评分","服务质量得分","服务等级"]
data_2 = data_2[out_1]
#输出服务质量标注结果，文件名按题目要求
data_2.to_csv("hotel_service_level.csv",index=False)
