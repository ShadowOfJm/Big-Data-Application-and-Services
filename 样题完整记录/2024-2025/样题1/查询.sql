use house_market;

# 统计每个区域的在售房源数量和平均价格
select
    district,
    count(*) as 在售房源数量,
    avg(price) as 平均价格
from house_info
where status = '在售'
group by district;

# 查询成交价格高于该区域平均成交价格的房源信息
select hi.house_id,hi.community,hi.district,hi.layout,hi.area,hi.price,hi.floor_info,hi.orientation,hi.status
from house_info as hi
join transaction_records as tr
    on tr.house_id = hi.house_id
where tr.transaction_price > (
    select avg(tr2.transaction_price)
    from transaction_records as tr2
    join house_info as hi2
        on tr2.house_id = hi2.house_id
    where hi2.district = hi.district
);

# 查询距离地铁站1000米以内的小区及其房源数量
select ci.community_id,ci.community_name,ci.district,count(hi.house_id) as 房源数量
from community_info as ci
join house_info as hi
    on ci.community_name = hi.community
where ci.subway_distance <= 1000
group by ci.community_id,ci.community_name,ci.district;

# 统计每种户型的平均单价（按面积计算）并按降序排列
select avg(price / area) as 平均单价,layout
from house_info
group by layout
order by 平均单价 desc;

# 查询最近一个月内成交的房源信息及其所在小区详情
select ci.community_id,ci.community_name,ci.district,ci.build_year,ci.property_fee,ci.subway_distance
from transaction_records as tr
join house_info as hi
    on hi.house_id = tr.house_id
join community_info as ci
    on ci.community_name = hi.community
where tr.transaction_date >= subdate(curdate(), interval 1 month);
