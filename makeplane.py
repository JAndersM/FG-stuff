import os
import sys
import lxml.etree as ET
import shutil

def makeplane(args):
    plane_name=args[1]
    if len(args)>1 :
        plane_description=args[2]
    else :
        plane_description = args[1]
    makedirs(plane_name)
    makeset(plane_name, plane_description)
    populate(plane_name)
    jsbsim(plane_name, plane_description)

def makedirs(plane_name):
    try:
        os.mkdir(plane_name)
        print(f"Directory '{plane_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{plane_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{plane_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    dirs = ["Models", "Effects", "Systems",
            "Sounds", "Engines", "Instruments",
            "Resources", "Nasal", "Previews"]
    for d in dirs:
        try:
            os.mkdir(plane_name + "/" + d)
            print(f"Directory '{d}' created successfully.")
        except FileExistsError:
            print(f"Directory '{d}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{d}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

def makeset(plane_name, plane_description):
    tree = ET.parse("aircraftfiles/set.xml")
    root=tree.getroot()
    changes= {"description" : plane_description,
              "aero" : plane_name,
              "model/path": "Model/"+plane_name + "-model.xml",
              }
    for key in changes.keys() :
        desc=tree.xpath("/PropertyList/sim/"+key)
        desc[0].text=changes[key]
    with open(plane_name+"/"+plane_name+"-set.xml", 'w') as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
        f.write("\n\n")
        f.write(ET.tostring(root, encoding='unicode'))
        print("Set file created.")

def populate(plane_name) :
    fs={"help.xml" : "/help.xml",
        "instruments.xml" : "/Instruments/instruments.xml",
        "sounds.xml": "/Sounds/sounds.xml",
        "systems.xml": "/Systems/systems.xml",
        "model.xml": "/Models/"+plane_name+"-model.xml"
        }
    for key in fs.keys() :
        try:
            shutil.copy("aircraftfiles/"+key, plane_name+fs[key])
            print(fs[key]+" created.")
        except PermissionError:
            print("Permission denied.")
        except:
            print("Error occurred while copying file.")

def jsbsim(plane_name, plane_description) :
    tree = ET.parse("aircraftfiles/jsbsim.xml")
    root = tree.getroot()
    name=tree.xpath("/fdm_config")
    name[0].set("name", plane_name)
    desc=tree.xpath("/fdm_config/fileheader/description")
    desc[0].text=plane_description
    shutil.copy("aircraftfiles/jsbsim-header.txt", plane_name+"/"+plane_name + ".xml")
    with open(plane_name+"/"+plane_name+".xml", 'a') as f:
        f.write("\n")
        f.write(ET.tostring(root, encoding='unicode'))
        print("JSBsim file created.")

if __name__ == '__main__':
    makeplane(sys.argv)
