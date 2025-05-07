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
  
  calcdigits: func(value, scale) {
    var v=[math.floor(value/100/scale),0,0];
    v[1]=math.floor(value/10/scale-v[0]*10);
    v[2]=math.floor(value/scale-v[0]*100-v[1]*10);
    return v;
  },
  
  uppdate: func() {
  	var speed=getprop("/instrumentation/gps/indicated-ground-speed-kt");
  	var course=getprop("/instrumentation/gps/indicated-track-true-deg");
  	var u = [0,0,0];
  	var l = [0,0,0];
  	#Speed
  	if (speed<100) {
  		setprop("instrumentation/gps-annunciator/udot",1);
  		u=me.calcdigits(speed,0.1);
  	} else {
  		setprop("instrumentation/gps-annunciator/udot",0);
 			u=me.calcdigits(speed,1);
  	}
  	#Course
  	if (speed<0.2) {
  	# dashes
			l[0]=10;
			l[1]=10;
			l[2]=10;
		} else {
 			l=me.calcdigits(course,1);
  	}
  	setprop("instrumentation/gps-annunciator/u100",u[0]);
  	setprop("instrumentation/gps-annunciator/u10",u[1]);
  	setprop("instrumentation/gps-annunciator/u1",u[2]); 
  	setprop("instrumentation/gps-annunciator/l100",l[0]);
  	setprop("instrumentation/gps-annunciator/l10",l[1]);
  	setprop("instrumentation/gps-annunciator/l1",l[2]);  	
  },
};

var gps=Gps.new();
gps.timer.start();

