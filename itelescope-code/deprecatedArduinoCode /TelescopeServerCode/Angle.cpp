/* 
 * File:   Angle.cpp
 * Author: simon
 * 
 * Created on 20 March 2011, 17:28
 */

#include "Angle.h"

void Angle::DtoR(){
    radians = degrees*M_PI/180;
}

void Angle::FillAngleContainers()
{
    HrsMinsSecs = AngleHMS(degrees);
    HrsMins = AngleHM(degrees);
    DegsMinsSecs = AngleDMS(degrees);
    DegsMins = AngleDM(degrees);
}

AngleDegs::AngleDegs(double degs){
    degrees = degs;
    DtoR();
    FillAngleContainers();
}

AngleDegs::AngleDegs(int degs, double decmins){
    degrees = (double)degs + decmins/60;
    DtoR();
    FillAngleContainers();
}

AngleDegs::AngleDegs(int degs, int mins, double secs){
    degrees = (double)degs + ((double)mins + secs/60)/60;
    DtoR();
    FillAngleContainers();
}

AngleHrs::AngleHrs(double hours){
    degrees = hours*360/24;
    DtoR();
    FillAngleContainers();
}

AngleHrs::AngleHrs(int hours, double dechmins){
    degrees = (hours + dechmins/60)*360/24;
    DtoR();
    FillAngleContainers();
}

AngleHrs::AngleHrs(int hours, int hminutes, double hsecs){
    degrees = (hours + (hminutes + hsecs/60)/60)*360/24;
    DtoR();
    FillAngleContainers();
}

AngleRads::AngleRads(double rads){
    radians = rads;
    degrees = rads*180/M_PI;
    FillAngleContainers();
}

AngleHMS::AngleHMS(double Degrees){
    while(Degrees<0)
    {
        Degrees = Degrees+360;
    }
    Degrees = fmod(Degrees,360);//constrain the angle to within one rotation;
    Seconds = fmod((Degrees*240),60);
    Minutes = (int)floor(Degrees*240/60)%60;
    Hours = floor(Degrees*240/3600);
}

AngleHM::AngleHM(double Degrees){
    while(Degrees<0)
    {
        Degrees = Degrees+360;
    }
    Degrees = fmod(Degrees,360);//constrain the angle to within one rotation;
    Minutes = fmod(Degrees*4,60);
    Hours = floor(Degrees*4/60);
}

AngleDMS::AngleDMS(double Degs){
    Seconds = fmod(Degs*3600,60);
    if(Degs>0)
    {
        Degrees = floor(Degs);
        Minutes = (int)floor(Degs*60)%60;
    }
    else
    {
        Degrees = ceil(Degs);
        Minutes = (int)ceil(Degs*60)%60;
    }

}

AngleDM::AngleDM(double Degs){
    Minutes = fmod(Degs*60,60);
    if(Degs>0)
    {
        Degrees = floor(Degs);
    }
    else
    {
        Degrees = ceil(Degs);
    }
}


