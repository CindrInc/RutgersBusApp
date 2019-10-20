import googlemaps,json,requests,urllib, urllib3,urllib.parse
from math import sin,cos,sqrt,atan2,radians
from urllib.parse import urlencode


gmaps = googlemaps.Client(key = 'AIzaSyByZ1krKUMWCADrjkGIYty8F3-vfTtcdEQ')

#Assuming final destination is Academic Building, change for later


# url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((
#             ('origin', closestBusLocation),
#             ('destination', classLocation)
#  ))
# ur = urllib.request.urlopen(url)
# result = json.load(ur)

# for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
#     j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] 
#     print (j)
#     print(i)
#     break