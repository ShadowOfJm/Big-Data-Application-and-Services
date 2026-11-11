use bigdata;

create table hotel(
    id int primary key auto_increment comment '酒店编号',
    hotel_name varchar(255) comment '酒店名称',
    city varchar(255) comment '城市',
    province varchar(255) comment '省份',
    level varchar(255) comment '星级',
    room_num int comment '房间数',
    score double comment '评分',
    commnet_num varchar(255) comment '评论数'
);

create table comment(
    id int primary key auto_increment comment '评论编号',
    name varchar(255) comment '酒店名称',
    commentator varchar(255) comment '评论人',
    score double comment '评分',
    comment_time datetime comment '评论时间',
    content varchar(255) comment '评论内容'
);
