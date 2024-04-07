import math
import csv
import subprocess

#Read from csv
coord=[]
with open('route.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        coord.append([row[1],row[0]])

print(coord)
#Change tile_width for different latitudes
#https://wiki.flightgear.org/Tile_Index_Scheme

def tile_width(lat_floor):
   if lat_floor>=22 and lat_floor<62:
       return 0.25
   if lat_floor>=62 and lat_floor<76:
       return 0.5
   return NaN
   
indexl=[]
for crd in coord:
    lat=float(crd[0])
    lon=float(crd[1])
    base_y = math.floor(lat)
    tw=tile_width(base_y)
    y = math.trunc((lat - base_y) * 8)
    base_x = math.floor(math.floor(lon / tw) * tw)
    x = math.floor((lon - base_x) / tw)
    index=(int(lon + 180) << 14) + (int(lat + 90) << 6) + (y << 3) + x
    indexl.append(index)

#Remove doubles
indexl=list( dict.fromkeys(indexl) )
print(indexl)

for index in indexl:
    subprocess.run(["python3","creator.py", "--scenery_folder", "/home/anders/photoscenery", "--index",str(index) ], capture_output=False, text=True)
