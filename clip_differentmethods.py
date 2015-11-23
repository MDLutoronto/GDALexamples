# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import subprocess
import os, sys

import osgeo.ogr as ogr
import osgeo.osr as osr

import operator
from osgeo import gdal, gdalnumeric, ogr, osr

# Canada Census Tract 2011 shape file to be clipped
shpfilename = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e\gct_000b11a_e.shp"

# Toronto Polygon shapefile used to clip
TOshpfilename = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\neighbourhoods_planning_areas_wgs84\NEIGHBORHOODS_WGS84.shp"

# Torotno Census Tract 2011 shape file clipped
outputfilename = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\Toronto_clippedGdalPython.shp"
outputfilename1 = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\Toronto_clippedGdal1.shp"
outputfilename2 = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\Toronto_clippedGdal2.shp"
outputfilename3 = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\Toronto_clippedGdal3.shp"
outputfilename4 = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\Toronto_clippedGdal4.shp"

driver = ogr.GetDriverByName('ESRI Shapefile')

#Method 1: clipping
# Create an OGR layer from a boundary shapefile
canshp = driver.Open(shpfilename, 0) # 0 means read-only. 1 means writeable.
shpclipper = driver.Open(TOshpfilename, 0) # 0 means read-only. 1 means writeable.

Canlyr = canshp.GetLayer()
TOlyr = shpclipper.GetLayer()

# Remove output shapefile if it already exists
if os.path.exists(outputfilename):
    driver.DeleteDataSource(outputfilename)
    print "deleted ", outputfilename


outDataSource = driver.CreateDataSource(outputfilename)
out_lyr_name = os.path.splitext( os.path.split(outputfilename )[1] )[0]
outLayer = outDataSource.CreateLayer(out_lyr_name[:-4], geom_type=ogr.wkbMultiPolygon)
if outLayer is None:
    print "Layer creation failed.\n"

#clipping
Canlyr.Clip(TOlyr,outLayer)
outDataSource.Destroy()
shpclipper.Destroy()
canshp.Destroy()



'''
#Method 2: clipping
canshp = driver.Open(shpfilename, 0) # 0 means read-only. 1 means writeable.
shpclipper = driver.Open(TOshpfilename, 0) # 0 means read-only. 1 means writeable.

Canlyr = canshp.GetLayer()
TOlyr = shpclipper.GetLayer()


minX, maxX, minY, maxY = TOlyr.GetExtent()
print minX, minY, maxX, maxY

TOpoly = TOlyr.GetNextFeature()
geom = TOpoly.GetGeometryRef()

Canlyr.SetSpatialFilter(geom)
# Write output
# Remove output shapefile if it already exists
if os.path.exists(outputfilename1):
    driver.DeleteDataSource(outputfilename1)
    print "deleted ", outputfilename1

    
# Create the output shapefile
outDataSource1 = driver.CreateDataSource(outputfilename1)
out_lyr_name = os.path.splitext( os.path.split(outputfilename1 )[1] )[0]
outLayer = outDataSource1.CopyLayer(Canlyr,out_lyr_name ,['OVERWRITE=YES'])
outDataSource1.Destroy()
shpclipper.Destroy()
canshp.Destroy()

'''



'''
#Method 3: clipping
#wkt = "POLYGON ((-103.81402655265633 50.253951270672125,-102.94583419409656 51.535568561879401,-100.34125711841725 51.328856095555651,-100.34125711841725 51.328856095555651,-93.437060743203844 50.460663736995883,-93.767800689321859 46.450441890315041,-94.635993047881612 41.613370178339181,-100.75468205106476 41.365315218750681,-106.12920617548238 42.564247523428456,-105.96383620242338 47.277291755610058,-103.81402655265633 50.253951270672125))"                                                                                 
#layer.SetSpatialFilter(ogr.CreateGeometryFromWkt(wkt))
if os.path.exists(outputfilename3):
    driver.DeleteDataSource(outputfilename3)
    print "deleted ", outputfilename3


canshp = driver.Open(shpfilename, 0) # 0 means read-only. 1 means writeable.
shpclipper = driver.Open(TOshpfilename, 0) # 0 means read-only. 1 means writeable.

TOlyr = shpclipper.GetLayer()
points = []
for i in range(TOlyr.GetFeatureCount()):
    Canlyr = canshp.GetLayer()
    TOpoly = TOlyr.GetNextFeature()
    if TOpoly is not None:
        wkt = "POLYGON (("
        geom = TOpoly.GetGeometryRef()
        pts = geom.GetGeometryRef(0)
        for p in range(pts.GetPointCount()):
            wkt += "%f %f," %(pts.GetX(p), pts.GetY(p))
            points.append((pts.GetX(p), pts.GetY(p)))
        wkt = wkt[:-1]
        wkt += "))"
        #clipping
        #Canlyr.SetSpatialFilter(geom)
        Canlyr.SetSpatialFilter(ogr.CreateGeometryFromWkt(wkt))
        outDataSource = driver.CreateDataSource(outputfilename3[:-5]+str(i+3)+".shp")
        out_lyr_name = os.path.splitext( os.path.split(outputfilename3[:-5]+str(i+3)+".shp")[1] )[0]
        outLayer = outDataSource.CopyLayer(Canlyr,out_lyr_name ,['OVERWRITE=YES'])
        outDataSource.Destroy()

print len(points)
shpclipper.Destroy()
canshp.Destroy()
'''

'''
#Method 4: Clipping
# ogr2ogr -f "ESRI Shapefile"  -clipsrc NEIGHBORHOODS_WGS84.shp U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e_Toronto_clippedGdal_redo  U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e\gct_000b11a_e.shp
# Clipping process**
#subprocess.call(["ogr2ogr", "-f", "ESRI Shapefile", "-clipsrc", TOshpfilename, outputfilename4[:-4], shpfilename], shell=True)
'''

'''
# Close DataSources
#shpclipper.Destroy()
#canshp.Destroy()
#outDataSource3.Destroy()
'''
