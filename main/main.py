from main.Random_circuit_gen import *
from Matrix_gen import *
from SG import *
if __name__ == '__main__':
    # this is program to calculate the distance and the number of cnot gate of initial circuit


    qnum = 9        #量子ビット数
    cnot_count = 25 #CNOTゲート数
    print("生成随机初始回路，计算距离------------------------------------------------------------------------")
    # txt keep the information of circuits qubits and gates

    address = "test_new.txt"
    # randomly generate circuits

    Circuit_txt(9,25)
    # distance calculation

    print("原电路距离和:", get_dis("test_new.txt"))
    for item in Matrix_trans(gen_circuit_ex(qnum, address)):
        print(str(item) + ",")
    matrix_initial = Matrix_trans(gen_circuit_ex(qnum, address))
    print("..................initial matrix........................")
    # perform steiner gauss elimantion

    result = St_down(matrix_initial)
    print("res",result)
    if len(result[1]) > 0:
        count = result[1].pop()
    else:
        count = 0
    upper_matrix = result[0]
    result = St_up(upper_matrix)
    if len(result[1]) > 0:
        count = count + result[1].pop()
    print("cnot gates:",count)








