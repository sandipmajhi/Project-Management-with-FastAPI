import pandas as pd
import json
import urllib
# from urllib import request, parse

import requests
import json

users_df = pd.read_excel('Designation_Employees.xlsx')

# for data in users_df.iterrows():
#     print(data[1].to_dict())



login_url = 'http://127.0.0.1:8000/login'
logout_url = 'http://127.0.0.1:8000/logout'

data = json.dumps({"email":"admin@example.com","password":"admin"})
x = requests.post(login_url, data)
print(x.json())

access_token = x.json()["access_token"]

headers = {"Authorization":f"Bearer {access_token}"}

y = requests.get(logout_url, headers=headers)

print(y.json())


