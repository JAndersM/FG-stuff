#Flap helper, Triggers flap sound
#Plankflex helper, calculates compression in m
#Multiplay helper, copies tied propertise
var oldtack=0;

var helper_funcs = func() {
 #Flap sound
 if (oldtack != math.sgn(getprop("/fdm/jsbsim/aero/sail/alpha-deg"))) {
   setprop("/sim/sound/flap",1);
   oldtack = math.sgn(getprop("/fdm/jsbsim/fcs/tack"));
  } else { 
  	setprop("/sim/sound/flap",0);
  }
  # Plankflex
  setprop("/gear/stbrd-comp", (getprop("/fdm/jsbsim/gear/unit[3]/compression-ft") or 0)*0.3);
	setprop("/gear/port-comp", (getprop("/fdm/jsbsim/gear/unit[2]/compression-ft") or 0)*0.3);
  # Multiplay
  setprop("/controls/flight/beta", (getprop("/fdm/jsbsim/aero/mybeta-deg") or 0));
	setprop("/controls/flight/tack", math.sgn((getprop("/fdm/jsbsim/aero/sail/alpha-deg") or 0)));
}


var timer = maketimer(0.1, helper_funcs);
timer.start();
print("Nasal: Helper start");

