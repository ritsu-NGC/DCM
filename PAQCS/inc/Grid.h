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


#ifndef GRID_H
#define	GRID_H

#include <stdlib.h>
#include <time.h>
#include <vector> 
#include <iostream>
#include <utility>
#include <algorithm>
#include <climits>
#include <iomanip>
#include <map>

using namespace std;

template<typename A, typename B>
ostream& operator<<(ostream &str, pair<A,B> &p){
    str<<"("<<p.first<<","<<p.second<<")";
    return str;
}

template<typename A>
ostream& operator<<(ostream &str, vector<A> &vec){
    for (int i=0;i<vec.size();i++)
        str<<vec[i]<<" ";
    str<<endl;
    return str;
}

template<typename A>
ostream& operator<<(ostream &str, vector<vector<A> > &grid){
    for (int j=0;j<grid.size();j++){
        for (int i=0;i<grid[j].size();i++){
            str<<setw(3)<<grid[j][i];
        }
        str<<endl;
    }
    return str;
}

template<typename A, typename B>
ostream& operator<<(ostream &str, map<A,B> &m){
    for (typename map<A,B>::iterator i=m.begin();i!=m.end();i++)
        str<<i->first<<": "<<i->second<<endl;
    str<<endl;
    return str;
}


class Grid{
private:
    vector<vector<int> > _allocate;
    vector<vector<int> > _freedom;
    
    int _width;
    int _height;
    bool _isTall; // Shape of the grid  Tall: **              
    
    void freedom(); // compute freedom of the grid
    void updateFreedom(pair<int,int>);
public:
    Grid(){}
    Grid(int width, int height);
    Grid(const Grid &);
    const Grid& operator=(const Grid &);
    void resetGrid();
    vector<vector<int> > getAlloc(){return _allocate;}
    int getW(){return _width;}
    int getH(){return _height;}
    bool getShape(){return _isTall;}
    pair<int, int> placeNeighbor(int idx, int rest_deg, int rest_act, vector<int> act, vector<pair<int,int> >pos);
    pair<int, int> idxToLoc(int idx); // give index and return location
    int locToIdx(pair<int,int> loc){return _allocate[loc.second][loc.first];} // give location and return idx
    void printGrid();
    void trivialLocate();//for testing
    void randomLocate();
};

double costFun(pair<int,int> &, vector<pair<int,int> > &, vector<int> &, int, int, int);
int max(int, int, int, int);    
int dist(pair<int,int> a, pair<int,int>b); // compute distance
#endif	/* GRID_H */

