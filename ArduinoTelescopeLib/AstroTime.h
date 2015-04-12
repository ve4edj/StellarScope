/* 
 * File:   AstroTime.h
 * Author: simon
 *
 * Created on 02 December 2011, 15:34
 */

#ifndef ASTROTIME_H
#define	ASTROTIME_H

#include "DateTime.h"
#include<math.h>
#include "Angle.h"

class AstroTime {
public:
    AstroTime();
 
    //some functions for timey stuff
    DateTime CalcLSTFromUT(DateTime,double);
    double ConvHAToRA(double, DateTime, double);
    void ConvHorToEqu(Angle, Angle, Angle, double*, double*);
private:
    DateTime CalcGSTFromUT(DateTime);
    DateTime ConvLongTUraniaTime(double,bool*);
    double To24Hr(double);
    double GetJulianDay(DateTime, int);
    DateTime CalcUTFromZT(DateTime, int);


};

#endif	/* ASTROTIME_H */

