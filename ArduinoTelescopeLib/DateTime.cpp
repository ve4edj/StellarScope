/* 
 * File:   DateTime.cpp
 * Author: simon
 * 
 * Created on 20 March 2011, 20:31
 */

#include "DateTime.h"

DateTime::DateTime(int yr, int mth, int dy, int hr, int min, double sec)
{
    Year= yr; Month=mth; Day=dy; Hour=hr; Minute=min; Seconds=sec;
    SetDecTime();
}

void DateTime::SetDecHours(double hrs)
{
    Year = 0;
    Month = 0;
    Day = 0;
    Hour = floor(hrs);
    Minute = floor(fmod(hrs,1)*60);
    Seconds = fmod(fmod(hrs,1)*60,1)*60;
    SetDecTime();
}

void DateTime::SetDecTime()
{
    DecTime = (double)Hour + ((double)Minute + Seconds/60)/60;
}