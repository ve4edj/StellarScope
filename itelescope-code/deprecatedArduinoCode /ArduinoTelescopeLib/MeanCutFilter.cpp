/* 
 * File:   MeanCutFilter.cpp
 * Author: simon
 * 
 * Created on 16 December 2011, 17:10
 */

#include "MeanCutFilter.h"

MeanCutFilter::MeanCutFilter() {
    fHolder = 5001;
}

MeanCutFilter::MeanCutFilter(int fIn)
{
    fHolder = fIn;
}

int MeanCutFilter::Filter(int input[],int length)
{
    int* pBuffer = input;

    for(int i = 0; i<floor(length/2); i++)
    {
        cut(pBuffer,length);
    }

    return(getMean(pBuffer,length));

}

int MeanCutFilter::getMean(int* pArr, int length)
{
    int Sum = 0;
    int count = 0;
    for(int i=0; i<length; i++)
    {
        if(*pArr!=fHolder)
        {
            Sum+=*pArr;
            count++;
        }
        pArr++;
    }

    int M= floor(Sum/count+0.5);
    return(M);
}

void MeanCutFilter::cut(int* pArr, int length)
{
    int mean = getMean(pArr,length);
    int* pAit = pArr;
    int diffRef = 0;
    int q = 0;
    bool qfull = false;

    for(int i=0; i<length; i++)
    {
        if(*pAit!=fHolder)
        {
            int diff = fabs(mean-*pAit);
            if(diff>diffRef)
            {
                diffRef=diff;
                q=i;
                qfull=true;
            }
        }
        pAit++;
    }

    if(qfull)
    {
        arrayShuffle(pArr,length,q);
    }
}

void MeanCutFilter::arrayShuffle(int* pArr, int length, int index)
{
    int* KillIndex = pArr + index;
    for(int i=0; i<length; i++)
    {
        if(pArr==KillIndex)
        {
            *pArr=fHolder;
        }
        pArr++;
    }
}
