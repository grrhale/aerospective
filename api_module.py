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
		latmax = (latitude - .2500)
	elif latmin <= 0:
		latmax = (latitude - .1500)
	else: exit()

	if longmin > 0:
		longmax = (longitude - .2500)
	elif longmin <= 0:
		longmax = (longitude - .2500)
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
	'BBOX':str(full_coords)[1:-1],
	'dataType':'A',
	'format':str('application/json'),
	'verbose':0,
	'monitorType':0,
	'includerawconcentrations':0,
	'API_KEY':config.API_key}

	#API_resp = re.get(url)
	#data = API_resp.text
	#parse_json = json.loads(data)
	url_parsed = url+urllib.parse.urlencode(params, safe='/,')
	
	transl_table = dict.fromkeys(map(ord, '+'), None)
	url_parsed_ready = url_parsed.translate(transl_table)
	
	return(url_parsed_ready)
	#air_qual_data = pd.json_normalize(parse_json['data'])
