import requests
from jqpy import jq
# response = requests.get("http://api.open-notify.org/astros.json")
response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=290592634318c8d5dd28f1d53c44cc47")
json = response.json()
# print(json)
# for person in json['people']:
#     print(person['name'])

print(jq(".weather[].main", json))