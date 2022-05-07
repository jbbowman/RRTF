import openrouteservice
import json
import folium
from openrouteservice import convert

def f1():
 client = openrouteservice.Client(key='5b3ce3597851110001cf6248306ecbc8079946f483cba81d17c4144a')
 coords = ((80.21787585263182,6.025423265401452),(80.23929481745174,6.019639381180123))
 geometry = client.directions(coords)['routes'][0]['geometry']
 decoded = convert.decode_polyline(geometry)
 print(decoded)

 m = folium.Map(location=[6.074834613830474, 80.25749815575348], zoom_start=10, control_scale=True, tiles="cartodbpositron")
 folium.GeoJson(decoded).add_to(m)

 m.save('map.html')


def f2():
 import openrouteservice
 """ - setup openrouteservice client with api key, you can signup https://openrouteservice.org 
       if you don't have API key. Its totaly free😊
     - After signup, you can see your API key available under the dashboard tab.
 """
 client = openrouteservice.Client(key='5b3ce3597851110001cf6248306ecbc8079946f483cba81d17c4144a')
 # set location coordinates in longitude,latitude order
 coords = ((44.96629100000001, -93.27985849446074), (45.30056500000001, -93.34716400000001))
 # call API
 res = client.directions(coords)
 # test our response
 with(open('test.json', '+w')) as f:
  f.write(json.dumps(res, indent=4, sort_keys=True))


def f3():
 client = openrouteservice.Client(key='5b3ce3597851110001cf6248306ecbc8079946f483cba81d17c4144a')
 coords = ((-93.347164, 45.300565), (-93.347164, 45.300565))

 geometry = client.directions(coords)['routes'][0]['geometry']
 decoded = convert.decode_polyline(geometry)
 print(decoded)
 res = client.directions(coords)
 duration = round(res['routes'][0]['summary']['distance']/1000,1)

 print(duration)

def f4():
 client = openrouteservice.Client(key='5b3ce3597851110001cf6248306ecbc8079946f483cba81d17c4144a')
 coords = ((-93.347164, 45.300565), (-93.347164, 45.300565))
 # call API
 res = client.directions(coords)
 # test our response
 with(open('test.json', '+w')) as f:
  f.write(json.dumps(res, indent=4, sort_keys=True))

f3()