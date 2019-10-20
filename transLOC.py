import requests
import json
KEY = "2c6a319638msh64a975ebd56c812p105d1ejsna95ccb20b00f"
HOST = "transloc-api-1-2.p.rapidapi.com"
headers = {
    'x-rapidapi-host': HOST,
    'x-rapidapi-key': KEY
    }


url_agencies = "https://transloc-api-1-2.p.rapidapi.com/agencies.json"
querystring_agencies = {"agencies":"1323"}


url_arrival_estimates = "https://transloc-api-1-2.p.rapidapi.com/arrival-estimates.json"
querystring_arrival_estimates = {"agencies":"1323"} #"routes":"4000421,4000592,4005122","stops":"4002123,4023414,4021521"

url_routes = "https://transloc-api-1-2.p.rapidapi.com/routes.json"
querystring_routes = {"agencies": "1323","format":"json"}

url_stops = "https://transloc-api-1-2.p.rapidapi.com/stops.json"
querystring_stops = {"agencies":"1323"}

#All the JSON information
response_agencies = requests.request("GET", url_agencies, headers=headers, params=querystring_agencies)
rutgers = response_agencies.json()

response_arrival_estimates = requests.request("GET", url_arrival_estimates, headers=headers, params=querystring_arrival_estimates)
rutgers_arrival_estimates = response_arrival_estimates.json()

response_stops = requests.request("GET", url_stops, headers=headers, params=querystring_stops)
rutgers_stops = response_stops.json()

response_routes = requests.request("GET", url_routes, headers=headers, params=querystring_routes)
rutgers_routes = response_routes.json()

STOPS_ID = {}
STOPS_LOC = {}
for i in rutgers_stops["data"]:
    if i["name"] not in STOPS_ID:
        STOPS_ID[i["name"]] = i["stop_id"]
    if i["name"] not in STOPS_LOC:
        STOPS_LOC[i["name"]] = (i["location"]["lat"],i["location"]["lng"])

f = open("stops_id.json", "w")
f.write(f"{STOPS_ID}")
f.close()

f = open("stops_loc.json","w")
f.write(f"{STOPS_LOC}")
f.close()


    