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


#ifndef INTERACTIVEGRAPH_H
#define	INTERACTIVEGRAPH_H

#include <stack>
#include <map>
#include <set>
#include <vector>
#include <queue>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <utility>
#include "math.h"
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/property_map/property_map.hpp>
#include "Grid.h"


using namespace boost;
using std::map;
using std::set;
using std::priority_queue;
using std::deque;
using std::vector;
using std::string;
using std::ifstream;
using std::ios;
using std::stringstream;
using std::pair;
using std::cout;
using std::endl;
using std::stack;

enum edge_act_t {edge_act}; // e_ij=the interaction of v_i to v_j
enum vertex_idx_t {vertex_idx}; // index of the vertex

typedef property<edge_act_t, int> EdgeProperties;
typedef property<vertex_idx_t, int> VertexProperties;

typedef adjacency_list<vecS, vecS,  undirectedS, VertexProperties, EdgeProperties > Graph;

namespace boost{
    BOOST_INSTALL_PROPERTY(edge,act);
    BOOST_INSTALL_PROPERTY(vertex,idx);
}

typedef graph_traits<Graph>::vertices_size_type     vertex_size;
typedef graph_traits<Graph>::edges_size_type        edge_size;
typedef graph_traits<Graph>::vertex_descriptor      vertex_descriptor;
typedef graph_traits<Graph>::vertex_iterator        vertex_iterator;
typedef graph_traits<Graph>::edge_descriptor        edge_descriptor;
typedef graph_traits<Graph>::edge_iterator          edge_iterator;
typedef graph_traits<Graph>::out_edge_iterator      out_edge_iterator;
typedef graph_traits<Graph>::in_edge_iterator       in_edge_iterator;

typedef property_map<Graph,vertex_idx_t>::type    map_vertex_idx;
typedef property_map<Graph,edge_act_t>::type       map_edge_act;

typedef pair<int,int> locg; // location on grid
typedef pair<pair<int,int>,pair<int,int> > locswap;

class Node{
public:
    int _idx; // index of the node
    int _deg; // degree, the number of qubits to which it interacts
    int _act; // action, the number of two-qubit gates to which it interacts

    Node(int idx, int deg, int act):_idx(idx),_deg(deg),_act(act){}
    bool operator<(const Node &n) const { 
        bool answer=false;
        double deg1=_deg;
        double act1=_act;
        double deg2= n._deg;
        double act2= n._act;
        
        // trivial node
        if (deg1==0 && deg2==0)
            return false;
        if (deg1==0)
            return true;        
        if (deg2==0)
            return false;
       
        double rate1=act1/deg1;   
        double rate2=act2/deg2;

        // act-->rate-->deg
        if (act1 < act2)
           answer=true;  
        else if (act1==act2){
            if (rate1 < rate2)                      
                answer=true; 
            else if (rate1==rate2)
                if(deg1 < deg2)
                    answer=true;     
        }
        return answer;
            
    }
};

class InterActGraph{
private: 
    Graph _g;
    string _filename;
    int _numAct;   // equals number of two-qubit gates
    int _origQubit; // original qubit
    int _numQubit; // equals number of vertex (some dummy qubits may be added)
    int _num2QGate;
    map<string,int> _nameToIdx;
    map<int,string> _idxToName;
    vector<Node> _node;   
    Grid _grid; // records qubit info flow
    Grid _placement;// records placement (fixed) (It should be redundant..... in
                    // insertSwap2 function, I made an extra copy.
    string _cktbuffer; // store the input ckt file
    void addNode(int i);
    void addEdge(int i, int j);
    void addAct(int i, int j);
    void buildMaps();
public:
    InterActGraph(string, int=1, int=1, int=-1);
    int getOrigQubit(){return _origQubit;}
    int getGridWidth(){return _placement.getW();}
    int getGridHeight(){return _placement.getH();}
    int getNum2Qgate(){return _num2QGate;}
    string getFileName(){return _filename;}
    void resetGrid();
    void mapToGrid(int=-1);
    void trivialMapToGrid();//for testing
    void randomMapToGrid();
    void printGraph();
    void printInfo();
    void printCurrentQubitFlow(){return _grid.printGrid();}
    void printNodeRanking();
    int insertSwap1(string);
    pair<int,int> insertSwap2(string,int,int=0);    
};
bool isTwoQubitGate(string);
void findPath(locg control, locg target,  vector<locg > &path);
double shortestPath(locg pos_control, locg pos_target, locg via, vector<locswap > &path, pair<locg ,locg > &cTot,
        vector<vector< int> > &allocation, deque<pair<int,int> > &future, bool isTall);
void trail(locg start, locg end, int quadrant, vector<locg> &visited, vector<locg> &oneRoute, vector<vector<locg> > &allRoute, bool);
void swapQubit(locg a, locg b, vector<vector<int> > &locMap);
void swapQubit(int a, int b, map<int,locg> &locMap);
void printGrid(vector<vector<int> > &grid);
vector<locg> findMidPoint(locg &, locg &, bool);
void fillFutureGateBuffer(istream &,map<string,int>&, deque<pair<int,int> > &future, int=1);
#endif	/* INTERACTIVEGRAPH_H */

