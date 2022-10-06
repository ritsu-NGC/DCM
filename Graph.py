class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
    def addNeigbor(self,nbr,weight):
        self.connectedTo[nbr] = weight
    def __str__(self):
        return str(self.id) + " is connectedTo:" + str([x.id for x in self.connectedTo])
    def getConnections(self):
        return self.connectedTo.keys()
    def getId(self):
        return self.id
    def getWeight(self,nbr):
        return self.connectedTo[nbr]


class Graph():
    # 为了得到后续算法需要的图 需要重写图的方法
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVex = Vertex(key)
        self.vertList[key] = newVex
        return newVex
    def getVextices(self,i):
        if i in self.vertList:
            return self.vertList[i]
        else:
            return None
    def __contains__(self, item):
        return item in self.vertList
    def addEdge(self,f,t,weight = 1):

        if f not in self.vertList:
            self.addVertex(f)
        if t not in self.vertList:
            self.addVertex(t)
        if f in self.vertList:
            if self.vertList[t] in self.vertList[f].connectedTo:
                self.vertList[f].connectedTo[self.vertList[t]] = self.vertList[f].connectedTo[self.vertList[t]] + 1
            else:
                self.vertList[f].addNeigbor(self.vertList[t],weight)
    def showGraph(self):
        for vertex in self.vertList:
            print("------------------------------------------------------------------------------")
            print("qubit:{0}".format(self.vertList[vertex].id))
            for nbr in self.vertList[vertex].connectedTo:
                    print("target：{0},weight:{1}".format(nbr.id, self.vertList[vertex].connectedTo[nbr]))
    def getVetices(self):
        return self.vertList.keys()
    def __iter__(self):
        return iter(self.vertList.values())





