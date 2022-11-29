from SG import *
def unit(matrix):
    unit =[
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
    ]
    if matrix == unit:
        print("ok")
    else:
        print("no")
if __name__ == '__main__':


    matrix2 = [
        [1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 1, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 1, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 1],
    ]
    count = 0
    operation_d1 = [[5,6],[0,5],]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)


    print("/////////////////////////////////////////////")
    operation_d1 = [[1,4],[4,5],[4,7],[3,8],[2,3],[1,2],[1,4]]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)
    operation_d1 = [[4,7],[2,3],[3,4],[2,3]]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)
    operation_d1 = [[3,8],[5,6],[4,5],[3,4]]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)
    operation_d1 = [[5,4],[4,5],]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)
    operation_d1 = [[6,5],[6,7],[7,8],[6,7],[5,6],[6,7]]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)
    operation_d1 = [[7,8],]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)
    operation_d1 = [[8,3],[7,4],[7,6],[8,7]]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)
    operation_d1 = [[4,3],[7,4],[6,5],[7,6]]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)

    operation_d1 = [[2,1],[6,5],[5,4],[4,3],[3,2],[4,3],[5,4],[6,5]]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)
    operation_d1 = [[5,4],[4,1],[5,4]]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)
    operation_d1 = [[1,0],[2,1],[3,2],[4,3]]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)
    operation_d1 = [[1,0],[3,2],[2,1],[3,2],[2,1],[1,0]]
    count = count + len(operation_d1)
    matrix2 = colum_cal(matrix2,operation_d1)
    for line in matrix2:
        print(line)
    print(count)






















































    unit(matrix2)









