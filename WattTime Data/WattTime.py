# import requests
#
# register_url = 'https://api2.watttime.org/v2/register'
# params = {'username': 'william',
#           'password': 'qwerty123456!',
#           'email': 'qp543me@uuf.me',
#           'org': 'williams world'}
# rsp = requests.post(register_url, json=params)
# print(rsp.text)

# import requests
# from requests.auth import HTTPBasicAuth
#
# login_url = 'https://api2.watttime.org/v2/login'
# token = requests.get(login_url, auth=HTTPBasicAuth('william', 'qwerty123456!')).json()['token']
#
# region_url = 'https://api2.watttime.org/v2/ba-from-loc'
# headers = {'Authorization': 'Bearer {}'.format(token)}
# params = {'latitude': '42.372', 'longitude': '-72.519'}
# rsp = requests.get(region_url, headers=headers, params=params)
# print(rsp.text)

import requests
from requests.auth import HTTPBasicAuth

login_url = 'https://api2.watttime.org/v2/login'
token = requests.get(login_url, auth=HTTPBasicAuth('william', 'qwerty123456!')).json()['token']

index_url = 'https://api2.watttime.org/index'
headers = {'Authorization': 'Bearer {}'.format(token)}
params = {'ba': 'CAISO_NORTH'}
rsp=requests.get(index_url, headers=headers, params=params)
print(rsp.text)

# import requests
# from requests.auth import HTTPBasicAuth
#
# login_url = 'https://api2.watttime.org/v2/login'
# token = requests.get(login_url, auth=HTTPBasicAuth('william', 'qwerty123456!')).json()['token']
#
# data_url = 'https://api2.watttime.org/v2/data'
# headers = {'Authorization': 'Bearer {}'.format(token)}
# params = {'ba': 'CAISO_NORTH',
#           'starttime': '2022-12-12T20:30:00-0800',
#           'endtime': '2022-12-16T20:45:00-0800'}
# rsp = requests.get(data_url, headers=headers, params=params)
# print(rsp.text)
