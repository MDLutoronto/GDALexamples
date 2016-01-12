# Prints the spatial reference and feature count of shapefiles in a directory
# and then checks if all shapefiles have the same spatial reference

# ogr documentation: http://www.gdal.org/classOGRLayer.html

import os
from osgeo import ogr

ws = r"PATH"

ref_list_check = []
x = "filler"
count = 0
fail_list = []

# find all shps in directory
for subdir, dirs, files in os.walk(ws):
    for file in files:
        if file.endswith(('.shp')):
            print "______________________________"
            print file
            # shp path:
			shp = os.path.join(subdir, file)
            # open shp with driver
			driver = ogr.GetDriverByName('ESRI Shapefile')
            dataSource = driver.Open(shp, 0)
            # check if shp doesn't open
			if dataSource is None:
                fail_list.append(file)
            else:
				print shp
				layer = dataSource.GetLayer()
				# get feature count and print
				featureCount = layer.GetFeatureCount()
				print "Number of features:"
				print featureCount
				# get spatial ref and print
				spatialRef = layer.GetSpatialRef()
				print "Spatial Reference"
				print spatialRef
				# check if a new spatial ref
				if x != str(spatialRef):
					ref_list_check.append(1)
				x = str(spatialRef)
				count = count + 1

print "______________________________"
print "total shps checked:"
print count
print "______________________________"

# print results
if fail_list != []:
    print "some files are corrupt:"
    print fail_list
if ref_list_check != [1]:
    print "there are multiple spatial refs"
else:
    print "all have the same spatial ref:"
    print spatialRef
