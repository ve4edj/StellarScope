/* 
 * File:   AltAz.h
 * Author: simon
 *
 * Created on 30 January 2011, 19:50
 */

#ifndef ALTAZ_H
#define	ALTAZ_H

#include<math.h>
#include "Angle.h"
#include "DateTime.h"

class AltAz {
public:
    Angle Alt,
            Az,
            RA,// Right angle
            Dec;//Declination
    AltAz();
    void UpdateTime(DateTime time);
    void ConvertToAltAz(Angle ra, Angle  dec);
    void AddPostion(Angle lat, Angle lon);
    void ConvertToRaDec(Angle Alt, Angle Az);
private:
    //Class Members
    double UT;//Universal Time
    Angle
        ST,//Siderial Time
        Lat,//Latitude
        Long,//Longitude
        HA;// hour angle
        

    //Class Private Functions
    bool isLeapYear(int Year);
    double J2000Day(int Year,int Month,int Day,double Time);
    double JulianDay(int Year,int Month,int Day,double Time);
    double Param360(double);
    Angle SiderealTime(DateTime UTin,Angle Long);
    double CalcGSTFromUT(DateTime dDate);
    double ConvLongTUraniaTime(Angle fLong, bool *bAdd);
    void UpdateHA();
    Angle NewSiderealTime(DateTime UTin,Angle Long);
};

#endif	/* ALTAZ_H */

