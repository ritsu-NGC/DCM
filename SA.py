
from distance_cal import distance_cal
import math
import random
import copy

def dis_cal(placement):# 函数优化问题
    # print("new placement:",placement)
    r2 = open("test_new.txt", "r")
    tol_dis = 0
    # w = open("Mnew_cir.txt", "w")
    for line in r2.readlines():
        gate = line.split()
        # print(gate)
        if gate[0] == "CNOT":
            gate[1] = "q" + str(placement.index(gate[1]))
            gate[2] = "q" + str(placement.index(gate[2]))
            str_gate = gate[0] + " " + gate[1] + " " + gate[2] + "\n"
            # print(str_gate)
            # print(gate)
            tol_dis = tol_dis + distance_cal(gate[1][1],gate[2][1])
            # print(tol_dis)
            # print(tol_dis)

    return tol_dis,placement
class SA:
    def __init__(self, initial_place,initial_dis, iter=3, T0=2, Tf=0.1, alpha=0.99):
        self.start_place = initial_place
        self.start_res = initial_dis
        self.iter = iter  # 内循环迭代次数,即为L =100
        self.alpha = alpha  # 降温系数，alpha=0.99
        self.T0 = T0  # 初始温度T0为100
        self.Tf = Tf  # 温度终值Tf为0.01
        self.T = T0  # 当前温度
        self.placement = []
        self.dis = []
        self.most_best = []
        """
        random()这个函数取0到1之间的小数
        如果你要取0-10之间的整数（包括0和10）就写成 (int)random()*11就可以了，11乘以零点多的数最大是10点多，最小是0点多
        该实例中x1和x2的绝对值不超过5（包含整数5和-5），（random() * 11 -5）的结果是-6到6之间的任意值（不包括-6和6）
        （random() * 10 -5）的结果是-5到5之间的任意值（不包括-5和5），所有先乘以11，取-6到6之间的值，产生新解过程中，用一个if条件语句把-5到5之间（包括整数5和-5）的筛选出来。
        """
        self.history = {'f': [], 'T': []}

    def generate_new(self,num_qubit):  # 扰动产生新解的过程
        while True:
            return random.sample(range(0,num_qubit),2)

    def GetMin(self,all):
        min = 1000000
        output = []
        for item in all:
            if min > item[0]:
                min = item[0]
                output = [min,item[1]]
        return output




    def Metrospolis(self, f, f_new):  # Metropolis准则
        if f_new <= f:
            return 1
        else:
            p = math.exp((f - f_new) / self.T)
            if random.random() < p:
                return 1
            else:
                return 0

    # def best(self):  # 获取最优目标函数值
    #     if self.dis != []:
    #         min = 100000
    #         for dis in self.dis:
    #             if min > dis:
    #                 min = dis
    #         self.start_res = min
    #         print("min:",min)
    #         index = self.dis.index(min)
    #         self.start_place = self.placement[index]
    #         self.dis = []
    #         self.placement = []
    #         return self.start_place,self.start_res
    #     else:
    #         return None

    def run(self):
        count = 0
        tool = 0
        min = 1000000
        all_accpet = []
        current_accept = []
        # 外循环迭代，当前温度小于终止温度的阈值
        while self.T > self.Tf:

            # 内循环迭代100次
            for i in range(self.iter):
                count += 1
                # print(count)
                change_x_y = self.generate_new(9)
                # print(change_x_y)
                # 产生扰乱 修改量子点列中的两个位置
                # print("start:",self.start_res,self.start_place)
                place_new = self.start_place
                tool = place_new[change_x_y[0]]
                place_new[change_x_y[0]] = place_new[change_x_y[1]]
                place_new[change_x_y[1]] = tool
                # print("new placement:",place_new)
                result = dis_cal(place_new)
                # print("计算：",dis_cal(place_new))
                # print("结果：",result)
                f_new = result[0]
                if self.Metrospolis(self.start_res, f_new):# 判断是否接受新值
                    # print("接受：",result)
                    current_accept.append(copy.deepcopy(result))
                    # print("当前结果:",current_accept)


            if self.T > self.Tf:
                # 温度按照一定的比例下降（冷却）
                self.T = self.T * self.alpha
            # print("当前轮次初始解:",self.start_res,self.start_place)
            # if self.start_res == dis_cal(self.start_place)[0]:
            #     print("yes")
            # else:
            #     print("wrong")

            if current_accept != []:
                # for cur_res in current_accept:
                #     print("当前轮所有解：",cur_res)
                #     if cur_res[0] == dis_cal(cur_res[1])[0]:
                #         print("yes")
                #     else:
                #         print("wrong")
                for res in current_accept:
                    if min > res[0]:
                        min = res[0]
                        place_wait = res[1]
                print("当前轮最优解：",min,place_wait)
                if min == dis_cal(place_wait)[0]:
                    print("yes")
                else:
                    print("wrong")
                all_accpet.append([copy.deepcopy(min),copy.deepcopy(place_wait)])
                # print("all_acc:",all_accpet)
                self.start_res = copy.deepcopy(min)
                self.start_place = copy.deepcopy(place_wait)
                current_accept = []
                min = 1000000
                # 迭代L次记录在该温度下最优解
                # self.GetMin(all_accpet)
        return all_accpet

if __name__ == '__main__':
    # print(dis_cal(['q1', 'q0', 'q8', 'q2', 'q3', 'q5', 'q4', 'q6', 'q7']))
    sa = SA(['q1', 'q7', 'q8', 'q5', 'q3', 'q2', 'q4', 'q6', 'q0'],36)

    # for item in sa.run():
    #     print("结果：",item)
    #     if item[0] == dis_cal(item[1])[0]:
    #         print("yes")
    #     else:
    #         print("wrong")
    print(sa.GetMin(sa.run()))

    # print(sa.run())
    # for inter in sa.run():
    #     print(inter)
    #     print(".................")

    # print(dis_cal( ['q1', 'q7', 'q8', 'q5', 'q6', 'q2', 'q4', 'q3', 'q0']))


