/* 
 * File:   Coordinates.cpp
 * Author: simon
 * 
 * Created on 19 July 2011, 22:05
 */

#include "Coordinates.h"

Coordinates::Coordinates() {
}

Coordinates::Coordinates(Observer PosTme) {
    TimeAndLoc = PosTme;
}

void Coordinates::SetAzAlt(Angle AzIn, Angle AltIn){
    Alt = AltIn;
    Az = AzIn;
    double fSinDecl;
    double fCosH;

    fSinDecl = (sin(Alt.radians) * sin(TimeAndLoc.Lat.radians)) + (cos(Alt.radians) * cos(TimeAndLoc.Lat.radians) * cos(Az.radians));
    Dec = AngleRads(asin(fSinDecl));
    fCosH = ((sin(Alt.radians) - (sin(TimeAndLoc.Lat.radians) * sin(Dec.radians))) / (cos(TimeAndLoc.Lat.radians) * cos(Dec.radians)));
    Angle HA = AngleRads(acos(fCosH));
    if (sin(Az.radians) > 0)
    {
        HA = AngleDegs(360 - HA.degrees);
    }

    Ra = AngleDegs(TimeAndLoc.LST.degrees-HA.degrees);



}

void Coordinates::SetRaDec(Angle RaIn, Angle DecIn){
    Ra = RaIn;
    Dec = DecIn;

    Angle HA = AngleDegs(TimeAndLoc.LST.degrees - Ra.degrees);

    double Altr = asin(sin(Dec.radians)*sin(TimeAndLoc.Lat.radians)+cos(Dec.radians)*cos(TimeAndLoc.Lat.radians)*cos(HA.radians));

    Alt = AngleRads(Altr);

    double A = acos((sin(Dec.radians)-sin(Alt.radians)*sin(TimeAndLoc.Lat.radians))/(cos(Alt.radians)*cos(TimeAndLoc.Lat.radians)));
    if(sin(HA.radians)>0){
        Az = AngleRads(2*M_PI-A);
    }
    else{
        Az = AngleRads(A);
    }

}

void Coordinates::SetAzAltJ2000(Angle AzIn, Angle AltIn)
{
    Alt = AltIn;
    Az = AzIn;
    
    Angle b = AngleDegs(90 - TimeAndLoc.Lat.degrees);
    double ld = cos(Alt.radians)*cos(Az.radians);
    double md = cos(Alt.radians)*sin(Az.radians);
    double nd = sin(Alt.radians);
    double pha = atan2(-md,(-cos(b.radians)*ld + sin(b.radians)*nd));
    Angle Ha = AngleRads(pha);
    Dec = AngleRads(asin(sin(b.radians)*ld + cos(b.radians)*nd));

    Ra = AngleDegs(Param360(TimeAndLoc.LST.degrees-Ha.degrees));
    
}

void Coordinates::CorrectToJ2000()
{
    Angle Raplus = AngleHrs(-0,-0,-33.83);
    Angle Decplus = AngleDegs(0,3,40.46);
    Ra = AngleDegs(Ra.degrees + Raplus.degrees);
    Dec = AngleDegs(Dec.degrees + Decplus.degrees);
}

