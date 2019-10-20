from flask import Flask, request
from twilio.rest import Client
import googlemaps, json, requests
from math import sin,cos,sqrt,atan2,radians
import time
import datetime
from dateutil import parser
import urllib.parse

# Assuming current location is Tillet hall
def getClosestStop(currentLatitude, currentLongitude):
    stops = {'College Avenue Student Center': (40.503222, -74.451962), 'Student Activities Center Northbound': (40.5039, -74.44883), 'Stadium': (40.514479, -74.466153), 'Werblin Back Entrance': (40.51868, -74.46147), 'Hill Center (NB)': (40.521892, -74.463127), 'Science Building': (40.523938, -74.464221), 'Library of Science': (40.5262, -74.46583), 'Busch Suites': (40.525831, -74.458724), 'Busch Student Center': (40.52363, -74.45808), 'Buell Apartments': (40.521807, -74.456701), 'New Brunswick Train Station-George Street stop': (40.49768, -74.44451), 'New Brunswick Train Station-Somerset Street stop': (40.4982, -74.44511), 'Red Oak Lane': (40.48299, -74.43754), 'Food Sciences Building': (40.47891, -74.435714), 'Katzenbach': (40.48304, -74.4316), 'College Hall': (40.48563, -74.43744), 'Northbound Public Safety Building on George Street': (40.487628, -74.440209), 'Zimmerli Arts Museum': (40.49963, -74.44505), 'Werblin Main Entrance': (40.518637, -74.459854), 'Davidson Hall': (40.52588, -74.45863), 'Livingston Plaza': (40.525106, -74.438584), 'Livingston Student Center': (40.524313, -74.436397), 'Quads': (40.519863, -74.433567), 'Allison Road Classrooms': (40.523612, -74.465127), 'Bravo Supermarket': (40.49138, -74.44264), 'Colony House': (40.50617, -74.46223), 'Rockoff Hall - 290 George Street': (40.49183, -74.44304), 'Southbound Public Safety Building on George Street': (40.487428, -74.440207), 'Lipman Hall': (40.481294, -74.436266), 'Biel Road': (40.48, -74.432522), 'Henderson': (40.48095, -74.42872), 'Gibbons': (40.48523, -74.43194), 'George Street Northbound at Liberty Street': (40.49325, -74.4434), 'George Street Northbound at Paterson Street': (40.495286, -74.443878), 'Scott Hall': (40.49957, -74.44824), 'Nursing School': (40.494289, -74.449676), 'Visitor Center': (40.51514, -74.46191), 'Golden Dome': (40.739565, -74.174067), '180 W Market St': (40.741274, -74.186955), 'Bergen Building': (40.743386, -74.191461), 'Blumenthal Hall': (40.739281, -74.175143), 'Boyden Hall': (40.740978, -74.174247), 'Boyden Hall (Arrival)': (40.742252, -74.173605), 'CLJ': (40.741242, -74.172097), 'Clinical Academic Building': (40.494193, -74.450171), 'Dental School': (40.742285, -74.190294), 'ECC': (40.736597, -74.178506), 'Frank E. Rodgers Blvd and Cleveland Ave': (40.74689, -74.156253), 'Hospital': (40.741868, -74.191581), 'Harrison Ave & Passaic Ave': (40.745337, -74.163914), 'ICPH': (40.742787, -74.183882), 'Kearny Ave & Dukes St.': (40.755473, -74.155429), 'Kearny Ave and Bergen Ave': (40.759206, -74.151806), 'Kearny Ave and Midland Ave': (40.770516, -74.145217), 'Kearny Ave and Quincy St': (40.765954, -74.147548), 'Kmart': (40.760165, -74.160356), 'Medical School': (40.739719, -74.189567), 'Medical School (Arrival)': (40.739686, -74.189452), 'NJIT': (40.741192, -74.178811), 'Penn Station': (40.734819, -74.164721), 'Physical Plant': (40.744492, -74.172539), 'RBHS Piscataway Hoes Lane': (40.52457, -74.470034), 'RBHS Piscataway Hoes Lane (hidden arrival)': (40.524345, -74.470014), 'ShopRite': (40.756612, -74.161946), 'University North': (40.746147, -74.17175), 'Washington Park': (40.743789, -74.170569), 'Broad St': (40.746906, -74.1711), 'New Street': (40.743956, -74.181941), 'Public Safety Building on Commercial Southbound': (40.487913, -74.439383), 'Student Activities Center Southbound': (40.504249, -74.449742), 'George Street Southbound at Paterson Street': (40.495066, -74.443999), 'Livingston Health Center': (40.523479, -74.442508), 'Hill Center (SB)': (40.521872, -74.463417), 'City Lot 15': (39.952097, -75.126481), 'City Lot 16': (39.953253, -75.125933), 'Law School (5th Street Under the Law Bridge)': (39.947582, -75.120661), 'Nursing and Science Building [NSB]': (39.943979, -75.120531), 'Business and Science Building [BSB]': (39.948557, -75.123476), 'Best Western Robert Treat Hotel': (40.739023, -74.168556)}

    buschStops = {'Stadium': (40.514479, -74.466153), 'Werblin Back Entrance': (40.51868, -74.46147), 'Hill Center (NB)': (40.521892, -74.463127), 'Science Building': (40.523938, -74.464221), 'Library of Science': (40.5262, -74.46583), 'Busch Suites': (40.525831, -74.458724), 'Busch Student Center': (40.52363, -74.45808), 'Buell Apartments': (40.521807, -74.456701)}

    distance = 999
    closestStartStop = ''
    closestLatitude = 0
    closestLongitude = 0
    for k,v in stops.items():
        R = 6373.0
        lat1 = radians(currentLatitude)
        lon1 = radians(currentLongitude)
        lat2 = radians(v[0])
        lon2 = radians(v[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        tempdistance = R * c
        if (tempdistance < distance):
            distance = tempdistance
            closestStartStop = k
            closestLatitude = v[0]
            closestLongitude = v[1]


    start1 = str(currentLatitude) + "," + str(currentLongitude)
    end1 = str(closestLatitude) + "," + str(closestLongitude)

    gmaps = googlemaps.Client(key = 'AIzaSyByZ1krKUMWCADrjkGIYty8F3-vfTtcdEQ')
    my_dist = gmaps.distance_matrix(start1,end1,mode='walking')['rows'][0]['elements'][0]
    str1 = str(my_dist)
    dict2 = list(my_dist.values())[1]

    return (closestStartStop, list(dict2.values())[0])


def getDestination(building):
    stops = {'College Avenue Student Center': (40.503222, -74.451962), 'Student Activities Center Northbound': (40.5039, -74.44883), 'Stadium': (40.514479, -74.466153), 'Werblin Back Entrance': (40.51868, -74.46147), 'Hill Center (NB)': (40.521892, -74.463127), 'Science Building': (40.523938, -74.464221), 'Library of Science': (40.5262, -74.46583), 'Busch Suites': (40.525831, -74.458724), 'Busch Student Center': (40.52363, -74.45808), 'Buell Apartments': (40.521807, -74.456701), 'New Brunswick Train Station-George Street stop': (40.49768, -74.44451), 'New Brunswick Train Station-Somerset Street stop': (40.4982, -74.44511), 'Red Oak Lane': (40.48299, -74.43754), 'Food Sciences Building': (40.47891, -74.435714), 'Katzenbach': (40.48304, -74.4316), 'College Hall': (40.48563, -74.43744), 'Northbound Public Safety Building on George Street': (40.487628, -74.440209), 'Zimmerli Arts Museum': (40.49963, -74.44505), 'Werblin Main Entrance': (40.518637, -74.459854), 'Davidson Hall': (40.52588, -74.45863), 'Livingston Plaza': (40.525106, -74.438584), 'Livingston Student Center': (40.524313, -74.436397), 'Quads': (40.519863, -74.433567), 'Allison Road Classrooms': (40.523612, -74.465127), 'Bravo Supermarket': (40.49138, -74.44264), 'Colony House': (40.50617, -74.46223), 'Rockoff Hall - 290 George Street': (40.49183, -74.44304), 'Southbound Public Safety Building on George Street': (40.487428, -74.440207), 'Lipman Hall': (40.481294, -74.436266), 'Biel Road': (40.48, -74.432522), 'Henderson': (40.48095, -74.42872), 'Gibbons': (40.48523, -74.43194), 'George Street Northbound at Liberty Street': (40.49325, -74.4434), 'George Street Northbound at Paterson Street': (40.495286, -74.443878), 'Scott Hall': (40.49957, -74.44824), 'Nursing School': (40.494289, -74.449676), 'Visitor Center': (40.51514, -74.46191), 'Golden Dome': (40.739565, -74.174067), '180 W Market St': (40.741274, -74.186955), 'Bergen Building': (40.743386, -74.191461), 'Blumenthal Hall': (40.739281, -74.175143), 'Boyden Hall': (40.740978, -74.174247), 'Boyden Hall (Arrival)': (40.742252, -74.173605), 'CLJ': (40.741242, -74.172097), 'Clinical Academic Building': (40.494193, -74.450171), 'Dental School': (40.742285, -74.190294), 'ECC': (40.736597, -74.178506), 'Frank E. Rodgers Blvd and Cleveland Ave': (40.74689, -74.156253), 'Hospital': (40.741868, -74.191581), 'Harrison Ave & Passaic Ave': (40.745337, -74.163914), 'ICPH': (40.742787, -74.183882), 'Kearny Ave & Dukes St.': (40.755473, -74.155429), 'Kearny Ave and Bergen Ave': (40.759206, -74.151806), 'Kearny Ave and Midland Ave': (40.770516, -74.145217), 'Kearny Ave and Quincy St': (40.765954, -74.147548), 'Kmart': (40.760165, -74.160356), 'Medical School': (40.739719, -74.189567), 'Medical School (Arrival)': (40.739686, -74.189452), 'NJIT': (40.741192, -74.178811), 'Penn Station': (40.734819, -74.164721), 'Physical Plant': (40.744492, -74.172539), 'RBHS Piscataway Hoes Lane': (40.52457, -74.470034), 'RBHS Piscataway Hoes Lane (hidden arrival)': (40.524345, -74.470014), 'ShopRite': (40.756612, -74.161946), 'University North': (40.746147, -74.17175), 'Washington Park': (40.743789, -74.170569), 'Broad St': (40.746906, -74.1711), 'New Street': (40.743956, -74.181941), 'Public Safety Building on Commercial Southbound': (40.487913, -74.439383), 'Student Activities Center Southbound': (40.504249, -74.449742), 'George Street Southbound at Paterson Street': (40.495066, -74.443999), 'Livingston Health Center': (40.523479, -74.442508), 'Hill Center (SB)': (40.521872, -74.463417), 'City Lot 15': (39.952097, -75.126481), 'City Lot 16': (39.953253, -75.125933), 'Law School (5th Street Under the Law Bridge)': (39.947582, -75.120661), 'Nursing and Science Building [NSB]': (39.943979, -75.120531), 'Business and Science Building [BSB]': (39.948557, -75.123476), 'Best Western Robert Treat Hotel': (40.739023, -74.168556)}
    buildings = {'AB':(40.502020, -74.447779), 'ARC':(40.525060, -74.463690),'ARH':(40.486260, -74.435690), 'BE':(40.522470, -74.440720), 'BH':(40.503210, -74.449580), 'BIO':(40.480910, -74.438880), 'BME':(40.525940, -74.460360), 'BL':(40.481740, -74.439980),'BT':(40.480850, -74.438310),'CA':(40.503640, -74.448490),'CCB':(40.525169, -74.462990), 'CDL':(40.480770, -74.436590), 'CI':(40.505600, -74.453700),'COR':(40.519350, -74.462010),'DAV':(40.482520, -74.439850),'ED':(40.501860, -74.446930),'EN':(40.520790, -74.458370),'FBO':(40.525060, -74.462590),'FH':(40.503080, -74.447120),'LSH':(40.52412657652403,-74.43608881983533),'TIL':(40.5219, -74.4360)}


    finalLatitude = 0
    finalLongitude = 0
    for k,v in buildings.items():
        if buildling==k:
            finalLatitude=v[0]
            finalLongitude=v[1]
            break
        
    distance = 999
    closestStop = ''
    closestLatitude = 0
    closestLongitude = 0
    classLocation = str(finalLatitude) + ',' + str(finalLongitude)
    walkingEstimate = ''
    stopToGetOff = ''

    for k,v in stops.items():
        templocation = str(v[0]) + ',' + str(v[1])
        original = gmaps.distance_matrix(templocation,classLocation,mode='walking')['rows'][0]['elements'][0]
        tempdistance = list(original.values())[0]
        tempdistance = list(tempdistance.values())[0]
        tempWalkingDistance = list(original.values())[1]
        tempWalkingDistance = list(tempWalkingDistance.values())[0]
        if tempdistance.endswith(' km'):
            tempdistance = tempdistance[:-3]

        tempdistance = float(tempdistance)

        if (tempdistance < distance):
            distance = tempdistance
            closestStop = k
            closestLatitude = v[0]
            closestLongitude = v[1]
            walkingEstimate = tempWalkingDistance

    # closestBusLocation = str(closestLatitude) + ',' + str(closestLongitude)
    return (closestStop, walkingEstimate)

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

MY_NUMBER = '+12028731360'
client = Client(
    'ACeb6138939e2bed3db062b27e1ff1f0b9',
    '6b8dba6a75710911d8a1982c8ffb6ae7'
)

def bus_to_bus(location,destination,route):

    if STOP_ID[destination] in ROUTES_STOPS[route] and STOP_ID[location] in ROUTES_STOPS[route]:
        url_arrival_estimates = "https://transloc-api-1-2.p.rapidapi.com/arrival-estimates.json"
        querystring_destination_estimates = {"agencies":"1323","stops":STOP_ID[destination],"routes":ROUTE_ID[route]}
        querystring_location_estimates = {"agencies":"1323","stops":STOP_ID[location],"routes":ROUTE_ID[route]}

        url_vehicles = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json"
        querystring_vehicles = {"agencies":"1323"}

       

        response_destination_estimates = requests.request("GET", url_arrival_estimates, headers=headers, params=querystring_destination_estimates)
        response_location_estimates = requests.request("GET", url_arrival_estimates, headers=headers, params=querystring_location_estimates)

        rutgers_location_estimates = response_location_estimates.json()
        rutgers_destination_estimates = response_destination_estimates.json()

        destination_estimates = rutgers_destination_estimates["data"][0]["arrivals"]
        location_estimates = rutgers_location_estimates["data"][0]["arrivals"]

        response_vehicles = requests.request("GET", url_vehicles, headers=headers, params=querystring_vehicles)
        rutgers_vehicles = response_vehicles.json()

        # vehicles = {}
        # for i in rutgers_vehicles["data"]["1323"]:
        #     print(i["route_id"])
        #     if i["route_id"] not in vehicles:
        #         vehicles[i["route_id"]] = i["vehicle_id"]
        
        # vehicle = vehicles[ROUTE_ID[route]]
        if rutgers_location_estimates["data"] == [] or rutgers_destination_estimates["data"] == []:
           return "NO buses i think"
        else:
            location_vehicle_time = {}
            print(type(rutgers_location_estimates["data"]))
            for i in rutgers_location_estimates["data"][0]["arrivals"]:
                print(i)
                location_vehicle_time[i["arrival_at"]] = i["vehicle_id"]
            
            destination_vehicle_time = {}
            for i in rutgers_destination_estimates["data"][0]["arrivals"]:
                print(i)
                destination_vehicle_time[i["arrival_at"]] = i["vehicle_id"]
            
            
            times = []
            for k,v in location_vehicle_time.items():
                for i,j in destination_vehicle_time.items():
                    if v == j:
                        k = parser.parse(k).replace(tzinfo=None)
                        i = parser.parse(i).replace(tzinfo=None)
                        times.append(i-k)
            
            
            times = list(filter(lambda y: y >= 0,list(map(lambda x: x.total_seconds(),times))))
            print(times)
            return min(times)/60
            
    else:
        return -1 #f"{destination} not in {route}"

def sendMessage(time, walk, busTime):
    message = client.messages.create(
        to='+17326924957',
        from_=MY_NUMBER,
        body=f'RU Moving?! You have class soon! It will take {time + busTime} minutes to get there and {walk} minute to get to the bus stop. Get moving now, or you\'re going to be late'
    )
    print(message.sid)

app = Flask(__name__)

@app.route('/getClosestStop')
def getClosestStopRoute():
    latitude = float(request.args['latitude'])
    longitude = float(request.args['longitude'])
    print(latitude, longitude)
    (closestStop, mins) = getClosestStop(latitude, longitude)
    # sendMessage(mins)
    return json.dumps({
        "closestStop": closestStop,
        "mins": mins
    })

@app.route('/getBusPrediction')
def getBusPrediction():
    stop = urllib.parse.unquote(request.args['stop'])
    ests = arrival_Estimate(stop, 'Route Weekend 1')
    return json.dumps({
        "estimates": ests
    })

@app.route('/getBus2Bus')
def getBus2Bus():
    stop = urllib.parse.unquote(request.args['stop'])
    est = bus_to_bus(stop, 'Livingston Student Center', 'Route Weekend 1')
    print(est)
    return json.dumps({
        "estimate": est
    })


@app.route('/sendText')
def sendTextRoute():
    walk = int(request.args['walk'])
    time = int(request.args['time'])
    busTime = int(request.args['busTime'])
    sendMessage(time, walk, busTime)
    return 'succses'