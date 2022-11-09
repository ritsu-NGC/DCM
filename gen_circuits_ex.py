import random
import numpy as np


def random_circuit(Nbits:int,Ngates:int):
    qc=[]
    qx=[]
    gates_SET=('H','CX')
    gates_weight=(0,10)
    for num_gates in range(0,Ngates):
        t = random.randint(0, sum(gates_weight) - 1)
        for i, val in enumerate(gates_weight):
            t -= val
            if t < 0:
                if(gates_SET[i]=='CX'):
                    qc.append(random.sample(range(Nbits),2))
                else:
                    qc.append('H')

    return qc

def circuit_to_state(qc:list,Nbits:int):
    state=np.identity(Nbits)
    state=np.asmatrix(state)
    state=state.astype(np.int8)
    for i in range(0,len(qc)):
        dxor(state,int(qc[i][0]),int(qc[i][1]))
    return state