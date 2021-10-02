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

### Since we don't see bias in the above maps, let's continue
dvcoords = []
dv18coords = []
dv19coords = []
dv20coords = []
dv21coords = []

dv_tot = crime.query("OFFENSE_CODE == 1313 or OFFENSE_CODE == 1315 or OFFENSE_CODE == 5309 or OFFENSE_CODE == 1316 or OFFENSE_CODE == 1006")

print(dv_tot)
length = dv_tot.shape[0]

for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if dv_tot['GEO_LAT'].values[a] > 15 :
        dvcoords.append([dv_tot['GEO_LAT'].values[a],dv_tot['GEO_LON'].values[a]])
       
dv_map = folium.Map(mapcenter,zoom_start=11)
dv_map.add_child(plugins.HeatMap(dvcoords, radius=12))
dv_mapsave =  os.path.join(folder , "dvmaptot.html")
dv_map.save(outfile=dv_mapsave)

dv18 = dv_tot[dv_tot['REPORTED_DATE'].str.contains(r'(?!$)2018(?!$)')]
print(dv18)
length = dv18.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if dv18['GEO_LAT'].values[a] > 15 :
        dv18coords.append([dv18['GEO_LAT'].values[a],dv18['GEO_LON'].values[a]])
dv_18map = folium.Map(mapcenter,zoom_start=11)
dv_18map.add_child(plugins.HeatMap(dv18coords, radius=12))
dv_18mapsave =  os.path.join(folder , "dvmap18.html")
dv_18map.save(outfile=dv_18mapsave)

dv19 = dv_tot[dv_tot['REPORTED_DATE'].str.contains(r'(?!$)2019(?!$)')]
print(dv19)
length = dv19.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if dv19['GEO_LAT'].values[a] > 15 :
        dv19coords.append([dv19['GEO_LAT'].values[a],dv19['GEO_LON'].values[a]])
dv_19map = folium.Map(mapcenter,zoom_start=11)
dv_19map.add_child(plugins.HeatMap(dv19coords, radius=12))
dv_19mapsave =  os.path.join(folder , "dvmap19.html")
dv_19map.save(outfile=dv_19mapsave)

dv20 = dv_tot[dv_tot['REPORTED_DATE'].str.contains(r'(?!$)2020(?!$)')]
print(dv20)
length = dv20.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if dv20['GEO_LAT'].values[a] > 15 :
        dv20coords.append([dv20['GEO_LAT'].values[a],dv20['GEO_LON'].values[a]])
dv_20map = folium.Map(mapcenter,zoom_start=11)
dv_20map.add_child(plugins.HeatMap(dv20coords, radius=12))
dv_20mapsave =  os.path.join(folder , "dvmap20.html")
dv_20map.save(outfile=dv_20mapsave)

dv21 = dv_tot[dv_tot['REPORTED_DATE'].str.contains(r'(?!$)2021(?!$)')]
print(dv21)
length = dv21.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if dv21['GEO_LAT'].values[a] > 15 :
        dv21coords.append([dv21['GEO_LAT'].values[a],dv21['GEO_LON'].values[a]])
dv_21map = folium.Map(mapcenter,zoom_start=11)
dv_21map.add_child(plugins.HeatMap(dv21coords, radius=12))
dv_21mapsave =  os.path.join(folder , "dvmap21.html")
dv_21map.save(outfile=dv_21mapsave)
## can you see where activist's bias against men regarding Domestic Violence originates?
## is the incidence as evenly spread as traffic tickets in the maps?
## let's see what the maps look like by offense code...
dv1006coords = []
dv1313coords = []
dv1315coords = []
dv1316coords = []
dv5309coords = []

dv1006 = crime.query("OFFENSE_CODE == 1006")
print(dv1006)
length = dv1006.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if dv1006['GEO_LAT'].values[a] > 15 :
        dv1006coords.append([dv1006['GEO_LAT'].values[a],dv1006['GEO_LON'].values[a]])
dv_1006map = folium.Map(mapcenter,zoom_start=11)
dv_1006map.add_child(plugins.HeatMap(dv1006coords, radius=12))
dv_1006mapsave =  os.path.join(folder , "dvmap1006.html")
dv_1006map.save(outfile=dv_1006mapsave)

dv1313 = crime.query("OFFENSE_CODE == 1313")
print(dv1313)
length = dv1313.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if dv1313['GEO_LAT'].values[a] > 15 :
        dv1313coords.append([dv1313['GEO_LAT'].values[a],dv1313['GEO_LON'].values[a]])
dv_1313map = folium.Map(mapcenter,zoom_start=11)
dv_1313map.add_child(plugins.HeatMap(dv1313coords, radius=12))
dv_1313mapsave =  os.path.join(folder , "dvmap1313.html")
dv_1313map.save(outfile=dv_1313mapsave)

dv1315 = crime.query("OFFENSE_CODE == 1315")
print(dv1315)
length = dv1315.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if dv1315['GEO_LAT'].values[a] > 15 :
        dv1315coords.append([dv1315['GEO_LAT'].values[a],dv1315['GEO_LON'].values[a]])
dv_1315map = folium.Map(mapcenter,zoom_start=11)
dv_1315map.add_child(plugins.HeatMap(dv1315coords, radius=12))
dv_1315mapsave =  os.path.join(folder , "dvmap1315.html")
dv_1315map.save(outfile=dv_1315mapsave)

dv1316 = crime.query("OFFENSE_CODE == 1316")
print(dv1316)
length = dv1316.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if dv1316['GEO_LAT'].values[a] > 15 :
        dv1316coords.append([dv1316['GEO_LAT'].values[a],dv1316['GEO_LON'].values[a]])
dv_1316map = folium.Map(mapcenter,zoom_start=11)
dv_1316map.add_child(plugins.HeatMap(dv1316coords, radius=12))
dv_1316mapsave =  os.path.join(folder , "dvmap1316.html")
dv_1316map.save(outfile=dv_1316mapsave)

dv5309 = crime.query("OFFENSE_CODE == 5309")
print(dv5309)
length = dv5309.shape[0]
for a in range(length):
    ##we need a test to eliminate NANs (not a number) so we append the array if the Latitude value is north of Mexico
    if dv5309['GEO_LAT'].values[a] > 15 :
        dv5309coords.append([dv5309['GEO_LAT'].values[a],dv5309['GEO_LON'].values[a]])
dv_5309map = folium.Map(mapcenter,zoom_start=11)
dv_5309map.add_child(plugins.HeatMap(dv5309coords, radius=12))
dv_5309mapsave =  os.path.join(folder , "dvmap5309.html")
dv_5309map.save(outfile=dv_5309mapsave)

print("You've just placed over 2.2 million points into heat maps in under 3 minutes. Good job.")