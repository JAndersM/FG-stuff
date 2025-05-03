#Flap helper
# Triggers flap sound

var oldtack=0;

var flap_helper = func() {
 if (oldtack != math.sgn(getprop("/fdm/jsbsim/aero/sail/alpha-deg"))) {
   setprop("/sim/sound/flap",1);
   oldtack = math.sgn(getprop("/fdm/jsbsim/fcs/tack"));
  } else { 
  	setprop("/sim/sound/flap",0);
  }
}

var timer = maketimer(0.1, flap_helper);
timer.start();
print("Nasal: Tack sound");
