/* 
 * File:   AstroTime.cpp
 * Author: simon
 * 
 * Created on 02 December 2011, 15:34
 */

#include "AstroTime.h"

AstroTime::AstroTime() {
}

DateTime AstroTime::CalcLSTFromUT(DateTime dDate, double fLong)
{
        double fGST;
        double fLST;
        DateTime dLST;
        bool bAdd = false;
        double fTimeDiff;

        fGST = CalcGSTFromUT(dDate).DecTime;
        fTimeDiff = ConvLongTUraniaTime(fLong, &bAdd).DecTime;

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
        dLST.SetDecHours(fLST);
        return dLST;
}

DateTime AstroTime::CalcGSTFromUT(DateTime dDate){
        double fJD;
        double fS;
        double fT;
        double fT0;
        DateTime dGST;
        double fUT;
        double fGST;

        fJD = GetJulianDay(dDate, 0);
        fS = fJD - 2451545.0;
        fT = fS / 36525.0;
        fT0 = 6.697374558 + (2400.051336 * fT) + (0.000025862 * fT * fT);
        fT0 = To24Hr(fT0);
        fUT = dDate.DecTime;
        fUT = fUT * 1.002737909;
        fGST = fUT + fT0;
        while (fGST > 24)
        {
                fGST = fGST - 24;
        }
        dGST.SetDecHours(fGST);
        return dGST;
    }

DateTime AstroTime::ConvLongTUraniaTime(double fLong, bool* pbAdd)
{
    //double fHours;
    double fMinutes;
    //double fSeconds;
    DateTime dDate;
    //DateTime dTmpDate;

    fMinutes = fLong * 4;
    if (fMinutes < 0)
    {
            *pbAdd = false;
    }
    else
    {
            *pbAdd = true;
    }
    fMinutes = fabs(fMinutes);

    dDate.SetDecHours(fMinutes/60);
    return dDate;
}

double AstroTime::ConvHAToRA(double fHA, DateTime dUT, double fLong)
{
    //Convert Hour Angle to Right Ascension at specified time and longitude
    double fLST;
    double fRA;

    fLST = CalcLSTFromUT(dUT, fLong).DecTime;

    fRA = fLST - fHA;
    fRA = To24Hr(fRA);

    return fRA;
}

void AstroTime::ConvHorToEqu(Angle AfLatitude, Angle AfAlt, Angle AfAzim, double* pfHA,double* pfDecl)
{
        double fSinDecl;
        double fCosH;

        //INPUT RADIANS fAlt = Trig.DegToRad(fAlt);
        //INPUT RADIANSfAzim = Trig.DegToRad(fAzim);
        //INPUT RADIANSfLatitude = Trig.DegToRad(fLatitude);

        double fLatitude = AfLatitude.radians;
        double fAlt = AfAlt.radians;
        double fAzim = AfAzim.radians;
        fSinDecl = (sin(fAlt) * sin(fLatitude)) + (cos(fAlt) * cos(fLatitude) * cos(fAzim));
        *pfDecl = asin(fSinDecl);
        fCosH = ((sin(fAlt) - (sin(fLatitude) * sin(*pfDecl))) / (cos(fLatitude) * cos(*pfDecl)));
        *pfHA = AngleRads(acos(fCosH)).degrees;
        if (sin(fAzim) > 0)
        {
                *pfHA = 360 - *pfHA;
        }

        *pfDecl = AngleRads(*pfDecl).degrees;
        *pfHA = *pfHA / 15.0;
}

double AstroTime::To24Hr(double inTime)
{

    while (inTime >= 24)
    {
            inTime = inTime - 24;
    }
    while (inTime < 0)
    {
            inTime = inTime + 24;
    }
    return inTime;

}


double AstroTime::GetJulianDay(DateTime dDate, int iZone)

{
        double fJD;
        double iYear;
        double iMonth;
        double iDay;
        double iHour;
        double iMinute;
        double iSecond;
        double iGreg;
        double fA;
        double fB;
        double fC;
        double fD;
        double fFrac;

        dDate = CalcUTFromZT(dDate, iZone);

        iYear = dDate.Year;
        iMonth = dDate.Month;
        iDay = dDate.Day;
        iHour = dDate.Hour;
        iMinute = dDate.Minute;
        iSecond = dDate.Seconds;
        fFrac = iDay + ((iHour + (iMinute / 60) + (iSecond / 60 / 60)) / 24);
        if (iYear < 1582)
        {
                iGreg = 0;
        }
        else
        {
                iGreg = 1;
        }
        if ((iMonth == 1) || (iMonth == 2))
        {
                iYear = iYear - 1;
                iMonth = iMonth + 12;
        }

        fA = (long)floor(iYear / 100);
        fB = (2 - fA + (long)floor(fA / 4)) * iGreg;
        if (iYear < 0)
        {
                fC = (int)floor((365.25 * iYear) - 0.75);
        }
        else
        {
                fC = (int)floor(365.25 * iYear);
        }
        fD = (int)floor(30.6001 * (iMonth + 1));
        fJD = fB + fC + fD + 1720994.5;
        fJD = fJD + fFrac;
        return fJD;
}

DateTime AstroTime::CalcUTFromZT(DateTime dDate, int iZone)
{
    if (iZone >= 0)
    {
        dDate.Hour-=iZone;
    }
    else
    {
        dDate.Hour+=iZone;
    }

    return(dDate);
}
