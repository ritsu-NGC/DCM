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


#include <stack>
#include "../inc/InteractiveGraph.h"

InterActGraph::InterActGraph(string file, int width, int height, int look):_numAct(0),_numQubit(0),_filename(file){
    
    ifstream input(file.c_str(),ifstream::in);
    
    int num2QGate=0;
    
    if (!input){
        cout<<"Cannot open file: "<<file<<endl;
        exit(1);
    }
    
    string s,token;
    
    while (getline(input,s)){  //iterate for each line
        _cktbuffer+=(s+'\n');
        stringstream ss;
        ss.str(s); // convert to stringstream
        ss>>token;
        
        if (token.compare("#")==0)
            continue;
        if (token.compare(".qubit")==0)
            continue;
        if (token.compare(".begin")==0){ 
            _origQubit=_numQubit;
            //resize tile
            if (_numQubit>width*height){
                // cout<<"Grid too small! #qubit="<<_numQubit<<" Grid="<<width<<"x"<<height<<endl;
                height=ceil(sqrt(_numQubit));
                // width=ceil(sqrt(_numQubit));
                width=ceil((double)_numQubit/height);              
                // cout<<"Resize it to "<<width<<"x"<<height<<endl;
            }
            
            // declare grid
            _placement=Grid(width,height);
            _grid=Grid(width,height);
            
            int qubit=_numQubit;
            for (int i=0;i<width*height-qubit;i++) //fill blank qubits
            {
                string name("xxc");
                name+='0'+i;
                _nameToIdx.insert(pair<string, int>(name,_numQubit));
                _idxToName.insert(pair<int,string>(_numQubit,name));
                addNode(_numQubit++);
            }
            continue;
        }
           
        if (token.compare("qubit")==0){ // qubit declaration
            ss>>token;
            _nameToIdx.insert(pair<string, int>(token,_numQubit));
            _idxToName.insert(pair<int,string>(_numQubit,token));
            addNode(_numQubit++);
            continue;
        }
        if (token.compare("Prep0")==0)
            continue;
        
        if (token.compare(".end")==0)
            continue;
        if (token.compare("CNOT")==0 || token.compare("SWAP")==0 || 
            token.compare("CZ")==0 || token.compare("GEO")==0 || 
            token.compare("CP")==0 || token.compare("ZENO")==0){
            int idx1,idx2;
            ss>>token;
            idx1=_nameToIdx[token];
            ss>>token;
            idx2=_nameToIdx[token];
            if (look!=-1){
                if (num2QGate<=look){
                    addEdge(idx1,idx2);              
                }
            }else{
                addEdge(idx1,idx2); 
            }            
            num2QGate++;       
        }          
    }
    buildMaps();
    input.close();
    _num2QGate=num2QGate;
}

void InterActGraph::addNode(int idx){
    vertex_descriptor v;
    map_vertex_idx    vertex_idx_map = get (vertex_idx,_g );   
    v=boost::add_vertex(_g);
    put(vertex_idx_map,v,idx);
}

void InterActGraph::addEdge(int idx1, int idx2){
    vertex_descriptor v1,v2;
    edge_descriptor e;
    map_edge_act     edge_act_map = get(edge_act, _g);
    bool exist;
    v1=vertex(idx1,_g);
    v2=vertex(idx2,_g);
    tie(e,exist)=edge(v1,v2,_g);
    if (!exist){ // if edge not exist, create it
        add_edge(v1,v2,1,_g);
    }
    else{ // if edge exist, add weight (act) by 1
        put(edge_act_map,e,++get(edge_act_map,e));
    }
}

// for debugging
void InterActGraph::printGraph(){
    vertex_descriptor s,t;
    edge_iterator e_ii,e_end;
    map_edge_act edge_act_map = get(edge_act, _g);
    map_vertex_idx vertex_idx_map = get(vertex_idx, _g);
    
    cout<<"Number of nodes = "<<num_vertices(_g)<<endl;
    cout<<"Number of edges = "<<num_edges(_g)<<endl;
    cout<<"u --> v    act"<<endl;
    for (tie(e_ii,e_end)=edges(_g);e_ii!=e_end;++e_ii){
        s=source(*e_ii,_g);
        t=target(*e_ii,_g);
        cout<<get(vertex_idx_map,s)<<"     "<<get(vertex_idx_map,t)<< "     " << get(edge_act_map,*e_ii)<<endl;
    }
}

void InterActGraph::buildMaps(){
    vertex_iterator v_ii,v_end;
    out_edge_iterator e_ii,e_end;
    int idx;
    int degree;
    
    map_vertex_idx vertex_idx_map = get(vertex_idx, _g);
    map_edge_act edge_act_map = get(edge_act, _g);
    
    for (tie(v_ii,v_end)=vertices(_g);v_ii!=v_end;++v_ii){
        idx=get(vertex_idx_map,*v_ii);
        degree=out_degree(*v_ii,_g);
        int act=0;
        for (tie(e_ii,e_end)=out_edges(*v_ii,_g);e_ii!=e_end;++e_ii){
            act+=get(edge_act_map,*e_ii);
        }
        Node node(idx,degree,act);
        _node.push_back(node);
        
    }
}

// for debugging
void InterActGraph::printInfo(){
    cout<<"-------- Graph info: ----------"<<endl;
    cout << "vertex --> degree --> act"<<endl;
    for(int i=0;i<_node.size();i++)
        cout<<_node[i]._idx<<" "<<_node[i]._deg<<" "<<_node[i]._act<<endl;
}

// layout qubit in-order, i.e., q0, q1, q2, ...
void InterActGraph::trivialMapToGrid(){
    _placement.trivialLocate();
    _grid=_placement;
  
}

// random layout, without routing optimization
void InterActGraph::randomMapToGrid(){
    _placement.randomLocate();
    _grid=_placement;
}

// reset the qubit layout
void InterActGraph::resetGrid(){
    _placement.resetGrid();
    _grid=_placement;
}

// for debugging
void InterActGraph::printNodeRanking(){
    vector<Node> nodes=_node;
    sort(nodes.begin(),nodes.end());
    cout<<"Node ranking: "<<endl;
    for (int i=nodes.size()-1;i>=0;i--)
        cout<<setw(2)<<nodes[i]._idx<<" " ;
    cout<<endl;
}

// qubit placement
void InterActGraph::mapToGrid(int rootIdx){
    
    // Select root, which has highest act/deg
    Node maxNode=_node[0];
    bool done=true;
    
    
    queue<Node> que;
    out_edge_iterator e_ii,e_end;
    vertex_descriptor v,v_adj;
    map_vertex_idx    vertex_idx_map = get (vertex_idx,_g );   
    map_edge_act      edge_act_map = get (edge_act,_g );  
    int v_adj_idx;
    vector<bool> processed(_node.size(),false);
    vector<vector<pair<int,int> > > neighbors(_node.size());
    vector<vector<int> >neighborsAct(_node.size());
    vector<int> deg(_node.size()); // degree table 
    vector<int> act(_node.size()); // action table
    for (int i=0;i<_node.size();i++){
        deg[i]=_node[i]._deg;
        act[i]=_node[i]._act;
    }
      
    pair<int,int> center(_placement.getW()/2,_placement.getH()/2); 
    vector<Node> nodes=_node;

    sort(nodes.begin(),nodes.end());

    do{
        // select root
        if(rootIdx==-1 || !done){
            for (int i=nodes.size()-1;i>=0;i--){
                if (!processed[nodes[i]._idx]){
                    maxNode=_node[nodes[i]._idx];
                    break;
                }
            }           
        }
        else{

            // use n-th rank of sorted node
            maxNode=_node[nodes[nodes.size()-1-rootIdx]._idx];
        }
        neighbors[maxNode._idx].push_back(center);
        neighborsAct[maxNode._idx].push_back(0);
        
        que.push(maxNode);
        //place node
        while (!que.empty()){
            Node cur=que.front();
            
            que.pop();
            if (processed[cur._idx])
                continue;        

            pair<int,int> location=_placement.placeNeighbor(cur._idx,deg[cur._idx],act[cur._idx],neighborsAct[cur._idx],neighbors[cur._idx]);
            
            processed[cur._idx]=true;            
            
            // find adjacent vertices
            priority_queue<Node> priQue;
            v=vertex(cur._idx,_g);
            for(tie(e_ii,e_end)=out_edges(v,_g);e_ii!=e_end;e_ii++)
            {
                v_adj=target(*e_ii,_g);
                v_adj_idx=get(vertex_idx_map,v_adj);
                deg[v_adj_idx]-=1;
                act[v_adj_idx]-=get(edge_act_map,*e_ii);
                if (!processed[v_adj_idx])
                { 
                    neighbors[v_adj_idx].push_back(location); // set the nearby node   
                    neighborsAct[v_adj_idx].push_back(get(edge_act_map,*e_ii));
                    priQue.push(_node[v_adj_idx]);
                }
            }            
            while (!priQue.empty()){
                Node w=priQue.top();
               
                que.push(w);
                priQue.pop();
            }
        }        
        // detect if all node are processed
        bool all_proc=true;
        for (int i=0;i<processed.size();i++){
            all_proc&=processed[i];
        }       
        done=all_proc;
    }while(!done);
    // copy placement to grid (information flow)
    _grid=_placement;    
}

// the function does trivial placement and routing (costB)
int InterActGraph::insertSwap1(string outname){
   
    istringstream infile(_cktbuffer);
    ofstream outfile(outname.c_str(),ofstream::out);
    string line;
    int numSwap=0;
    bool PRINTBOUND=false;
    
    if (PRINTBOUND)
        outfile<<"# 2D circuit mapped."<<endl;

    while (getline(infile,line)){   
        string token;
        istringstream iss(line);
        iss>>token;
        if (token.compare(".qubit")==0){
            if (PRINTBOUND){
                outfile<<".qubit "<<_numQubit<<endl<<endl;
            
            // print qubit declaration
            for (int idx=0;idx<_numQubit;idx++)
                outfile<<"qubit "<<_idxToName[idx]<<endl;
            }
        }
        else if (token.compare("qubit")==0)
            continue;
        
        else if (isTwoQubitGate(token)){
            // insert SWAP if needed
            int target;
            int control;
            string gate=token;
            iss>>token;
            control=_nameToIdx[token];
            iss>>token;
            target=_nameToIdx[token];
            string rest;
            iss>>rest;
            // get node location
            pair<int,int> pos_control=_grid.idxToLoc(control);
            pair<int,int> pos_target=_grid.idxToLoc(target);
            if (dist(pos_control,pos_target)==1) // adjacent gates
                outfile<<line<<endl;
            else{ 
                vector<pair<int,int> > path;
                findPath(pos_control,pos_target,path);
                
                //generate SWAP forward
                for (int i=0;i<path.size()-1;i++){
                    if (PRINTBOUND)
                        outfile<<"SWAP "<< _idxToName[control]<<" "<<_idxToName[_grid.locToIdx(path[i+1])]<<endl;
                    numSwap++;
                }
                // apply adjacent 2-qubit gate
                if (PRINTBOUND)
                    outfile<<gate<<" "<<_idxToName[control]<<" "<<_idxToName[target]<<" "<<rest<<endl;
                //generate SWAP backward
                for (int i=path.size()-1;i>0;i--){
                    if (PRINTBOUND)
                        outfile<<"SWAP "<< _idxToName[control]<<" "<<_idxToName[_grid.locToIdx(path[i])]<<endl;
                    numSwap++;
                }
            }        
        }
        else{
            if (PRINTBOUND)
                outfile<<line<<endl;
        }     
    }
    
    outfile.close();
    return numSwap;
}


// optimized placement and routing

// dumpMode:
// 0: only do estimation, do not dump circuit
// 1: dump non-position-recover circuit (CostU)
// 2: dump position-recover circuit (CostR)

pair<int,int> InterActGraph::insertSwap2(string outname, int lookahead, int dumpMode){
    
    bool DEBUG=false;
    //preMode only does prediction
    istringstream infile(_cktbuffer);
    istringstream ahead(_cktbuffer);
    ofstream outfile(outname.c_str(),ofstream::out);
    string layoutfile=outname+".layout";
    // generate layout file
    if (dumpMode>0){
        ofstream layout(layoutfile.c_str(),ofstream::out);
        vector<vector<int> > placement=_placement.getAlloc();
        for (int j=0;j<_placement.getH();j++){
            for (int i=0;i<_placement.getW();i++){
                layout<<_idxToName[placement[j][i]]<<" ";
            }
            layout<<endl;
        }
        layout.close();
    }

    
    string line,aheadline;
    deque<pair<int,int> > futureGate;
    vector<locswap> swapStack;
    
    int beginLine=0;
    int numSwap=0;
    int beforeFinalSwap;
    
    //copy grid info (info flow)
    vector<vector<int> > allocation=_grid.getAlloc();
    //set qubit name grid mapping
    vector<vector<string> > qbname(_grid.getH(),vector<string>(_grid.getW()));
    for (int j=0;j<_grid.getH();j++){
        for (int i=0;i<_grid.getW();i++){
            qbname[j][i]=_idxToName[allocation[j][i]];
        }
    }

    // to compute the shortest distance
    map<int,locg> idxToLoc; // index to location
    for (int j=0;j<allocation.size();j++){
        for (int i=0;i<allocation[j].size();i++)
        {
            int idx=allocation[j][i];
            locg loc=pair<int,int>(i,j);
            idxToLoc.insert(pair<int,locg> (idx,loc));
        }
    }
    if (DEBUG)
        cout<<idxToLoc;
    
    while (getline(infile,line)){   
        beginLine++;
        string token;
        istringstream iss(line);
        iss>>token;
        if (token.compare(".qubit")==0){
 
            if (dumpMode){
                outfile<<".qubit "<<_numQubit<<endl<<endl;           
                // print qubit declaration
                for (int idx=0;idx<_numQubit;idx++)
                    outfile<<"qubit "<<_idxToName[idx]<<endl;
            }
        }
        else if (token.compare("qubit")==0)
            continue;
        
        else if (token.compare(".begin")==0){
            if (dumpMode) // print the begin line
                outfile<<line<<endl;
            // move ahead ptr to the start of ckt
            for (int i=0;i<beginLine;i++)
                getline(ahead,aheadline);
            // fill in future gate buffer
            fillFutureGateBuffer(ahead,_nameToIdx,futureGate,lookahead);

        }
        
        else if (isTwoQubitGate(token)){
            // insert SWAP if needed
            int target;
            int control;
            string gate=token;
            iss>>token;
            string ctlName=token;
            control=_nameToIdx[token];
            iss>>token;
            string tarName=token;
            target=_nameToIdx[token];
            if (DEBUG){
                cout<<"-------------------------------------"<<endl;
                cout<<"[control]: "<<control<<" [target]: "<<target<<endl;
            }
            string rest;
            iss>>rest;
            // get node location (info location)
            locg pos_control=idxToLoc[control];
            locg pos_target=idxToLoc[target];
           
            // real qubit name
        
            if (dist(pos_control,pos_target)==1){ // adjacent gates
                
                if (dumpMode){
                   
                    // print circuit
                    outfile<< gate<<" "<<qbname[pos_control.second][pos_control.first]<<" "<<
                            qbname[pos_target.second][pos_target.first]<<" "<<rest<<endl;
                }
                if (DEBUG){
                    cout<<"**adjacent gates: "<<control<<" "<<target<<endl;
                }
                    
                //fill a new two qubit gate to ahead buffer
                fillFutureGateBuffer(ahead,_nameToIdx,futureGate);           
            }
            else{ // not adjacent gate, insert SWAP chain   
                             
                if (DEBUG)
                    cout<<"Generate path:"<<endl;
                // generate different mid points
                vector<locg> mid;                    
                mid=findMidPoint(pos_control,pos_target,_grid.getShape());

                vector<vector<locswap> > stotal;
                vector<pair<locg,locg> > cTot; // all adjacent control and target locations
                double costMin=INT_MAX;
                double cost,minIdx=0;
                for (int i=0;i<mid.size();i++){
                    if (DEBUG)
                        cout<<"Mid= "<<mid[i]<<endl;
                    vector<locswap>spath; //shortest swap path
                    pair<locg,locg> ct;
                    cost= INT_MAX;
                    
                    // mid point cannot equal to target point
                    cost= shortestPath(pos_control, pos_target, mid[i], spath, ct ,allocation, futureGate, _grid.getShape());
                    stotal.push_back(spath);
                    cTot.push_back(ct);
                    if (DEBUG)
                        cout<<"~~~ This route "<<i<<" cost= "<<cost<<endl;                  

                    if (cost<costMin){
                        costMin=cost;
                        minIdx=i;
                    }
                }

                if (DEBUG)
                    cout<<"********Select mid route: "<<minIdx<<" cost="<<costMin<<endl;

                //The best solution
                vector<locswap> &spath=stotal[minIdx];

                // push the forward swap chain to stack and print out swap chains to outfile
                for (int i=0;i<spath.size();i++){
                    // idx1 and idx2 are index of current flow
                    int idx1=allocation[spath[i].first.second][spath[i].first.first];
                    int idx2=allocation[spath[i].second.second][spath[i].second.first];

                    if(dumpMode){                       
                        // print circuit
                        outfile<<"SWAP "<<qbname[spath[i].first.second][spath[i].first.first]<<" "<<
                                qbname[spath[i].second.second][spath[i].second.first]<<endl;
                    }
                    numSwap++;
                    swapQubit(spath[i].first,spath[i].second,allocation);
                    swapQubit(idx1,idx2,idxToLoc);
                }
                
                //push swap to stacks    
                // trace swap dependency 
                vector<vector<bool> > dep (_grid.getH(),vector<bool>(_grid.getW(),false));
           
                for(vector<locswap>::iterator kr=spath.begin();kr!=spath.end();kr++){
                    locg r1=kr->first;
                    locg r2=kr->second;
                    bool hasSameSwap=false;
                    for (vector<locswap>::reverse_iterator st=swapStack.rbegin();st!=swapStack.rend();st++){
                    // update swap dependency table
                        locg q1=st->first;
                        locg q2=st->second;
                        bool valid=(!dep[q1.second][q1.first]) && (!dep[q2.second][q2.first]); // don't violate dependency
                        dep[q1.second][q1.first]=true;
                        dep[q2.second][q2.first]=true;
                        if (valid){
                            if ((r1==q1 && r2==q2) || (r1==q2) && (r2==q1)){// same operation
                                //delete the swap gate in stack
                                swapStack.erase(--st.base());                           
                                hasSameSwap=true;
                                break;
                            } 
                        }
                    }
                    if (!hasSameSwap)
                        swapStack.push_back(*kr);
                }
                // print now-adjacent gate 
                if(dumpMode){
                   
                    outfile<< gate<<" "<<qbname[cTot[minIdx].first.second][cTot[minIdx].first.first]<<" "<<
                            qbname[cTot[minIdx].second.second][cTot[minIdx].second.first]<<" "<<rest<<endl; 
                }

                // print current map                    
                if (DEBUG){
                    cout<<allocation<<endl;
                    // cout<<idxToLoc<<endl;
                    cout<<"swapStack: "<<endl;
                    for (int i=0;i<swapStack.size();i++) 
                        cout<<swapStack[i]<<" ";
                    cout<<endl;
                }
                //fill a new two qubit gate to ahead buffer
                fillFutureGateBuffer(ahead,_nameToIdx,futureGate);             
            }            
        }
        
        else if (token.compare(".end")==0){
            
            string infolayout=outname+".layout";
            if (dumpMode==1){
                ofstream info(infolayout.c_str(),ofstream::out);
                //"*** This is the final layout of information flow!"
                 
                for (int j=0;j<_grid.getH();j++){
                    for (int i=0;i<_grid.getW();i++){
                        info<<_idxToName[allocation[j][i]]<<" ";
                    }
                    info<<endl;
                }
                info.close();
            }
            
            
            // pop out remaining swap gates
            beforeFinalSwap=numSwap;
            while(!swapStack.empty()){
                locswap sw=swapStack.back();
                swapStack.pop_back();
                int idx1=allocation[sw.first.second][sw.first.first];
                int idx2=allocation[sw.second.second][sw.second.first];
                
                
                if(dumpMode==2){
               
                    outfile<< "SWAP "<<qbname[sw.first.second][sw.first.first]<<" "<<
                            qbname[sw.second.second][sw.second.first]<<endl;
                }
                numSwap++;
                swapQubit(sw.first,sw.second,allocation);
                swapQubit(idx1,idx2,idxToLoc);
            }
           
            if(dumpMode)
                outfile<<".end"<<endl;
            if (DEBUG){
                cout<<"End of Ckt!"<<endl;
                cout<<allocation<<endl;
                cout<<idxToLoc<<endl;
            }
        }
        
        else{
            if(dumpMode)
                outfile<<line<<endl;
        }     
    }

    outfile.close();   
    return pair<int,int> (beforeFinalSwap,numSwap);     
}

void findPath(locg pos_control, locg pos_target, vector<locg> &path){
    path.push_back(pos_control);
    int xDiff=pos_target.first-pos_control.first;
    if (xDiff>0){ // move right
        // two qubit on the same row
        if (pos_control.second==pos_target.second){
            for (int x=1;x<xDiff;x++){
                path.push_back(pair<int,int> (pos_control.first+x, pos_control.second));
            }
        }
        else {
            for (int x=1;x<=xDiff;x++){
                path.push_back(pair<int,int> (pos_control.first+x, pos_control.second));
            }      
        }
    }
    else{ // move left
        if (pos_control.second==pos_target.second){ // in the same row
            for (int x=-1;x>xDiff;x--){
                path.push_back(pair<int,int> (pos_control.first+x,pos_control.second));
            } 
        }
        else {
            for (int x=-1;x>=xDiff;x--){
                path.push_back(pair<int,int> (pos_control.first+x,pos_control.second));
            }
        }
    }

    int yDiff=pos_target.second-pos_control.second;
    if (yDiff<0){ // move up
        for (int y=-1;y>yDiff;y--){
            path.push_back(pair<int,int> (pos_target.first, pos_control.second+y));
        }
    }
    else { // move down
        for (int y=1;y<yDiff;y++){
            path.push_back(pair<int,int> (pos_target.first,pos_control.second+y));
        }                  
    }
 
}

// find all possible routes
void trail(locg start, locg end, int quadrant, vector<locg> &visited, vector<locg> &oneRoute, vector<vector<locg> > &allRoute, bool isTall)
{
       
    if (start==end){
        oneRoute.push_back(start);
        allRoute.push_back(oneRoute);
        oneRoute.pop_back();
        return;
    }
    
    for (int i=0;i<visited.size();i++){
        if (visited[i]==start) //has been visited
            return;
    }
    
    switch(quadrant){ // exceed boundary
        case 1:
            if (start.first>end.first || start.second<end.second)
                return;
            break;
        case 2:
            if (start.first<end.first || start.second<end.second)
                return;
            break;
        case 3:
            if (start.first<end.first || start.second>end.second)
                return;
            break;
        case 4:
            if (start.first>end.first || start.second>end.second)
                return;
            break;
    }
    oneRoute.push_back(start);
    visited.push_back(start);
    
    locg right(start.first+1,start.second);
    locg left(start.first-1,start.second);
    locg up(start.first,start.second-1);
    locg down(start.first,start.second+1);
    
    switch(quadrant){          
        case 1:        
            if (isTall){
                trail(right,end,quadrant,visited,oneRoute,allRoute,isTall);     
                trail(up,end,quadrant,visited,oneRoute,allRoute,isTall);
            }
            else{
                trail(up,end,quadrant,visited,oneRoute,allRoute,isTall);
                trail(right,end,quadrant,visited,oneRoute,allRoute,isTall);   
            }
            break;
        case 2:
            if (isTall){
                trail(left,end,quadrant,visited,oneRoute,allRoute,isTall);
                trail(up,end,quadrant,visited,oneRoute,allRoute,isTall);
            }
            else{
                trail(up,end,quadrant,visited,oneRoute,allRoute,isTall);
                trail(left,end,quadrant,visited,oneRoute,allRoute,isTall);
            }
            break;
        case 3:
            if(isTall){
                trail(left,end,quadrant,visited,oneRoute,allRoute,isTall);
                trail(down,end,quadrant,visited,oneRoute,allRoute,isTall);
            }
            else {
               trail(down,end,quadrant,visited,oneRoute,allRoute,isTall); 
               trail(left,end,quadrant,visited,oneRoute,allRoute,isTall);
            }
            break;
        case 4:
            if(isTall){
                trail(right,end,quadrant,visited,oneRoute,allRoute,isTall);
                trail(down,end,quadrant,visited,oneRoute,allRoute,isTall);
            }
            else{
                trail(down,end,quadrant,visited,oneRoute,allRoute,isTall);
                trail(right,end,quadrant,visited,oneRoute,allRoute,isTall);
            }
            break;
    }
    oneRoute.pop_back();
    visited.pop_back();
}

//select the best path from control to target through mid
double shortestPath(locg control, locg target, locg mid, vector<locswap> &path, pair<locg, locg> & ct,
        vector<vector< int> > &allocation, deque<pair<int,int> > &future, bool isTall){
    
    int quadrantCM,quadrantTM;
    
    if (mid.first>=control.first && mid.second<control.second)
        quadrantCM=1;
    else if (mid.first<control.first && mid.second<control.second)
        quadrantCM=2;
    else if (mid.first<control.first && mid.second>=control.second)
        quadrantCM=3;
    else if (mid.first>=control.first && mid.second>=control.second)
        quadrantCM=4;
    
    if (mid.first>=target.first && mid.second<target.second)
        quadrantTM=1;
    else if (mid.first<target.first && mid.second<target.second)
        quadrantTM=2;
    else if (mid.first<target.first && mid.second>=target.second)
        quadrantTM=3;
    else if (mid.first>=target.first && mid.second>=target.second)
        quadrantTM=4;
    
    vector<locg> visited;
    vector<locg> route;
    vector<vector<locg> >allCtlMid;
    vector<vector<locg> >allTarMid;
    // =============================
    // process control to mid route
    // =============================
    trail(control,mid,quadrantCM,visited,route,allCtlMid,isTall);
    int bestRouteCM=0;
    int minCostCM=INT_MAX;
    
    map<int,locg> nodeToLoc; // for compute the shortest distance
    for (int j=0;j<allocation.size();j++){
        for (int i=0;i<allocation[j].size();i++)
        {
            int idx=allocation[j][i];
            locg loc=pair<int,int>(i,j);
            nodeToLoc.insert(pair<int,locg> (idx,loc));
        }
    }
    
    for (int r=0;r<allCtlMid.size();r++){ // select route        
        vector<vector<int> > tmpAlloc=allocation;
        map <int,locg> tmpMap=nodeToLoc;
        //generate new map
        for (int i=0;i<allCtlMid[r].size()-1;i++){ 
            int bit1=tmpAlloc[allCtlMid[r][i].second][allCtlMid[r][i].first];
            int bit2=tmpAlloc[allCtlMid[r][i+1].second][allCtlMid[r][i+1].first];
            swapQubit(allCtlMid[r][i],allCtlMid[r][i+1],tmpAlloc);
            swapQubit(bit1,bit2,tmpMap);
        }

        int costCM=0;
        for (int i=0;i<future.size();i++){
            costCM+=(dist(tmpMap[future[i].first],tmpMap[future[i].second]));
        }
        
        // select the best route
        if (costCM<minCostCM){
            bestRouteCM=r;
            minCostCM=costCM;
        }
                   
    }
    
    // process 
    visited.clear();
    route.clear();
    
    
    // =============================
    // process target to mid route
    // =============================
    
 //   cout<<"Do target to mid point"<<endl;
    trail(target,mid,quadrantTM,visited,route,allTarMid,isTall);
    int bestRouteTM=0;
    int minCostTM=INT_MAX;
    
    for (int r=0;r<allTarMid.size();r++){ // select route        
        vector<vector<int> > tmpAlloc=allocation;
        map <int,locg> tmpMap=nodeToLoc;
        int s=allTarMid[r].size();
        //generate new map
        for (int i=0;i<(s-2);i++){ 
            int bit1=tmpAlloc[allTarMid[r][i].second][allTarMid[r][i].first];
            int bit2=tmpAlloc[allTarMid[r][i+1].second][allTarMid[r][i+1].first];
            swapQubit(allTarMid[r][i],allTarMid[r][i+1],tmpAlloc);
            swapQubit(bit1,bit2,tmpMap);
        }
 
        int costTM=0;
        for (int i=0;i<future.size();i++){
            costTM+=(dist(tmpMap[future[i].first],tmpMap[future[i].second]));
        }
        
        // select the best route
        if (costTM<minCostTM){
            bestRouteTM=r;
            minCostTM=costTM;
        }                  
    }
    
    // push the best route to path
    path.clear();
    // interleave insert swap
    int k=0, l=0;  
    int s=allTarMid[bestRouteTM].size();
    while (k<allCtlMid[bestRouteCM].size()-1 || l<(s-2)){
        if (k<allCtlMid[bestRouteCM].size()-1)
            path.push_back(locswap(allCtlMid[bestRouteCM][k],allCtlMid[bestRouteCM][k+1]));
        int s=allTarMid[bestRouteTM].size();
        if (l<(s-2))
            path.push_back(locswap(allTarMid[bestRouteTM][l],allTarMid[bestRouteTM][l+1]));
        k++;
        l++;
    }
    // Derive the final routed position
    // q0 q1 q2
    // q3 q4 q5 
    // CNOT q0 q5
    // route q0->q1->q4->q5
    //       ctl     via tar
    // SWAP q0 q1
    // SWAP q1 q4
    // CNOT q4 q5
    // ct.first=locg(q4)
    // ct.second=locg(q5)
    
    int len1=allCtlMid[bestRouteCM].size()-1;
    int len2=allTarMid[bestRouteTM].size()-2;
    len1>0?ct.first=allCtlMid[bestRouteCM][len1]:ct.first=control;
    len2>0?ct.second=allTarMid[bestRouteTM][len2]:ct.second=target;
    // when the mid point is target, special case, target is swapped by control chain
    if (ct.first==ct.second){
        if (mid!=target){
            cout<<"error!"<<endl;
            exit(1);
        }
        ct.second=allCtlMid[bestRouteCM][len1-1];
    }

    //compute final cost
   
    vector<vector<int> > tmpAlloc=allocation;
    map <int,locg> tmpMap=nodeToLoc;
    for (int i=0;i<allCtlMid[bestRouteCM].size()-1;i++){ 
        int bit1=tmpAlloc[allCtlMid[bestRouteCM][i].second][allCtlMid[bestRouteCM][i].first];
        int bit2=tmpAlloc[allCtlMid[bestRouteCM][i+1].second][allCtlMid[bestRouteCM][i+1].first];
        swapQubit(allCtlMid[bestRouteCM][i],allCtlMid[bestRouteCM][i+1],tmpAlloc);
        swapQubit(bit1,bit2,tmpMap);
    }
    for (int i=0;i<(int) allTarMid[bestRouteTM].size()-2;i++){ 
        int bit1=tmpAlloc[allTarMid[bestRouteTM][i].second][allTarMid[bestRouteTM][i].first];
        int bit2=tmpAlloc[allTarMid[bestRouteTM][i+1].second][allTarMid[bestRouteTM][i+1].first];
        swapQubit(allTarMid[bestRouteTM][i],allTarMid[bestRouteTM][i+1],tmpAlloc);
        swapQubit(bit1,bit2,tmpMap);
    }
    
    double costFinal=0;
    for (int i=0;i<future.size();i++){
            costFinal+=(dist(tmpMap[future[i].first],tmpMap[future[i].second]));
    }

    return costFinal;   
}

void swapQubit(locg a, locg b, vector<vector<int> > &locMap){
    int tmp=locMap[a.second][a.first];
    locMap[a.second][a.first]=locMap[b.second][b.first];
    locMap[b.second][b.first]=tmp;
}

void swapQubit(int a, int b, map<int,locg> &locMap){
    locg tmp=locMap[a];
    locMap[a]=locMap[b];
    locMap[b]=tmp;
}

bool isTwoQubitGate(string token){
    if (token.compare("CNOT")==0 || token.compare("CZ")==0 ||
            token.compare("CP")==0 || token.compare("SWAP")==0 ||
            token.compare("GEO")==0 || token.compare("ZENO")==0)
        return true;
    else
        return false;
}


vector<locg> findMidPoint(locg & pos_control, locg & pos_target, bool isTall){
    
    // find all possible meeting points
    vector<locg> out;
    vector<int>  mid; 
    int ctl_x=pos_control.first;
    int ctl_y=pos_control.second;
    int tar_x=pos_target.first;
    int tar_y=pos_target.second;
  
    // start from half distance
    // if distance is 10: 5->4->6->3->7...
    int fullDist=dist(pos_control,pos_target)+1;
    int halfDist=(fullDist)/2;
    int step=0;
    int d=halfDist;
    for (int i=0;i<=fullDist;i++){
        step=i*pow(-1,i);
        d+=step;
        if (d<=fullDist && d>=0)
            mid.push_back(d);   
    }
  
    int quadrant, stepX, stepY;
    
    //*** mid point cannot equal to tar
    if (isTall){ 
        for (int i=0;i<mid.size();i++){
            int halfDist=mid[i];
            if (ctl_x<tar_x && ctl_y>=tar_y){
                quadrant=1;
                stepX=1;
                stepY=1;

                int x=ctl_x;
                int y=ctl_y-halfDist;
                while (y<=ctl_y){         
                    if (y>=tar_y && x<=tar_x)
                        out.push_back(locg(x,y));
                    x+=stepX;
                    y+=stepY;
                }    
            }
            else if (ctl_x>=tar_x && ctl_y>=tar_y){
                quadrant=2;
                stepX=-1;
                stepY=1;

                int x=ctl_x;
                int y=ctl_y-halfDist;
                while (y<=ctl_y){
                    if (y>=tar_y && x>=tar_x )
                        out.push_back(locg(x,y));
                    x+=stepX;
                    y+=stepY;
                }    
            }
            else if (ctl_x>=tar_x && ctl_y<tar_y){
                quadrant=3;
                stepX=-1;
                stepY=-1;

                int x=ctl_x;
                int y=ctl_y+halfDist;
                while (y>=ctl_y){
                    if (y<=tar_y && x>=tar_x )
                        out.push_back(locg(x,y));
                    x+=stepX;
                    y+=stepY;
                }


            }
            else{ 
                quadrant=4;
                stepX=1;
                stepY=-1;

                int x=ctl_x;
                int y=ctl_y+halfDist;
                while (y>=ctl_y){
                    if (y<=tar_y && x<=tar_x )
                        out.push_back(locg(x,y));
                    x+=stepX;
                    y+=stepY;
                }

            }
        }
    }
    else{
        
        for (int i=0;i<mid.size();i++){
            int halfDist=mid[i];
            if (ctl_x<tar_x && ctl_y>=tar_y){
                quadrant=1;
                stepX=-1;
                stepY=-1;

                int x=ctl_x+halfDist;
                int y=ctl_y;
                while (x>=ctl_x){
                    if (y>=tar_y && x<=tar_x  )
                        out.push_back(locg(x,y));
                    x+=stepX;
                    y+=stepY;
                }    
            }
            else if (ctl_x>=tar_x && ctl_y>=tar_y){
                quadrant=2;
                stepX=1;
                stepY=-1;

                int x=ctl_x-halfDist;
                int y=ctl_y;
                while (x<=ctl_x){
                    if (y>=tar_y && x>=tar_x )
                        out.push_back(locg(x,y));
                    x+=stepX;
                    y+=stepY;
                }    
            }
            else if (ctl_x>=tar_x && ctl_y<tar_y){
                quadrant=3;
                stepX=1;
                stepY=1;

                int x=ctl_x-halfDist;
                int y=ctl_y;
                while (x<=ctl_x){
                    if (y<=tar_y && x>=tar_x  )
                        out.push_back(locg(x,y));
                    x+=stepX;
                    y+=stepY;
                }


            }
            else{ 
                quadrant=4;
                stepX=-1;
                stepY=1;

                int x=ctl_x+halfDist;
                int y=ctl_y;
                while (x>=ctl_x){
                    if (y<=tar_y && x<=tar_x )
                        out.push_back(locg(x,y));
                    x+=stepX;
                    y+=stepY;
                }

            }
        }      
    }
    return out; 
}


void fillFutureGateBuffer(istream &ahead, map<string,int> &nameToIdx, deque<pair<int,int> > &futureGate, int updateline){
    string aline,atoken;
    
    int popline=0;
    while (!futureGate.empty() && popline<updateline){
        futureGate.pop_front();
        popline++;
    }
        
    popline=0;    
    while(popline<updateline && !ahead.eof()){
        if (getline(ahead,aline)){
            istringstream aiss(aline);
            aiss>>atoken;
            if (isTwoQubitGate(atoken)){
                int aCtl;
                int aTar;
                aiss>>atoken;
                aCtl=nameToIdx[atoken];
                aiss>>atoken;
                aTar=nameToIdx[atoken];
                futureGate.push_back(pair<int,int>(aCtl,aTar));
                popline++;
            }    
        }
        
    }
}