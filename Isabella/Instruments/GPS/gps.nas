var Gps= {

  new: func() {
    var m={parents:[Gps] };
    m.timer=nil;
    m.init();
    return m;
  },
  
  init: func() {
  	setprop("instrumentation/gps-annunciator/u100",0);
  	setprop("instrumentation/gps-annunciator/u10",1);
  	setprop("instrumentation/gps-annunciator/u1",2);
  	setprop("instrumentation/gps-annunciator/l100",3);
  	setprop("instrumentation/gps-annunciator/l10",4);
  	setprop("instrumentation/gps-annunciator/l1",5);
  	setprop("instrumentation/gps-annunciator/udot",1);
  	setprop("instrumentation/gps-annunciator/ldot",0);
  	setprop("instrumentation/gps-annunciator/light",0);
    me.timer=maketimer(1, me, me.uppdate);
  },
  
  modehandler: func(mode) {
  },
  
  uppdate: func() {
  	var speed=getprop("/instrumentation/gps/indicated-ground-speed-kt");
  	var course=getprop("/instrumentation/gps/indicated-track-true-deg");
  	var u = [0,0,0];
  	#Speed
  	if (speed<100) {
  		setprop("instrumentation/gps-annunciator/udot",1);
  		u[0]=math.floor(speed/10);
  		u[1]=math.floor(speed-10*u[0]);
  		u[2]=math.floor((speed-10*u[0]-u[1])*10);
  	} else {
  		setprop("instrumentation/gps-annunciator/udot",0);
  		u[0]=math.floor(speed/100);
  		u[1]=math.floor((speed-100*u[0])/10);
  		u[2]=math.floor(speed-100*u[0]-10*u[1]);  	
  	}
  	setprop("instrumentation/gps-annunciator/u100",u[0]);
  	setprop("instrumentation/gps-annunciator/u10",u[1]);
  	setprop("instrumentation/gps-annunciator/u1",u[2]); 
  	#Course
  	if (speed<0.2) {
  	# dashes
			u[0]=10;
			u[1]=10;
			u[2]=10;
		} else {
  		u[0]=math.floor(course/100);
  		u[1]=math.floor((course-100*u[0])/10);
  		u[2]=math.floor(course-100*u[0]-10*u[1]);
  	}
  	setprop("instrumentation/gps-annunciator/l100",u[0]);
  	setprop("instrumentation/gps-annunciator/l10",u[1]);
  	setprop("instrumentation/gps-annunciator/l1",u[2]);  	
  },
};

var gps=Gps.new();
gps.timer.start();

