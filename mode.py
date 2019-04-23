'''
This Python script is for Learning purpose on Mode Analytics, applying dataset on their platform.

Arthor: Jeff Zhong
Date: 04/23/19

'''

# Create Dictionaries
city_population = {
	'Tokyo': 1354555,
	'Beijing': 23435,
	'New York': 2345546,
	'San Franscico': 23453,
}

#Print out their keys
print(city_population.keys())
print(type(city_population.keys()))
for i in city_population.keys():
	print(i)
for j in city_population.values():
	print(j)

#Import Packages:
import numpy as np
pop_values = list(city_population.values())
print(pop_values)
print(np.mean(pop_values))

#Pandas DataFrames: It's a table much like in SQL or Excel. It's similar in structure,too
#making it possible to use similar operations such as aggregation, filtering and pivoting. 
import pandas as pd
datasets = pd.read_csv('./watsi.csv')
datasets = pd.DataFrame(datasets)

#The Initial problem of failing to read the csv file is because there's no zero index in the dataset
data = datasets.iloc[:].head(n = 5)
data = data.fillna('')
print(data)
print('\n')
print(data['url'])
print(data.ix[1])

#Counting with .values_counts()
import matplotlib.pyplot as plt
data2 = datasets.iloc[:]
data2 = data2.fillna('')
print('---------------------')
print('Value_counts() starts here:')
print(datasets['title'].value_counts()[:20])
plot = datasets['title'].value_counts()[:20].plot(kind = 'barh')
print('\n')
#Visualize it
#plt.show()
print('---------------------')
print('Top Fifteen referrer starts here:')
homepage_index = (data2['title'] == 'Watsi | Fund medical treatments for people around the world')
watsi_homepage = data2[homepage_index]
print(watsi_homepage['referrer'].value_counts()[:15])
print('\n')
print('---------------------')
print('Top Ten referrer Domains starts here:')
print(watsi_homepage['referrer_domain'].value_counts()[:10])

#Partially matching text with .str.contains()
print('\n')
print('---------------------')
print('Find referrers which contain the word medical:')
medical_referrer_index = data2['referrer'].str.contains('medical')
medical_referrals = data2[medical_referrer_index]
print(medical_referrals)

#Defining Functions:
print(data2['platform'].value_counts())
mobile = ['Apple','Android','Blackberry','Nokia']
def is_in_mobile(platform):
	if platform in mobile:
		print('This is great success.')

is_in_mobile('Blackberry')

#Import the US domestic flights records from the US Department of Transportation:
print('\n')
print('---------------------')
print('Import New File for next project:')
Trans_data = pd.read_csv('./Transportation.csv')
Trans_data = Trans_data.iloc[:].fillna(np.nan)
print(Trans_data.sample(n=5))
print(Trans_data.sort_values(by= 'arr_delay', ascending = False)[:10]['carrier_delay'])

#Calculate the percentage that was delayed:
def is_delayed(x):
	return x > 0
Trans_data['delayed'] = Trans_data['arr_delay'].apply(lambda x: x > 0)

not_delayed = Trans_data['delayed'].value_counts()[0]
delayed = Trans_data['delayed'].value_counts()[1]
total_flights = not_delayed + delayed
print ("Percentage of delayed is:" ,(float(delayed)/total_flights))

#Playing with the Group-by function:
print('\n')
print('---------------------')
print('Python Group By Function:')
group_by_carrier = Trans_data.groupby(['unique_carrier','delayed'])
print(group_by_carrier.size())
unstack = group_by_carrier.size().unstack()
print(unstack)
unstack.plot(kind = 'barh', stacked = True, figsize = [16,6], colormap = 'winter')
# plt.show()

#Pivot Table:
print('\n')
print('---------------------')
print('Pivot Table starts from here:')
flights_by_carrier = Trans_data.pivot_table(index = 'flight_date', columns = 'unique_carrier', values = 'flight_num', aggfunc = 'count')
print(flights_by_carrier.head())
delayed_list = ['carrier_delay','weather_delay', 'late_aircraft_delay', 'nas_delay', 'security_delay']
flight_delay_by_day = Trans_data.pivot_table(index = 'flight_date', values = delayed_list, aggfunc = 'sum')
print(flight_delay_by_day)
flight_delay_by_day.plot(kind = 'area', figsize = [16,6], stacked = True, colormap = 'autumn')
# plt.show()

delayed_flights = Trans_data[Trans_data['delayed'] == True]
print(delayed_flights['unique_carrier'].value_counts())
delayed_by_carrier = Trans_data.groupby(['unique_carrier','delayed']).size().unstack().reset_index()
delayed_by_carrier['flights_count'] = (delayed_by_carrier[False] + delayed_by_carrier[True])
delayed_by_carrier['proportion_delayed'] = delayed_by_carrier[True]/delayed_by_carrier['flights_count']
print(delayed_by_carrier.sort_values('proportion_delayed', ascending = False))

#Plotting Histogram:
bin_values = np.arange(start = -50, stop = 200, step = 10)
us_mq_airlines_index = Trans_data['unique_carrier'].isin(['US', 'MQ'])
us_mq_airlines = Trans_data[us_mq_airlines_index]
group_carrier = us_mq_airlines.groupby('unique_carrier')['arr_delay']
print(group_carrier.describe())
print(group_carrier)
# group_carrier.plot(kind = 'hist', bins = bin_values, figsize = [16,6], alpha = .4, legend = True)
plt.show()

