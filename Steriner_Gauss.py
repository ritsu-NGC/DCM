# coding:utf-8
import numpy as np

class bfsNode:
    # linkids: linked nodeId list
    # previousids : the previous nodeId
    # id: current nodeId
    # distance: distance between current node and root node
    # status: 0, 1, 2    0 means freash node, 1 means processing node, 2 means completed node

    def __init__(self, linkIds, id, distance, status):
        self.linkIds = linkIds
        self.previousId = None
        self.id = id
        self.distance = distance
        self.status = status

    def display(self):
        print("(currentId:", self.id, "linkIds:", self.linkIds, ")") #diplays linkIds for each node

    def displayMore(self):
        print("(currentId:", self.id, "distance:", self.distance, "previousId:", self.previousId, ")")   #display node details


def createBfsTree(l, _fr, type=0):
    # type=0: tree for lower triangular matrix
    # type=1: tree for upper triangular matrix
    n = int(np.sqrt(l))
    # m = np.arange(l).reshape(n, n)   # convert to n*n arrary
    # print(m)
    m = np.array([[0, 1, 2],
                  [5, 4, 3],
                  [6, 7, 8]])

    # m = np.array([[0, 1, 2, 3, 4, 5],
    #               [11,10,9, 8, 7, 6],
    #               [12,13,14,15,16,17],
    #               [18,19,20,21,22,23],
    #               [29,28,27,26,25,24],
    #               [30,31,32,33,34,35]])

    # m = np.array([[0, 1, 2, 3],
    #               [7, 6, 5, 4],
    #               [8, 9, 10,11],
    #               [15,14,13,12]])

    #
    # m = np.array([[0, 1, 2],
    #               [5, 4, 3]])

    print(m)
    for i in np.arange(n):
        if np.mod(i, 2) == 1:
            m[i] = sorted(m[i], reverse=True)     # revise the list if an odd row
    result = []
    if type == 0:
        for i in np.arange(n):
            for j in np.arange(n):
                links = []
                if j+1 < n and m[i][j+1] > _fr:  # _fr矩阵的对角线行数
                    links.append(m[i][j+1])
                if j-1 >= 0 and m[i][j-1] > _fr:
                    links.append(m[i][j-1])
                if i+1 < n and m[i+1][j] > _fr:
                    links.append(m[i+1][j])
                if i-1 >= 0 and m[i-1][j] > _fr:
                    links.append(m[i-1][j])      # get neighbour nodes for each node
                result.append(bfsNode(links, m[i][j], None, 0))         # generate linkIds
    elif type == 1:
        for i in np.arange(n):
            for j in np.arange(n):
                links = []
                if j+1 < n and m[i][j+1] < _fr:
                    links.append(m[i][j+1])
                if j-1 >= 0 and m[i][j-1] < _fr:
                    links.append(m[i][j-1])
                if i+1 < n and m[i+1][j] < _fr:
                    links.append(m[i+1][j])
                if i-1 >= 0 and m[i-1][j] < _fr:
                    links.append(m[i-1][j])      # get neighbour nodes for each node
                result.append(bfsNode(links, m[i][j], None, 0))         # generate linkIds
    elif type == 2:
        for i in np.arange(n):
            for j in np.arange(n):
                links = []
                if j + 1 < n and m[i][j+1] != _fr:
                    links.append(m[i][j + 1])
                if j - 1 >= 0 and m[i][j-1] != _fr:
                    links.append(m[i][j - 1])
                if i + 1 < n and m[i+1][j] != _fr:
                    links.append(m[i + 1][j])
                if i - 1 >= 0 and m[i-1][j] != _fr:
                    links.append(m[i - 1][j])  # get neighbour nodes for each node
                result.append(bfsNode(links, m[i][j], None, 0))  # generate linkIds
    return result


def createBfsTree1(l, _fr):  # tree for bakup
    n = int(np.sqrt(l))
    m = np.arange(l).reshape(n, n)   # convert to n*n arrary
    # print(m)
    for i in np.arange(n):
        if np.mod(i, 2) == 1:
            m[i] = sorted(m[i], reverse=True)     # revise the list if an odd row
    result = []
    for i in np.arange(n):
        for j in np.arange(n):
            links = []
            if j+1 < n and m[i][j+1] > _fr:
                links.append(m[i][j+1])
            if j-1 >= 0 and m[i][j-1] > _fr:
                links.append(m[i][j-1])
            if i+1 < n and m[i+1][j] > _fr:
                links.append(m[i+1][j])
            if i-1 >= 0 and m[i-1][j] > _fr:
                links.append(m[i-1][j])      # get neighbour nodes for each node
            result.append(bfsNode(links, m[i][j], None, 0))         # generate linkIds
    return result

def getBfsNode(ind, nodes):
    for node in nodes:
        if node.id == ind:
            return node
    return None

# this function will be only for single target, to be elemented
def bfsFunction(fr, nodes):
    queue = []
    fr.distance = 0
    fr.status = 1
    queue.append(fr)
    while (len(queue)>0):
        curr = queue.pop(0)
        np.random.shuffle(curr.linkIds)      # disorder the linkIds
        for i in curr.linkIds:
            linkNode = getBfsNode(i, nodes)
            if linkNode.status == 0:
                linkNode.previousId = curr.id
                linkNode.distance = curr.distance + 1
                linkNode.status = 1    # if it is a fresh node, then change it to process node
                queue.append(linkNode)
            curr.status = 2      # complete all neighbour scan

# this function will be only for multiple targets
def bfsFunctionAll(fr, tos, nodes):
    queue = []      # queue for process nodes
    routeList = []  # route list
    queue.append([fr])
    while (len(queue) > 0):
        curr = queue.pop(0)
        _curr = curr[-1]
        for i in np.arange(len(tos)):
           if tos[i] == _curr:
                routeList.append(list(map(lambda x: x.id, curr)))     # if the expected node is found, then put it into routeList
            # continue
        for i in _curr.linkIds:             # scan all its neighbour nodes
            linkNode = getBfsNode(i, nodes)
            # print(getBfsNode(0, nodes).status)
            if linkNode.status == 0:
                currCopy = curr.copy()
                currCopy.append(linkNode)   #produce new route
                # for k in currCopy:
                #    print(k.id, k.status)
                # print("next")
                queue.append(currCopy)
        _curr.status = 2
    return routeList

def getRoute(to, nodes):
    result = [to.id]
    resultRev = []
    while(to.previousId is not None):
        to = getBfsNode(to.previousId, nodes)
        result.append(to.id)
    for i in np.arange(len(result)-1, -1, -1):
        resultRev.append(result[i])
    return resultRev

# produce best route for only one target, to be elemented
def run(n, _fr, _to, type = 0):
    nodes = createBfsTree(n, _fr, type)
    # _fr = 0
    fr = getBfsNode(_fr, nodes)    #obtain start node
    # _to = 7
    to = getBfsNode(_to, nodes)    #obtain end node
    bfsFunction(fr, nodes)
    bestRoute = getRoute(to, nodes)
    return bestRoute, nodes


def subsets(l, n):   # get all subsets
    s = []
    if l == []:
        yield []   # return the empty list
    else:
        _1st = l[0]
        _others = l[1:]
        for i in subsets(_others, n):  # scan others
            yield i  # subsets of others
            if len([_1st] + i) <= n:
                yield [_1st] + i     # all subsets


# produce best route for multiple targets
def runAll(n, _fr, _tos, type=0):
    tos = []
    # _to = 7
    nodes1 = createBfsTree(n, _fr, type)
    # _fr = 0
    fr = getBfsNode(_fr, nodes1)  # obtain start node
    for _to in _tos:
        to = getBfsNode(_to, nodes1)    # obtain end node
        tos.append(to)
    routeList = bfsFunctionAll(fr, tos, nodes1)     # get all the possible routes for each target
    # print(routeList)
    l = len(tos)

    def f(x):
        z = len({y[-1] for y in x})
        return z
    _routeSet = [s for s in subsets(routeList, l) if len(s) == l and f(s) == l]     # get the all the candidate routes for multiple targes
    # print(_routeSet)
    maxLen = np.inf
    tSet = set()
    routeSet = []
    for i in _routeSet:
        tSet.clear()
        for j in i:
            tSet = tSet.union(set(j))
        if len(tSet) < maxLen:
            maxLen = len(tSet)
            routeSet = i
    # print(routeSet)       # pick the best route which cross the smallest nodes

    return routeSet



seq = []


# convert lower triangular matrix
def guassLower(data, j,  bestRoute, type=0):
    L2 = []
    # from start node to end node, bestRoute length from longest to shortest
    bestRoute = sorted(bestRoute, key=len, reverse=True)
    for k in bestRoute:  # scan each route
        for k1 in np.arange(len(k)):
            curr = k[k1]
            next = k[k1 + 1]
            if data[curr][j] == 1 and data[next][j] == 0:
                L2.append((curr, next))
                data[next] = data[curr] ^ data[next]  # do xor for each two rows
                print(next, "=", next, "exor", curr, "->\n", data)
            if k1 + 1 == len(k) - 1:
                # if data[curr][j] == 1 and data[next][j] == 1:
                #     print("test:", curr, next)
                #     L2.append((curr, next))
                #     data[next] = data[curr] ^ data[next]  # do xor for last column
                #     # print("(",curr, ",", next,")->", data)
                break
    #print(L2)
    _L2 = handleOnes(data, j,  bestRoute, type)
    #print(data)
    L2.extend(_L2)
    return L2


def handleOnes(data, j,  bestRoute, type=0):
    L2 = []
    L2Can = []
    #bestRoute = sorted(bestRoute, key=len, reverse=False)
    # from end node to start node, bestRoute length from longest to shortest

    for k in bestRoute:  # scan each route
        k = k[-1::-1]  # from end node to start node
        for k1 in np.arange(len(k)):
            curr = k[k1]
            next = k[k1 + 1]
            if [next, curr] not in L2Can:
                L2Can.append([next, curr])
            if k1 + 1 == len(k) - 1:
                break            #anyway need to break
    #get all possible combinations
    def perm(arr, pos=0):
        if pos == len(arr):
            yield arr
        for i in np.arange(pos, len(arr)):
            arr[pos], arr[i] = arr[i], arr[pos]
            for _ in perm(arr, pos + 1):
                yield _
    #print(L2Can)
    #print(data)
    res = perm(L2Can)
    #print(len(list(res)))
    #print(list(res))

    for k in res:
        _data = data.copy()
        _L2 = L2.copy()
        _dataList = []
        for k1 in k:
            #print(k1)
            _L2.append((k1[0], k1[1]))
            _data[k1[1]] = _data[k1[0]] ^ _data[k1[1]]
            _dataList.append(_data.copy())
        #print("process",_data[:j, j], type)
        if (_data[j+1:,j] == np.zeros(_data.shape[1]-j-1)).all() and type == 0:     # lower
            data[:] = _data[:]
            L2 = _L2
            for k2i, k2 in enumerate(_L2):
                # print("(", k2[0], "exor", k2[1], ")->\n", _dataList[k2i])
                print(k2[1], "=", k2[1], "exor", k2[0], "->\n", _dataList[k2i])

        #print("after:", data[j:, j])
        if (_data[0:j, j] == np.zeros(j)).all() and type == 1:  # upper
            #print(_L2)
            #print(_data)
            data[:] = _data[:]
            L2 = _L2
            for k2i, k2 in enumerate(_L2):
                # print("(", k2[0], "exor", k2[1], ")->\n", _dataList[k2i])
                print(k2[1], "=", k2[1], "exor", k2[0], "->\n", _dataList[k2i])

            break


     #handle mixed columns
    # print("test",_L2)
    # for k1 in _L2:
    #     if data[k1[0],j] == 0 and data[k1[1],j] == 0:
    #         _L2.append((k1[0], k1[1]))
    #         data[k1[1]] = data[k1[0]] ^ data[k1[1]]

    return L2     # [(a, b), (b, c)] means b = a ^ b, c = b ^ c


#convert upper triangular matrix
def guassUpper(data, j,  bestRoute):
    L2 = guassLower(data, j,  bestRoute, 1)
    return L2     # [(a, b), (b, c)] means b = a ^ b, c = b ^ c


def handleZeroStart(data, j,  bestRoute):
    L2 = []
    bestRoute = sorted(bestRoute, key=len, reverse=True)
    for k in bestRoute:  # scan each route
        k = k[-1::-1]  # from end node to start node
        for k1 in np.arange(len(k)):
            curr = k[k1]
            next = k[k1 + 1]
            if data[curr][j] == 1 and data[next][j] == 0:
                L2.append((curr, next))
                data[next] = data[curr] ^ data[next]  # do xor for each two rows
                print("(", curr, ",", next, ")->\n", data)
            if k1 + 1 == len(k) - 1:
                break            #anyway need to break
        if data[j][j] == 0:
            break
    return L2     #[(a, b), (b, c)] means b = a ^ b, c = b ^ c


if __name__ == '__main__':
    n = 9
    count = 0




    data1 = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1]])

    data = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0],
        [1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1]])

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
