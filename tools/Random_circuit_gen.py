import copy
import random
    # randomly generate circuits and get a txt of circuits

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
        print(gate)
        # print("random",gate)
        mid = [gate[1],gate[0]]
        if gate not in gate_list and mid not in gate_list:
            gate_list.append(gate)
        # print(gate_list)
        # for gate in gate_list:
        #     mid = copy.deepcopy(gate)
        #     gate_t = [mid[1],mid[0]]
        #     if gate_t in gate_list:
        #         print("... can not compute...")
                # raise Exception("... can not compute...")

    return gate_list




if __name__ == '__main__':
    # print(Random_gates(9,3))
    list = Circuit_txt(9,20)
    print(list)