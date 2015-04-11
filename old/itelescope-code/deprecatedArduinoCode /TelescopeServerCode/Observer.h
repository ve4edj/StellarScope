/* 
 * File:   Observer.h
 * Author: simon
 *
 * Created on 19 July 2011, 21:42
 */

#ifndef OBSERVER_H
#define	OBSERVER_H

#include "Angle.h"
#include "DateTime.h"
#include "Navigation.h"

class Observer : public Navigation{
public:
    Angle Lat;
    Angle Long;
    Angle LST;
    DateTime Time;
    Observer();
    Observer(Angle la, Angle lo);
    void UpdateTime(DateTime tme);
private:
    void SiderealTime();
    bool isLeapYear(int Year);
    double J2000Day(int Year,int Month,int Day,double Time);

};

#endif	/* OBSERVER_H */

