"""
 AEROSPECTIVE
 Data pulled from:
 EPA government AirNow API (Air Quality): https://www.airnow.gov/
 Open Meteo (Historical temperature data): https://open-meteo.com/
 This program relies on United States ZIP codes to draw data; it is
 currently only useful within the United States.
"""
import pandas as pd
import api_module as am
import data_module as dm
import visual_module as vm

# ask user for area they want data for (zipcode in 5 digit format) 
user_zip = input(f'Please enter your zipcode (#####): ')

# assign a latitude and longitude to the latlong var from user's input
latlong = am.get_location(user_zip)

# convert that latitude and longitude into a second lat/long, to meet the
# airNow API's requirements to return data
AirNow_input = am.zip_square(latlong[0], latlong[1])

# pull data from AirNow, using the second generated latitude/longitude
AirNow_data = am.AirNow_pull(AirNow_input[0], 
	AirNow_input[1], 
	AirNow_input[2], 
	AirNow_input[3])

# pull data from OpenMeteo, using the latitude and longitude generated
# from the user's zipcode
weather_data_raw = am.meteo_pull(latlong[0], latlong[1])

# clean the OpenMeteo data to prepare it for merge with AirNow data
weather_data = dm.weather_data_clean(weather_data_raw['hourly.time'], 
	weather_data_raw['hourly.temperature_2m'])

# clean the AirNow data to prepare it for merge with OpenMeteo data
airqual_data = dm.airqual_data_clean(AirNow_data)

# merge OpenMeteo and AirNow data to put all useful data into the same 
# dataframe
df_aerospective = weather_data.merge(airqual_data, left_on='Date', right_on='Date')

# visualize our data:   
# create figure for the days with the worst aqi/temp in the past three months
vm.plot_days(df_aerospective, user_zip, 0)
# create figure for the days with the best aqi/temp in the past three months
vm.plot_days(df_aerospective, user_zip, 1)

print(dm.best30(df_aerospective))

