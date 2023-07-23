import pandas as pd

def weather_data_clean(dataframe1, dataframe2):

	d_list = dataframe1[0]
	t_list = dataframe2[0]
	
	d_df = pd.DataFrame(d_list)
	t_df = pd.DataFrame(t_list)

	weather_dataframe = pd.concat([d_df, t_df], axis=1)
	
	return(weather_dataframe)
