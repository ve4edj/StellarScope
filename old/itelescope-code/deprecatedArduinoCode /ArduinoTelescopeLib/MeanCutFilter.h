/* 
 * File:   MeanCutFilter.h
 * Author: simon
 *
 * Created on 16 December 2011, 17:10
 */

#ifndef MEANCUTFILTER_H
#define	MEANCUTFILTER_H
#include <math.h>

class MeanCutFilter {
    int fHolder;
public:
    MeanCutFilter();
    MeanCutFilter(int);
    int Filter(int[],int);
private:
    int getMean(int*,int);
    void cut(int*,int);
    void arrayShuffle(int*,int,int);
};

#endif	/* MEANCUTFILTER_H */

