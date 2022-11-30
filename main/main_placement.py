from get_circuit import *
from Matrix_gen import *
from main_SA import *
from SG import *

if __name__ == '__main__':
    # this is calculate the distance and number of CNOT gates of new layouts by PAQCS

    n = "10"
    ig = "30"
    # address of output
    ads = "C:\\Users\\apple\\OneDrive\\デスクトップ\\example"+ig+"gates\\"+n+"\\all.txt"
    w = open(ads,"a",encoding="UTF-8")

    # address of initial circuits
    ads_init = "C:\\Users\\apple\\OneDrive\\デスクトップ\\example"+ig+"gates\\initial\\"+n+".txt"

    # address of new layouts
    ads_place = "C:\\Users\\apple\\OneDrive\\デスクトップ\\example"+ig+"gates\\placement\\"+n+".layout"

    # distance calculate
    # get new circuits of new layouts
    get_new_cir(ads_place, ads_init)

    initial_place = get_initial(ads_place)
    w.write("排列: " + str(initial_place) + "\n")

    # distance calculation
    distance = get_dis("Mnew_cir.txt")
    print("placement得到新回路的距离", distance)
    w.write("distance: " + str(distance)+"\n")

    print("获取placement回路矩阵------------------------------------------------------------------------")
    qnum = 9        #量子ビット数
    cnot_count = 25 #CNOTゲート数

    # address of new circuit
    address = "Mnew_cir.txt"

    # get matrix basing circuits
    for item in Matrix_trans(gen_circuit_ex(qnum, address)):
        print(str(item)+",")
        w.write(str(item)+","+"\n")
    matrix_initial = Matrix_trans(gen_circuit_ex(qnum, address))
    print("..................initial matrix........................")


    # perform steiner gauss elimination
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

    w.write("num of cnot gates:" + str(count)+"\n")