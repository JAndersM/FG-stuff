import sys
import math
import subprocess
lat0=float(sys.argv[1])
lon0=float(sys.argv[2])
lat1=float(sys.argv[3])
lon1=float(sys.argv[4])

#Change tile_width for different latitudes
#https://wiki.flightgear.org/Tile_Index_Scheme


def tile_width(lat_floor):
    if lat_floor>=22 and lat_floor<62:
       return 0.25
    if lat_floor>=62 and lat_floor<76:
       return 0.5
    return NaN
   
nlat=math.ceil((lat1-lat0)/0.125)
nlon=math.ceil((lon1-lon0)/tile_width(lat0))

indexl=[]
for i in range(nlat):
    for j in range(nlon):
        lat=lat0+i*0.125
        lon=lon0+j*tile_width(lat0)
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
   
