use education;

# 查询每门课程的平均完成率
select c.id,c.course_name,c.category,avg(lr.completion_rate) as 平均完成率
from course as c
join learning_record as lr
    on c.id = lr.course_id
group by c.id,c.course_name,c.category;

# 统计每个课程类别的总报名人数
select category,sum(enrollment_count) as 总报名人数
from course
group by category;

# 查找观看时长超过课程时长的学习记录
select lr.user_id,lr.course_id,lr.watch_duration,lr.completion_rate,lr.last_watch_time,lr.quiz_score,lr.study_duration
from learning_record as lr
join course as c
    on c.id = lr.course_id
where lr.watch_duration > c.duration;
