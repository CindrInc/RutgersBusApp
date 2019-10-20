import requests
import json
import datetime
from dateutil import parser
import time

STOP_ID = {'College Avenue Student Center': '4229492', 'Student Activities Center Northbound': '4229496', 'Stadium': '4229500', 'Werblin Back Entrance': '4229504', 'Hill Center (NB)': '4229508', 'Science Building': '4229512', 'Library of Science': '4229516', 'Busch Suites': '4229520', 'Busch Student Center': '4229524', 'Buell Apartments': '4229528', 'New Brunswick Train Station-George Street stop': '4229532', 'New Brunswick Train Station-Somerset Street stop': '4229536', 'Red Oak Lane': '4229538', 'Food Sciences Building': '4229542', 'Katzenbach': '4229546', 'College Hall': '4229550', 'Northbound Public Safety Building on George Street': '4229554', 'Zimmerli Arts Museum': '4229558', 'Werblin Main Entrance': '4229562', 'Davidson Hall': '4229566', 'Livingston Plaza': '4229570', 'Livingston Student Center': '4229574', 'Quads': '4229576', 'Allison Road Classrooms': '4229578', 'Bravo Supermarket': '4229582', 'Colony House': '4229584', 'Rockoff Hall - 290 George Street': '4229588', 'Southbound Public Safety Building on George Street': '4229592', 'Lipman Hall': '4229596', 'Biel Road': '4229600', 'Henderson': '4229604', 'Gibbons': '4229608', 'George Street Northbound at Liberty Street': '4229612', 'George Street Northbound at Paterson Street': '4229616', 'Scott Hall': '4229620', 'Nursing School': '4229624', 'Visitor Center': '4229626', 'Golden Dome': '4229630', '180 W Market St': '4229634', 'Bergen Building': '4229636', 'Blumenthal Hall': '4229638', 'Boyden Hall': '4229640', 'Boyden Hall (Arrival)': '4229642', 'CLJ': '4229644', 'Clinical Academic Building': '4229646', 'Dental School': '4229648', 'ECC': '4229650', 'Frank E. Rodgers Blvd and Cleveland Ave': '4229652', 'Hospital': '4229654', 'Harrison Ave & Passaic Ave': '4229656', 'ICPH': '4229658', 'Kearny Ave & Dukes St.': '4229660', 'Kearny Ave and Bergen Ave': '4229662', 'Kearny Ave and Midland Ave': '4229664', 'Kearny Ave and Quincy St': '4229666', 'Kmart': '4229668', 'Medical School': '4229670', 'Medical School (Arrival)': '4229672', 'NJIT': '4229674', 'Penn Station': '4229676', 'Physical Plant': '4229678', 'RBHS Piscataway Hoes Lane': '4229680', 'RBHS Piscataway Hoes Lane (hidden arrival)': '4229682', 'ShopRite': '4229684', 'University North': '4229686', 'Washington Park': '4229688', 'Broad St': '4229690', 'New Street': '4229692', 'Public Safety Building on Commercial Southbound': '4229694', 'Student Activities Center Southbound': '4229696', 'George Street Southbound at Paterson Street': '4229698', 'Livingston Health Center': '4230628', 'Hill Center (SB)': '4231636', 'City Lot 15': '4231784', 'City Lot 16': '4231786', 'Law School (5th Street Under the Law Bridge)': '4231788', 'Nursing and Science Building [NSB]': '4231790', 'Business and Science Building [BSB]': '4231792', 'Best Western Robert Treat Hotel': '4232126'}
ROUTE_ID = {'Knight Mover 1': '4012660', 'Knight Mover 2': '4012662', 'Route A': '4012616', 'Route B': '4012618', 'Route C': '4012620', 'Route RBHS': '4012622', 'Route EE': '4012624', 'Route F': '4012626', 'Route H': '4012628', 'Route LX': '4012630', 'Route REXB': '4012632', 'Route REXL': '4012634', 'Route New BrunsQuick 1 Shuttle': '4012636', 'Route New BrunsQuick 2 Shuttle': '4012638', 'Newark Penn Station': '4012640', 'Newark Campus Connect': '4012642', 'Newark Kearny': '4012644', 'Newark Penn Station Express': '4012646', 'Newark Campus Connect Express': '4012648', 'Route Weekend 1': '4012650', 'Route Weekend 2': '4012652', 'Route All Campuses': '4012654', 'Newark Run Run Express': '4012656', 'Newark Run Run': '4012658', 'Summer 1': '4012664', 'Summer 2': '4012666', 'Weekend 1': '4012668', 'Weekend 2': '4012670', 'Camden Shuttle': '4013328'}
ROUTES_STOPS = {'Knight Mover 1': (), 'Knight Mover 2': (), 'Route A': ('4229492', '4229620', '4229496', '4229626', '4229500', '4229504', '4229508', '4229512', '4229516', '4229520', '4229524', '4229528', '4229562', '4229574'), 'Route B': ('4229574', '4229576', '4230628', '4229504', '4229508', '4229512', '4229516', '4229520', '4229524', '4229570'), 'Route C': ('4229500', '4229504', '4229508', '4229578', '4231636'), 'Route RBHS': ('4229680', '4229646', '4229682'), 'Route EE': ('4229492', '4229620', '4229536', '4229698', '4229588', '4229592', '4229538', '4229596', '4229542', '4229600', '4229604', '4229546', '4229608', '4229550', '4229554', '4229612', '4229532', '4229558', '4229496', '4229616'), 'Route F': ('4229492', '4229620', '4229694', '4229538', '4229596', '4229542', '4229600', '4229604', '4229546', '4229608', '4229550', '4229496'), 'Route H': ('4229492', '4229620', '4229532', '4229496', '4229562', '4229528', '4229524', '4229566', '4229516', '4229578', '4231636', '4229500', '4229536', '4229508'), 'Route LX': ('4229492', '4229620', '4229536', '4229496', '4229570', '4229574', '4229576', '4229532'), 'Route REXB': ('4229538', '4229596', '4229550', '4229582', '4229508', '4229578', '4231636', '4229588', '4229694'), 'Route REXL': ('4229538', '4229596', '4229550', '4229582', '4229570', '4229574', '4229588', '4229694', '4229696', '4229592'), 'Route New BrunsQuick 1 Shuttle': ('4229532', '4229624', '4229584', '4229492', '4229620'), 'Route New BrunsQuick 2 Shuttle': ('4229532', '4229624', '4229616', '4229558', '4229496', '4229492', '4229584'), 'Newark Penn Station': ('4229676', '4229672', '4229654', '4229636', '4229648', '4229634', '4229658', '4229674', '4229638'), 'Newark Campus Connect': ('4229640', '4229674', '4229658', '4229636', '4229670', '4229650', '4229644', '4229688', '4229690', '4229686', '4229678'), 'Newark Kearny': ('4229640', '4229674', '4229688', '4229656', '4229652', '4229660', '4229662', '4229666', '4229664', '4229668', '4229684'), 'Newark Penn Station Express': ('4229670', '4229654', '4229676'), 'Newark Campus Connect Express': ('4229640', '4229670', '4229644', '4229688'), 'Route Weekend 1': ('4229492', '4229620', '4229536', '4229496', '4229626', '4229504', '4229508', '4229512', '4229516', '4229520', '4229524', '4229570', '4229574', '4229576', '4229696', '4229694', '4229538', '4229596', '4229542', '4229600', '4229604', '4229546', '4229608', '4229550', '4229554', '4229612', '4229616', '4229532', '4229558'), 'Route Weekend 2': ('4229492', '4229620', '4229536', '4229698', '4229588', '4229592', '4229538', '4229596', '4229542', '4229600', '4229604', '4229546', '4229608', '4229550', '4229496', '4229570', '4229574', '4229576', '4229524', '4229566', '4229516', '4229578', '4229508'), 'Route All Campuses': ('4229492', '4229620', '4229536', '4229496', '4229626', '4229504', '4229508', '4229512', '4229516', '4229520', '4229524', '4229570', '4229574', '4229576', '4229696', '4229694', '4229538', '4229596', '4229542', '4229600', '4229604', '4229546', '4229608', '4229550', '4229554', '4229612', '4229616', '4229532', '4229558'), 'Newark Run Run Express': ('4229640', '4229692', '4232126', '4229644', '4229688', '4229642'), 'Newark Run Run': ('4232126', '4229644', '4229688', '4229690', '4229678', '4229692', '4229640', '4229630', '4229676'), 'Summer 1': ('4229492', '4229620', '4229536', '4229496', '4229626', '4229504', '4229508', '4229512', '4229516', '4229520', '4229524', '4229570', '4229574', '4229576', '4229696', '4229694', '4229538', '4229596', '4229542', '4229600', '4229604', '4229546', '4229608', '4229550', '4229554', '4229612', '4229616', '4229532', '4229558'), 'Summer 2': ('4229492', '4229620', '4229536', '4229698', '4229588', '4229592', '4229538', '4229596', '4229542', '4229600', '4229604', '4229546', '4229608', '4229550', '4229496', '4229570', '4229574', '4229576', '4229524', '4229566', '4229516', '4229578', '4229508'), 'Weekend 1': ('4229492', '4229620', '4229536', '4229496', '4229626', '4229504', '4229508', '4229512', '4229516', '4229520', '4229524', '4229570', '4229574', '4229576', '4229696', '4229694', '4229538', '4229596', '4229542', '4229600', '4229604', '4229546', '4229608', '4229550', '4229554', '4229612', '4229616', '4229532', '4229558'), 'Weekend 2': ('4229492', '4229620', '4229536', '4229698', '4229588', '4229592', '4229538', '4229596', '4229542', '4229600', '4229604', '4229546', '4229608', '4229550', '4229496', '4229570', '4229574', '4229576', '4229524', '4229566', '4229516', '4229578', '4229508'), 'Camden Shuttle': ('4231784', '4231786', '4231788', '4231790', '4231792')}

#len(ROUTE_ID) == len(ROUTES_STOPS) 
KEY = "2c6a319638msh64a975ebd56c812p105d1ejsna95ccb20b00f"
HOST = "transloc-api-1-2.p.rapidapi.com"
headers = {
    'x-rapidapi-host': HOST,
    'x-rapidapi-key': KEY
    }
def arrival_Estimate(location,route):
    url_arrival_estimates = "https://transloc-api-1-2.p.rapidapi.com/arrival-estimates.json"
    querystring_arrival_estimates = {"agencies":"1323","stops":STOP_ID[location],"routes":ROUTE_ID[route]}

    response_arrival_estimates = requests.request("GET", url_arrival_estimates, headers=headers, params=querystring_arrival_estimates)
    rutgers_arrival_estimates = response_arrival_estimates.json()
    if not rutgers_arrival_estimates['data']:
        return "NO BUSES AVAILABLE??"

    else:
        estimates = rutgers_arrival_estimates["data"][0]["arrivals"]
        arrival_data = []
        for i in estimates:
            # print(i)
            # print("---------------")
            arrival_data.append(i["arrival_at"])

        
        #first_arrival_data = estimates[0]["arrival_at"]
        #current_time = str(datetime.datetime.fromtimestamp(time.time()))
        
        # first_arrival_data = first_arrival_data[11:19]
        # current_time = current_time[11:19]
        
        # first_arrival_data = datetime.datetime.strptime(first_arrival_data, '%H:%M:%S').time()
        # current_time = datetime.datetime.strptime(current_time, '%H:%M:%S').time()
        arrival_data = list(map(lambda x: parser.parse(x).replace(tzinfo=None),arrival_data))
        current_time = datetime.datetime.now()
        print(arrival_data)
        arrival_data = list(map(lambda x: str(x - current_time),arrival_data))
        return arrival_data

def bus_to_bus(location,destination,route):
    for k,v in ROUTES_STOPS:

    if STOP_ID[destination] in ROUTES_STOPS[route]:
        url_arrival_estimates = "https://transloc-api-1-2.p.rapidapi.com/arrival-estimates.json"
        querystring_arrival_estimates = {"agencies":"1323","stops":STOP_ID[destination],"routes":ROUTE_ID[route]}
        
        response_arrival_estimates = requests.request("GET", url_arrival_estimates, headers=headers, params=querystring_arrival_estimates)
        rutgers_arrival_estimates = response_arrival_estimates.json()
        print(rutgers_arrival_estimates)
        estimates = rutgers_arrival_estimates["data"][0]["arrivals"]
        arrival_data = []
        for i in estimates:
            print(i)
            print("---------------")
            
    else:
        return f"{destination} not in {route}"


bus_to_bus("Scott Hall","George Street Northbound at Paterson Street","Route Weekend 1")