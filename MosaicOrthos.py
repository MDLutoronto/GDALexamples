# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 11:39:31 2020
Create a mosaic of images in a folder using gdal
@author: fortinm
based on this tutorial https://www.neonscience.org/merge-lidar-geotiff-py
"""

import numpy as np
import matplotlib as plt
import subprocess, glob
from osgeo import gdal
files_to_mosaic = glob.glob('E:\\2018\\*.tif')
files_string = " ".join(files_to_mosaic)
command = "python ../gdal_merge.py -o Mosaic.tif -of gtiff " + files_string
output = subprocess.check_output(command)
output

