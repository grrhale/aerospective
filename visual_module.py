import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.lines import Line2D
import data_module as dm
	
	# function to generate a seaborn plot of the worst and the
	# best days to be outside determined by low/high AQI and low/high temperature
def plot_days(df, zipcode, a):
	# set title for this plot as str to var to save space
	worstd_title = 'Worst days for high AQI and high mean temperature over\nthe past three months in/around zipcode ' + zipcode
	bestd_title = 'Best days for low AQI and low mean temperature over\n the past three months in/around zipcode ' + zipcode
	# use data module to sort the data for temp/aqi and assign the df
	# if passed a 0, sort the worst days, if passed a 1, sort the best
	if a == 0:
		data = dm.tenworst_days(df).reset_index()
	elif a == 1:
		data = dm.tenbest_days(df).reset_index()
		
	# set up seaborn barplot for AQI
	chart = sns.barplot(x=data['Date'], 
		y=data['AQI'], 
		color='b')
	
	if a == 0:
		chart.set(title = worstd_title)
	elif a == 1:
		chart.set(title = bestd_title)

	# calculate scaling to put temp/AQI in the same chart
	width_scale = 0.45
	for bar in chart.containers[0]:
		bar.set_width(bar.get_width() * width_scale)

	chart2 = chart.twinx()
	sns.barplot(x=data['Date'], 
		y=data['Mean Temperature(°F)'], 
		alpha=0.7, 
		ax=chart2, 
		color='r')

	for bar in chart2.containers[0]:
		x = bar.get_x()
		w = bar.get_width()
		bar.set_x(x+w * (1- width_scale))
		bar.set_width(w * width_scale)
	# set tick label configuration
	chart.set_xticklabels(chart.get_xticklabels(), rotation=45, fontsize=10, horizontalalignment='right')

	# manually set up legend so colors and labels make sense, then plot
	AQI_leg = Line2D([],[],color='blue', label='AQI')
	mtemp_leg = Line2D([],[],color='lightcoral', label='Mean Temp')
	plt.legend(bbox_to_anchor=(1.05, 1), handles=[AQI_leg, mtemp_leg], frameon=False)
	plt.tight_layout()
	plt.show()

