/*
The stellarium telescope library helps building
telescope server programs, that can communicate with stellarium
by means of the stellarium TCP telescope protocol.
It also contains smaple server classes (dummy, Meade LX200).

Author and Copyright of this file and of the stellarium telescope library:
Johannes Gajdosik, 2006

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include "ServerR2D2.hpp"
#include "Socket.hpp" // GetNow

#include <math.h>
#include<iostream>
#include "R2Duino.hpp"
#include "Angle.h"
#include "AltAz.h"
#include "DateTime.h"
#include "Observer.h"
#include "Coordinates.h"
#include <time.h>

ServerR2D2::ServerR2D2(int port)
            :Server(port)
{
    LastRA = 0.0;
    LastDec = 0.0;
	current_pos[0] = desired_pos[0] = 1.0;
	current_pos[1] = desired_pos[1] = 0.0;
	current_pos[2] = desired_pos[2] = 0.0;
	next_pos_time = -0x8000000000000000LL;
        //CallArd = R2Duino();
}

void ServerR2D2::step(long long int timeout_micros)
{
	long long int now = GetNow();
	if (now >= next_pos_time)
	{
		next_pos_time = now + 500000;
		current_pos[0] = 3*current_pos[0] + desired_pos[0];
		current_pos[1] = 3*current_pos[1] + desired_pos[1];
		current_pos[2] = 3*current_pos[2] + desired_pos[2];
		double h = current_pos[0]*current_pos[0]
		         + current_pos[1]*current_pos[1]
		         + current_pos[2]*current_pos[2];
		
		if (h > 0.0)
		{
			h = 1.0 / sqrt(h);
			current_pos[0] *= h;
			current_pos[1] *= h;
			current_pos[2] *= h;
		}
		else
		{
			current_pos[0] = desired_pos[0];
			current_pos[1] = desired_pos[1];
			current_pos[2] = desired_pos[2];
		}
		
		//const double ra = atan2(current_pos[1],current_pos[0]);
		//const double dec = atan2(current_pos[2],
		  //                       sqrt(current_pos[0]*current_pos[0]+current_pos[1]*current_pos[1]));

                R2Duino CallArd = R2Duino();
                time_t timeNow;
                timeNow = time(NULL);
                stringstream tString("");
                tString<<"T";
                tString<<timeNow;
                cout<<tString.str()<<endl;
                CallArd.SendMessage(tString.str());
                CallArd.RunLoop();

                Angle Dec = AngleRads(CallArd.DE);
                Angle RA = AngleRads(CallArd.RA);

                if(RA.radians == 0 && Dec.radians == 0)
                {
                  RA = AngleRads(LastRA);
                  Dec = AngleRads(LastDec);
                }

                LastRA = RA.radians;
                LastDec = Dec.radians;
                //Angle RA= AngleDegs(267);
                //Angle Dec = AngleDegs(15);
                //Angle Lat = AngleDegs(49);
                //Angle Long = AngleDegs(2);//TODO un hardcode angles.

                //time_t rawtime;
                //struct tm * timeinfo;

                /*time ( &rawtime );
                timeinfo = localtime ( &rawtime );
                DateTime TimeNow = DateTime((timeinfo->tm_year + 1900),(timeinfo->tm_mon + 1),timeinfo->tm_mday,timeinfo->tm_hour,timeinfo->tm_min,timeinfo->tm_sec);
                Observer Ob1 = Observer(Lat,Long);
                Ob1.UpdateTime(TimeNow);
                
                Coordinates Cc = Coordinates(Ob1);
                //AltAz AngleConvert = AltAz();
                //AngleConvert.AddPostion(Lat,Long);
                //AngleConvert.UpdateTime(TimeNow);
                //AngleConvert.ConvertToRaDec(Alt,Az);

                Angle RAA = AngleDegs(267);
                Angle Decc = AngleDegs(15);*/

                //const double ra = AngleConvert.RA.radians;
                //const double dec = AngleConvert.Dec.radians;
                const double ra = RA.radians;
                double decp = Dec.radians;
                if(decp>M_PI)
                {
                    decp = -2*M_PI+decp;
                }
                const double dec = decp;
		const unsigned int ra_int = (unsigned int)floor(
		                               0.5 +  ra*(((unsigned int)0x80000000)/M_PI));
		const int dec_int = (int)floor(0.5 + dec*(((unsigned int)0x80000000)/M_PI));
		const int status = 0;
		sendPosition(ra_int,dec_int,status);
                cout<<"*******************\n";
                cout<<"CP1= "<<ra<<"\n";
                cout<<"CP2= "<<dec<<"\n";
                //cout<<"CP3= "<<TimeNow.Hour<<":"<<TimeNow.Minute<<":"<<TimeNow.Seconds<<"\n";
	}
	
	Server::step(timeout_micros);
}

void ServerR2D2::gotoReceived(unsigned int ra_int, int dec_int)
{
	const double ra = ra_int*(M_PI/(unsigned int)0x80000000);
	const double dec = dec_int*(M_PI/(unsigned int)0x80000000);
	const double cdec = cos(dec);
        cout<<"goingto....................................\n";
        cout<<"ra="<<ra<<"\n";
        cout<<"dec="<<dec<<"\n";
	desired_pos[0] = cos(ra)*cdec;
	desired_pos[1] = sin(ra)*cdec;
	desired_pos[2] = sin(dec);
}


