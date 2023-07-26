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
import matplotlib.pyplot as plt
import api_module as am
import data_module as dm

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

# merge OpenMeteo and AirNow data to put all useful data in the same 
# dataframe
df_aerospective = weather_data.merge(airqual_data, left_on='Date', right_on='Date')

# visualize our data
worst_title = 'Worst days for high AQI and high mean temperature in\nthe past three months around zipcode ' + user_zip

f, axes = plt.subplots(1, 3, sharex=False)
sns.despine(left=False)

worstdata = dm.tenworst_days(df_aerospective)
worst_chart = sns.barplot(data=worstdata.reset_index(), x='Date', y='AQI')

worst_chart.set(title = worst_title)
worst_chart.set_xticklabels(worst_chart.get_xticklabels(), rotation=45, fontsize=10, horizontalalignment='right')

plt.tight_layout()
plt.show()

print(dm.tenworst_days(df_aerospective))

