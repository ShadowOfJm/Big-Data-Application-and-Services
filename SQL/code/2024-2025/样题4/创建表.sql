use tourism;

create table scenic_spot(
    spot_id int primary key,
    spot_name varchar(20),
    city varchar(6),
    level varchar(5),
    type varchar(6),
    ticket_price decimal,
    opening_hours varchar(10),
    max_capacity int
);

create table visitor_flow(
    record_id int primary key,
    spot_id int,
    visit_date date,
    visitor_count int,
    peak_hour time,
    weather varchar(10),
    is_holiday boolean,
    foreign key (spot_id) references scenic_spot(spot_id)
);