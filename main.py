from Random_circuit_gen import *
from get_circuit import *
from Matrix_gen import *
from SG import *
if __name__ == '__main__':
    # 这个程序是随机生成初始回路
    # 计算 初始回路的距离
    # 并steiner gauss
    # test_new.txt 中生成新的随机电路
    # 并输出生成了那几个门
    qnum = 9        #量子ビット数
    cnot_count = 25 #CNOTゲート数
    print("生成随机初始回路，计算距离------------------------------------------------------------------------")
    # 修改产生的门的数量
    address = "test_new.txt"

    Circuit_txt(9,25)
    print("原电路距离和:", get_dis("test_new.txt"))
    for item in Matrix_trans(gen_circuit_ex(qnum, address)):
        print(str(item) + ",")
    matrix_initial = Matrix_trans(gen_circuit_ex(qnum, address))
    print("..................initial matrix........................")
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








