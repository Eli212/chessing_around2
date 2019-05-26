#Or Zaidman id: 313230088

class IteratorClass:
    def __init__(self,graph):
        self._allGraph = graph._map.keys()
        self._current = 0


    def __next__(self):
        self._current += 1

        if self._current < len(self._allGraph):
          return self._allGraph[self._current]
        raise StopIteration

class Graph:
    def __init__(self, map=None):
        if (len(map) == 0) or (not isinstance(map, dict)):
            self._map = dict()
            self._startNode = None
            self._endNode = None
        else:
            self._map = map
            temp = Graph.find_start_node(self._map)
            if temp is None:
                print("error")
            else:
                self._startNode = temp
            temp = Graph.find_end_node(self._map)
            if temp is None:
                print("error")
            else:
                self._endNode = temp

    def add_activity(self,activity,afterSet = None):
        if activity.name in self._map:
            return "%s is exists" %(activity.name)

        if afterSet is None:
            self._map[activity.name] = dict()
            add = dict()
            add={self._startNode:activity.duration}
            self._map[activity.name] = add
            self._startNode = activity.name

        else:
            add={activity.name:activity.duration}
            s = afterSet
            s = str(s)
            self._map[s].update(add)

    @staticmethod
    def find_end_node(map):
        for key in map:
            if len(map[key]) == 0:
                return key
        return None

    @staticmethod
    def find_start_node(map):
        counter = dict()
        for key in map:
            counter[key] = 0

        for key in map:
            trans = map[key]
            for tran in trans:
                counter[tran] += 1

        for state in counter:
            if counter[state] == 0:
                return state

        return None

    def find_isolate(self, map):
        counter = dict()
        for key in map:
            counter[key] = 0

        for key in map:
            trans = map[key]
            for tran in trans:
                counter[tran] += 1

        for key in map:
            if len(map[key]) != 0:
                counter[key] += 1
        found = list()
        for i in map:
            if counter[i] == 0:
                found.append(i)

        return found

    def __iter__(self):
        return IteratorClass(self)




    def __str__(self):
        s=""
        for i in self._map:
          s += "%s -> %s \n" %(i, self._map[i])
        return s

    def get_start_node(self):
        return self._startNode


    def find_early_start(self):
        vec = dict()
        que=[]
        for i in self._map:
            vec[i]=0
        first= self._map[self._startNode]
        que.append(self._startNode)
        while len(que) != 0:
            temp =str(que.pop(0))
            for sun in self._map[str(temp)]:
                que.append(sun)
                if  int(vec[sun]) <= int(vec[temp]) +  int(self._map[temp][sun]):
                    vec[sun] = int(vec[temp]) +  int(self._map[temp][sun])
        return vec

    def find_last_start(self,vecEarly):
        vec = dict()
        que = []
        for i in self._map:
            vec[i] = 0
        first = self._map[self._startNode]
        que.append(self._startNode)
        vec[self._startNode] = vecEarly[self._startNode]
        while len(que) != 0:
            temp = str(que.pop(0))
            for sun in self._map[str(temp)]:
                que.append(sun)
                x = self._map[str(temp)][sun]
                if(vec[sun] >= vec[str(temp)]-x) | (vec[sun] == 0):
                 vec[sun] = vec[str(temp)]-x
        return vec

    def upsade_down(self):
        temp = dict()
        newGraph= dict()
        count=0
        for i in self._map:
            for son in  self._map[i]:
             add= self.returnNumber(self._map.get(str(i)).values())
             if str(son)  not in newGraph:
               newGraph[son] = {i: add[count]}
               count += 1
             else:
                 newGraph.get(son).update({i: add[count]})
            count=0
        for i in range(1,self._map.__len__()):
            if str(i) not in newGraph.keys():
                newGraph[str(i)] = {}
        return(newGraph)

    def returnNumber(self,number):
        list =[]
        for i in number:
            list.append(i)
        return list
    def calculateSlackTime1(self,vecEarly,vecLast):
        lst = list()
        for i in vecLast:
            vecLast[i]=vecLast[i]-vecEarly[i]
            if vecLast[i] != 0:
                lst.append(vecLast[i])
        return vecLast

    def calculateSlackTime2(self,vecLst):
        lst=list()
        for i in vecLst:
            if vecLst[i] != 0:
                lst.append(vecLst[i])
        lst.sort()
        return lst

    def sum_all_slacks(self,l):
        sum = 0
        for i in l:
            sum += i
        return sum

    def find_Critical_path(self,slackLst):
         current = self._startNode
         lstSlack = list()

         for i in slackLst:
            if slackLst.get(i)==0:
                 current = str(i)
                 lstSlack.append(current)
                 pass
         lstSlack.sort(key= int)
         print("critical path:",lstSlack)


class Activity:
    def __init__(self,name,duration):
        self.name = name
        self.duration = duration

    def get_name(self):
        return self.name

    def __str__(self):
        return "%s value(%s)" %(self.name,self.duration)


if __name__ == '__main__':
    mapInput = {"1": {"2":6},
           "2": {"3": 4, "4": 3, "6": 6},
           "3": {"5": 2},
           "4": {"9": 4},
           "5": {"6": 3},
           "6": {"7": 2,"8": 4},
           "7": {"11": 4},
           "8": {"11": 1},
           "9": {"10": 1},
           "10": {"11": 4},
           "11": {}
            }

    gra = Graph(mapInput)
    print("input praoh:\n",gra)

    vec = gra.find_early_start()
    newGraphUpSide = Graph(gra.upsade_down())

    vec2 = newGraphUpSide.find_last_start(vec)
    print("upside graph:\n",newGraphUpSide)
    print("isolate activity:",gra.find_isolate(gra._map))

    activityNew = Activity("12",2)
    gra.add_activity(activityNew,3)
    print("after added activity:",gra)
    lTemp = (gra.calculateSlackTime1(vec,vec2))
    lstAll = gra.calculateSlackTime2(lTemp)
    print("list of all slacks: ",lstAll)
    print("sum of all slacks:",gra.sum_all_slacks(lstAll))
    gra.find_Critical_path(lTemp)
