# 1) Script creates contour files for a series of DEMs in a folder. 
# 2) script then merges the contours from that same folder and merges them into one shapefile
# see http://manpages.ubuntu.com/manpages/bionic/man1/ogrmerge.1.html

for files in DEM/*.img 
do gdal_contour -a CONTOUR $files $files.shp -i 5; 
done


ogrmerge.py -single -o DEM/DEMCONTOURS.shp DEM/*.shp -src_layer_field_name NAME #NAME is the field name that will contain the origin of the contour

