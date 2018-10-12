select userid,
       count(*) as workout_user_num,
       collect_list(workoutid) as workout_set,
       collect_list(starttime) as workout_time_set
from(
	select x.userid as userid,
	       x.workoutid as workoutid,
	       x.starttime as starttime,
	       y.paidtype as paidtype
	from(
		       select distinct key,
		       userid,
		       workoutid,
		       starttime
		       from training.training_record
		       where (dt >= '2018-08-01' and dt < '2018-10-01' and workoutid is not null)
		       order by starttime
	   ) x
	inner join(
		       select id,
		       paidtype
		       from zeus.workout
		 ) y
	on x.workoutid = y.id
   )
as T
group by userid


