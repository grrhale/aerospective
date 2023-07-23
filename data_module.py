import pandas as pd

# function to clean weather data and narrow it to day by day mean
# temperature, rather than hour by hour temperature readings
def weather_data_clean(dataframe1, dataframe2):

	date_list = dataframe1[0]
	temp_list = dataframe2[0]
	
	date_df = pd.DataFrame(date_list)
	temp_df = pd.DataFrame(temp_list)

	weather_dataframe = pd.concat([date_df, temp_df], axis=1)
	weather_dataframe.columns=['UTC', 'Temperature(°F)']
	
	weather_dataframe['UTC'] = weather_dataframe.apply(lambda x:
		x['UTC'][:-6], axis = 1)
	weather_dataframe = weather_dataframe.groupby(['UTC']).mean()
	
	return(weather_dataframe)

# function to clean AirNow data: narrows it from hour-by-hour to 
# day-by-day and produces an mean air quality reading for each day in 
# the last 3 months (in PM2.5) by averaging all available weather station
# data
def airqual_data_clean(dataframe):
	
	date_list = dataframe['UTC']
	AQI_PM25_list = dataframe['AQI']
	
	date_df = pd.DataFrame(date_list)
	AQI_PM25_df = pd.DataFrame(AQI_PM25_list)
	
	airqual_dataframe = pd.concat([date_df, AQI_PM25_df], axis=1)
	airqual_dataframe['UTC'] = airqual_dataframe.apply(lambda x:
		x['UTC'][:-6], axis = 1)
	airqual_dataframe = airqual_dataframe.groupby(['UTC']).mean()
	
	return(airqual_dataframe)
