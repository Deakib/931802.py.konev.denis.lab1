import requests
import json

url = 'http://127.0.0.1:8080'
tz_for_url = 'Asia/Tokyo'
url_with_tz = url + '/' + tz_for_url

print('\t\t\tGET REQUESTS')

print('\t1st task:')
print(requests.get(url).text)
print()

print('\t2nd task:')
print(requests.get(url_with_tz).text)
print()

print('\t\t\tPOST REQUESTS')

print('\t3rd task:')
#with tz
data = {'type': 'time', 'tz_start': tz_for_url}
print('Time in ' + tz_for_url + ' is ' + requests.post(url = url, data = json.dumps(data)).text)
#without tz
data = {'type': 'time'}
print('Time is ' + requests.post(url = url, data = json.dumps(data)).text)
print()

print('\t4th task:')
#with tz
data = {'type': 'date', 'tz_start': tz_for_url}
print('Date in ' + tz_for_url + ' is ' + requests.post(url = url, data = json.dumps(data)).text)
#without tz
data = {'type': 'date'}
print('Date is ' + requests.post(url = url, data = json.dumps(data)).text)
print()

print('\t5th task:')
#no time zones
data = {'type': 'datediff'}
print('1. Difference between time zones is ' + requests.post(url = url, data = json.dumps(data)).text)
#only start time zone
data = {'type': 'datediff', 'tz_start': tz_for_url}
print('2. Difference between time zones is ' + requests.post(url = url, data = json.dumps(data)).text)
#only end time zone
data = {'type': 'datediff', 'tz_end': tz_for_url}
print('3. Difference between time zones is ' + requests.post(url = url, data = json.dumps(data)).text)
#both time zones
data = {'type': 'datediff', 'tz_start': tz_for_url, 'tz_end': 'America/Los_Angeles'}
print('4. Difference between time zones is ' + requests.post(url = url, data = json.dumps(data)).text)
data = {'type': 'datediff', 'tz_start': 'Canada/Central', 'tz_end': 'Australia/Tasmania'}
print('5. Difference between time zones is ' + requests.post(url = url, data = json.dumps(data)).text)
