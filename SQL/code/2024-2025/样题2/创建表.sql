use education;

create table course(
    id int primary key ,
    course_name varchar(50),
    category varchar(50),
    level varchar(50),
    duration int,
    price decimal,
    instructor  varchar(50),
    avg_rating float,
    enrollment_count int
);

create table learning_record(
    id int primary key,
    user_id int,
    course_id int,
    watch_duration int,
    completion_rate float,
    last_watch_time datetime,
    quiz_score float,
    study_duration int
);
