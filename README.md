# Isabella
Isabella iceboat model


# FG tools
An add-on for Blender that helps with exporting animations, effects and models. It also adds an axis object that can be used in animations.
Exports either to system console or export.xml placed in the blend file directory.

Adds:

An FG Tools tab right hand side 3D view

An Axis Mesh object in the Add menu


Animations:

Select all objects that you want animated. Make the one used for center or axis the active one. (Selected last)
Choose animation type etc.

Choose axis. If the Active object is an Axis it will be used as center and axis ignoring the axis selected. You can choose Axis: export it as an axis-object or its vertices coordinates.

The active objects origin will be used as center.


Effects and model placement:

The selected objects will be exported in xml-tags for effect respective model.

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

Installation: download the aircraftfiles directory and makeplane.py

Usage: pyton3 makeplane.py aircraft_name "Aircraft description"


Needs the lmxl python3 library

# Photo area
Runs creator.py ( https://github.com/nathanielwarner/flightgear-photoscenery/blob/master/creator.py ) over a specified "rectangular" area: python3 photoarea.py lat0 lon0 lat1 lon1

Obs: Before running the program first time change the <path to folder> on the last line of the program to the relative path to your photoscenery folder.

Note. You need to change tile width function below 22 latitude

# Photo route
Same as area but with coordinates specified in a csv-file route.csv
