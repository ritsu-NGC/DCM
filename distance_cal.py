
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
def distance_cal_16bit(c,t):
    dis = {"d0": [0,1,2,3,4,3,2,1,2,3,4,5,6,5,4,3],
     "d1": [1,0,1,2,3,2,1,2,3,2,3,4,5,4,3,4],
     "d2": [2,1,0,1,2,1,2,3,4,3,2,3,4,3,4,5],
     "d3": [3,2,1,0,1,2,3,4,5,4,3,2,3,4,5,6],
     "d4": [4,3,2,1,0,1,2,3,4,3,2,1,2,3,4,5],
     "d5": [3,2,1,2,1,0,1,2,3,2,1,2,3,2,3,4],
     "d6": [2,1,2,3,2,1,0,1,2,1,2,3,4,3,2,1],
     "d7": [1,2,3,4,3,2,1,0,1,2,3,4,5,4,3,2],
     "d8": [2,3,4,5,4,3,2,1,0,1,2,3,4,3,2,1],
     "d9": [3,2,3,4,3,2,1,2,1,0,1,2,3,2,1,2],
    "d10": [4,3,2,3,2,1,2,3,2,1,0,1,2,1,2,3],
    "d11": [5,4,3,2,1,2,3,4,3,2,1,0,1,2,3,4],
    "d12": [6,5,4,3,2,3,4,5,4,3,2,1,0,1,2,3],
    "d13": [5,4,3,4,3,2,3,4,3,2,1,2,1,0,1,2],
    "d14": [4,3,4,5,4,3,2,3,2,1,2,3,2,1,0,1],
    "d15": [3,4,5,6,5,4,3,2,1,2,3,4,3,2,1,0],
           }
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
            # print(gate[1][1],gate[2][1])
            tol_dis = tol_dis + distance_cal(gate[1][1],gate[2][1])
            # print(tol_dis)
    return tol_dis

def get_dis_16bit(address):
    r = open(address,"r")
    tol_dis = 0
    for line in r.readlines():
        gate = line.split()
        if gate[0] == "CNOT":
            print("gate:",gate)
            c = gate[1].strip("q")
            t = gate[2].strip("q")
            print(c,t)
            tol_dis = tol_dis + distance_cal_16bit(c,t)
            print(tol_dis)

    return tol_dis



if __name__ == '__main__':
    # get_dis("test_new.txt")
    print(get_dis_16bit("test_new.txt"))