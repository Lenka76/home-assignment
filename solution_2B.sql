-- Problematic part of join:

FROM sales_internal as i
LEFT JOIN sales_external as e
ON i.checkout_date = e.sale_date  --> here
   AND i.retailer_id = e.retailer_id


/* In the join there are  used columns checkout_date which is day when sale happened, but in external table (sale_date column) 
it is date of first day of the week when sale took place. 
The external sales will join only on the internal sales that were made on the first day of the week by same retailer. 
If the retailer did not make any internal sale on the first day of the week, data of the external sales from the same week 
would be missing in the final report. 

For fix, in the sales_internal table we can check the first date in each week if it is Monday:
    -> if it is Monday, use that date
    ->  if it is other day,then calculate date for Monday in that week 
With this solution there souldn't miss any sales, but all external sales will be assigned to first day of week. 
*/
with data as (
SELECT *
     , ROW_NUMBER() OVER (PARTITION BY retailer_id, YEARWEEK(checkout_date, 1) ORDER BY WEEKDAY(checkout_date) ASC ) AS rn
FROM sales_internal as id
)

SELECT *
    , CASE WHEN RN =1 AND WEEKDAY(checkout_date) <> 0 THEN checkout_date - WEEKDAY(checkout_date)
            ELSE checkout_date
        END AS first_date_of_week
FROM data as i
-- then use first_date_of_week to join sales_external table instead of checkout_date
LEFT JOIN sales_external as e
ON i.first_date_of_week = e.sale_date
AND i.retailer_id = e.retailer_id

