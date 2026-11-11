use education;

create table course(
    course_id int primary key,
    title varchar(255),
    subject varchar(100),
    difficulty char(10),
    total_lessons int,
    original_price decimal(10,2),
    current_price decimal(10,2),
    teacher_name varchar(100),
    publish_date date,
    total_students int,
    avg_review_score float
);

create table study_behavior(
    record_id bigint primary key,
    user_id int,
    course_id int,
    access_date date,
    daily_study_minutes int,
    finished_lessons int,
    assignment_score float,
    is_joined_discussion tinyint,
    note_count int,
    foreign key (course_id) references course(course_id)
);
