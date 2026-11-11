use tourism_analysis;

create table destination(
    dest_id int primary key auto_increment,
    dest_name varchar(100),
    country varchar(50),
    region varchar(50),
    dest_type varchar(30),
    avg_rating decimal(3,2),
    best_season varchar(50),
    estimated_cost decimal(10,2)
);

create table travel_record(
    record_id bigint primary key auto_increment,
    user_id varchar(50),
    dest_id int,
    travel_date date,
    travel_days int,
    total_expense decimal(10,2),
    transport_mode varchar(20),
    is_group_tour tinyint(1),
    satisfaction int,
    foreign key (dest_id) references destination(dest_id)
);
