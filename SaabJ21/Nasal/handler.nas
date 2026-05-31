#Nasal helper functions

#Init
#Init Canopy movement
var canopy = aircraft.door.new("/controls/canopy/", 5);

var autostart = func {
  setprop("/controls/engines/engine[0]/cutoff", 0);
  setprop("/controls/engines/engine[0]/magnetos", 2);
  gui.popupTip("Press 's' to start");
}
