/* 
 * File:   Observer.cpp
 * Author: simon
 * 
 * Created on 19 July 2011, 21:42
 */

#include "Observer.h"

Observer::Observer() {
}

Observer::Observer(Angle la, Angle lo) {
    Lat = la; Long = lo;
    UpdateTime(DateTime(2000,1,1,12,0,0));
}

void Observer::UpdateTime(DateTime Tme){
    Time = Tme;
    SiderealTime();

}

void Observer::SiderealTime()
{
    double J2000 = J2000Day(Time.Year,Time.Month,Time.Day,Time.DecTime);


    double GMST = 280.46061837 + 360.98564736629 * J2000;

    double LMST = GMST + Long.degrees;

    LST = AngleDegs(Param360(LMST));
    
}

bool Observer::isLeapYear(int Year){
    bool temp;
    if(Year % 400 == 0 ){
        temp = true;
    }
    else if(Year % 100 == 0){
        temp = false;
    }
    else if(Year % 4 == 0){
        temp = true;
    }
    else{
        temp = false;
    }

    return(temp);
}

double Observer::J2000Day(int Year, int Month, int Day,double Time){
    const int JmonthsN [] = {0,31,59,90,120,151,181,212,243,273,304,334};
    const int JmonthsL [] = {0,31,60,91,121,152,182,213,244,274,305,335};
    double J2000 = -731.5;
    for(int y=1998; y<Year; y++){
        if(isLeapYear(y)){
            J2000+=366;
        }
        else{
            J2000+=365;
        }
    }

    if(isLeapYear(Year)){
        J2000+=JmonthsL[Month-1];
    }
    else{
        J2000+=JmonthsN[Month -1];
    }

    J2000+=Day;
    J2000+=(Time/24);

    return(J2000);
}


