use hddb;

#查询最高气温超过 30 且天气为多云的所有记录
select *
from weather
where max_temp > 30
  and weather_condition = '多云';

#统计城市阿克苏最高气温超过 17 度的记录，并按照最高气温降序排列
select *
from weather
where city_name = '阿克苏'
  and max_temp > 17
order by max_temp desc;

#统计每个城市当日天气状况为多云的天数，并按照天数降序排列
select city_name as 城市,
       count(*) as 多云天数
from weather
where weather_condition = '多云'
group by city_name
order by 多云天数 desc;

#查询属于亚热带季风气候，最高气温大于 30 度且风力大于 2 级的城市名称和最高气温
select city_name as 城市名称,
       max_temp as 最高气温
from weather
where climate = '亚热带季风气候'
  and max_temp > 30
  and wind_level > 2;
