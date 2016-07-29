# creates point shapefiles for csv tables with different utm projections

# file naming convention should be utm26917 with XY field names of utm_x and utm_y

cd csv_by_utm_zone
for i in *
do
	echo "----------------------------"
	echo "$i"
	f="${i%.*}"
	n="${f:3}"
	echo "$f"
	echo "$n"
	ogr2ogr "$f".shp -t_srs "EPSG:4269" "$f".csv -dialect sqlite -sql "SELECT MakePoint(CAST(utm_x as REAL), CAST(utm_y as REAL), "$n") Geometry, * FROM "$f""
done
echo "----------------------------"

# excerpt for just one table conversion:

# ogr2ogr out.shp -t_srs "EPSG:4269" in.csv -dialect sqlite -sql "SELECT MakePoint(CAST(utm_x as REAL), CAST(utm_y as REAL), 26917) Geometry, * FROM in"

# or if you have a .vrt file:

# ogr2ogr -f "ESRI Shapefile" . gaf.csv && ogr2ogr -f "ESRI Shapefile" . gaf.vrt
