# Reads in the raw (converted negative) csv and creates a date/time stamp that will match the format of accel files, during second round (when new files were obtained from external HD, the negative Longitude values were calculated in this script
import numpy as np
import pandas as pd
import os
import datetime

# Defining file path
file = "./path/to/gps"
# creating name for end merge document
name = os.path.splitext(os.path.basename(file))[0]
# Read in data and parse date/time to DateTime format
data = pd.read_csv(file,parse_dates=[[5,6]])
# New coloumn to convert longitude into a negative quadrant
data['long_1']= data['LONGITUDE'].apply(lambda x: x*-1)
# New column that allows join to be made
data['date_stamp'] = pd.to_datetime(data['LOCAL DATE_LOCAL TIME'],dayfirst=False)
#output
out= "./path/out/" +name
# saving new file to csv
data.to_csv(out +'_neg_stmp.csv' ,date_format='%Y%m%d %H:%M:%S')

### New File originally
# Reads in the raw csv and creates a date/time stamp that will match the format of GPS files, new acti from external HD had the date format reversed day was not first

 # Defining file path
 file = "./path/to/accel"
 # Read in data and parse date/time to DateTime format
 data = pd.read_csv(file,header=10,parse_dates=[[0,1]],dayfirst=False)
 # New column that allows join to be made
 data['date_stamp'] = pd.to_datetime(data['Date_ Time'],dayfirst=False)
 # creating name for end merge document
 name = os.path.splitext(os.path.basename(file))[0]
 #output
 out= "./path/out/" +name
 # saving new file to csv
 data.to_csv(out +'_stmp.csv' ,date_format='%Y%m%d %H:%M:%S')



### New File originally
 # Merges accel and gps files based on time

 # directing filepath to csv documents for both GPS and accel data
 gps = "./path/to/gps/"
 accel =  "./path/to/accel"

 # creating name for end merge document
 name = os.path.splitext(os.path.basename(gps))[0]

 date = '%Y-%m-%d %H:%M:%S'

 # function to read both date_stamp columns for merging
 dateparse= lambda x: pd.to_datetime(x, unit='s')

 # Reading in the csv's including a date parser to read date_stamp as datetime object
 gps_dat = pd.read_csv(gps, parse_dates=['date_stamp'],date_parser=dateparse)
 accel_dat = pd.read_csv(accel,parse_dates=['date_stamp'],date_parser=dateparse)

 # Making the time stamp an index and resampling/merging on the timestamp. Skipped values are left blank
 merged = (accel_dat.set_index('date_stamp')
     .resample('5S')
     .last()
     .join(gps_dat.set_index('date_stamp')
         .resample('5S')
         .last(),
     rsuffix='_r')
 )

 # Dropping temp. columns for merge
 merged = merged.drop('Unnamed: 0' ,1)
 merged = merged.drop('Unnamed: 0_r', 1)

 # Creating file that keeps track of accel that doesn't have location data
 drp_gps = pd.isnull(merged)
 drp_gps = drp_gps[drp_gps['long_1'] == True]
 drp_num = drp_gps.count()

 # Removing data without a location
 merged = merged.dropna(subset=['long_1'],how='all')


 # Defining path and saving csv
 out_path = "./out/path"+name
 merged.to_csv(out_path +'_merg.csv' ,date_format=date)
 drp_gps.to_csv(out_path +'_drp.csv' ,date_format=date)
 drp_num.to_csv(out_path + '_count.csv')
