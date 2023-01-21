import json
from datetime import datetime
from typing import Iterator
from collections import defaultdict # to be used in another possible solution mentioned below

bucket='my_bucket'
base_path = '/xxx/yyy/zzz'
specific_paths=['/abc','/def']
dictionary=defaultdict(list)

# 1BA - calculate for each id a minimum and maximum month without month gaps

def get_all_keys(bucket, full_path)  -> Iterator[str]:
    return NotImplemented

# On the input you know your bucket, base_path and all the specific paths -> create function that create full path for all specific paths
def create_full_path(base_path, specific_path):
    full_path = base_path + specific_path

    return full_path 

for specific_path in specific_paths:
    full_path=create_full_path(base_path, specific_path)
    keys = get_all_keys(bucket, full_path)
    id_entries={}   #or id_entries=defaultdict(list)

    for key in keys:
        id_,date_,_ = key.split('/')
        id_ = id_.split('=')[1]
        date_=date_.split('=')[1]

        if id_ not in id_entries:   #if using defaultdict(), this if condition is not necessary
            id_entries[id_] = []

        id_entries[id_].append(datetime.strptime(date_, '%Y-%m-%d'))
    
    for id_, dates in id_entries.items():
        max_date = max(dates)
        min_date = min(dates)

        dictionary[specific_path].append( { 'id': id_, 
                                            'max_month': max_date,
                                            'min_month': min_date})

# 1BB - write the output to a json file
json_output = json.dumps(dictionary, indent=4)

with open('output.json', 'w', encoding='utf-8') as outputfile:
    outputfile.write(json_output)

#1BC - report missing months
dictionary_missing_months=defaultdict(list)

for specific_path in specific_paths:
    full_path=create_full_path(base_path, specific_path)
    keys = get_all_keys(bucket, full_path)
    id_entries={}  

    for key in keys:
        id_,date_,_ = key.split('/')
        id_ = id_.split('=')[1]
        date_=date_.split('=')[1]

        if id_ not in id_entries:   
            id_entries[id_] = []

        id_entries[id_].append(datetime.strptime(date_, '%Y-%m-%d'))

    for id_, dates in id_entries.items():
        max_date = max(dates)
        min_date = min(dates)
        months = [x.month for x in dates]

        missing_months = [x for x in range(1, 13) if x not in months]

        dictionary_missing_months[specific_path].append( {  'id': id_, 
                                                            'max_month': max_date,
                                                            'min_month': min_date,
                                                            'missing_months': missing_months})

# 1BB - write the output to a json file
json_output_missing_months = json.dumps(dictionary_missing_months, indent=4)

with open('output.json', 'w', encoding='utf-8') as outputfile:
    outputfile.write(json_output_missing_months)