/* 
 * File:   Navigation.cpp
 * Author: simon
 * 
 * Created on 19 July 2011, 21:59
 */

#include "Navigation.h"

Navigation::Navigation() {
}

double Navigation::Param360(double InP){
    double OuP;
    if(InP > 360){
        OuP = InP - 360;
        OuP = Param360(OuP);
    }
    else if (InP < 0){
        OuP = InP + 360;
        OuP = Param360(OuP);
    }
    else{
        OuP = InP;
    }

    return(OuP);
}



