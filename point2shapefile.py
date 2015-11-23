# reference for this: http://invisibleroads.com/tutorials/gdal-shapefile-points-save.html
# reference for reading csv: http://www.gdal.org/drv_csv.html

#reference 0: http://gdal.org/python/osgeo.ogr-module.html
#reference 1: https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
#reference 2: http://geospatialpython.com/2011/02/clip-raster-using-shapefile.html
#reference 3: http://www.gdal.org/
# http://www.gis.usu.edu/~chrisg/python/2009/docs.html
# http://www.gis.usu.edu/~chrisg/python/2009/
# http://gdal.org/python/osgeo.ogr.DataSource-class.html
# http://www.gdal.org/ogr_apitut.html
# http://gdal.org/java/org/gdal/ogr/DataSource.html
#http://gdal.org/java/org/gdal/ogr/Layer.html#Clip(org.gdal.ogr.Layer, org.gdal.ogr.Layer)
# http://gdal.org/python/osgeo.ogr.Layer-class.html

import subprocess
import os, sys
from optparse import OptionParser

import osgeo.ogr as ogr
import osgeo.osr as osr

import operator
from osgeo import gdal, gdalnumeric, ogr, osr
#import Image, ImageDraw
import csv

'''
if __name__ == "__main__":
    ## Toronto Polygon shapefile used to clip
    #TOshpfilename = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\neighbourhoods_planning_areas_wgs84\NEIGHBORHOODS_WGS84.shp"

    ## Canada Census Tract 2011 shape file to be clipped
    #shpfilename = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e\gct_000b11a_e.shp"

    ## Torotno Census Tract 2011 shape file clipped
    #outputfilename = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e_Toronto_clippedGdal.shp"

    parser = OptionParser(usage="usage: %prog [options] pointsfile.txt/.csv result.shp",
                          version="%prog 1.0")
                          
    options, args = parser.parse_args()
    if len(args) !=2 :
        parser.error("Wrong number of inputs")
        exit(0)
    else:
        pointfilename, outputshpfilename = args
'''
    
inputfilename = r"U:\STAFF\SGH\ArcGIS\GDAL\all_toronto\all_toronto.csv"
outputpointshpfilename = r"U:\STAFF\SGH\ArcGIS\GDAL\all_toronto\all_toronto_points_M1B5K8.shp"
outputpolyshpfilename = r"U:\STAFF\SGH\ArcGIS\GDAL\all_toronto\all_toronto_polygons_M1B5K8.shp"
outputconvexpolyshpfilename = r"U:\STAFF\SGH\ArcGIS\GDAL\all_toronto\all_toronto_convexpolygons_M1B5K8.shp"
outputspidershpfilename = r"U:\STAFF\SGH\ArcGIS\GDAL\all_toronto\all_toronto_spider_M1B5K8.shp"


long_lats = {}
list_of_long_lat = []
with open(inputfilename, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        list_of_long_lat.append([row[17],row[19],row[20]])  #read Longitude and Latitude
        if row[17] in long_lats.keys():
            long_lats[row[17]].append([row[19],row[20]])  #read Longitude and Latitude
        else:
            long_lats[row[17]]=[[row[19],row[20]]]


#print list_of_long_lat[0:2]
        
#Set spatial reference.
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

#Create shapefile.
driver = ogr.GetDriverByName('ESRI Shapefile')

#############################################################
##################  points     ############################
#############################################################
shapeData = driver.CreateDataSource(outputpointshpfilename)   #'points-shifted.shp'

#Create layer.
#layer = shapeData.CreateLayer('layer1', spatialReference, ogr.wkbPoint)
layer = shapeData.CreateLayer('layer1', spatialReference, ogr.wkbMultiPoint)
layerDefinition = layer.GetLayerDefn()

'''
#Create point.
multipoint = ogr.Geometry(ogr.wkbMultiPoint)
###point1
point = ogr.Geometry(ogr.wkbPoint)
#point.SetPoint(0, 474595, 4429281)
point.AddPoint(-79.5628135, 43.6093021)
multipoint.AddGeometry(point)
####point2
point = ogr.Geometry(ogr.wkbPoint)
#point1 = ogr.Geometry(ogr.wkbPoint)
point.AddPoint(-79.4450116, 43.6950641) 
multipoint.AddGeometry(point)
#print multipoint.ExportToWkt()
'''

#convert points of csv into ogr multipoint
multipoint = ogr.Geometry(ogr.wkbMultiPoint)
for i in range(1,len(list_of_long_lat)):
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(float(list_of_long_lat[i][1]), float(list_of_long_lat[i][2]))
    multipoint.AddGeometry(point)


#Put point as a geometry inside a feature.
featureIndex = 0
feature = ogr.Feature(layerDefinition)
#feature.SetGeometry(point)
feature.SetGeometry(multipoint)
feature.SetFID(featureIndex)

#Put feature in a layer.
layer.CreateFeature(feature)

#Flush.
shapeData.Destroy()

#############################################################
##################  polygons     ############################
#############################################################
shapeData = driver.CreateDataSource(outputpolyshpfilename)   #'points-shifted.shp'

#Create layer.
layer = shapeData.CreateLayer('layer1', spatialReference, ogr.wkbMultiPolygon)
layerDefinition = layer.GetLayerDefn()

#convert points of csv into ogr multipolygons
multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
for i in long_lats.keys():
    if not i=='POSTALCODE':
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for j in range(len(long_lats[i])):
            ring.AddPoint(float(long_lats[i][j][0]), float(long_lats[i][j][1]) )
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        convexpoly = poly.ConvexHull()
        multipolygon.AddGeometry(poly)


#Put point as a geometry inside a feature.
featureIndex = 0
feature = ogr.Feature(layerDefinition)
#feature.SetGeometry(point)
feature.SetGeometry(multipolygon)
feature.SetFID(featureIndex)

#Put feature in a layer.
layer.CreateFeature(feature)

#Flush.
shapeData.Destroy()

##################  Convex polygon     ############################
#save convex hull from inut layer to output layer
inDriver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = inDriver.Open(outputpolyshpfilename, 0)
inLayer = inDataSource.GetLayer()

# Collect all Geometry
geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
for feature in inLayer:
    geomcol.AddGeometry(feature.GetGeometryRef())

# Calculate convex hull
convexhull = geomcol.ConvexHull()


# Create the output shapefile
outDriver = ogr.GetDriverByName("ESRI Shapefile")
outDataSource = outDriver.CreateDataSource(outputconvexpolyshpfilename)
outLayer = outDataSource.CreateLayer("postal_convexhull", geom_type=ogr.wkbPolygon)

# Add an ID field
idField = ogr.FieldDefn("id", ogr.OFTInteger)
outLayer.CreateField(idField)

# Create the feature and set values
featureDefn = outLayer.GetLayerDefn()
feature = ogr.Feature(featureDefn)
feature.SetGeometry(convexhull)
feature.SetField("id", 1)
outLayer.CreateFeature(feature)

# Close DataSource
inDataSource.Destroy()
outDataSource.Destroy()


#############################################################
##################  Spider     ############################
#############################################################
shapeData = driver.CreateDataSource(outputspidershpfilename)   #'points-shifted.shp'

#Create layer.
layer = shapeData.CreateLayer('layer1', spatialReference, ogr.wkbMultiLineString)
layerDefinition = layer.GetLayerDefn()

spider = ogr.Geometry(ogr.wkbMultiLineString)
for i in range(1,len(list_of_long_lat)):
    for j in range(1,len(list_of_long_lat)):
        if not i==j:
            line = ogr.Geometry(ogr.wkbLineString)
            line.AddPoint(float(list_of_long_lat[i][1]), float(list_of_long_lat[i][2]))
            line.AddPoint(float(list_of_long_lat[j][1]), float(list_of_long_lat[j][2]) )
            spider.AddGeometry(line)


#Put point as a geometry inside a feature.
featureIndex = 0
feature = ogr.Feature(layerDefinition)

#feature.SetGeometry(point)
feature.SetGeometry(spider)
feature.SetFID(featureIndex)

#Put feature in a layer.
layer.CreateFeature(feature)

#Flush.
shapeData.Destroy()



