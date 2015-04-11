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

#ifndef _SERVER_R2D2_HPP_
#define _SERVER_R2D2_HPP_

#include "Server.hpp"
#include "R2Duino.hpp"

//! Telescope server class for a virtual telescope that requires no physical device.
//! Useful for remote connection testing.
class ServerR2D2 : public Server
{
public:
    double LastRA;
    double LastDec;
	ServerR2D2(int port);
	void step(long long int timeout_micros);
	
private:
	void gotoReceived(unsigned int ra_int,int dec_int);
	double current_pos[3];
	double desired_pos[3];
	long long int next_pos_time;
        //R2Duino CallArd;
};

#endif
