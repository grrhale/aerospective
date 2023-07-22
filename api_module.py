import config
import pgeocode
import urllib.parse
import requests as re
import json
import pandas as pd
import datetime
import dateutil.relativedelta

# function to convert zipcode to coordinates
def get_location(zipcode):
	nomi = pgeocode.Nominatim('us')
	a = nomi.query_postal_code(zipcode)
	latitude = a['latitude']
	longitude = a['longitude']
	return(latitude, longitude)

# function to convert coordinates from zipcode to a second set of latlongs,
# bounding an area of the zipcode location which can be fed to the AirNow API
def zip_square(latitude, longitude):
	latmax = (latitude + .5)
	longmax = (longitude + .5)
	
	latmin = (latitude - .5)
	longmin = (longitude - .5)

	return(longmin,latmin,longmax,latmax)

# function to pull air quality data for the past three months from the 
# AirNow API
def AirNow_pull(longmin, latmin, longmax, latmax):

	full_coords = [round(longmin, 4), round(latmin, 4), round(longmax, 4), round(latmax, 4)]
	print(full_coords)
	
	enddate = datetime.datetime.now().date()
	startdate = enddate + dateutil.relativedelta.relativedelta(months=-3)
	
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
	
	url_parsed = url+urllib.parse.urlencode(params, safe='/,')
	
	transl_table = dict.fromkeys(map(ord, '+'), None)
	url_parsed_ready = url_parsed.translate(transl_table)
	print(url_parsed_ready)
	
	API_resp = re.get(url_parsed_ready)
	AirNow_data = API_resp.text
	parse_json = json.loads(AirNow_data)

	zip_air_data = pd.json_normalize(parse_json[0:])

	df = pd.DataFrame.from_dict(zip_air_data)
	
	return(df)
