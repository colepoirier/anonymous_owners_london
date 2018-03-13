##Load libraries
import pandas as pd
import time
import missingno as mgno
import re
import matplotlib
import numpy as np
import seaborn as sns
from datetime import datetime
from log_progress import log_progress

##Set styling for numbers (thousand commans, no scientific notaiton etc) and charts
pd.options.display.float_format = '{:20,.2f}'.format
matplotlib.style.use('ggplot')
#%matplotlib inline
##Load October 2015 data
data_2015 = pd.read_csv('oct_2015_ov_data.csv',low_memory=False)
##Load October 2017 data
#data_2017 = pd.read_sql('data',con='sqlite:///data/oct_2017_ov_data_product.sqlite')
##Add in snapshot date
data_2015['date_snapshot'] = pd.to_datetime('2015-10-31')
#data_2017['date_snapshot'] = pd.to_datetime('2017-10-1')
##Combine files into a single dataframe
#data = pd.concat([data_2015,data_2017])
data =data_2015
##Exclude last row which appears to be a summary
data = data[:-1]
##Inspect first few rows of data
data.tail(5)
##Create stacked version of original table which is better for counts
data.columns = ['Title_Number', 'Tenure', 'Property_Address', 'Price_Paid', 'District',\
       'County', 'Region', 'Postcode', '1-Proprietor_Name',\
       '1-Company_Registration', '1-Proprietorship',\
       '1-Country_Incorporated', '1-Proprietor_Address_1',\
       '1-Proprietor_Address_2', '1-Proprietor_Address_3', '2-Proprietor_Name',\
       '2-Company_Registration', '2-Proprietorship',\
       '2-Country_Incorporated', '2-Proprietor_Address_1',\
       '2-Proprietor_Address_2', '2-Proprietor_Address_3', '3-Proprietor_Name',\
       '3-Company_Registration', '3-Proprietorship',\
       '3-Country_Incorporated', '3-Proprietor_Address_1',\
       '3-Proprietor_Address_2', '3-Proprietor_Address_3', '4-Proprietor_Name',\
       '4-Company_Registration', '4-Proprietorship',\
       '4-Country_Incorporated', '4-Proprietor_Address_1',\
       '4-Proprietor_Address_2', '4-Proprietor_Address_3',\
       'Date_Proprietor_Added', 'Additional_Proprietor_Indicator',\
       'Multiple_Address_Indicator','date_snapshot']
data.set_index(['Title_Number','Tenure', 'Property_Address', 'Price_Paid', 'District',\
       'County', 'Region', 'Postcode','Date_Proprietor_Added', 'Additional_Proprietor_Indicator',\
       'Multiple_Address_Indicator','date_snapshot'], inplace=True)
tuples = tuple(data.columns.str.split("-"))
tuples = [x[::-1] for x in tuples]
data.columns = pd.MultiIndex.from_tuples(tuples)
data = data.stack(level = 1)
##data = data.reset_index(level = 1, drop = True)
data = data.reset_index()
data.rename(columns={'level_12': 'Proprietor_Number'},inplace=True)
data.set_index('date_snapshot',inplace=True)
##Create a pseudo unique column for companies which is a combination of first line of address and name. May
##want to bottom this out a bit more
data['Proprietor_Address_1'] = data['Proprietor_Address_1'].fillna('')
data['Proprietor_Name'] = data['Proprietor_Name'].fillna('')
data['unique_company'] = data['Proprietor_Name'] + data['Proprietor_Address_1']
##Size of dataset
print(data.shape)
##Look at how well filled out fields are
mgno.matrix(data_2015)