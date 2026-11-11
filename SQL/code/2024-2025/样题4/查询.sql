use tourism;

# 查询2024年1月每个景区的总游客人数。查询结果需要显示景区名称、所在城市和游客总数，并按游客总数降序排列
select s.spot_name,s.city,sum(v.visitor_count) as 游客总数
from scenic_spot as s
join visitor_flow as v
    on s.spot_id = v.spot_id
where v.visit_date between '2024-01-01' and '2024-01-31'
group by s.spot_id,s.spot_name,s.city
order by 游客总数 desc;

# 统计每个景区在节假日和非节假日的平均游客数量。查询结果需要显示景区名称、景区等级、节假日平均游客数和非节假日平均游客数，按景区编号排序
select s.spot_id,s.spot_name,s.level,
    avg(case when v.is_holiday = 1 then v.visitor_count end) as 节假日平均游客数,
    avg(case when v.is_holiday = 0 then v.visitor_count end) as 非节假日平均游客数
from scenic_spot as s
join visitor_flow as v
    on s.spot_id = v.spot_id
group by s.spot_id,s.spot_name,s.level
order by s.spot_id;

# 找出所有景区中单日游客量超过该景区最大承载量的情况。查询结果需要显示景区名称、参观日期、实际游客数量、最大承载量和超出人数，按超出人数降序排列
select s.spot_name,v.visit_date,v.visitor_count as 实际游客数量,s.max_capacity as 最大承载量,
    v.visitor_count - s.max_capacity as 超出人数
from scenic_spot as s
join visitor_flow as v
    on s.spot_id = v.spot_id
where v.visitor_count > s.max_capacity
order by 超出人数 desc;
