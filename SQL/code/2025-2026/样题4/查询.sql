use tourism_analysis;

#查询 2024 年各季度（Q1:1-3月, Q2:4-6月, Q3:7-9月, Q4:10-12月）的出行总人次和人均花费
select quarter(r.travel_date) as 季度,
       count(*) as 出行总人次,
       round(sum(r.total_expense) / count(*), 2) as 人均花费
from travel_record as r
where year(r.travel_date) = 2024
group by quarter(r.travel_date)
order by 季度;

#统计不同“目的地类型”在跟团游和自由行中的占比
select d.dest_type as 目的地类型,
       sum(case when r.is_group_tour = 1 then 1 else 0 end) as 跟团游次数,
       sum(case when r.is_group_tour = 0 then 1 else 0 end) as 自由行次数,
       round(sum(case when r.is_group_tour = 1 then 1 else 0 end) / count(*) * 100, 1) as 跟团游占比
from travel_record as r
join destination as d
on r.dest_id = d.dest_id
group by d.dest_type
order by 跟团游次数 desc;

#找出“人均预估费用”低于实际“人均花费”20%以上的目的地
select d.dest_name as 目的地名称,
       d.country as 所在国家,
       d.estimated_cost as 预估人均费用,
       round(sum(r.total_expense) / count(*), 2) as 实际人均花费,
       round(sum(r.total_expense) / count(*) - d.estimated_cost, 2) as 差值
from travel_record as r
join destination as d
on r.dest_id = d.dest_id
group by d.dest_id, d.dest_name, d.country, d.estimated_cost
having 实际人均花费 > d.estimated_cost * 1.2
order by 差值 desc;
