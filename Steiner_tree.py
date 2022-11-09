import copy
from itertools import product
import itertools as it
import copy
route = []

# 给出control bit 和 target bit 得出所有可能路径合集
def find_route(con,tar):
    map = [
    [0,[1,5]],
    [1,[2,4]],
    [2,[3]],
    [3,[4,8]],
    [4,[5,7]],
    [5,[6]],
    [6,[7]],
    [7,[8]],
    [8,[]],]
    if con == tar or map[con][1] == []:
        pass
    else:
        for node in map[con][1]:
            route.append([con,node])
            find_route(node,tar)
    return
# 将所有路径合集拆成单个路径的集合
def breakdown(list,tar,con):
    # print(list)
    all_routes = []
    route = []
    for item in list:
        # print(list.index(item))
        if item[0] in route:
                # 结果路径终点-----
            index_f = list.index(item)
            index_f = index_f - 1
            final = list[index_f][1]
                # 结果路径终点-----
                # 路径确认完成，装起来
            route.append(final)
            # print("函数中路径：",route)
            route = route
            all_routes.append(route.copy())
                # 构建新路径，删掉多余点
            index = route.index(item[0])
            while len(route) - 1 >= index:
                route.pop()
        route.append(item[0])
    ff = list.pop()[1]
    route.append(ff)
    all_routes.append(route)
    return all_routes
# 去除掉到达错误终点的路径
def get_correct_route(list,tar,con):
    route_cor = []
    for tree in list:
        final = tree[len(tree) - 1]
        if final == con:
            route_cor.append(tree)
    return route_cor

def get_branches(con,tar):
    global route
    find_route(con, tar)
    # print("route:",route)
    all = breakdown(route, con, tar)
    # print("all:",all)
    branches = get_correct_route(all, con, tar)
    route = []
    return branches

# 多target bits 的情况
def get_all_branches(con,tar):
    all_bra = {}
    for tar_i in tar:
        # print(tar_i,":")
        branches = get_branches(con,tar_i)
        # for i in branches:
        #     print(i)

        all_bra[tar_i] = branches
    return all_bra
# 根据多target bits 结果生成steiner tree
def get_steiner(branches):
    storage = []

    for value in branches.values():
        storage.append(value)
    return storage
# 单行中所有的门组合在一起
def turn_tree(storage):
    n = len(storage)
    trees = []
    count = 0
    if n == 1:
        result = storage[0]
    elif n == 2:
        result = product(storage[0],storage[1])
    elif n == 3:
        result = product(storage[0], storage[1],storage[2])
    elif n == 4:
        result = product(storage[0], storage[1],storage[2],storage[3])
    elif n == 5:
        result = product(storage[0], storage[1],storage[2],storage[3],storage[4])
    elif n == 6:
        result = product(storage[0], storage[1],storage[2],storage[3],storage[4],storage[5])
    elif n == 7:
        result = product(storage[0], storage[1],storage[2],storage[3],storage[4],storage[5],storage[6])
    elif n == 8:
        result = product(storage[0], storage[1],storage[2],storage[3],storage[4],storage[5],storage[6],storage[8])
    for re in result:
        ki = re
        count += 1
        trees.append(ki)
    return trees
# 代表每个门的list组合成一个list
def tree_sys(list):
    print(list)
    print(type(list))
    tree = []
    # print("初始树：",tree)
    tree = list[0]
    for l in list:
        if len(l) < len(tree):
            tree = l
    # print("min:",tree)
    for l2 in list:
        for ele in l2:
            if ele not in tree:
                tree.append(ele)
    return tree
# 从所有树之中选出最小的树
def select_min_tree(tree):
    min = tree[0]
    for tr in tree:
        # print(tr)
        if len(tr) < len(min):
            min = copy.deepcopy(tr)

    return min
# 给定steiner tree 给定target bit 生成gauss map
def Gauss_map(steiner,tar):
    print("steiner:",steiner)
    index = 0
    list = steiner
    map = [
    [0,[1,5]],
    [1,[2,4]],
    [2,[3]],
    [3,[4,8]],
    [4,[5,7]],
    [5,[6]],
    [6,[7]],
    [7,[8]],
    [8,[]],]
    sten = sorted(list)
    print("sten:",sten)
    map_st = []
    for num in sten:
        # print(map[num])
        map_st.append(map[num])
    # print(map_st)
    group = []
    while index < len(sten) - 1:
        now = sten[index]
        cango = map_st[index][1]
        index += 1
        next = sten[index]
        if next in cango:
            group.append([now,next])
        elif next in map_st[index - 2][1]:
            now = sten[index - 2]
            group.append([now,next])
        elif next in map_st[index - 3][1]:
            now = sten[index - 3]
            group.append([now,next])
        elif next in map_st[index - 4][1]:
            now = sten[index - 4]
            group.append([now,next])
    return group
# 废弃掉了 不好用
def Gauss_map2(group,tar):
    waitoadd = []
    index = 0
    while index < len(group) - 1:
        if group[index][1] != group[index+ 1][0] or (index+1) == len(group):
            elimate = group[index][1]
            tar.remove(elimate)
            waitoadd.reverse()
            print("这是一个终止")
            print(waitoadd)
            for ele in waitoadd:
                group.insert(index,ele)
                index += 1
            waitoadd = []

        else:
            waitoadd.append(group[index])
        index += 1
    # print(waitoadd)
    waitoadd.reverse()
    # print(waitoadd)
    group = group + waitoadd
    print(group)
    # 消除多余项
    tar.pop()
    # print(tar)
    for item in tar:
        print("item:",item)
        i = 0
        while item != group[i][1] and i < len(group)-1 :
            i +=1
        print("i",i)
        # group.pop(i)
        del group[i]

    return group
# 最后一步 用这个函数
def new_Gauss_map2(group,tar):
    list = []
    inlight = copy.deepcopy(tar)
    deletate_light = []
    dl_list = []
    for index in range(len(group)):
        if index == len(group) - 1 or group[index][1] < group[index + 1][0]:
            list.append(group[index])
            dl_list.reverse()
            list = list + dl_list
            deletate_light = []
            dl_list = []
        else:
            deletate_light.append(group[index][1])
            dl_list.append(group[index])
            if group[index][1] in inlight:
                pass
            else:
                list.append(group[index])

    return list



if __name__ == '__main__':

    # print(get_all_branches(1,[4,6,7]))
    # print("..............................")
    # print(get_all_branches(1,[4,6,7]))
    # print()
    # print(get_steiner(get_all_branches(1,[4,6,7])))
    res = get_steiner(get_all_branches(3,[4,6,8]))
    print(".............................")

    list = []
    trees = turn_tree(res)
    count = 0
    for i in turn_tree(res):
        # print(i)
        count += 1
        list.append(i)
    print("..................")
    list2 = copy.deepcopy(list)
    for il in list:
        print(il)
        print(type(il))
    print("..................")
    list_final = []
    for i in range(len(list2)):
        # print(i)
        # print("复制品：",list2[i])
        list[i] = copy.deepcopy(list2[i])
        print("xxx")
        li = tree_sys(list[i])
        # print("li:",li)
        list_final.append(li)
    print("..............................final..........................")
    for it in list_final:
        print(it)
    print("..................min......................")
    print("selected:",select_min_tree(list_final))
    steiner_tr = select_min_tree(list_final)

    print(":",Gauss_map(steiner_tr,[4,6,8]))
    group = Gauss_map(steiner_tr,[4,6,8])
    # print("2:",Gauss_map2(group,[4,6,8]))
    print("2:", new_Gauss_map2(group, [4, 6, 8]))



