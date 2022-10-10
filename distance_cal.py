
def distance_cal(c,t):
    dis = {"d0": [0, 1, 2, 3, 2, 1, 2, 3, 4],
     "d1": [1, 0, 1, 2, 1, 2, 3, 2, 3],
     "d2": [2, 1, 0, 1, 2, 3, 4, 3, 2],
     "d3": [3, 2, 1, 0, 1, 2, 3, 2, 1],
     "d4": [2, 1, 2, 1, 0, 1, 2, 1, 2],
     "d5": [1, 2, 3, 2, 1, 0, 1, 2, 3],
     "d6": [2, 3, 4, 3, 2, 1, 0, 1, 2],
     "d7": [3, 2, 3, 2, 1, 2, 1, 0, 1],
     "d8": [4, 3, 2, 1, 2, 3, 2, 1, 0]}
    conbit = "d" + c
    dis_tar = dis.get(conbit)
    return dis_tar[int(t)]

def get_dis(address):
    r = open(address,"r")
    tol_dis = 0
    for line in r.readlines():
        gate = line.split()
        if gate[0] == "CNOT":
            # print("is cnot gate")
            tol_dis = tol_dis + distance_cal(gate[1][1],gate[2][1])
    return tol_dis




if __name__ == '__main__':
    get_dis("test_new.txt")
    print(get_dis("test_new.txt"))