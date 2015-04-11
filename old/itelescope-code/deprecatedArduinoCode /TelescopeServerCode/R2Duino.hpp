/* 
 * File:   R2Duino.hpp
 * Author: simon
 *
 * Created on 20 January 2011, 17:20
 */

#ifndef R2DUINO_HPP
#define	R2DUINO_HPP

#include <cstdlib>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <sstream>
#include <iostream>

using namespace std;

class R2Duino {
public:

    //class members
    FILE *infile;
    double RA,DE;

    //class constructor
    R2Duino();

    //class Functions
    void RunLoop();
    void SendMessage(string);




};

#endif	/* R2DUINO_HPP */

