/* 
 * File:   main.cpp
 * Author: simon
 *
 * Created on 30 January 2011, 19:50
 */

#include "Observer.h"
#include "Angle.h"
#include "Coordinates.h"



//using namespace std;

/*
 * 
 */
int main(int argc, char** argv) {
//TODO everything is right except HA to RA conversion (HA and Dec are good). Sidereal time is wrong. Use the calculation in the urania source to fix.

    DateTime Tnow = DateTime(2011,7,26,14,13,50);
    Angle Lat = AngleDegs(48,51,36);
    Angle Long = AngleDegs(2,20,24);
    Observer Ob1 = Observer(Lat,Long);
    Ob1.UpdateTime(Tnow);
    Coordinates Ca = Coordinates(Ob1);
    Angle RA = AngleHrs(17,48,0);
    Angle Dec = AngleDegs(15,0,0);
    Ca.SetRaDec(RA,Dec);
    Angle AltRead = AngleDegs(0,21,35);
    Angle AzRead = AngleDegs(67,16,49);
    Coordinates Cb = Coordinates(Ob1);
    Cb.SetAzAlt(AzRead,AltRead);
    Cb.CorrectToJ2000();
   
    
    return 0;
}

