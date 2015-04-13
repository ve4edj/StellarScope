/* 
 * File:   R2Duino.cpp
 * Author: simon
 * 
 * Created on 20 January 2011, 17:20
 */

#include "R2Duino.hpp"

R2Duino::R2Duino() {
    const char *inname = "/dev/ttyACM0";
    int baud = 9600;
    infile = fopen(inname, "r+");
    char inbuf[80];

    /*
       Instead of all of the "usual" stuff to set up
       the input port, I'll just cheat with stty
    */
    sprintf(inbuf, "stty -F %s %d raw", inname, baud);
    system(inbuf);
    if (!infile) {
        fprintf(stderr, "Can't open %s for reading.\n", inname);
        exit(EXIT_FAILURE);
    }
    printf("Opened %s for reading\n.", inname);
}

void R2Duino::RunLoop(){
    bool Leap = false;
    while(Leap == false){
        bool Jump = false;
        stringstream TheLine("");

        while (Jump == false) {
            int inchar;
            inchar = (unsigned int)getc(infile);
            if (inchar == '\n') {
                    Jump = true;
                }
            TheLine<<(char)inchar;


        }

        string TL2 = TheLine.str();


        if(TL2.size()>=39 && TL2.size()<=41)
        {
            try{
                int Bi1,Bi2,Bi3;
                Bi1 = TL2.find("[",16);
                Bi2 = TL2.find("]",16);
                Bi3 = TL2.find(",",Bi1);

                string RAstr = TL2.substr(Bi1+1,(Bi3-Bi1-1));
                string Decstr = TL2.substr(Bi3+1,(Bi2-Bi3-1));


                RA = atof((char*)RAstr.c_str());
                DE = atof((char*)Decstr.c_str());
                Leap =true;
            }
            catch(exception e)
            {
                printf("aborted Capture",e.what());
            }


        }


    }
}

void R2Duino::SendMessage(string message)
{
    //const char *inname = "/dev/ttyACM0";
    //FILE *outfile = fopen(inname, "w");
    int e;
    string::iterator mIt = message.begin();
    while(mIt != message.end())
    {
        e = putc((unsigned int)*mIt,infile);
        mIt++;
    }

}


