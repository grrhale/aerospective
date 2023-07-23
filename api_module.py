import config
import pgeocode
import urllib.parse
import requests as re
import json
import pandas as pd
import datetime
import dateutil.relativedelta

# setting enddate (most recent date reported) and startdate (date 3 months previous)
# data is limited due to API limitations - temperatures for the immediate previous
# seven days are not included in the Open Meteo API
enddate = datetime.datetime.now().date() + dateutil.relativedelta.relativedelta(days=-7)
startdate = enddate + dateutil.relativedelta.relativedelta(months=-3)

# function to convert zipcode to coordinates (takes zip, returns coords)
def get_location(zipcode):
	nomi = pgeocode.Nominatim('us')
	a = nomi.query_postal_code(zipcode)
	latitude = a['latitude']
	longitude = a['longitude']
	return(latitude, longitude)

# function to convert coordinates from zipcode/pgeocode to a second set 
#of latlongs, bounding an area of the zipcode location which can be fed 
# to the AirNow API. (AirNow requires two sets of coordinates)
def zip_square(latitude, longitude):
	latmax = (latitude + .5)
	longmax = (longitude + .5)
	
	latmin = (latitude - .5)
	longmin = (longitude - .5)

	return(longmin,latmin,longmax,latmax)

# function to pull air quality data for the past three months from the 
# AirNow API
def AirNow_pull(longmin, latmin, longmax, latmax):

	full_coords = [round(longmin, 4), round(latmin, 4), \
	round(longmax, 4),round(latmax, 4)]
	
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
	
	API_resp = re.get(url_parsed_ready)
	AirNow_data = API_resp.text
	parse_json = json.loads(AirNow_data)

	zip_air_data = pd.json_normalize(parse_json[0:])

	df = pd.DataFrame.from_dict(zip_air_data)
	
	if df.shape[0] == 0:
		print('No EPA data found! If this zipcode is fairly remote,\n'
		'try using a zipcode closer to a population center or known\n'
		'monitoring station.')
		exit()
	
	return(df)

# function to pull weather data for the past three months from the National
# Weather Service API
def meteo_pull(latitude, longitude):
	
	latitude = latitude
	longitude = longitude

	url = 'https://archive-api.open-meteo.com/v1/archive?'
	
	params = {'latitude':round(latitude, 2),
	'longitude':round(longitude, 2),
	'start_date':str(startdate),
	'end_date':str(enddate),
	'hourly':'temperature_2m',
	'temperature_unit':'fahrenheit',
	'windspeed_unit':'mph',
	'precipitation_unit':'inch',
	'timezone':'auto'}
	
	url_parsed_ready = url+urllib.parse.urlencode(params, safe='/,')
	
	API_resp = re.get(url_parsed_ready)
	weather_data = API_resp.text
	parse_json = json.loads(weather_data)
	
	zip_weather_data = pd.json_normalize(parse_json)
	
	df = pd.DataFrame.from_dict(zip_weather_data)
	
	return(df)
