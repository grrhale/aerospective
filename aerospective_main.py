#  AEROSPECTIVE
#  Data pulled from:
#  EPA government AirNow API: https://www.airnow.gov/
#  and from the National Weather Service API: https://api.weather.gov/

import pandas as pd
import seaborn as sns
import api_module as am

# Ask user 
user_zip = input(f'Please enter your zipcode (#####): ')

latlong = am.get_location(user_zip)

print(latlong)
print(am.zip_square(latlong[0], latlong[1]))

test_f_input = am.zip_square(latlong[0], latlong[1])

test_date_print = am.AirNow_pull(test_f_input[0], 
	test_f_input[1], 
	test_f_input[2], 
	test_f_input[3])

print(test_date_print)
