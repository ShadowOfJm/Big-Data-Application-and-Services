use house_market;
# 创建房源信息表
create table house_info(
    house_id int primary key,
    community varchar(100),
    district varchar(50),
    layout varchar(50),
    area decimal(10,2),
    price decimal(12,2),
    floor_info  varchar(50),
    orientation varchar(50),
    status enum('在售','出售') default '在售'
);

#创建小区信息表
create table community_info(
    community_id int primary key,
    community_name varchar(100),
    district varchar(50),
    build_year year,
    property_fee decimal(10,2),
    subway_distance int
);

#创建交易记录表
create table transaction_records(
    record_id int primary key,
    house_id int ,
    transaction_date date,
    transaction_price decimal(12,2) not null ,
    price_change decimal(12,2),
    transaction_type varchar(50) default '二手房',
    foreign key (house_id) references house_info(house_id)
);

