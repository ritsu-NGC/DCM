import pythonds
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from Graph import *


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


if __name__ == '__main__':
    # g = Graph()
    # g.addEdge(0,3)
    # g.addEdge(1,5)
    # g.addEdge(0,3)
    # g.addEdge(5,1)
    # g.addEdge(1,5)
    # g.showGraph()
    qft = QuantumCircuit(5)
    qft.cx(0,3)
    qft.cx(1,4)
    qft.cx(0,3)
    qft.cx(4,3)
    qft.cx(0,3)

    get_circuit(qft).showGraph()




