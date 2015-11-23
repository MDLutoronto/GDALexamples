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

if __name__ == "__main__":
    ## Toronto Polygon shapefile used to clip
    #TOshpfilename = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\neighbourhoods_planning_areas_wgs84\NEIGHBORHOODS_WGS84.shp"

    ## Canada Census Tract 2011 shape file to be clipped
    #shpfilename = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e\gct_000b11a_e.shp"

    ## Torotno Census Tract 2011 shape file clipped
    #outputfilename = r"U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e_Toronto_clippedGdal.shp"

    parser = OptionParser(usage="usage: %prog [options] clipping.shp source.shp result.shp",
                          version="%prog 1.0")
                          
    options, args = parser.parse_args()
    if len(args) !=3 :
        parser.error("Wrong number of inputs")
        exit(0)
    else:
        TOshpfilename, shpfilename, outputfilename = args
    
    driver = ogr.GetDriverByName('ESRI Shapefile')

    # Create an OGR layer from a boundary shapefile
    canshp = driver.Open(shpfilename, 0) # 0 means read-only. 1 means writeable.
    shpclipper = driver.Open(TOshpfilename, 0) # 0 means read-only. 1 means writeable.

    # Check to see if shapefile is found.
    if canshp is None:
        print 'Could not open %s' % (shpfilename)
    else:
        print 'Opened %s' % (shpfilename)
        layer = canshp.GetLayer()
        featureCount = layer.GetFeatureCount()
        print "Number of features in %s: %d" % (os.path.basename(shpfilename),featureCount)


    # Check to see if shapefile is found.
    if shpclipper is None:
        print 'Could not open %s' % (TOshpfilename)
    else:
        print 'Opened %s' % (TOshpfilename)
        layer = shpclipper.GetLayer()
        featureCount = layer.GetFeatureCount()
        print "Number of features in %s: %d" % (os.path.basename(TOshpfilename),featureCount)


    Canlyr = canshp.GetLayer()
    TOlyr = shpclipper.GetLayer()
    TOpoly = TOlyr.GetNextFeature()

    TOlyr.GetName()
    layerDefinition = TOlyr.GetLayerDefn()
    for i in range(layerDefinition.GetFieldCount()):
        print layerDefinition.GetFieldDefn(i).GetName()
    #feat = TOlyr.GetNextFeature()
    #n=1
    #while feat is not None:
        #feat = TOlyr.GetNextFeature()
        #n +=1
    #print n

    # Get the layer extent coordinates
    minX, maxX, minY, maxY = TOlyr.GetExtent()
    print minX, minY, maxX, maxY
    # ogr2ogr -clipsrc -79.639264937 43.580995995 -79.115243191 43.855457183 U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e_Toronto_clippedGdal.shp  U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e\gct_000b11a_e.shp
    # ogr2ogr -f "ESRI Shapefile"  -clipsrc -79.639264937 43.580995995 -79.115243191 43.855457183 U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e_Toronto_clippedGdal  U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e\gct_000b11a_e.shp
    # ogr2ogr -f "ESRI Shapefile"  -clipsrc NEIGHBORHOODS_WGS84.shp U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e_Toronto_clippedGdal_redo  U:\STAFF\SGH\ArcGIS\2011-CensusCanada\gct_000b11a_e\gct_000b11a_e.shp
    # Clipping process**
    #subprocess.call(["ogr2ogr", "-f", "ESRI Shapefile", "-clipsrc", clipping_shp, output_shp, input_shp], shell=True)


    #from OSGeo4W shell
    # ogr2ogr -clipsrc [xmin ymin xmax ymax] |WKT|datasource|spat_extent]         #dst.shp src.shp  
    #[-clipdst [xmin ymin xmax ymax]|WKT|datasource] -clipdst 5 40 15 55 france_4326.shp europe_laea.shp


    #lyr = inDataSource.GetLayer('example')
    #for feat in lyr:
        #geom = feat.GetGeometryRef()
        #print geom.ExportToWkt()

    points = []
    geom = TOpoly.GetGeometryRef()
    pts = geom.GetGeometryRef(0)
    for p in range(pts.GetPointCount()):
        points.append((pts.GetX(p), pts.GetY(p)))
    #wkt = "POLYGON ((-103.81402655265633 50.253951270672125,-102.94583419409656 51.535568561879401,-100.34125711841725 51.328856095555651,-100.34125711841725 51.328856095555651,-93.437060743203844 50.460663736995883,-93.767800689321859 46.450441890315041,-94.635993047881612 41.613370178339181,-100.75468205106476 41.365315218750681,-106.12920617548238 42.564247523428456,-105.96383620242338 47.277291755610058,-103.81402655265633 50.253951270672125))"                                                                                 
    #layer.SetSpatialFilter(ogr.CreateGeometryFromWkt(wkt))
    print len(points)

    #clipping
    Canlyr.SetSpatialFilter(geom)

    # Write output
    # Remove output shapefile if it already exists
    if os.path.exists(outputfilename):
        driver.DeleteDataSource(outputfilename)
        print "deleted ", outputfilename
    # Create the output shapefile
    outDataSource = driver.CreateDataSource(outputfilename)
    out_lyr_name = os.path.splitext( os.path.split(outputfilename )[1] )[0]
    print out_lyr_name
    print outputfilename
    outLayer = outDataSource.CopyLayer(Canlyr,out_lyr_name ,['OVERWRITE=YES'])
    if outLayer is None:
        print "Layer creation failed.\n"
    '''
    outLayer = outDataSource.CreateLayer(out_lyr_name, ogr.wkbMultiPolygon)
    if outLayer is None:
        print "Layer creation failed.\n"
        

    # Add input Layer Fields to the output Layer if it is the one we want
    inLayerDefn = Canlyr.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        fieldName = fieldDefn.GetName()
        outLayer.CreateField(fieldDefn)

    # Get the output Layer's Feature Definition
    outLayerDefn = outLayer.GetLayerDefn()

    # Add features to the ouput Layer
    for inFeature in Canlyr:
        # Create output Feature
        outFeature = ogr.Feature(outLayerDefn)
        outFeature.SetGeometry(geom)            #clipping

        # Add field values from input Layer
        for i in range(0, outLayerDefn.GetFieldCount()):
            fieldDefn = outLayerDefn.GetFieldDefn(i)
            fieldName = fieldDefn.GetName()
            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(),
                inFeature.GetField(i))
        outLayer.CreateFeature(outFeature)
    '''

    # Close DataSources
    shpclipper.Destroy()
    canshp.Destroy()
    outDataSource.Destroy()



    #ulX, ulY = world2Pixel(geoTrans, minX, maxY)
    #lrX, lrY = world2Pixel(geoTrans, maxX, minY)
    # Calculate the pixel size of the new image
    #pxWidth = int(lrX - ulX)
    #pxHeight = int(lrY - ulY)
    #clip = srcArray[:, ulY:lrY, ulX:lrX]
