use hddb;

#向天气表中插入三亚、上海、乌鲁木齐三条记录
insert into new_weather(province_id,city_name,zip_code,levels,climate)
values (1016,'三亚',572000,2,'热带海洋性季风气候');

insert into new_weather(province_id,city_name,zip_code,levels,climate)
values (1026,'上海',200000,1,'亚热带季风气候');

insert into new_weather(province_id,city_name,zip_code,levels,climate)
values (1032,'乌鲁木齐',830000,2,'中温带半干旱大陆性气候');

#查看天气表的全部记录
select * from new_weather;

#为天气表添加气候介绍字段 comment，并查询天气表的结构
alter table new_weather add column comment varchar(255);
desc new_weather;
