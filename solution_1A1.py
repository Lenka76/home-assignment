import re
from datetime import datetime
# testing example of generated strings
generated_output = ['2000-05-25', '22', 'yahoo', 'loading.json', '43548674645', '1999-05-28', 'lady.csv', '555.56']

#function to filter integers
integer = lambda x: x.isdigit()

#function to filter files ending on .json or .csv
files = lambda x: x.endswith(".json") or x.endswith('.csv')

#function to filter dates in ISO format, with possibility to match non-valid date
dates = lambda x: re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", x)

#alternative solution not using lambda function:
"""
def is_isodate(x):
    try:
        datetime.strptime(x, '%Y-%m-%d')
        return True
    except ValueError:
        return False
"""

#filter generated output
all_integers = filter(integer, generated_output)
all_files = filter(files, generated_output)
all_dates = filter(dates, generated_output)
# alternative: all_dates = filter(is_isodate, generated_output)

for x in all_integers:
    print(x)
for x in all_files:
    print(x)
for x in all_dates:
    print(x)