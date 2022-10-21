from get_circuit import *
from Matrix_gen import *
from Steriner_Gauss import *

if __name__ == '__main__':
    # 将placement算法得到的新回路
    # 计算距离
    # 生成矩阵
    address_placement = "test_new_out.txt (8).layout" # 新placement文件名
    get_new_cir_16bit(address_placement, "test_new.txt")
    # 计算距离
    print("placement得到新回路的距离", get_dis_16bit("Mnew_cir.txt"))
    # 生成placement新回路的矩阵
    print("获取placement回路矩阵------------------------------------------------------------------------")
    qnum = 16        #量子ビット数
    cnot_count = 8 #CNOTゲート数
    address = "Mnew_cir.txt"
    # 输出记录方便
    for item in Matrix_trans(gen_circuit_ex(qnum, address)):
        print(item)
    matrix_initial = Matrix_trans(gen_circuit_ex(qnum, address))

    print("steiner gauss====------------------------------------------------------------------------")
    n = 16
    count = 8
    data = np.array(matrix_initial)
    print(data)
    targets = []
    trans = []
# convert to upper triangular matrix
    seq = np.arange(n)
    for j in seq:     # scan columns
        targets.clear()
        for i in np.arange(n):    # scan rows
            if j == i:
                fr = i
                # if data[i][j] == 0:
                #     targets.append(i)
            if data[i][j] == 1 and i > j:    # only lower triangular is considered
                targets.append(i)
        bestRoute = runAll(n, fr, targets)
        # bestRoute = list(map(lambda x: list(map(lambda y: {y: data[y][j]}, x)), _bestRoute))
        print("今の実行する列：{}列目".format(j), bestRoute)

        if (data[j][j] == 1):    #if the start spot is 1
            L2 = guassLower(data, j, bestRoute)
        else:                    # if the start spot is 0
            L2 = handleZeroStart(data, j, bestRoute)
            _L2 = guassLower(data, j, bestRoute)
            L2.extend(_L2)
        count += len(L2)
        trans.append(L2)
        print("{}列目{}つ変換経路：".format(j, len(L2)), L2)
        print(data)
    print("上三角変換の計数:", count, trans)
    print("上三角行列:")
    print(data)
    print("##########################")


    seq = sorted(seq, reverse=True)
    # convert to E matrix
    for j in seq:     # scan columns
        targets.clear()
        for i in np.arange(n):    # scan rows
            if j == i:
                fr = i
                # if data[i][j] == 0:
                #     targets.append(i)
            if data[i][j] == 1 and i < j:    # only lower triangular is considered
                targets.append(i)
        bestRoute = runAll(n, fr, targets, 1)
        # bestRoute = list(map(lambda x: list(map(lambda y: {y: data[y][j]}, x)), _bestRoute))
        print("ターゲットへの経路：{}列目".format(j), bestRoute)
        if (data[j][j] == 1):  # if the start spot is 1
            L2 = guassUpper(data, j, bestRoute)
        else:  # if the start spot is 0
            L2 = handleZeroStart(data, j, bestRoute)
            _L2 = guassUpper(data, j, bestRoute)
            L2.extend(_L2)
        count += len(L2)
        trans.append(L2)
        print("{}列目{}つ変換経路：".format(j, len(L2)), L2)
        print(data)
    print("CNOTゲートの計数:", count, trans)
    print("単位行列:")
    print(data)