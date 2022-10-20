import random


def Circuit_txt(qubit_num,gate_num):
    w = open("test_new.txt","w")
    num = ".qubit " + str(qubit_num)+ "\n"
    w.write(num)
    # w.write("\r\n")
    for i in range(qubit_num):
        qubit = "qubit q" + str(i) + "\n"
        # print(qubit)
        w.write(qubit)

    w.write(".begin\n")
    # w.write("\r\n")
    gate_list =  Random_gates(qubit_num,gate_num)
    for gate in gate_list:
        strs = "CNOT q"+str(gate[0]) + " q"+str(gate[1])+ "\n"
        print(strs)
        w.write(strs)
    w.write(".end\n")

def Random_gates(qubit_num,gate_num):
    gate_list = []
    while len(gate_list) < gate_num:
        gate = random.sample(range(0, qubit_num), 2)
        not_in = True
        for item in gate_list:
            if gate == item:
                not_in = False
        if not_in:
            gate_list.append(gate)

    return gate_list




if __name__ == '__main__':
    # print(Random_gates(9,3))
    Circuit_txt(9,3)