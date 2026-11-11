use bigdata;

# 统计各省份的平均酒店评分，并将评分低于该省份平均分的酒店评分上调0.5分（评分上限为5分）
update hotel as h
join (
    select province, avg(score) as avg_score
    from hotel
    group by province
) as a
    on h.province = a.province
set h.score = least(5, h.score + 0.5)
where h.score < a.avg_score;

# 查找出每个城市评论数最多的酒店及其详细信息
select h.city,h.id,h.hotel_name,h.province,h.level,h.room_num,h.score,h.commnet_num
from hotel as h
join (
    select city,max(commnet_num) as max_commnet_num
    from hotel
    group by city
) as t
    on h.city = t.city and h.commnet_num = t.max_commnet_num;

# 找出所有发表过3条及以上差评（评分小于等于2分）的评论人，并列出这些评论人的评论时间、评论内容及对应的酒店名称，按评论时间降序排序
select cm.commentator,cm.comment_time,cm.content,cm.name as 酒店名称
from comment as cm
join (
    select commentator
    from comment
    where score <= 2
    group by commentator
    having count(*) >= 3
) as t
    on cm.commentator = t.commentator
where cm.score <= 2
order by cm.comment_time desc;
