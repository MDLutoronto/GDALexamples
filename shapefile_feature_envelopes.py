#python script that goes through a shapefile and lists the bounding box information and the feature's name from the attribute table.
import os
from osgeo import ogr
shapefile = "/Users/marcelfortin/Documents/data/ArcCanada2.0/prov99.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(shapefile, 0)
layer = dataSource.GetLayer()
# print out envelopes/bounding boxes
layer.ResetReading()
layerDefinition = layer.GetLayerDefn()
for feature in layer:
    env = feature.GetGeometryRef().GetEnvelope()
    #field 0 needs to be changed to reflect the field containing the desired information.
    fieldName = layerDefinition.GetFieldDefn(0).GetName()
    fieldValue = feature.GetField(fieldName)
    bbox = [fieldName, fieldValue, env[0], env[2], env[1], env[3]]
    #print 'Bounding Box ' + str(env)
    print 'Bounding Box ' + str(bbox)
    
    #help from both http://gis.stackexchange.com/questions/3821/how-can-i-convert-a-shapefile-to-lat-and-lon-boundaries and
    # http://pcjericks.github.io/py-gdalogr-cookbook/layers.html#iterate-over-features and referenced here:
    #http://gdal.org/python/osgeo.ogr.Geometry-class.html
    #By Marcel
    
