"""
 AEROSPECTIVE
 Data pulled from:
 EPA government AirNow API (Air Quality): https://www.airnow.gov/
 Open Meteo (Historical temperature data): https://open-meteo.com/
 This program relies on United States ZIP codes to draw data; it is
 currently only useful within the United States.
"""

import pandas as pd
import seaborn as sns
import api_module as am
import data_module as dm
import csv

# Ask user for area they want data for (zipcode in 5 digit format) 
user_zip = input(f'Please enter your zipcode (#####): ')

# Assign a latitude and longitude to the latlong var from user's input
latlong = am.get_location(user_zip)

# Convert that latitude and longitude into a second lat/long, to meet the
# AirNow API's requirements to return data
AirNow_input = am.zip_square(latlong[0], latlong[1])

# Pull data from AirNow, using the second generated latitude/longitude
AirNow_data = am.AirNow_pull(AirNow_input[0], 
	AirNow_input[1], 
	AirNow_input[2], 
	AirNow_input[3])

# Pull data from OpenMeteo, using the latitude and longitude generated
# from the user's zipcode
weather_data_raw = am.meteo_pull(latlong[0], latlong[1])

# Clean the OpenMeteo data to prepare it for merge with AirNow data
weather_data = dm.weather_data_clean(weather_data_raw['hourly.time'], 
	weather_data_raw['hourly.temperature_2m'])

# Clean the AirNow data to prepare it for merge with OpenMeteo data
airqual_data = dm.airqual_data_clean(AirNow_data)

# Merge OpenMeteo and AirNow data
df_aerospective = weather_data.merge(airqual_data, left_on='UTC', right_on='UTC')

print(df_aerospective)

