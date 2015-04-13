/* 
 * File:   Position.cpp
 * Author: simon
 * 
 * Created on 19 July 2011, 21:32
 */

#include "Position.h"

Position::Position() {}

Position::Position(double La, double Lo){
    Lat = AngleDegs(La);
    Long = AngleDegs(Lo);
}

Position::Position(int LaD, double LaM, int LoD, double LoM){
    Lat = AngleDegs
}



