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
# also checks if zipcode fits required parameters (is a 5 digit number)
def get_location(zipcode):
	if len(zipcode) != 5:
		print('Not a valid zipcode.')
		exit()
	elif type(zipcode) != int:
		nomi = pgeocode.Nominatim('us')
		a = nomi.query_postal_code(zipcode)
		latitude = a['latitude']
		longitude = a['longitude']
	else:
		print('Not a valid zipcode.')
		exit()
	return(latitude, longitude)

# function to convert coordinates from zipcode/pgeocode to a minimum and maximum
# roughly encompassing the zipcode location which can be fed 
# to the AirNow API. (AirNow requires two sets of coordinates, and generates a rectangle
# from them to create a boundary)
def zip_square(latitude, longitude):
	latmax = (latitude + .25)
	longmax = (longitude + .25)
	
	latmin = (latitude - .25)
	longmin = (longitude - .25)

	return(longmin,latmin,longmax,latmax)

# function to pull air quality data for the past three months from the 
# AirNow API, using the minimum and maximum generated by zip_square
def AirNow_pull(longmin, latmin, longmax, latmax):
	
	# list all coordinates
	full_coords = [round(longmin, 4), round(latmin, 4), \
	round(longmax, 4),round(latmax, 4)]
	
	# build/encode the url to get data from the API, setting all
	# parameters including coords and API key from config.py
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
	
	# allow '/' ',' and '+' characters in URL as AirNow requires them
	url_parsed = url+urllib.parse.urlencode(params, safe='/,')
	transl_table = dict.fromkeys(map(ord, '+'), None)
	
	# assign url to var
	url_parsed_ready = url_parsed.translate(transl_table)
	
	# get data, load it into dataframe, and return it unless it is empty
	API_resp = re.get(url_parsed_ready)
	AirNow_data = API_resp.text
	parse_json = json.loads(AirNow_data)

	zip_air_data = pd.json_normalize(parse_json)

	df = pd.DataFrame.from_dict(zip_air_data)
	
	# if the url returned no data, there likely isn't a single monitoring
	# station within the bounding square. let the user know. station 
	# locations can be checked here: https://fire.airnow.gov/
	if df.shape[0] == 0:
		print('No EPA data found! If this zipcode is fairly remote,\n'
		'try using a zipcode closer to a population center or known\n'
		'monitoring station.')
		exit()
	
	return(df)

# function to pull weather data for the past three months from the
# OpenMeteo API
def meteo_pull(latitude, longitude):
	
	# assign lat and long to vars to work with them
	latitude = latitude
	longitude = longitude
	
	# build/encode the url to get data from the API, setting all
	# parameters
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
	
	# assign url to var
	url_parsed_ready = url+urllib.parse.urlencode(params, safe='/,')
	
	# get data, load it into a dataframe, and return it
	API_resp = re.get(url_parsed_ready)
	weather_data = API_resp.text
	parse_json = json.loads(weather_data)
	
	zip_weather_data = pd.json_normalize(parse_json)
	
	df = pd.DataFrame.from_dict(zip_weather_data)
	
	return(df)
