use education;

#查询各难度级别课程的平均好评率与平均学习人数
select c.difficulty as 难度级别,
       round(avg(c.avg_review_score),2) as 平均好评率,
       round(avg(c.total_students),0) as 平均学习人数
from course as c
group by c.difficulty;

#统计每位主讲教师名下所有课程的总学习人次（需关联学习行为表）
select c.teacher_name as 主讲教师,
       count(s.record_id) as 总学习人次
from course as c
join study_behavior as s
on c.course_id = s.course_id
group by c.teacher_name
order by 总学习人次 desc;

#找出“编程”学科中，当日学习时长超过 60 分钟且完成了作业（作业得分大于 0）的所有学习记录
select s.*
from course as c
join study_behavior as s
on c.course_id = s.course_id
where c.subject = '编程'
  and s.daily_study_minutes > 60
  and s.assignment_score > 0;
