/* 
 * File:   Angle.h
 * Author: simon
 *
 * Created on 20 March 2011, 17:28
 */

#ifndef ANGLE_H
#define	ANGLE_H
#include <math.h>

class AngleHMS {
public:
    int Hours, Minutes;
    double Seconds;

public:
    AngleHMS(){};
    AngleHMS(double Degrees);
};

class AngleHM {
public:
    int Hours;
    double Minutes;

public:
    AngleHM(){};
    AngleHM(double Degrees);
};

class AngleDMS {
public:
    int Degrees, Minutes;
    double Seconds;

public:
    AngleDMS(){};
    AngleDMS(double Degs);
};

class AngleDM {
public:
    int Degrees;
    double Minutes;
public:
    AngleDM(){};
    AngleDM(double Degs);
};


class Angle {
//Class members
public:
    double
        degrees,
        radians;
    AngleHMS HrsMinsSecs;
    AngleHM HrsMins;
    AngleDMS DegsMinsSecs;
    AngleDM DegsMins;

public:
    Angle(){};

protected:
    void DtoR();
    void FillAngleContainers();
    double OneRot(double);

};

class AngleDegs : public Angle{

public:
    AngleDegs(double degrees);
    AngleDegs(int degrees, double decmins);
    AngleDegs(int degrees, int minutes, double secs);


};

class AngleHrs : public Angle{
public:
    AngleHrs(double hours);
    AngleHrs(int hours, double dechmins);
    AngleHrs(int hours, int hminutes, double hsecs);

};

class AngleRads : public Angle{
public:
    AngleRads(double rads);
};



#endif	/* ANGLE_H */

