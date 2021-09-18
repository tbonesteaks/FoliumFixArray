import os
import time
import datetime
from dateutil.parser import parse
import pandas as pd
import numpy as np

##This file is set up for you to play with regex pulls from a dataframe off of the CSV root.py uses.
##IF you already downloaded the CSV from the city of Denver, this part is setting everything else up for you.
##IF you changed the place where your CSV file resides, please amend the variables...

folder = 'data'
file = 'crime.csv'
file_path = os.path.join(folder, file)
crime = pd.read_csv(file_path)
print(crime)

##If you see the data pop out when your run this the first time, everything worked. 
## Uncomment the rows below to start searching the data... 
c20 = crime[crime['REPORTED_DATE'].str.contains(r'(?!$)2020(?!$)')]
print(c20)
length = c20.shape[0]

