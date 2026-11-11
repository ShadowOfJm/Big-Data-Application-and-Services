import pandas as pd

df = pd.read_csv('cleaned_tree_c5_7.csv')

#子任务一：价格区间标注
#题目要求：估值低于该区域平均估值的 70% 记低价值，70%~130% 记中价值，超过 130% 记高价值
#先按区域分组对估值求均值，得到一张"区域 -> 该区域平均估值"的对照表
region_avg = df.groupby('区域')['估值(元)'].mean()


# 3. 定义分类函数
def classify_value(row):
    val = row['估值(元)']
    avg = row['区域均值']

    if val < avg * 0.7:
        return '低价值'
    elif val <= avg * 1.3:
        return '中价值'
    else:
        return '高价值'



#把区域均值按区域名逐行匹配回原数据（原代码写成 df['区域均值'] = region_avg，
#Series 赋值是按索引对齐的，而 region_avg 的索引是区域名、df 的索引是 0~160，
#对不上会导致整列变成空值，于是所有记录都被判成"高价值"，这里改用 map 按区域名取值）
df['区域均值'] = df['区域'].map(region_avg)
df['价值区间'] = df.apply(classify_value,axis=1)

df = df.drop(columns=['区域均值'])
#题目给出的格式表只有 编号、地块名称、胸径(cm)、估值(元)、价值区间 五列，
#原来直接 to_csv 会把 10 个原始列全部输出、也没有编号列，这里补一列从 1 开始的编号，
#再按题目规定的五列顺序输出
df["编号"] = range(1, len(df)+1)
out1 = ["编号", "地块名称", "胸径(cm)", "估值(元)", "价值区间"]
df[out1].to_csv('value_range_mark.csv', index=False)

#子任务二：区域丰富度标注
#题目要求按"区域内树木记录数量"与"全市平均数量"比较来标注五个区域的物种丰富度：
#高丰富度 > 全市平均的 120%；中丰富度在 80%~120% 之间；低丰富度 < 全市平均的 80%
#先用 value_counts 统计每个区域的树木记录条数
area_count = df['区域'].value_counts()
#全市平均数量 = 各区域记录条数的平均值（5 个区域共 161 条，平均 32.2 条）
area_avg = area_count.mean()


#按记录条数与全市平均的倍数关系判定丰富度等级
def classify_richness(count):
    if count > area_avg * 1.2:
        return '高丰富度'
    elif count >= area_avg * 0.8:
        return '中丰富度'
    else:
        return '低丰富度'


#把每个区域先判成一个等级，做成"区域 -> 丰富度"的对照表，再按区域名贴回每一条记录
area_label = {a: classify_richness(b) for a, b in area_count.items()}
df['区域丰富度'] = df['区域'].map(area_label)

#题目给出的格式表为 编号、地块名称、区域、胸径(cm)、估值(元)、区域丰富度 六列，按此顺序输出
out2 = ["编号", "地块名称", "区域", "胸径(cm)", "估值(元)", "区域丰富度"]
df[out2].to_csv('area_richness_mark.csv', index=False)
