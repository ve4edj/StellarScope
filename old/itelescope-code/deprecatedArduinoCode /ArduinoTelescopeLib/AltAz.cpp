/* 
 * File:   AltAz.cpp
 * Author: simon
 * 
 * Created on 30 January 2011, 19:50
 */

#include "AltAz.h"
#include "DateTime.h"
#include "Angle.h"


AltAz::AltAz() {
}

void AltAz::UpdateTime(DateTime time){
    UT = time.DecTime;
    double J2000 = J2000Day(time.Year,time.Month,time.Day,time.DecTime);
    const double T1 = 100.46;
    const double T2 = 0.985647;
    const int T3 = 15;
    double STd = T1 + T2*J2000 + Long.degrees + T3*UT;
    STd = Param360(STd);
    //ST = AngleDegs(STd);
    //ST = SiderealTime(time,Long);
   // double JD = JulianDay(time.Year,time.Month,time.Day,time.DecTime);
    //double preST = get_apparent_sidereal_time(JD);
    //Angle PaST = AngleHrs(preST);
    //Angle ST2 = AngleDegs(PaST.degrees + Long.degrees);
    ST = NewSiderealTime(time,Long);
    int B=0;
}

void AltAz::ConvertToAltAz(Angle ra, Angle  dec){
    RA = ra;
    Dec = dec;
    UpdateHA();

    double Altr = asin(sin(Dec.radians)*sin(Lat.radians)+cos(Dec.radians)*cos(Lat.radians)*cos(HA.radians));

    Alt = AngleRads(Altr);

    double A = acos((sin(Dec.radians)-sin(Alt.radians)*sin(Lat.radians))/(cos(Alt.radians)*cos(Lat.radians)));
    if(sin(HA.radians)>0){
        Az = AngleRads(2*M_PI-A);
    }
    else{
        Az = AngleRads(A);
    }

}

void AltAz::ConvertToRaDec(Angle AltIn, Angle AzIn){
    Alt = AltIn;
    Az = AzIn;
    double fSinDecl;
    double fCosH;

    fSinDecl = (sin(Alt.radians) * sin(Lat.radians)) + (cos(Alt.radians) * cos(Lat.radians) * cos(Az.radians));
    Dec = AngleRads(asin(fSinDecl));
    fCosH = ((sin(Alt.radians) - (sin(Lat.radians) * sin(Dec.radians))) / (cos(Lat.radians) * cos(Dec.radians)));
    HA = AngleRads(acos(fCosH));
    if (sin(Az.radians) > 0)
    {
        HA = AngleDegs(360 - HA.degrees);
    }

    RA = AngleDegs(ST.degrees-HA.degrees);
}

void AltAz::AddPostion(Angle lat, Angle lon){
    Lat = lat;
    Long = lon;
}

bool AltAz::isLeapYear(int Year){
    bool temp;
    if(Year % 400 == 0 ){
        temp = true;
    }
    else if(Year % 100 == 0){
        temp = false;
    }
    else if(Year % 4 == 0){
        temp = true;
    }
    else{
        temp = false;
    }

    return(temp);
}

double AltAz::J2000Day(int Year, int Month, int Day,double Time){
    const int JmonthsN [] = {0,31,59,90,120,151,181,212,243,273,304,334};
    const int JmonthsL [] = {0,31,60,91,121,152,182,213,244,274,305,335};
    double J2000 = -731.5;
    for(int y=1998; y<Year; y++){
        if(isLeapYear(y)){
            J2000+=366;
        }
        else{
            J2000+=365;
        }
    }

    if(isLeapYear(Year)){
        J2000+=JmonthsL[Month-1];
    }
    else{
        J2000+=JmonthsN[Month -1];
    }

    J2000+=Day;
    J2000+=(Time/24);

    return(J2000);
}

double AltAz::JulianDay(int Year, int Month, int Day,double Time)
{
    return(2451545.0 + J2000Day(Year,Month,Day,Time));
}

double AltAz::Param360(double InP){
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

void AltAz::UpdateHA(){
    HA = AngleDegs(ST.degrees-RA.degrees);
}

Angle AltAz::SiderealTime(DateTime UTin, Angle Long){
    double fGST;
    double fLST;
    Angle dLST;
    bool bAdd = false;
    bool *pbAdd = &bAdd;
    double fTimeDiff;

    fGST = CalcGSTFromUT(UTin);
    fTimeDiff = ConvLongTUraniaTime(Long, pbAdd);

    if (bAdd == true)
    {
            fLST = fGST + fTimeDiff;
    }
    else
    {
            fLST = fGST - fTimeDiff;
    }

    while (fLST > 24)
    {
            fLST = fLST - 24;
    }

    while (fLST < 0)
    {
            fLST = fLST + 24;
    }
    dLST = AngleHrs(fLST);
    return(dLST);
}

double AltAz::ConvLongTUraniaTime(Angle fLong, bool *bAdd)
{
        double fMinutes;

        fMinutes = fLong.degrees * 4;
        if (fMinutes < 0)
        {
                *bAdd = false;
        }
        else
        {
                *bAdd = true;
        }
        fMinutes = fabs(fMinutes);


        return (fMinutes/60);
}

double AltAz::CalcGSTFromUT(DateTime dDate)
{
        double fJD;
        double fS;
        double fT;
        double fT0;
        double fUT;
        double fGST;

        fJD = JulianDay(dDate.Year,dDate.Month,dDate.Day,dDate.DecTime);
        fS = fJD - 2451545.0;
        fT = fS / 36525.0;
        fT0 = 6.697374558 + (2400.051336 * fT) + (0.000025862 * fT * fT);
        fT0 = fmod(fT0,24);
        fUT = dDate.DecTime;
        fUT = fUT * 1.002737909;
        fGST = fUT + fT0;
        while (fGST > 24)
        {
                fGST = fGST - 24;
        }

        return(fGST);
}

Angle AltAz::NewSiderealTime(DateTime UTin, Angle Long)
{
    double J2000Whole = 367*UTin.Year - floor(7*(UTin.Year + floor((UTin.Month+9)/12))/4) + floor(275*UTin.Month/9) + UTin.Day - 730531.5;
    double J2000Frac = (UTin.Hour + UTin.Minute/60 + UTin.Seconds/3600)/24;

    double J2000b = J2000Whole + J2000Frac;
    double J2000 = J2000Day(UTin.Year,UTin.Month,UTin.Day,UTin.DecTime);


    double GMST = 280.46061837 + 360.98564736629 * J2000;

    double LMST = GMST + Long.degrees;

    Angle SidTime = AngleDegs(Param360(LMST));
    return(SidTime);
}
