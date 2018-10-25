select userid,
count(*) as mo_user_num,
collect_list(product_id) as mo_productId_set,
collect_list(product_name) as mo_productName_set
from(
	select a.buyer_id as userid,
        b.item_id as item_id,
        b.product_id as product_id,
        b.product_name as product_name
	from(
		select distinct pay_id,
                buyer_id
		from keep_ods.ods_mo_order_pay
		where(pay_time >= '2017-01-01'and pay_time < '2018-10-01' and pay_status == 302)
	) a
	inner join(
		select y.product_id as product_id,
                y.order_item_id as item_id,
                y.product_name as product_name,
		x.pay_id as pay_id
		from(
			select distinct order_id,
			pay_id
			from keep_ods.ods_mo_order_info
		) x
		inner join(
			select i.order_id as order_id,
                        i.order_item_id as order_item_id,
			j.product_id as product_id,
                        i.product_name as product_name
			from(
				select distinct order_id,
				order_item_id,
				product_id,
				product_name
				from keep_ods.ods_mo_order_item
                        ) i
                        inner join(
				select distinct product_id
				from mo.ods_mo_product
				where (product_status == 1 and
				       data_type == 1 and
				       product_id > 0 and
				       brand_id not in (26, 27))
                        ) j
                        on i.product_id = j.product_id
		) y
		on x.order_id = y.order_id
	) b
	on a.pay_id = b.pay_id
) as T
group by userid
