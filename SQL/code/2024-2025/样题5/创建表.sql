use bigdata;

create table hotel(
    id int primary key,
    hotel_name varchar(100),
    city varchar(50),
    province varchar(50),
    level varchar(20),
    room_num int,
    score double,
    commnet_num varchar(50)
);

create table comment(
    id int primary key,
    name varchar(100),
    commentator varchar(50),
    score double,
    comment_time datetime,
    content varchar(500)
);
