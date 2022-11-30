# DCM
This program aims to find optmial layouts of logic circuits to reduce the number of CNOT gates in converted physical circuits, and the flowcharts is in this folder.
The program is basing on Simulated Annealing. And initial solution is got from PAQCS. 
PAQCS uses the source code for the paper, "PAQCS: Physical Design-aware Fault-tolerant Quantum Circuit Synthesis," IEEE Transactions on VLSI Systems, which is a backup from the source. You may want to refer to the original Readme file.
The main function is to obtain optimal layouts with smaller distances. 
In the end, select smallest 10 layouts from the accepted list and perform Steiner-Gauss elimination on these layouts to select the layouts with minimum CNOT gates in converted circuits.  

