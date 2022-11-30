from SA import *
from get_circuit import *
from Matrix_gen import *

from SG import *
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
    # this is calculate the distance and number of CNOT gates of the most optimal layouts by Simulated Annealing
    n = "10"
    ig = "30"

    # address of output
    ads = "C:\\Users\\apple\\OneDrive\\デスクトップ\\example"+ig+"gates\\"+n+"\\all.txt"
    w = open(ads, "a" ,encoding="UTF-8")

    # get initial layouts getting by PAQCS
    address_initial = "C:\\Users\\apple\\OneDrive\\デスクトップ\\example"+ig+"gates\\placement\\"+n+".layout"
    ads_init = "C:\\Users\\apple\\OneDrive\\デスクトップ\\example"+ig+"gates\\initial\\"+n+".txt"
    initial_place = get_initial(address_initial)
    initial_dis = get_dis("Mnew_cir.txt")
    w.write("原排列: " + str(initial_place) + "\n")
    print("SA初始距离", initial_dis)
    # w.write("原距离和: " + str(initial_dis) + "\n")
    # 开始S

    # index  perform times of SA
    for index in range(0,1):
        count = 0
        print("index:",index)
        w.write("index: " + str(index) + "\n")

        # perform SA
        sa = SA(initial_place, initial_dis,ads = ads_init )
        # get all accepted layouts
        sarun = sa.run()
        print("all",sarun)

        # find the layouts with minimun distance
        SA_dis_pla = GetMin(sarun)
        print("SA后最优解")
        print(SA_dis_pla)

        # print optimal layout and distance
        w.write("新距离和和新排列: " + str(SA_dis_pla) + "\n")
        SA_pla = SA_dis_pla[1]

        # generate new circuit of the optimal layouts
        get_new_cir_list(SA_pla,ads_init)
        print("SA得到新回路的距离：", get_dis("Mnew_cir.txt"))
        print("获取SA回路矩阵------------------------------------------------------------------------")


        qnum = 9        #量子ビット数
        # address of new circuit
        address = "Mnew_cir.txt"

        #  get matrix of circuit and print
        for item in Matrix_trans(gen_circuit_ex(qnum, address)):
            print(str(item)+",")
            w.write(str(item) +"," + "\n")
        matrix_initial = Matrix_trans(gen_circuit_ex(qnum, address))

        # perform steiner gauss elimination and calculate the number of cnot gates
        print("steiner gauss====------------------------------------------------------------------------")
        result = St_down(matrix_initial)
        print("res", result)
        if len(result[1]) > 0:
            count = result[1].pop()
        else:
            count = 0
        upper_matrix = result[0]
        result = St_up(upper_matrix)
        if len(result[1]) > 0:
            count = count + result[1].pop()
        print("cnot gates:", count)
        w.write("cnot gates:" + str(count) + "\n")
