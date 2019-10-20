import googlemaps,json,requests
from math import sin,cos,sqrt,atan2,radians

#Assuming current location is Tillet hall

currentLatitude = 40.5219
currentLongitude = -74.4360
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

print('The nearest stop is ' + closestStartStop + ' and is ' + list(dict2.values())[0] + ' away')