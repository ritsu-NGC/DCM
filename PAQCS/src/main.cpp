/*-------------------------------------------------------------------------
 *                              PAQCS 
 *
 *         Copyright 2013 
 *                    Princeton University
 *                         All Rights Reserved
 *
 *                         
 *  PAQCS has been developed by Chia-Chun Lin at Princeton University,  
 *  Princeton.   
 *  If your use of this software contributes to a published paper, we  
 *  request that you cite our paper: C.-C. Lin, S. Sur-Kolay and N. K. Jha,
 *  "PAQCS: Physical Design-aware Fault-tolerant Quantum Circuit Synthesis," 
 *  IEEE Transactions on VLSI Systems, DOI: 10.1109/TVLSI.2014.2337302.
 *  
 *  Permission to use, copy, and modify this software and its 
 *  documentation is granted only under the following terms and 
 *  conditions. Both the above copyright notice and this permission notice 
 *  must appear in all copies of the software, derivative works or modified 
 *  versions, and any portions thereof, and both notices must appear in 
 *  supporting documentation.
 *
 *  This software may be distributed (but not offered for sale or   
 *  transferred for compensation) to third parties, provided such third 
 *  parties agree to abide by the terms and conditions of this notice.
 *
 *  This software is distributed in the hope that it will be useful to the
 *  community, but WITHOUT ANY WARRANTY; without even the implied warranty 
 *  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
 *
 *-----------------------------------------------------------------------*/


#include <cstdlib>
#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include "time.h"
#include "../inc/InteractiveGraph.h"
#include "../inc/Grid.h"
#include "../inc/InsertSwap.h"
#include <queue>

using namespace std;

int main(int argc, char** argv) {
 // calculate synthesis time
    if (argc<3 || argc==4 || argc==5){
        cout<<"<input file> <output file> <grid W> <grid H> <window size>"<<endl;
        exit(1);
    }
    
    string file(argv[1]);
    string outfile(argv[2]);
    int grid_W=1;
    int grid_H=1;
    int look=3;
    
    if (argc==6){
        grid_W=atoi(argv[3]);
        grid_H=atoi(argv[4]);
        look=atoi(argv[5]);
    }
    
    struct timespec time_start;
    clock_gettime(CLOCK_MONOTONIC,&time_start);
 
    InterActGraph graph(file,grid_W,grid_H,-1);

    int num2q=graph.getNum2Qgate();
    int minSwap=INT_MAX,numSwap;
    int bound, minbound;
    int minSwap2=INT_MAX;
    int minq,minl;
        
    cout<<"#qubit="<<graph.getOrigQubit()<<endl;
    cout<<"#2qGate: "<<num2q<<endl;
    cout<<"(W,H)= ("<<graph.getGridWidth()<<","<<graph.getGridHeight()<<")"<<endl;
       
    minSwap=INT_MAX; 
           
    for (int q=0;q<graph.getOrigQubit();q++) 
    {
        graph.resetGrid();
        graph.mapToGrid(q);
        pair<int,int> swaps;

        bound=graph.insertSwap1(outfile);
        swaps=graph.insertSwap2(outfile,look,1);

        if (swaps.first<minSwap){
            minSwap=swaps.first;
            minSwap2=swaps.second;
            minq=q;
            minl=look;
            minbound=bound;
        }       
    }
        
    cout<<"window size="<<minl<<","<< " costB="<<minbound<<", costR="<< minSwap2<<", costU= "<<minSwap<<endl;
  
    struct timespec time_end;
    clock_gettime(CLOCK_MONOTONIC, &time_end);
    double start_ns = time_start.tv_sec * 1000000000. + time_start.tv_nsec;
    double end_ns   =  time_end.tv_sec * 1000000000. +   time_end.tv_nsec;
    double duration = (end_ns-start_ns)/1000000000.;
    cout<<" ***Synthesis Time="<<duration<< "***" <<endl;
    
    return 0;
}