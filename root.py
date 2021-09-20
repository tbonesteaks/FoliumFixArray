import os
import time
import datetime
from dateutil.parser import parse
import shutil
import requests
import wget
import pandas as pd
import numpy as np
import folium
from folium import plugins


##Function to download csv if newer version exists.
def download(url: str, dest_folder: str, fname: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    file_path = os.path.join(dest_folder, fname)
     
    if os.path.exists(file_path):
        ftime = time.ctime(os.path.getctime(file_path))
        print(ftime)
    else:
        ftime = "January 1, 1990"
        print(ftime)

    r = requests.get(url, stream=True)
    if r.ok:
        url_date = r.headers['Date']
        print(url_date)    
    ##parse those dates
    datef = parse(ftime)
    print(datef.date())
    dateurl = parse(url_date)
    print(dateurl.date())

    if dateurl.date() < datef.date() or dateurl.date() == datef.date() :
        print("Using existing csv --> No need to download up to date existing file.")
    else:    
        if os.path.exists(file_path):
            print("Moving old Version of CSV to .old")
            destination = fname + ".old"
            dest_path = os.path.join(dest_folder, destination)
            shutil.move(os.path.abspath(file_path), os.path.abspath(dest_path))
            print("File moved successfully.")

        print("saving to", os.path.abspath(file_path))
        ##Downloading the file with wget
        wget.download(url, out=file_path)
##End download function

##Let's map some crime data...
## Start by setting variables for folder and file
folder = 'data'
file = 'crime.csv'
## Call download function with filename and folder vars
download("https://www.denvergov.org/media/gis/DataCatalog/crime/csv/crime.csv", dest_folder=folder, fname=file ,)

##When that all works, let's set file_path as a global variable (because above it is a function variable) and load the csv into a pandas dataframe
file_path = os.path.join(folder, file)
crime = pd.read_csv(file_path)
print(crime)
##When everything works, you just saw a dataframe pop out on the command line
##The stdout shows how many rows we have and the columns too
##First make 3 empty arrays for coords, next we'll use shape to get the array size value into a variable

coords = []
ccoords = []
tcoords = []

length = crime.shape[0]
print("Length of array: " + str(length) + " rows to pull coords from.")

##Python just told us how many rows we need to pull the coordinates from, and we have an empty array to append to. Let's START that LOOP.
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if crime['GEO_LAT'].values[a] > 15 :
        coords.append([crime['GEO_LAT'].values[a],crime['GEO_LON'].values[a]])
        ##IF the coordinates are good, then we need to test for crime or traffic and append accordingly
        if crime['IS_CRIME'].values[a] > 0:        
            ccoords.append([crime['GEO_LAT'].values[a],crime['GEO_LON'].values[a]])
        else:
            tcoords.append([crime['GEO_LAT'].values[a],crime['GEO_LON'].values[a]])

##Now let's see our new arrays - usually leave these next three lines commented out, they populate over a million coords to stdout
#print(coords)
#print(ccoords)
#print(tcoords)


##Create three maps from a map center point, add_child to the map, via HeatMap Plugin, and dump the array of coordinates
##You'll need a path to save the file, and then export the file to that path

mapcenter = [39.739433,-104.888853]
cmap = folium.Map(mapcenter,zoom_start=11)
cmap.add_child(plugins.HeatMap(coords, radius=25))
cmapsave =  os.path.join(folder , "mapout.html")
cmap.save(outfile=cmapsave)


ccmap = folium.Map(mapcenter,zoom_start=11)
ccmap.add_child(plugins.HeatMap(ccoords, radius=25))
ccmapsave = os.path.join(folder , "cmapout.html")
ccmap.save(outfile=ccmapsave)

tsmap = folium.Map(mapcenter,zoom_start=11)
tsmap.add_child(plugins.HeatMap(tcoords, radius=25))
tsmap
tsmapsave = os.path.join(folder ,"tmapout.html")
tsmap.save(outfile=tsmapsave)

## Delete those array variables to recover the ram
del cmap
del ccmap
del tsmap
del coords
del ccoords
del tcoords

##set new empty arrays for the first annual pull
coords = []
ccoords = []
tcoords = []
##we need to make a new dataframe from crime, with only 2021 values
c21 = crime[crime['REPORTED_DATE'].str.contains(r'(?!$)2021(?!$)')]
print(c21)
length = c21.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if c21['GEO_LAT'].values[a] > 15 :
        coords.append([c21['GEO_LAT'].values[a],c21['GEO_LON'].values[a]])
        ##IF the coordinates are good, then we need to test for crime or traffic and append accordingly
        if c21['IS_CRIME'].values[a] > 0:        
            ccoords.append([c21['GEO_LAT'].values[a],c21['GEO_LON'].values[a]])
        else:
            tcoords.append([c21['GEO_LAT'].values[a],c21['GEO_LON'].values[a]])

cmap = folium.Map(mapcenter,zoom_start=11)
cmap.add_child(plugins.HeatMap(coords, radius=7))
cmapsave =  os.path.join(folder , "mapout21.html")
cmap.save(outfile=cmapsave)


ccmap = folium.Map(mapcenter,zoom_start=11)
ccmap.add_child(plugins.HeatMap(ccoords, radius=7))
ccmapsave = os.path.join(folder , "cmapout21.html")
ccmap.save(outfile=ccmapsave)

tsmap = folium.Map(mapcenter,zoom_start=11)
tsmap.add_child(plugins.HeatMap(tcoords, radius=7))
tsmap
tsmapsave = os.path.join(folder ,"tmapout21.html")
tsmap.save(outfile=tsmapsave)

## Delete those array variables to recover the ram
del cmap
del ccmap
del tsmap
del coords
del ccoords
del tcoords

##set new empty arrays for the next annual pull
coords = []
ccoords = []
tcoords = []
##we need to make a new dataframe from crime, with only 2020 values
c20 = crime[crime['REPORTED_DATE'].str.contains(r'(?!$)2020(?!$)')]
print(c20)
length = c20.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if c20['GEO_LAT'].values[a] > 15 :
        coords.append([c20['GEO_LAT'].values[a],c20['GEO_LON'].values[a]])
        ##IF the coordinates are good, then we need to test for crime or traffic and append accordingly
        if c20['IS_CRIME'].values[a] > 0:        
            ccoords.append([c20['GEO_LAT'].values[a],c20['GEO_LON'].values[a]])
        else:
            tcoords.append([c20['GEO_LAT'].values[a],c20['GEO_LON'].values[a]])

cmap = folium.Map(mapcenter,zoom_start=11)
cmap.add_child(plugins.HeatMap(coords, radius=7))
cmapsave =  os.path.join(folder , "mapout20.html")
cmap.save(outfile=cmapsave)


ccmap = folium.Map(mapcenter,zoom_start=11)
ccmap.add_child(plugins.HeatMap(ccoords, radius=7))
ccmapsave = os.path.join(folder , "cmapout20.html")
ccmap.save(outfile=ccmapsave)

tsmap = folium.Map(mapcenter,zoom_start=11)
tsmap.add_child(plugins.HeatMap(tcoords, radius=7))
tsmap
tsmapsave = os.path.join(folder ,"tmapout20.html")
tsmap.save(outfile=tsmapsave)


## Delete those array variables to recover the ram
del cmap
del ccmap
del tsmap
del coords
del ccoords
del tcoords

##set new empty arrays for the next annual pull
coords = []
ccoords = []
tcoords = []
##we need to make a new dataframe from crime, with only 2019 values
c19 = crime[crime['REPORTED_DATE'].str.contains(r'(?!$)2019(?!$)')]
print(c19)
length = c19.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if c19['GEO_LAT'].values[a] > 15 :
        coords.append([c19['GEO_LAT'].values[a],c19['GEO_LON'].values[a]])
        ##IF the coordinates are good, then we need to test for crime or traffic and append accordingly
        if c19['IS_CRIME'].values[a] > 0:        
            ccoords.append([c19['GEO_LAT'].values[a],c19['GEO_LON'].values[a]])
        else:
            tcoords.append([c19['GEO_LAT'].values[a],c19['GEO_LON'].values[a]])

cmap = folium.Map(mapcenter,zoom_start=11)
cmap.add_child(plugins.HeatMap(coords, radius=7))
cmapsave =  os.path.join(folder , "mapout19.html")
cmap.save(outfile=cmapsave)


ccmap = folium.Map(mapcenter,zoom_start=11)
ccmap.add_child(plugins.HeatMap(ccoords, radius=7))
ccmapsave = os.path.join(folder , "cmapout19.html")
ccmap.save(outfile=ccmapsave)

tsmap = folium.Map(mapcenter,zoom_start=11)
tsmap.add_child(plugins.HeatMap(tcoords, radius=7))
tsmap
tsmapsave = os.path.join(folder ,"tmapout19.html")
tsmap.save(outfile=tsmapsave)


## Delete those array variables to recover the ram
del cmap
del ccmap
del tsmap
del coords
del ccoords
del tcoords

##set new empty arrays for the next annual pull
coords = []
ccoords = []
tcoords = []
##we need to make a new dataframe from crime, with only 2018 values
c18 = crime[crime['REPORTED_DATE'].str.contains(r'(?!$)2018(?!$)')]
print(c18)
length = c18.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if c18['GEO_LAT'].values[a] > 15 :
        coords.append([c18['GEO_LAT'].values[a],c18['GEO_LON'].values[a]])
        ##IF the coordinates are good, then we need to test for crime or traffic and append accordingly
        if c18['IS_CRIME'].values[a] > 0:        
            ccoords.append([c18['GEO_LAT'].values[a],c18['GEO_LON'].values[a]])
        else:
            tcoords.append([c18['GEO_LAT'].values[a],c18['GEO_LON'].values[a]])

cmap = folium.Map(mapcenter,zoom_start=11)
cmap.add_child(plugins.HeatMap(coords, radius=7))
cmapsave =  os.path.join(folder , "mapout18.html")
cmap.save(outfile=cmapsave)


ccmap = folium.Map(mapcenter,zoom_start=11)
ccmap.add_child(plugins.HeatMap(ccoords, radius=7))
ccmapsave = os.path.join(folder , "cmapout18.html")
ccmap.save(outfile=ccmapsave)

tsmap = folium.Map(mapcenter,zoom_start=11)
tsmap.add_child(plugins.HeatMap(tcoords, radius=7))
tsmap
tsmapsave = os.path.join(folder ,"tmapout18.html")
tsmap.save(outfile=tsmapsave)

print("You've just placed over 2 million points into heat maps in under 3 minutes. Good job.")