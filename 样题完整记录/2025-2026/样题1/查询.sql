use tree_statistics;

#统计每个区域的树木数量和平均树龄
select count(tree_id) as 树木数量,region as 所在区域, avg(age) as 平均年龄
from tree_info
group by region;

#查询高度高于该区域平均高度的树木信息
select t1.tree_id,t1.species,t1.region,t1.age,t1.height,t1.diameter,t1.health_status,t1.planting_date
from tree_info as t1
where t1.height > (
	select avg(t2.height) from tree_info as t2
	where t2.region = t1.region
);

#查询主要土壤类型为“壤土”的区域及其树木数量
select ri.region_name,count(tree_id) as 树木数量
from region_info as ri
join tree_info as ti
on ri.region_name = ti.region
where ri.soil_type = "壤土"
group by  ri.region_name;

#统计每种树种的最高高度和平均胸径，并按最高高度降序排列
select t.species,max(t.height) as 最高高度,avg(t.diameter) as 平均胸径
from tree_info as t
group by t.species
order by 最高高度 desc;

#查询最近一年内有生长记录的树木信息及其所在区域详情
select t.*,r.*,g.*
from growth_records as g
join tree_info as t
on t.tree_id = g.tree_id
join region_info as r
on r.region_name = t.region
where timestampdiff(year,t.planting_date,g.measure_date) <= 1;
