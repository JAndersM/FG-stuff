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

aircraft.livery.init("Aircraft/Isabella/Models/Liveries");
print("Liveries init");

#Called when s is pressed
var initpush = func {
	setprop("/fdm/jsbsim/external_reactions/start-push/magnitude",50);
	if (pushtimer.isRunning == 0 and getprop("/controls/push") == 1) { pushtimer.start();}
}

#Called when s is released or time runs out
var stoppush= func {
	setprop("/fdm/jsbsim/external_reactions/start-push/magnitude",0);
	if (pushtimer.isRunning == 1) { pushtimer.stop();}
}

var pushtimer = maketimer(2.5, stoppush);
pushtimer.simulatedTime=1;
var timer = maketimer(0.1, helper_funcs);
timer.start();
print("Isabella: Helper functions start");

var placetrack = func(position, winddirection) {
	var pathround = 'Models/Marks/roundingmark.ac';
	var pathstart = 'Models/Marks/startline.ac';
	var pathfinish = 'Models/Marks/finishmark.ac';
	var start = geo.put_model(pathstart, position.apply_course_distance(winddirection, 10), 0);
	var roundd=geo.put_model(pathround, position.apply_course_distance(winddirection, 100),0);
	var roundu = geo.put_model(pathround, position.apply_course_distance(winddirection, 1000),0);
	position.apply_course_distance(winddirection, -1000);
	var finish = geo.put_model(pathfinish, position.apply_course_distance(winddirection-90, 60), 0);
}

#placetrack(geo.aircraft_position(), 0);
