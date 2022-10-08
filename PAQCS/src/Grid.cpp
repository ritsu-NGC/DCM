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


#include "../inc/Grid.h"

//This is the cost function of placement
double costFun(pair<int,int> &center, vector<pair<int,int> > &neighbor, vector<int> &placed_act, int rest_deg, int rest_act, int freedom){

    double cost=0;
    double placed_neighbor_cost=0;
    double non_placed_cost=0;
    
    for (int i=0;i<neighbor.size();i++){
        placed_neighbor_cost+=(dist(center,neighbor[i])-1)*placed_act[i];
    }
    
    if (rest_deg>0)
            non_placed_cost=min(0,rest_deg-freedom)* (double) rest_act/rest_deg;
 
    cost=(placed_neighbor_cost+non_placed_cost)*10+(rest_deg-freedom);

    return cost;
}

int max(int a, int b, int c, int d){
    int t1, t2;
    t1=a>b?a:b;
    t2=c>d?c:d;
    return t1>t2?t1:t2;
}

int dist(pair<int,int> a, pair<int,int>b){
    return abs(a.first-b.first)+abs(a.second-b.second);
}

Grid::Grid(const Grid & g){
    _allocate=g._allocate;
    _freedom=g._freedom;
    _width=g._width;
    _height=g._height;
    _isTall=g._isTall;
}

const Grid & Grid::operator =(const Grid &g){
    if (this!=&g){
        _allocate=g._allocate;
        _freedom=g._freedom;
        _width=g._width;
        _height=g._height;
        _isTall=g._isTall;
    }
}

Grid::Grid(int width, int height):_width(width),_height(height){
    _allocate=vector<vector<int> > (_height,vector<int>(_width,-1));
    _freedom =vector<vector<int> > (_height,vector<int>(_width,0));
    freedom();
    // set shape of the grid
    if (width<=height)
        _isTall=true;
    else
        _isTall=false;

}


void Grid::resetGrid(){
    for(int j=0;j<_height;j++){
        for(int i=0;i<_width;i++){
            _allocate[j][i]=-1;
            
            _freedom[j][i]=0;
        }
    }
    freedom();
}

void Grid::freedom(){
    for (int j=0;j<_height;j++){
        for (int i=0;i<_width;i++){
            int free=0;
            if (i-1>=0) // left
                if (_allocate[j][i-1]==-1) 
                    free++;
            if (j-1>=0) 
                if (_allocate[j-1][i]==-1) // up
                    free++;
            if (i+1<_width) // right
                if (_allocate[j][i+1]==-1)
                    free++;
            if (j+1<_height)
                if (_allocate[j+1][i]==-1)
                    free++;
            _freedom[j][i]=free;
        }
    }
        
}

void Grid::updateFreedom(pair<int,int> pos){
    int x=pos.first;
    int y=pos.second;
    _freedom[y][x]=0;
    
    if (x-1>=0)
        _freedom[y][x-1]=max(0,--_freedom[y][x-1]);
    if (x+1<_width)
        _freedom[y][x+1]=max(0,--_freedom[y][x+1]);
    if (y-1>=0)
        _freedom[y-1][x]=max(0,--_freedom[y-1][x]);
    if (y+1<_height)
        _freedom[y+1][x]=max(0,--_freedom[y+1][x]);
    
}


void Grid::printGrid(){
    cout<<"----- Print Grid -----"<<endl;
    cout<<"--- allocation map ---"<<endl;
    for (int j=0;j<_height;j++){
        for (int i=0;i<_width;i++){
            cout<<std::setw(3)<<_allocate[j][i]<<" ";
        }
        cout<<endl;
    }
}


pair<int, int> Grid::placeNeighbor(int idx, int rest_deg, int rest_act, vector<int> placed_act, vector<pair<int,int> >neighbor){
    int x,y;
    //use first neighbor as starting point
    x=neighbor[0].first;
    y=neighbor[0].second;
    int maxDist=max(dist(neighbor[0],pair<int,int>(0,0)),
                    dist(neighbor[0],pair<int,int>(0,_height-1)),
                    dist(neighbor[0],pair<int,int>(_width-1,0)),
                    dist(neighbor[0],pair<int,int>(_width-1,_height-1)));
   // cout<<"Maxdist="<<endl;
   // cout<<maxDist<<endl;
    
    // 1  2  3  4
    // 5  6  7  8
    // 9 10 11 12  
    // center 6: 7->10->5->2->8->11->9->1->3->4    
    pair<int,int> bestPlace(-1,-1);
    double minCost=INT_MAX;    
    double cost;
    // compute center point
    if (_allocate[y][x]<0){
        pair<int,int> cur(x,y);
        cost=costFun(cur,neighbor,placed_act,rest_deg,rest_act,_freedom[y][x]);
        if (cost<minCost){
            bestPlace=cur;
            minCost=cost;
        }
    }
    // compute neighbor point
    for (int dist=1;dist<=maxDist;dist++){

        int a=dist,b=0;
        int a_step=-1, b_step=1;
     
        for (int m=0;m<4*dist;m++){
            if(_isTall){
                if ((x+a)<_width && (x+a)>=0 && (y+b)<_height && (y+b)>=0){ // valid location
                   
                    //cout<<"("<<x+a<<","<<y+b<<")"<<endl;
                    if (_allocate[y+b][x+a]<0){ // not allocated
                        pair<int,int> cur(x+a,y+b);
                                              
                        cost=costFun(cur,neighbor,placed_act,rest_deg,rest_act,_freedom[y+b][x+a]);

                        if (cost<minCost){
                            bestPlace=cur;
                            minCost=cost;
                        }
                    }   
                }
            }
            else{
                if ((x+b)<_width && (x+b)>=0 && (y+a)<_height && (y+a)>=0){ // valid location
                    //cout<<"("<<x+a<<","<<y+b<<")"<<endl;
                    if (_allocate[y+a][x+b]<0){ // not allocated
                        pair<int,int> cur(x+b,y+a);

                        double cost=costFun(cur,neighbor,placed_act,rest_deg,rest_act,_freedom[y+a][x+b]);

                        if (cost<minCost){
                            bestPlace=cur;
                            minCost=cost;
                        }
                    }   
                }
            }
            
            if(a==-dist)
                a_step=1;
            if(b==dist)
                b_step=-1;
            else if (b==-dist)
                b_step=1;

            a+=a_step;
            b+=b_step;
        }
    }    
    
    if (bestPlace.first==-1){
        cout<<"Error of placing qubit!, no allocation found"<<endl;
        cout<<"maxDist= "<<maxDist<<endl;
        cout<<"idx= "<<idx<<endl;
        for (int j=0;j<_allocate.size();j++){
            for(int i=0;i<_allocate[j].size();i++){
                cout<<setw(3)<<_allocate[j][i]<<" ";
            }
            cout<<endl;
        }
        
        for (int j=0;j<_freedom.size();j++){
            for(int i=0;i<_freedom[j].size();i++){
                cout<<setw(3)<<_freedom[j][i]<<" ";
            }
            cout<<endl;
        }
        
    }
    _allocate[bestPlace.second][bestPlace.first]=idx;
  
    updateFreedom(bestPlace);
    return bestPlace;
}

pair<int, int> Grid::idxToLoc(int idx){
    for (int j=0;j<_height;j++){
        for (int i=0;i<_width;i++){
            if (_allocate[j][i]==idx)
                return pair<int,int>(i,j);
        }
    }
}

void Grid::trivialLocate(){
    int k=0;
    for (int j=0;j<_height;j++){
        for (int i=0;i<_width;i++){
            _allocate[j][i]=k;
            _freedom[j][i]=0;
            k++;
        }
    }
}

void Grid::randomLocate(){
    vector <int> arr(_width*_height);
    for (int i=0;i<arr.size();i++){
        arr[i]=i;
    }
    srand(time(NULL));  
    // random shuffle
    for (int i=0;i<arr.size();i++){
         
        int random=rand()%arr.size();
        int tmp=arr[i];
        arr[i]=arr[random];
        arr[random]=tmp;
    }
    
    int k=0;
    for (int j=0;j<_height;j++){
        for (int i=0;i<_width;i++){
            _allocate[j][i]=arr[k];
            _freedom[j][i]=0;
            k++;
        }
    }    
    
}