import pythonds
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from pythonds.graphs import Graph,Vertex,PriorityQueue
class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
    def addNeigbor(self,nbr,weight):
        self.connectedTo[nbr] = weight
    def __str__(self):
        return str(self.id) + " is connectedTo:" + str([x.id for x in self.connectedTo])
    def getConnections(self):
        return self.connectedTo.keys()
    def getId(self):
        return self.id
    def getWeight(self,nbr):
        return self.connectedTo[nbr]

# 为了得到后续算法需要的图 需要重写图的方法
class Graph():
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVex = Vertex(key)
        self.vertList[key] = newVex
        return newVex
    def getVextices(self,i):
        if i in self.vertList:
            return self.vertList[i]
        else:
            return None
    def __contains__(self, item):
        return item in self.vertList
    def addEdge(self,f,t,cost = 0):
        if f not in self.vertList:
            self.addVertex(f)
        if t not in self.vertList:
            self.addVertex(t)
        self.vertList[f].addNeigbor(self.vertList[t],cost)
    def showGraph(self):
        print(self.vertList)
        for vertex in self.vertList:
            print(self.getVextices(vertex))

        # print(type(self.getVextices(0)))
        # for ver_neig in self.getVextices(0).getConnections():
        #     print(ver_neig.id)
        # print(self.getVextices(0).getConnections())

        # for vertex in self.getVextices():
        #     print(type(vertex))
            # print(vertex.getConnections())

    def getVetices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())







def get_circuit(circuit):
    num_qubit = len(circuit.qubits)
    print("qubit数：",num_qubit)
    gates_ctl = []
    gates_tar = []
    gate_graph = Graph()
    for gate in circuit.data:
        if gate.operation.name == "cx":
            gate_graph.addEdge(gate.qubits[0].index,gate.qubits[1].index)

            gates_ctl.append(gate.qubits[0].index)
            gates_tar.append(gate.qubits[1].index)
    # print(gates_ctl)
    # print(gates_tar)
    return gate_graph





qc = QuantumCircuit(3,2)
qc.cx(0,1)
qc.cx(1,2)
qc.cx(0,2)
print([i for i in get_circuit(qc).vertices])


# help(pythonds.Graph.addEdge)
# get_circuit(qc)
# print(qc)
# print(qc.qubits)
# for qubit in qc.qubits:
#     print(qubit.index)
# print(len(qc.qubits))
# for gate in qc.data:
#     print(gate.operation.name)
#     print(gate.qubits[0].index,gate.qubits[1].index)
#     print(gate.qubits[0].register.size)
#     print(gate.qubits[0].register._bits)




