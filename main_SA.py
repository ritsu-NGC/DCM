from SA import *
from get_circuit import *
from Matrix_gen import *
from Steriner_Gauss import *
def get_initial(address_initial):
    r1 = open(address_initial,"r")
    data = r1.read().split()
    mid = data[3]
    data[3] = data[5]
    data[5] = mid
    print("SA初始排列：",data)
    return data
def placement_out(address,placement,nbit):
    w = open(address,"w")
    for item in placement:
        output = item + " "
        print(output)
        index = placement.index(item)
        row = index // nbit + 1
        print(row)
        # if row % 2 == 0:
        # else:
        #     w.write(output)

def get_new_cir_list(list,old_cir):
    data = list
    print("SA后新排列:",data)
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
    # 获取SA的初始解
    address_initial = "test_new_out.txt (16).layout"
    initial_place = get_initial(address_initial)
    initial_dis = get_dis("Mnew_cir.txt")
    print("SA初始距离", get_dis("Mnew_cir.txt"))
    # 开始S
    sa = SA(initial_place,initial_dis)
    # 输出距离和新排列
    SA_dis_pla = GetMin(sa.run())
    print("SA后最优解")
    print(SA_dis_pla)
    SA_pla = SA_dis_pla[1]
    get_new_cir_list(SA_pla,"test_new.txt")
    print("SA得到新回路的距离：", get_dis("Mnew_cir.txt"))
    print("获取SA回路矩阵------------------------------------------------------------------------")
    qnum = 9        #量子ビット数
    cnot_count = 3 #CNOTゲート数
    address = "Mnew_cir.txt"
    # 输出记录方便
    for item in Matrix_trans(gen_circuit_ex(qnum, address)):
        print(item)
    matrix_initial = Matrix_trans(gen_circuit_ex(qnum, address))

    print("steiner gauss====------------------------------------------------------------------------")
    n = 9
    count = 0
    data = np.array(matrix_initial)
    print(data)
    targets = []
    trans = []
    # convert to upper triangular matrix
    seq = np.arange(n)
    for j in seq:  # scan columns
        targets.clear()
        for i in np.arange(n):  # scan rows
            if j == i:
                fr = i
                # if data[i][j] == 0:
                #     targets.append(i)
            if data[i][j] == 1 and i > j:  # only lower triangular is considered
                targets.append(i)
        bestRoute = runAll(n, fr, targets)
        # bestRoute = list(map(lambda x: list(map(lambda y: {y: data[y][j]}, x)), _bestRoute))
        print("今の実行する列：{}列目".format(j), bestRoute)

        if (data[j][j] == 1):  # if the start spot is 1
            L2 = guassLower(data, j, bestRoute)
        else:  # if the start spot is 0
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
    for j in seq:  # scan columns
        targets.clear()
        for i in np.arange(n):  # scan rows
            if j == i:
                fr = i
                # if data[i][j] == 0:
                #     targets.append(i)
            if data[i][j] == 1 and i < j:  # only lower triangular is considered
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


