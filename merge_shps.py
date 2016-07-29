# merges all shapefiles in a folder using ogr2ogr
# outputs as merge.shp

import csv
import os
import time
from subprocess import call
import sys
from osgeo import ogr

# change to working directory and set as workspace if necessary
os.chdir("shp_folder")
ws = os.path.dirname(os.path.realpath(__file__))

# take file name of first shp in the folder
count = 0
x = "_"
for subdir, dirs, files in os.walk(ws):
    for file in files:
      if file.endswith(('.shp')) and x == "_":
        x = file


# loop shps and merge to one shp calling ogr2ogr shell commands
for subdir, dirs, files in os.walk(ws):
    for file in files:
      if file.endswith(('.shp')):
        print file
        count += 1
        if x == file:
          call(["ogr2ogr", "-f", "ESRI Shapefile", "merge.shp", "%s" %file])
        else:
          call(["ogr2ogr", "-f", "ESRI Shapefile", "-update", "-append", "merge.shp", "%s" %file, "-nln", "merge"])

print "--------------------------"
print "shps merged: ", count
