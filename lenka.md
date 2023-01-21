# Home assignments (Lenka)

## 1, Python

### 1A, couple of quick programming tasks

1A1, Let's have a string generator (`generator()`), we would like to write 3 filtering (lambda) functions, that would filter the generated output for:
 - 1A1A, only integers
 - 1A1A, those ending with ".json" or ".csv"
 - 1A1C, dates in ISO format (2019-05-27)

1A2, Let's have a folder with an unspecified number of CSV files that have various sizes. For each file we need to calculate a sum of a column in relation to another column (e.x. `sum(a) where b = 'foo'`).

1A3, Assume we have a web log with a list of addresses visited by users. This log is sorted by addresses.
 - 1A3A, calculate number of hits per address
 - 1A3B, how would you change your code if the log wasn't sorted?
 - 1A3C, how would you solve this without python? hint: unix tools (awk, sed, sort, ...)

### 1B, object store path min/max analysis
You have a specific prefix + key structure in your objects store (can be S3, HDFS, ...), that looks like this:
`protocol://bucket/base_path/specific_path/keys`  and a key has a structure of `id=some_value/month=yyyy-MM-dd/object{1, 2, 3, ...}`

Example:
s3://my-bucket/xxx/yyy/zzz/abc/id=123/month=2019-01-01/2019-01-19T10:31:18.818Z.gz
s3://my-bucket/xxx/yyy/zzz/abc/id=123/month=2019-02-01/2019-02-19T10:32:18.818Z.gz
s3://my-bucket/xxx/yyy/zzz/abc/id=333/month=2019-03-01/2019-06-19T10:33:18.818Z.gz
s3://my-bucket/xxx/yyy/zzz/def/id=123/month=2019-10-01/2019-10-19T10:34:18.818Z.gz
s3://my-bucket/xxx/yyy/zzz/def/id=333/month=2019-11-01/2019-12-19T10:35:18.818Z.gz

You have a function `get_all_keys(bucket, full_path) -> Iterator[str]` for getting all the keys for a full path (base_path + specific_path).

Notes:
On the input you know your bucket, base_path and all the specific paths you want to generate output for.
Also as shown in the example the month subkey has format of a date, but it's always yyyy-MM-01, so effectively it only gives you information about the year and month. Objects (files) within this structure have a timestamp, but this is a timestamp of when they have been created. For illustration, the last line in the example is an object (file) that was generated at '2019-12-19T10:35:18.818Z', but data in it are for the id of '333' and month of 2019-11.

**For each specific_path (there can be many):**
 - 1BA, calculate for each id a minimum and maximum month (there cannot be gaps between moths)
 - 1BB, write the output to a json file
 - 1BC, (optional/bonus) there can be gaps between months (missing months), so report them also in some appropriate structure

 ## 2, SQL

 ### 2A, query optimization
 Is it possible to optimize the query below? If so, what would be your approach? Just a note this runs on MySQL.

 ```
 select
    c.id,
	(select  count(distinct a.call_id) from activity a where a.call_id=c.id and activity_type_id=3) "accepted",
	(select  count(distinct a.call_id) from activity a where a.call_id=c.id and activity_type_id=4) "declined",
	(select  count(distinct a.call_id) from activity a where a.call_id=c.id and activity_type_id=5) "missed",
	if(ifnull(timestampdiff(second, c.mic_shared, c.end_time), '0')>0, ifnull(timestampdiff(second, c.mic_shared, c.end_time), '0'), 0) "talk_time_sec"
from `call` c
where date(c.call_created_time) = curdate()
and c.retailer_id = 1080
order by c.id
;
```

### 2B, reporting issues
There is a problem with one of the reports used by our internal customers. Apparently, for some of the days they don't see relevant rows on output :(
In this assignment you can just come up with an answer, SQL is not necessarily needed, but might be helpful for the explanation.

The report shows sales both internal (concluded on a call with a clerk (employee of the shop)) and external (concluded at the shop after a call with a clerk) on a daily basis.
We have 3 relevant tables that are essential for the report with following structure and meaning.

- sales_internal -- transactional records of internal sales (we might not have a record for each day)
```
transaction_id_int,
retailer_id, retailer_name,
call_id, call_date,
customer_id,
checkout_date, checkout_timestamp,
value, tax
```
- sales_external -- transactional records of external sales on weekly basis (i.e. sale_date is always the first date of a given the week), there might not be a record for each week
```
transaction_id_ext,
retailer_id, retailer_name,
sale_date,
customer_id,
total_value, tax
```
- sales_standard_daily -- daily table used for reporting with both internal and external sales aggregated to retailer_id and date,
```
retailer_id, retailer_name,
date
value, tax
```
The `sales_standard_daily` is created as select ... `sales_internal` left join `sales_external` on date and retailer.

The issue is that the report based on the `sales_standard_daily` table doesn't always show / include records from external sales table correctly.
Can you think of where the problem originates and how it could be fixed for the report?