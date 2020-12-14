import requests
import json

url = 'http://localhost:8000/'
tz = 'Europe/Moscow'
res = ''

print('GET without params')
res = requests.get(url)
print(res)

print('GET with bad params')
res = requests.get(url + 'Europe/Moskva')
print(res)

print('GET with params')
res = requests.get(url + tz)
print(res)

print('POST time')
json_tz = json.dumps({'tz': tz})
res = requests.post(url + 'api/v1/time', json_tz)
print(res)

print('POST date')
json_tz = json.dumps({'tz': tz})
res = requests.post(url + 'api/v1/date', json_tz)
print(res)

print('POST datediff with tz')
json_tz = json.dumps({
    "start": {"date": "12:00pm 2019-01-01", "tz": "UTC"},
    "end": {"date": "12:00pm 2019-01-01", "tz": "Europe/Moscow"}
})
res = requests.post(url + 'api/v1/datediff', json_tz)
print(res)

print('POST datediff end with tz')
json_tz = json.dumps({
    "start": {"date": "12:00pm 2019-12-01"},
    "end": {"date": "12:00pm 2019-12-01", "tz": "Europe/Moscow"}
})
res = requests.post(url + 'api/v1/datediff', json_tz)
print(res)

print('POST datediff without tz')
json_tz = json.dumps({
    "start": {"date": "12:00pm 2019-12-01"},
    "end": {"date": "12:00pm 2019-12-01"}
})
res = requests.post(url + 'api/v1/datediff', json_tz)
print(res)