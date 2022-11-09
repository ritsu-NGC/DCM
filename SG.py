import numpy as np
import copy
from Steiner_tree import *
def xor(line1,line2):
    for i in range(len(line1)):
        if line1[i] == 1:
            if line2[i] == 0:
                line2[i] = 1
            elif line2[i] == 1:
                line2[i] = 0
    return line1,line2
def colum_cal(matrix,operations):
    # count = len(operations)
    for item in operations:
        print(item)
        l1 = item[0]
        l2 = item[1]
        xor(matrix[l1], matrix[l2])
        line1 = xor(matrix[l1], matrix[l2])[0]
        line2 = xor(matrix[l1], matrix[l2])[1]

        matrix[l1] = line1
        matrix[l2] = line2

    return matrix
# get target bit list
def getTar(con,matrix):
    tar = []
    war = matrix[con][con]
    for index in range(con + 1,len(matrix)):
        if matrix[index][con] == 1:
            tar.append(index)
    return war,tar

def collect_map(con,tar):
    final = []
    if len(tar) == 1:
        step1 = get_all_branches(con,tar)
        step2 = get_steiner(step1)
        step3 = step2[0][0]
        # print(step3)
        # print( "step4",Gauss_map(step3, tar))
        step4 = Gauss_map(step3, tar)
        # print("step5", Gauss_map2(step4, tar))
        final = Gauss_map2(step4, tar)
    else:
        count = 0
        step1 = get_all_branches(con,tar)
        step2 = get_steiner(step1)
        list = []
        step3 = turn_tree(step2)
        for i in step3:
            count += 1
            list.append(i)
        list2 = copy.deepcopy(list)
        step4 = []
        for i in range(len(list2)):
            list[i] = copy.deepcopy(list2[i])
            li = tree_sys(list[i])
            step4.append(li)

        step5 = select_min_tree(step4)
        step6 = Gauss_map(step5,tar)
        final = new_Gauss_map2(step6,tar)

    return final

def St_down(matrix):
    leng = len(matrix)
    count = 0
    # print(leng)
    for index in range(leng):
        con = index
        war = getTar(con,matrix)[0]
        if war == 0:
            raise Exception("... control bit is 0...")
        tar = getTar(con,matrix)[1]
        operation = collect_map(con,tar)
        print(operation)
        count = count + len(operation)
        print(count)
        matrix = colum_cal(matrix,operation)
        for line in matrix:
            print(line)
        print(count)
        print("....................{0}..........................".format(index))

def matrix_rever(matrix):
    for row in matrix:
        row.reverse()
    matrix.reverse()
    # for it in matrix:
        # print(it)
    return matrix

def St_up(matrix):
    matrix = matrix_rever(matrix)
    for it in matrix:
        print(it)
    leng = len(matrix)

    count = 0
    print(leng)
    for index in range(leng):
        con = index
        war = getTar(con, matrix)[0]
        if war == 0:
            raise Exception("... control bit is 0...")
        tar = getTar(con, matrix)[1]
        if tar == []:
            continue
        operation = collect_map(con, tar)
        print(operation)
        # operation_r = copy.deepcopy(operation)
        # for item in operation_r:
        #     item.reverse()
        # print(operation_r)
        count = count + len(operation)
        print(count)
        matrix = colum_cal(matrix, operation)
        matrix2 = copy.deepcopy(matrix)
        matrix2 = matrix_rever(matrix2)
        for line in matrix2:
            print(line)
        print(count)

        print("....................{0}..........................".format(index))




if __name__ == '__main__':
    # matrix = [
    #  [1, 0, 0, 0, 1, 0, 1, 0, 0],
    #  [0, 1, 0, 0, 1, 0, 0, 0, 0],
    #  [0, 0, 1, 0, 1, 0, 1, 0, 0],
    #  [1, 0, 1, 1, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 1, 1, 1, 1, 1, 1],
    #  [0, 0, 1, 0, 0, 1, 0, 0, 0],
    #  [0, 0, 0, 1, 0, 1, 1, 0, 0],
    #  [0, 1, 0, 0, 0, 0, 0, 1, 0],
    #  [0, 0, 0, 1, 0, 0, 1, 0, 1]]
    # St_down(matrix)
    matrix = [[1, 0, 0, 0, 1, 0, 1, 0, 0],
              [0, 1, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 1, 0, 1, 0, 1, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 1]]
    St_up(matrix)
    # print("tar:",getTar(0,matrix))
    # con = 0
    # tar = getTar(0,matrix)[1]
    # count = 0
    # operation_d1 = collect_map(con,tar)
    # print(operation_d1)
    # count = count + len(operation_d1)
    # print(count)
    # matrix = colum_cal(matrix,operation_d1)
    # for line in matrix:
    #     print(line)
    # print(count)
    # print("....................1..........................")
    # print("tar:", getTar(1, matrix))
    # con = 1
    # tar = getTar(1,matrix)[1]
    # operation_d2 = collect_map(con, tar)
    # print(operation_d2)
    # count = count + len(operation_d2)
    # print(count)
    # matrix = colum_cal(matrix,operation_d2)
    # for line in matrix:
    #     print(line)
    # print(count)
    # print("....................2..........................")
    # con = 2
    # tar = getTar(2,matrix)[1]
    # operation_d3 = collect_map(con, tar)
    # print(operation_d3)
    # count = count + len(operation_d3)
    # print(count)
    # matrix = colum_cal(matrix,operation_d3)
    # for line in matrix:
    #     print(line)
    # print(count)
    # print("....................3..........................")
    # con = 3
    # tar = getTar(con,matrix)[1]
    # operation_d4 = collect_map(con, tar)
    # print(operation_d4)
    # count = count + len(operation_d4)
    # print(count)
    # matrix = colum_cal(matrix,operation_d4)
    # for line in matrix:
    #     print(line)
    # print(count)
    # print("....................4..........................")
    # con = 4
    # tar = getTar(con,matrix)[1]
    # operation_d5 = collect_map(con, tar)
    # print(operation_d5)
    # count = count + len(operation_d5)
    # print(count)
    # matrix = colum_cal(matrix,operation_d5)
    # for line in matrix:
    #     print(line)
    # print(count)
    # print("....................5..........................")
    # con = 5
    # tar = getTar(con,matrix)[1]
    # operation_d6 = collect_map(con, tar)
    # operation_d6 = [[6,5]] + operation_d6
    # print(operation_d6)
    # count = count + len(operation_d6)
    # print(count)
    # matrix = colum_cal(matrix,operation_d6)
    # for line in matrix:
    #     print(line)
    # print(count)
    # print("....................6..........................")
    # con = 6
    # tar = getTar(con,matrix)[1]
    # operation_d7 = collect_map(con, tar)
    # op = operation_d7
    # op = [[8,7],[7,6],[7,8],[6,7]]
    # print(op)
    # count = count + len(op)
    # print(count)
    # matrix = colum_cal(matrix,op)
    # for line in matrix:
    #     print(line)
    # print(count)
    # print("....................7..........................")
    # con = 7
    # tar = getTar(con,matrix)[1]
    # operation_d8 = collect_map(con, tar)
    # op = operation_d8
    # print(op)
    # count = count + len(op)
    # print(count)
    # matrix = colum_cal(matrix,op)
    # for line in matrix:
    #     print(line)
    # print(count)
    # print("....................8..........................")
    #
    #
    #

    # print("复杂情况。。。")
    # print("step1",get_all_branches(con,tar))
    # step1 = get_all_branches(con,tar)
    # print("step2",get_steiner(step1))
    # step2 = get_steiner(step1)
    # list = []
    # count = 0
    # print("step3",turn_tree(step2))
    # step3 = turn_tree(step2)
    # for i in step3:
    #     count += 1
    #     list.append(i)
    # list2 = copy.deepcopy(list)
    # list_final = []
    # for i in range(len(list2)):
    #     list[i] = copy.deepcopy(list2[i])
    #     li = tree_sys(list[i])
    #     list_final.append(li)
    # print("step4:",select_min_tree(list_final))
    # steiner_tr = select_min_tree(list_final)
    # print(":",Gauss_map(steiner_tr,[2,4,6,7]))
    # group = Gauss_map(steiner_tr,[2,4,6,7])
    # print("2:",Gauss_map2(group,[2,4,6,7]))

    # print("===========================================================================")
    # matrix2 = [
    #  [1, 0, 0, 0, 1, 0, 1, 0, 0],
    #  [0, 1, 0, 0, 1, 0, 0, 0, 0],
    #  [0, 0, 1, 0, 1, 0, 1, 0, 0],
    #  [1, 0, 1, 1, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 1, 1, 1, 1, 1, 1],
    #  [0, 0, 1, 0, 0, 1, 0, 0, 0],
    #  [0, 0, 0, 1, 0, 1, 1, 0, 0],
    #  [0, 1, 0, 0, 0, 0, 0, 1, 0],
    #  [0, 0, 0, 1, 0, 0, 1, 0, 1]]
    # count = 0
    # operation_d1 = [[0,1],[1,2],[2,3],[1,2],[0,1]]
    # count = count + len(operation_d1)
    # matrix2 = colum_cal(matrix2,operation_d1)
    # for line in matrix2:
    #     print(line)
    # print(count)
    #
    #
    #
    # operation_d2 = [[1,2],[2,3],[1,2],[1,4],[4,7],[1,4]]
    # count = count + len(operation_d2)
    # matrix2 = colum_cal(matrix2,operation_d2)
    # for line in matrix2:
    #     print(line)
    # print(count)
    #
    #
    # operation_d3 = [[3,4],[4,5],[3,4],[2,3]]
    # count = count + len(operation_d3)
    # matrix2 = colum_cal(matrix2,operation_d3)
    # for line in matrix2:
    #     print(line)
    # print(count)
    #
    # operation_d4 = [[4,5],[5,6],[4,5],[4,7],[3,4],[3,8]]
    # count = count + len(operation_d4)
    # matrix2 = colum_cal(matrix2,operation_d4)
    # for line in matrix2:
    #     print(line)
    # print(count)
    #
    # matrix = matrix2
    #
    # operation_d5 = [[6,7],[4,5],[5,6],[4,5]]
    # count = count + len(operation_d5)
    # matrix = colum_cal(matrix,operation_d5)
    # for line in matrix:
    #     print(line)
    # print(count)
    #
    # operation_d6 = [[6,5],[5,6]]
    # count = count + len(operation_d6)
    # matrix = colum_cal(matrix,operation_d6)
    # for line in matrix:
    #     print(line)
    # print(count)
    #
    # operation_d7 = [[8,7],[7,6],[7,8],[6,7]]
    # count = count + len(operation_d7)
    # matrix = colum_cal(matrix,operation_d7)
    # for line in matrix:
    #     print(line)
    # print(count)
    #
    # operation_d8 = [[7,8]]
    # count = count + len(operation_d8)
    # matrix = colum_cal(matrix,operation_d8)
    # for line in matrix:
    #     print(line)
    # print(count)
    # print(matrix)
    #
    # operation_u8 = [[7,4],[7,6],[6,5],[7,6],[8,7]]
    # count = count + len(operation_u8)
    # matrix = colum_cal(matrix,operation_u8)
    # for line in matrix:
    #     print(line)
    # print(count)
    #
    # operation_u6 = [[4,3],[6,5],[5,0],[3,2],[4,3],[5,4],[6,5]]
    # count = count + len(operation_u6)
    # matrix = colum_cal(matrix,operation_u6)
    # for line in matrix:
    #     print(line)
    # print(count)
    #
    # operation_u5 = [[5,0],[5,4],[4,3],[3,2],[4,3],[5,4]]
    # count = count + len(operation_u5)
    # matrix = colum_cal(matrix,operation_u5)
    # for line in matrix:
    #     print(line)
    # print(count)
    #
    # operation_u5 = [[1,0],[4,1],[4,3],[3,2],[4,3]]
    # count = count + len(operation_u5)
    # matrix = colum_cal(matrix,operation_u5)
    # for line in matrix:
    #     print(line)
    # print(count)
    #
    # operation_u4 = [[3,2]]
    # count = count + len(operation_u4)
    # matrix = colum_cal(matrix,operation_u4)
    # for line in matrix:
    #     print(line)
    # print(count)
    #
    # operation_u2 = [[1,0]]
    # count = count + len(operation_u2)
    # matrix = colum_cal(matrix,operation_u2)
    # for line in matrix:
    #     print(line)
    # print(count)

    # matrix_pl = [
    #     [1, 1, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 1, 0, 0, 0, 1, 0, 1, 0],
    #     [0, 0, 1, 0, 0, 1, 0, 1, 0],
    #     [0, 0, 0, 1, 0, 0, 0, 1, 0],
    #     [0, 1, 1, 0, 1, 0, 0, 0, 0],
    #     [1, 0, 0, 0, 1, 1, 0, 0, 0],
    #     [0, 0, 0, 0, 1, 1, 1, 0, 0],
    #     [1, 0, 0, 0, 1, 1, 1, 1, 1],
    #     [0, 0, 0, 1, 0, 0, 0, 0, 1],
    #     ]
    # count = 0
    # operation_d1 = [[5,6],[6,7],[5,6],[0,5]]
    # operations = operation_d1
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d2 = [[4,5],[1,4]]
    # operations = operation_d2
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d3 = [[2,3],[4,5],[3,4],[2,3]]
    # operations = operation_d3
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d4 = [[3,8],[3,4]]
    # operations = operation_d4
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d5 = [[5,6],[4,5],[4,7]]
    # operations = operation_d5
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d6 = [[6,5],[6,7],[5,6]]
    # operations = operation_d6
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d7 = [[7,6],[6,7]]
    # operations = operation_d7
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d8 = [[7,8]]
    # operations = operation_d8
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u1 = [[8,7],[7,6],[8,7]]
    # operations = operation_u1
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u2 = [[7,4],[4,1],[3,2],[4,3],[7,4]]
    # operations = operation_u2
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u3 = [[6,5]]
    # operations = operation_u3
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u4 = [[5,4],[4,1],[4,3],[3,2],[4,3],[5,4]]
    # operations = operation_u4
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u5 = [[4,3]]
    # operations = operation_u5
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u8 = [[1,0]]
    # operations = operation_u8
    # count = count + len(operations)
    # matrix = colum_cal(matrix_pl,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # matrix_sa = [
    # [1, 0, 0, 0, 0, 1, 0, 1, 0],
    # [0, 1, 1, 0, 0, 0, 0, 0, 0],
    # [0, 0, 1, 0, 1, 0, 0, 0, 0],
    # [0, 0, 0, 1, 1, 0, 0, 1, 0],
    # [1, 1, 0, 0, 1, 1, 0, 1, 1],
    # [0, 0, 0, 1, 0, 1, 1, 0, 0],
    # [0, 0, 0, 0, 1, 0, 1, 1, 0],
    # [0, 0, 0, 0, 0, 1, 0, 1, 1],
    # [0, 0, 0, 1, 0, 0, 0, 0, 1],]
    # count = 0
    # operation_d1 = [[4,1],[1,4],[0,1]]
    # operations = operation_d1
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d2 = [[4,1],[1,4]]
    # operations = operation_d2
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d3 = [[4,3],[3,4],[2,3]]
    # operations = operation_d3
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d4 = [[4,5],[3,4],[3,8]]
    # operations = operation_d4
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d5 = [[5,4],[6,7],[7,8],[6,7],[5,6],[4,5]]
    # operations = operation_d5
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d6 = [[6,5],[7,8],[6,7],[5,6]]
    # operations = operation_d6
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d7 = [[8,7],[7,6],[7,8],[6,7]]
    # operations = operation_d7
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_d8 = [[8,7],[7,8]]
    # operations = operation_d8
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u1 = [[4,3],[4,1],[5,4],[8,7],[7,6],[6,5],[7,6],[8,7]]
    # operations = operation_u1
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u2 = [[1,0],[4,1],[7,4],[7,6]]
    # operations = operation_u2
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u3 = [[5,0],[4,3],[5,4],[6,5]]
    # operations = operation_u3
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u4 = [[4,3],[5,0],[4,1],[5,4]]
    # operations = operation_u4
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u5 = [[4,3],[3,2],[4,3]]
    # operations = operation_u5
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u6 = [[3,2]]
    # operations = operation_u6
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)
    # operation_u7 = [[1,0]]
    # operations = operation_u7
    # count = count + len(operations)
    # matrix = colum_cal(matrix_sa,operations)
    # for line in matrix:
    #     print(line)
    # print(count)

