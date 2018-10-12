select schedule.userid as userid,
count(*) as kl_user_num,
collect_list(course.courseid) as kl_course_set,
collect_list(schedule.score) as kl_score_set,
collect_list(course.start) as kl_time_set
from(
        select
        distinct book.scheduleid as scheduleid,
        (case when book.userid is not null then book.userid else training.userid end) as userid,
        (case when training.userid is not null then 1 else 0.5 end) as score
        from(
                select userid,
                scheduleid
                from keep_ods.ods_kl_schedule_book_info
                where schedulestarttime >= '2018-08-01' and schedulestarttime < '2018-10-01'
        ) book
        left join(
                select distinct scheduleid,
		userid
                from keep_ods.ods_kl_gym_user_training_data
        ) training
        on book.scheduleid = training.scheduleid
) as schedule
inner join(
        select id,
        gymcourseid as courseid,
        start
        from keep_ods.ods_kl_room_schedule
	where start >= '2018-08-01' and start < '2018-10-01'
        order by start desc
) as course
on course.id = schedule.scheduleid
group by userid
sort by rand()
