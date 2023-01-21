from collections import Counter

# solution for 1A3A, assuming that address is in form 'nameofaddress.xx' - see file logs1A3A.txt
parsed_list = []

with open('logs1A3A.txt', 'r') as f:
    for line in f:
       parts = line.strip().split(';')
       parsed_list.append(parts)

addresses = [item[1] for item in parsed_list]

for address, hits in Counter(addresses).items():
   print(f"Address {address} has {hits} hits.")


#solution for 1A3B, assuming that address is in form 'nameofaddress.xx' - see file logs1A3B.txt
parsed_list = []

with open('logs1A3B.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(';')
        parsed_list.append(parts)

sorted_list = sorted(parsed_list, key=lambda x: x[1])
addresses = [item[1] for item in sorted_list]

for address, hits in Counter(addresses).items():
   print(f"Address {address} has {hits} hits.")


#solution for 1A3C if the log is sorted
# cut -d ';' -f 2 -s < logs1A3A.txt | uniq -c


#solution for 1A3C if the log is NOT sorted
# cut -d ';' -f 2 -s < log1A3B.txt | sort | uniq -c