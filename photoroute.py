import math
import csv
import subprocess

def tile_width(lat_floor):
    lf=abs(lat_floor)
    if lf<22:
       return 0.125
    if lf>=22 and lf<62:
       return 0.25
    if lf>=62 and lf<76:
       return 0.5
    return NaN

def findindex(lat, lon):
    base_y = math.floor(lat)
    tw=tile_width(base_y)
    y = math.trunc((lat - base_y) * 8)
    base_x = math.floor(math.floor(lon / tw) * tw)
    x = math.floor((lon - base_x) / tw)
    index=(int(lon + 180) << 14) + (int(lat + 90) << 6) + (y << 3) + x
    return index
    
#Read from csv
# rows with lat, lon
coords=[]
with open('route.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        print(row)
        if len(row)==2:
            coords.append([float(row[0]),float(row[1])])

#Add extra coordinates if needed
n=0
excoords=[]
while n<len(coords)-1:
    dla=coords[n+1][0]-coords[n][0]
    dta=dla/0.125
    dlo=coords[n+1][1]-coords[n][1]
    dto=dlo/tile_width(coords[n][0])
    d=math.floor(math.sqrt(dta*dta+dto*dto))
    if d>1:
        ddla=dla/d
        ddlo=dlo/d
        m=1
        while m<d:
            excoords.append([coords[n][0]+ddla*m, coords[n][1]+ddlo*m])
            m=m+1
    n=n+1
coords.extend(excoords)    

#Change tile_width for different latitudes
#https://wiki.flightgear.org/Tile_Index_Scheme
   
indexl=[]
for crd in coords:
    tw=tile_width(math.floor(crd[0]))
    indexl.append(findindex(crd[0]+0.125,crd[1]-tw))
    indexl.append(findindex(crd[0]+0.125,crd[1]))
    indexl.append(findindex(crd[0]+0.125,crd[1]+tw))
    indexl.append(findindex(crd[0],crd[1]-tw))
    indexl.append(findindex(crd[0],crd[1]))
    indexl.append(findindex(crd[0],crd[1]+tw))
    indexl.append(findindex(crd[0]-0.125,crd[1]-tw))
    indexl.append(findindex(crd[0]-0.125,crd[1]))
    indexl.append(findindex(crd[0]-0.125,crd[1]+tw))

#Remove doubles
indexl=list( dict.fromkeys(indexl) )
indexl.sort()
print("\nTiles:")
print(indexl)
print()
print(f"Download will take ~{len(indexl)} min and download ~{len(indexl)*12} MB")
a=input("Start download [J/N]:")
if a.lower()=="j" :
    for index in indexl:
        print("\nTile:", index)
        subprocess.run(["python3","creator.py", "--scenery_folder", "Photo", "--index", str(index) ], capture_output=False, text=True)
   
