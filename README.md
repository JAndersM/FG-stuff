# Isabella
Isabella iceboat model


# FG tools
Blender add-on for animation, effects and modelplacing


# Add Axis
Blender axis object
Useful for eg. Flightgear animation axis object.

To install:

1 Save the script where you want it.

2 In Blender preferences install the addon and check the box.

# Get axis 
Print axis coords from Blender. Useful for gltf export that doesn't handle axis objects.

# Make Plane
Creates and populates an aircraft directory structure

Usage: pyton3 makeplane.py aircraft_name "Aircraft description"

Needs the lmxl python3 library

# Photo area
Runs creator.py ( https://github.com/nathanielwarner/flightgear-photoscenery/blob/master/creator.py ) over a specified "rectangular" area: python3 photoarea.py lat0 lon0 lat1 lon1

Obs: write path to your photoscenery folder on the last line befor using the program.

Note. You need to change tile width function below 22 latitude

# Photo route
Same as area but with coordinates specified in a csv-file route.csv
