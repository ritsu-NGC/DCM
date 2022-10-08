#include "../inc/InsertSwap.h"


//void InsertSwap(InterActGraph &g, string outname){
//    ifstream infile(g.getFileName().c_str(),ifstream::in);
//    ofstream outfile(outname.c_str(),ofstream::out);
//    string line,token;
//    
//    while (getline(infile,line)){   
//        istringstream iss(line);
//        iss>>token;
//        if (token.compare("CNOT")==0 || token.compare("CZ")==0 ||
//            token.compare("CP")==0 || token.compare("SWAP")==0 ||
//            token.compare("GEO")==0 || token.compare("ZENO")==0){
//            // insert SWAP if needed
//            int target;
//            int control;
//            iss>>token;
//            target=
//            
//            
//        }
//        else{
//            outfile<<line<<endl;
//        }
//        
//    }
//}