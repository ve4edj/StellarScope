/* 
 * File:   Coordinates.h
 * Author: simon
 *
 * Created on 19 July 2011, 22:05
 */

#ifndef COORDINATES_H
#define	COORDINATES_H

#include "Navigation.h"
#include "Observer.h"
#include "AstroTime.h"

class Coordinates : public Navigation{
public:
    Angle Az,Alt,Ra,Dec;
    Observer TimeAndLoc;
    Coordinates();
    Coordinates(Observer PosTme);
    void SetAzAlt(Angle AzIn, Angle AltIn);
    void SetRaDec(Angle RaIn, Angle DecIn);
    void SetAzAltJ2000(Angle AzIn, Angle AltIn);
    void CorrectToJ2000();
private:

};

#endif	/* COORDINATES_H */

