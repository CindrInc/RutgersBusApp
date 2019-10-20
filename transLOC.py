import requests
import json
KEY = "2c6a319638msh64a975ebd56c812p105d1ejsna95ccb20b00f"
HOST = "transloc-api-1-2.p.rapidapi.com"
# url_arrival_estimates = "https://transloc-api-1-2.p.rapidapi.com/arrival-estimates.json"

# querystring = {"routes":"4000421,4000592,4005122","stops":"4002123,4023414,4021521","callback":"call","agencies":"12,16","":""}


# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)
url_agencies = "https://transloc-api-1-2.p.rapidapi.com/agencies.json"

querystring = {}

headers = {
    'x-rapidapi-host': HOST,
    'x-rapidapi-key': KEY
    }

response = requests.request("GET", url_agencies, headers=headers, params=querystring)
colleges = response.json()
count = 0
for i in colleges["data"]:
    if "Rutgers" in i["long_name"]:
        print(i)
    