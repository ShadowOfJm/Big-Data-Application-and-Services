import pandas as pd
import re
from dateutil import parser
#子任务一：用 pandas 读取 user_study_log.csv，并打印前 8 行（题目要求截图终端输出）
user_study_log = pd.read_csv("user_study_log.csv")
print(user_study_log.head(8))

#（1）删除“学习时长”为空值或小于等于 5 分钟的记录，保存为 cleaned_step1_N.csv，N 为删除的记录条数
#布尔条件：学习时长 <= 5，或学习时长为空（NaN），都判为无效记录
clean1 = (user_study_log["学习时长(分钟)"] <= 5)|(user_study_log["学习时长(分钟)"].isna())
#取反得到保留下来的正常记录
clean1_data = user_study_log[~clean1]
#N 就是被删掉的条数，直接写进文件名
N1 = clean1.sum()
filename1 = f"cleaned_step1_{N1}.csv"
clean1_data.to_csv(filename1,index=False)

#（2）将“测试得分”中小于 0 分的记录修正为 0 分、大于 100 分的记录修正为 100 分，保存为 cleaned_step2_N.csv
#N 是"修正"的条数，不是删除条数，这一步行数不变
clean2_copy = clean1_data.copy()
#分别统计低于 0 分和高出 100 分的条数，两者相加就是被修正的总条数
lower = clean2_copy["测试得分"] < 0
upper = clean2_copy["测试得分"] > 100
N2 = (lower.sum() + upper.sum())
#clip 一次性把越界值压回 [0, 100] 区间，等价于小于0改0、大于100改100
clean2_copy['测试得分'] = clean2_copy['测试得分'].clip(lower=0, upper=100)
clean2_data = clean2_copy
filename2 = f"cleaned_step2_{N2}.csv"
clean2_data.to_csv(filename2,index=False)

#（3）将“最近学习日期”列统一转换为 YYYY-MM-DD 格式，保存为 cleaned_step3_N.csv，N 为格式被修改的记录条数
clean3_copy = clean2_data.copy()

original_dates = clean3_copy['最近学习日期'].astype(str).copy()
#定义日期解析函数，统一把各种写法转换成 YYYY-MM-DD
#数据里实际存在三种写法：2026-09-22（本就是标准格式）、2026/09/22（斜杠）、20-08-2026（日-月-年）
#关键点：必须先用正则判断出原格式再分别处理，不能一律交给 dateutil 的 dayfirst=True，
#否则像 2026-10-05 这种已经是 YYYY-MM-DD 的标准值会被按"日-月-年"重新解释成 2026-05-10，把正确的日期改错
def safe_parse_date(date_str):
    #空值或空字符串直接返回 None
    if pd.isna(date_str) or str(date_str).strip() == '':
        return None
    s = str(date_str).strip()
    try:
        #情况一：本身就是 YYYY-MM-DD 标准格式，原样返回，不做任何改动
        if re.match(r'^\d{4}-\d{2}-\d{2}$', s):
            return s
        #情况二：2026/09/22 斜杠写法，把斜杠换成短横线即可
        if re.match(r'^\d{4}/\d{2}/\d{2}$', s):
            return s.replace('/', '-')
        #情况三：20-08-2026 是"日-月-年"，按位置重排成 年-月-日
        #依据：该格式第一段出现 13~31 的取值（共 415 条），说明第一段一定是"日"而不是"月"
        if re.match(r'^\d{2}-\d{2}-\d{4}$', s):
            d, m, y = s.split('-')
            return f"{y}-{m}-{d}"
        #其余少见写法兜底交给 dateutil 解析，再统一格式化
        parsed = parser.parse(s, dayfirst=True)
        return parsed.strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return None

#把转换函数逐行应用到“最近学习日期”列
clean3_copy['最近学习日期'] = clean3_copy['最近学习日期'].apply(safe_parse_date)

#统计格式被修改的记录条数 N：转换后非空，且与原始字符串不相等，就算被改过
mask_modified = (clean3_copy['最近学习日期'].notna()) & (clean3_copy['最近学习日期'] != original_dates)
N3 = int(mask_modified.sum())

#保存第三步清洗结果
filename3 = f'cleaned_step3_{N3}.csv'
clean3_copy.to_csv(filename3, index=False)


#（4）删除“章节完成率”大于 100%或小于 0%的异常记录，保存为 cleaned_step4_N.csv，N 为删除的记录条数
#章节完成率在数据里是 0~1 的小数（如 0.73 表示 73%），所以越界判断用 1 和 0
clean4_copy = clean3_copy.copy()
clean4 = (clean4_copy["章节完成率"] > 1) | (clean4_copy["章节完成率"] < 0)
clean4_data = clean4_copy[~clean4]
N4 = clean4.sum()
filename4 = f"cleaned_step4_{N4}.csv"
clean4_data.to_csv(filename4,index=False)


#（5）基于“学员ID”“课程ID”“最近学习日期”三列判断并删除完全重复的记录，保存为 cleaned_step5_N.csv，N 为删除的记录条数
clean5_copy = clean4_data.copy()
#先记下删除前的行数，删除后再算差值，差值就是 N
original = len(clean5_copy)
subset_cols = ["学员ID","课程ID","最近学习日期"]
#keep='first' 表示重复的记录只保留第一条
clean5_data = clean5_copy.drop_duplicates(subset_cols,keep='first')
N5 = original - len(clean5_data)
filename5 = f"cleaned_step5_{N5}.csv"
#这份 cleaned_step5_N.csv 是后续数据标注、数据分析、数据可视化的输入
clean5_data.to_csv(filename5,index=False)
