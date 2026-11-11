use tree_statistics;

create table tree_info(
    tree_id int primary key,
    species varchar(100) not null,
	region varchar(50) not null,
	age int not null,
	height decimal(6,2) not null,
	diameter decimal(6,2),
	health_status enum('健康','一般','较差') default '健康',
	planting_date date
);

create table region_info(
    region_id int primary key,
    region_name varchar(50) not null,
    area_size decimal(10,2),
    soil_type varchar(50),
    manager varchar(100)
);

create table growth_records(
    record_id int primary key,
    tree_id int,
    measure_date date,
    new_height decimal(6,2),
    health_update enum('健康','一般','较差'),
    note varchar(200),
    foreign key (tree_id) references tree_info(tree_id)
);
