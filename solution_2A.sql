 -- original query:
 select
    c.id,
	(select  count(distinct a.call_id) 
     from activity a 
     where a.call_id=c.id 
     and activity_type_id=3) "accepted",
	(select  count(distinct a.call_id)
     from activity a 
     where a.call_id=c.id 
     and activity_type_id=4) "declined",
	(select  count(distinct a.call_id) 
    from activity a 
    where a.call_id=c.id 
    and activity_type_id=5) "missed",
	if(ifnull(timestampdiff(second, c.mic_shared, c.end_time), '0')>0, ifnull(timestampdiff(second, c.mic_shared, c.end_time), '0'), 0) "talk_time_sec"
from `call` c
where date(c.call_created_time) = curdate()
and c.retailer_id = 1080
order by c.id
;

-- optimized:
WITH activity_counts as 
    (SELECT DISTINCT call_id, 
           SUM(CASE WHEN activity_type_id = 3 THEN 1 ELSE 0 END) as accepted,
           SUM(CASE WHEN activity_type_id = 4 THEN 1 ELSE 0 END) as declined,
           SUM(CASE WHEN activity_type_id = 5 THEN 1 ELSE 0 END) as missed
      FROM activity
      WHERE activity_type_id in (3, 4, 5)
      GROUP BY call_id)

SELECT c.id,
       ac.accepted,
       ac.declined,
       ac.missed,
       if(ifnull(timestampdiff(second, c.mic_shared, c.end_time), '0')>0, ifnull(timestampdiff(second, c.mic_shared, c.end_time), '0'), 0) "talk_time_sec"
FROM 'call' c
LEFT JOIN activity_counts ac 
ON c.id = ac.call_id
WHERE date(c.call_created_time) = curdate()
AND c.retailer_id = 1080
ORDER BY c.id
;