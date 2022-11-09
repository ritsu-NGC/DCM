import pythonds
from qiskit import *
from Graph import *
from distance_cal import *

def get_circuit(circuit):
    num_qubit = len(circuit.qubits)
    gates_ctl = []
    gates_tar = []
    gate_graph = Graph()
    for qubit in range(num_qubit):
        gate_graph.addVertex(qubit)
    for gate in circuit.data:
        if gate.operation.name == "cx":
            gate_graph.addEdge(gate.qubits[0].index,gate.qubits[1].index)

            gates_ctl.append(gate.qubits[0].index)
            gates_tar.append(gate.qubits[1].index)

    return gate_graph

def circuit_txt(name,circuit):
    # print(circuit.qubits)
    num_qubits = len(circuit.qubits)
    # print(num_qubits)
    str1 = name + ".txt"
    str2 = name + "_out.txt"
    with open(str1,"w") as w:
        w.write(".qubit {0}\n".format(num_qubits))
        for i in range(num_qubits):
            w.write("qubit q{0}\n".format(i))
        w.write(".begin\n")
        for gate in circuit.data:
            if gate.operation.name == "cx":
                w.write("CNOT q{0} q{1}\n".format(gate.qubits[0].index,gate.qubits[1].index))
        w.write(".end\n")
    open(str2,"w")

def get_new_cir(new_cir,old_cir):
    r1 = open(new_cir,"r")
    data = r1.read().split()
    print("错排列：", data)
    mid = data[3]
    data[3] = data[5]
    data[5] = mid
    print("新排列：",data)
    r2 = open(old_cir, "r")
    w = open("Mnew_cir.txt","w")
    for line in r2.readlines():
        gate = line.split()
        if gate[0] == "CNOT":
            # print(gate)
            gate[1] = "q" + str(data.index(gate[1]))
            gate[2] = "q" + str(data.index(gate[2]))
            # print(data.index(gate[1]),data.index(gate[2]))
            # print("改：",gate)
            str_gate = gate[0] + " " + gate[1] + " " +  gate[2] + "\n"
            w.write(str_gate)

def get_new_cir_16bit(new_cir,old_cir):
    r1 = open(new_cir,"r")
    data = r1.read().split()
    print("错排列：", data)
    mid = data[4]
    data[4] = data[7]
    data[7] = mid
    mid = data[15]
    data[15] = data[12]
    data[12] = mid
    mid = data[13]
    data[13] = data[14]
    data[14] = mid
    mid = data[6]
    data[6] = data[5]
    data[5] = mid

    print("新排列：",data)
    r2 = open(old_cir, "r")
    w = open("Mnew_cir.txt","w")
    for line in r2.readlines():
        gate = line.split()
        if gate[0] == "CNOT":
            # print(gate)
            gate[1] = "q" + str(data.index(gate[1]))
            gate[2] = "q" + str(data.index(gate[2]))
            # print(data.index(gate[1]),data.index(gate[2]))
            # print("改：",gate)
            str_gate = gate[0] + " " + gate[1] + " " +  gate[2] + "\n"
            w.write(str_gate)


if __name__ == '__main__':
    # g = Graph()
    # g.addEdge(0,3)
    # g.addEdge(1,5)
    # g.addEdge(0,3)
    # g.addEdge(5,1)
    # g.addEdge(1,5)
    # g.showGraph()
    qft = QuantumCircuit(9)

    # circ = QuantumCircuit(3)
    # circ.cx(0, 1)
    # circ.cx(0, 2)
    # print(circ.draw())

    # qft.cx(0,1)
    # qft.cx(0,3)
    # qft.cx(0,5)
    # qft.cx(0,7)
    # qft.cx(1,3)
    # qft.cx(2,5)
    # qft.cx(2,6)
    # qft.cx(2,7)
    # qft.cx(4,6)
    # qft.cx(4,7)
    # qft.cx(8,0)
    # qft.cx(8,1)
    # qft.cx(6,3)
    # qft.cx(6,5)
    # qft.cx(5,1)
    # qft.cx(5,3)
    # qft.cx(4,1)
    # qft.cx(2,1)
    # print(qft.data)
    # circuit_txt("test_new",qft)
    # get_new_cir_16bit("test_new_out.txt (18).layout","test_new.txt")
    # print("距离:",get_dis("test_new.txt"))
    # print("现距离",get_dis("Mnew_cir.txt"))
    r = open("Mnew_cir.txt","r")
    # print(r.read())
    gate_list = r.readlines()
    for item in gate_list:
        # print(item)
        # print(type(item))
        gate =item.split()
        con = int(gate[1].strip("q"))
        tar = int(gate[2].strip("q"))
        # print(con,tar)
        qft.cx(con,tar)
    print(qft.draw())









