
import numpy as np


def cnotgate(qc, con, tar):
    return qc.cx(con, tar)


def cnotmat(matrix, con, tar):

    matrix[tar,con] = 1
    return matrix

def gen_circuit_ex(qubit, address):
    cnot_mat = []
    gen_mat = np.diag([1]*qubit)
    read_gates = open(address,"r")
    for line in  read_gates.readlines():
        list = line.split()
        if list[0] == "CNOT":
            con = int(list[1][1])
            tar = int(list[2][1])
            gen_mat = cnotmat(gen_mat,con,tar)



    return gen_mat

if __name__ == '__main__':
    qnum = 9        #量子ビット数
    cnot_count = 3 #CNOTゲート数
    address = "test_new.txt"
    address2 = "Mnew_cir.txt"
    print(gen_circuit_ex(qnum,address))
    print("=================================")
    print(gen_circuit_ex(qnum,address2))


