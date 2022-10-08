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

PAQCS

[Introduction]

PAQCS does placement and routing for swap based quantum architecture. 
The input of PAQCS is a quantum logic circuit and output a quantum physical 
circuit where the operands of two-qubit gates are adjacent.

[Directory]

./inc: header files
./src: source files
./nbproject: files for building the project
./doc: papers related to PAQCS
./Log: example files

[Installation]
The installation of FTQLS requires Boost library, which can be downloaded 
from http://www.boost.org/

[Build]

make               --> build "Debug" mode
make CONF=Release  --> build "Release" mode

[Execution]
Commend:

./paqcs <input_file> <output_file> <grid_W> <grid_H> <window_size>

PAQCS will generate a layout file named "output file.layout".

For example, to synthesize QFT6.txt to a 2x3 grid, with optimization window of 3, enter:
./paqcs QFT6.txt QFT6_2D.txt 2 3 3

Two files will be generated: 
1) "QFT6_2D.txt", which is the output circuit.
2) "QFT6_2D.txt.layout", which is the layout of qubits.



 

