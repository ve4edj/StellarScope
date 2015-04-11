/* 
 * File:   Angle.cpp
 * Author: simon
 * 
 * Created on 20 March 2011, 17:28
 */

#include "Angle.h"

double Angle::OneRot(double degs)
{
    while(degs<0)
    {
        degs = degs+360;
    }
    degs = fmod(degs,360);//constrain the angle to within one rotation;
    
    return(degs);
}
void Angle::DtoR(){
    radians = degrees*M_PI/180;
}

void Angle::FillAngleContainers()
{
    degrees = OneRot(degrees);
    DtoR();
    HrsMinsSecs = AngleHMS(degrees);
    HrsMins = AngleHM(degrees);
    DegsMinsSecs = AngleDMS(degrees);
    DegsMins = AngleDM(degrees);
}

AngleDegs::AngleDegs(double degs){
    degrees = degs;
    FillAngleContainers();
}

AngleDegs::AngleDegs(int degs, double decmins){
    degrees = (double)degs + decmins/60;
    FillAngleContainers();
}

AngleDegs::AngleDegs(int degs, int mins, double secs){
    degrees = (double)degs + ((double)mins + secs/60)/60;
    FillAngleContainers();
}

AngleHrs::AngleHrs(double hours){
    degrees = hours*360/24;
    FillAngleContainers();
}

AngleHrs::AngleHrs(int hours, double dechmins){
    degrees = (hours + dechmins/60)*360/24;
    FillAngleContainers();
}

AngleHrs::AngleHrs(int hours, int hminutes, double hsecs){
    degrees = (hours + (hminutes + hsecs/60)/60)*360/24;
    FillAngleContainers();
}

AngleRads::AngleRads(double rads){
    degrees = rads*180/M_PI;
    FillAngleContainers();
}

AngleHMS::AngleHMS(double Degrees){
    Seconds = fmod((Degrees*240),60);
    Minutes = (int)floor(Degrees*240/60)%60;
    Hours = floor(Degrees*240/3600);
}

AngleHM::AngleHM(double Degrees){
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

