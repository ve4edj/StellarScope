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
    DecTime = (double)Hour + ((double)Minute + Seconds/60)/60;
}

