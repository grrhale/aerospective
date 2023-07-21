import config
import pgeocode
import urllib.parse
import requests as re
import json
import pandas as pd
from datetime import date
from datetime import datetime

# function to convert zipcode to coordinates
def get_location(zipcode):
	nomi = pgeocode.Nominatim('us')
	a = nomi.query_postal_code(zipcode)
	lati = a['latitude']
	longi = a['longitude']
	return(lati, longi)

# function to convert coordinates from zipcode to a second set of latlongs,
# bounding an area of the zipcode location which can be fed to the AirNow API
def zip_square(latitude, longitude):
	latmin = latitude
	longmin = longitude

	if latmin > 0:
		latmax = (latitude + .4000)
	elif latmin <= 0:
		latmax = (latitude + .4000)
	else: exit()

	if longmin > 0:
		longmax = (longitude - .4000)
	elif longmin <= 0:
		longmax = (longitude - .4000)
	else: exit()

	return(longmax,latmax,longmin,latmin)

# function to pull air quality data for the year from the AirNow API
def AirNow_pull(longmax, latmax, longmin, latmin):
	full_coords = [round(longmax, 4), round(latmax, 4), round(longmin, 4), round(latmin, 4)]
	print(full_coords)
	enddate = date.today()
	startdate = datetime.now().date().replace(month=1, day=1)
	
	url = 'https://www.airnowapi.org/aq/data/?'
	params = {'startDate':str(startdate)+'T00',
	'endDate':str(enddate)+'T00',
	'parameters':'PM25',
	'BBOX':full_coords,
	'dataType':'A',
	'format':str('application/json'),
	'verbose':0,
	'monitorType':0,
	'includerawconcentrations':0,
	'API_KEY':config.API_key}

	#API_resp = re.get(url)
	#data = API_resp.text
	#parse_json = json.loads(data)
	return(url+urllib.parse.urlencode(params, safe='/'))
	#air_qual_data = pd.json_normalize(parse_json['data'])


# airnow API pull example: 
# https://www.airnowapi.org/aq/data/?startDate=2023-01-01T00&endDate=2023-07-19T00&parameters=PM25&BBOX=-86.2405,37.7174,-85.7404,38.2174&dataType=A&format=application/json&verbose=0&monitorType=0&includerawconcentrations=0&API_KEY=

"""
import urllib.parse
url = 'https://example.com/somepage/?'
params = {'var1': 'some data', 'var2': 1337}
print(url + urllib.parse.urlencode(params))
https://example.com/somepage/?var1=some+data&var2=1337
"""
