use hddb;

create table new_weather(
    id int primary key auto_increment comment '城市ID',
    province_id int not null comment '省份ID',
    city_name varchar(255) not null comment '城市名称',
    zip_code int comment '邮编',
    levels int comment '城市等级',
    climate varchar(255) comment '气候条件'
);

create table weather(
    id int primary key,
    city_id int,
    city_name varchar(255),
    climate varchar(255),
    weather_condition varchar(50),
    max_temp double,
    wind_level int,
    weather_date date
);
