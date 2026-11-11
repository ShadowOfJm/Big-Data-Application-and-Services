use bike_data;

# 在 ride_records 表中查询骑行时长超过60分钟的记录数量
select count(*) as 骑行超时记录数
from ride_records
where ride_duration > 60;

# 在 bike_status 表中统计各个状态的单车数量
select status,count(bike_id) as 单车数量
from bike_status
group by status;
