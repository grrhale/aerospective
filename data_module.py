import pandas as pd

# function to clean weather data and narrow it to day by day mean
# temperature, rather than hour by hour temperature readings
def weather_data_clean(dataframe1, dataframe2):

	date_list = dataframe1[0]
	temp_list = dataframe2[0]
	
	date_df = pd.DataFrame(date_list)
	temp_df = pd.DataFrame(temp_list)

	weather_dataframe = pd.concat([date_df, temp_df], axis=1)
	weather_dataframe.columns=['Date', 'Mean Temperature(°F)']
	
	weather_dataframe['Date'] = weather_dataframe.apply(lambda x:
		x['Date'][:-6], axis = 1)
	weather_dataframe = weather_dataframe.groupby(['Date']).mean()
	
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
	airqual_dataframe.columns=['Date', 'AQI']
	airqual_dataframe['Date'] = airqual_dataframe.apply(lambda x:
		x['Date'][:-6], axis = 1)
	airqual_dataframe = airqual_dataframe.groupby(['Date']).mean()
	
	return(airqual_dataframe)
	
# function to find which ten dates have the worst overall temperature and
# worst overall air quality (highest temp/AQI combination)
def tenworst_days(dataframe):
	
	df_wo_lowtemps = dataframe[~(dataframe['Mean Temperature(°F)'] <= 75)]

	df_AQI_ordered = df_wo_lowtemps.sort_values('AQI')
	
	return(df_AQI_ordered.tail(10))

# function to find which ten dates have the best overall temperature and
# best overall air quality (lowest temp/AQI combination)
def tenbest_days(dataframe):
	
	df_wo_hightemps = dataframe[~(dataframe['Mean Temperature(°F)'] >= 74)]

	df_AQI_ordered = df_wo_hightemps.sort_values('AQI', ascending=False)
# ascending is set to false so the best date will be plotted on the right
# side of our output graph
	return(df_AQI_ordered.tail(10))
	
# function to find which of 3 possible 30 day spans have the best overall
# AQI and temperature combination
def best30(dataframe):
	first_30 = dataframe[0:31]
	second_30 = dataframe[31:62]
	third_30 = dataframe[62:93]
	
	first_30_ranked = first_30[['AQI','Mean Temperature(°F)']].mean()
	first_30_title = list(first_30.index[0]) # first_30.iloc[0, 31]
	
	return(first_30_ranked, first_30_title)
