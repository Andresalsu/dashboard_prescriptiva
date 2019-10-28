import pandas as pd
from shapely.geometry import Point
from geopandas import GeoDataFrame
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import fiona

df=pd.read_excel(r'/Users/andalval/Downloads/hello_docker_flask/datos mapa.xlsx')
#key="AIzaSyC-980k21JUmn8J-lJwJn6tUJVc_vC8tts"
#gmaps = googlemaps.Client(key)
geometry=[Point(xy) for xy in zip(df.x, df.y)]
crs={'init':'epsg:2263'}
gdf=GeoDataFrame(df, crs=crs, geometry=geometry)
gdf.head()