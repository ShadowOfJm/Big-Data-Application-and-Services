use bike_data;

create table ride_records(
    id int primary key ,
    bike_id varchar(6),
    user_id varchar(10),
    start_time datetime,
    end_time  datetime,
    start_location varchar(50),
    end_location varchar(50),
    ride_distance double,
    ride_duration int
);

create table bike_status(
    bike_id varchar(6) primary key ,
    status varchar(4),
    battery_level int,
    last_maintain_time datetime,
    current_location varchar(50),
    total_mileage double
);