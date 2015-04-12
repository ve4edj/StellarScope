/* 
 * File:   DateTime.h
 * Author: simon
 *
 * Created on 20 March 2011, 20:31
 */

#ifndef DATETIME_H
#define	DATETIME_H

#include<math.h>

class DateTime {
public:
    int
        Year,
        Month,
        Day,
        Hour,
        Minute;
    double
        DecTime,
        Seconds;
    DateTime(){};
    DateTime(int yr, int mth, int dy, int hr, int min, double sec);
    void SetDecHours(double);
private:
    void SetDecTime();
};

#endif	/* DATETIME_H */

