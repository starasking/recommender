select userid,
count(*) as mo_user_num,
collect_list(item_id) as mo_bought_item_set,
collect_list(pay_time) as mo_paytime_set,
collect_list(pay_id) as mo_payid_set,
collect_list(paid_fee) as mo_paid_fee_set
from(
	select a.buyer_id as userid,
	b.item_id as item_id,
	a.pay_id as pay_id,
	a.total_paid as paid_fee,
	a.pay_time as pay_time,
	a.pay_status as pay_status
	from(
		select distinct pay_id,
		buyer_id,
		pay_status,
		total_paid,
		pay_time
		from keep_ods.ods_mo_order_pay
		where(pay_time >= '2018-08-01'and pay_time < '2018-10-01' and pay_status == 302)
		order by pay_time
	) a
	inner join(
		select y.order_item_id as item_id,
		x.pay_id as pay_id
		from(
			select distinct order_id,
			pay_id
			from keep_ods.ods_mo_order_info
		) x
		inner join(
			select distinct order_id,
			order_item_id
			from keep_ods.ods_mo_order_item
		) y
		on x.order_id = y.order_id
	) b
	on a.pay_id = b.pay_id
) as T
group by userid
