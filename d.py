class Activity:
    def __init__(self, related=None):
        if related is None:
            related = {}
        self._related = related
        # self.name = name

    def get_related(self):
        return self._related

    def print_activities(self):
        for i in self._related.values():

    # def get_name(self):
    #     return self.name
    #
    # def setR(self,activi):
    #     self._related=activi.get_related()
    #
    # def __repr__(self):
    #     return "Activity()"
    #
    # def __str__(self):
    #      r = self._related
    #      # for item in r.keys():
    #      return "to %s take %s " %(r.keys(),r.get(r.keys()))


class Graph:
    def __init__(self, graph_dict=None):
            if graph_dict is None:
                graph_dict = {}
            self.__graph_dict = graph_dict

    def __str__(self):
         r = self.__graph_dict
         for item in r.keys():
            return "to %s take %s " % (r.keys(), r.values())

    def get_weeks(self):
        return self.values()

    def printG(self,graph):
        gr = self.__graph_dict
        for i in gr:
             for j in gr.get(i).get_related().values():
                print("Activity", i, "takes", j, "weeks")

    def addActivity(self,number,activity):
        gr =self.__graph_dict
        for i in gr:
            for item in activity.get_related().keys():
                if i == item:
                    gr.get(i).setR(activity)
                    gr.update({number:activity})
                    return

    def return_activity2(self, number):
        gr = self.__graph_dict
        count = 1
        for item in gr.values():
            if count > gr.__len__():
                return None
            if number in  item.get_related().keys():
                return count
            count = count + 1

    def return_activity(self, number):
        gr = self.__graph_dict
        count=1
        for item in gr.values():
            if count>gr.__len__():
                return None
            if number.get_related() == item.get_related():
                return count
            count = count + 1
    #
    def returnValue(self,x):
        gr = self.__graph_dict
        for i in gr:
            for item in gr.values():
                if item == x:
                    return i

    def returnValues2(self, x,y):
        gr = self.__graph_dict
        count = 1
        for i in gr.values():
            for item in i.get_related().keys():
                if count == x and y in i.get_related().keys():
                    return self.getNumber(i.get_related(),y)
            count+=1
    def getNumber(self,x,y):
            for item in x.keys():
                if item == y:
                    z=x.get(item)
                    return z
    def returnValues(self,x):
        gr = self.__graph_dict
        for i in gr.values():
            for item in i.get_related().keys():
                if item == x:
                    y=self.returnNumber(i.get_related().values())
                    return self.returnNumber(i.get_related().values())

    def returnNumber(self, number):
            for i in number:
                return i

    def slacks_time(self, start_vertex, end_vertex):
        gr=self.__graph_dict
        sum=0
        maxSum=0
        while (end_vertex != start_vertex and end_vertex != None or end_vertex != 1):
            numOfSplits= graph.counterN(end_vertex)
            if(numOfSplits.__len__()>1):
                counter = numOfSplits.__len__()
                for i in numOfSplits:
                            counter-=1
                            sum += self.returnValues2(i,end_vertex)
                            sum= self.slacks_time2(1, i,sum)
                            if sum>maxSum:
                              maxSum = sum
                              sum = 0
                              if counter == 0:
                                  return maxSum
            else:
                   sum += self.returnValues2(self.returnNumber(numOfSplits), end_vertex)
                   end_vertex = self.return_activity2(end_vertex)
        return max(maxSum,sum)

    def slacks_time2(self, start_vertex, end_vertex,sum):
        gr=self.__graph_dict
        while (end_vertex != start_vertex and end_vertex != None or end_vertex != 1):
            if (end_vertex == start_vertex and end_vertex == None or end_vertex == 1):
                  return sum
            numOfSplits = graph.counterN(end_vertex)
            if (numOfSplits.__len__() > 1):
                  for i in numOfSplits:
                       sum += self.returnValues(i)  # .get_related().values()
                       sum += self.slacks_time2(1, i,sum)
            else:
                        sum += self.returnValues(end_vertex)  # .get_related().values()
                        end_vertex = self.return_activity2(end_vertex)
        return sum

    def counterN(self,number):
        allSplits=[]
        gr = self.__graph_dict
        for i in gr.values():
            for item in i.get_related().keys():
                if item == number:
                    allSplits.append(graph.return_activity(i))
        return allSplits

    def find_isolated_activities(self):
        gr = self.__graph_dict
        counter = 1
        for i in gr.values():
            # for item in i.get_related():
                # print("asd: ", i.get_related())
            if len(i.get_related()) == 0:
                return counter
            counter += 1




if __name__ == '__main__':
        activity1 = Activity({2: 6}, "Activity 1")
        activity2 = Activity({3: 4, 4: 3, 6: 6}, "Activity 2")
        activity3 = Activity({5: 2}, "Activity 3")
        activity4 = Activity({9: 4}, "Activity 4")
        activity5 = Activity({6: 3}, "Activity 5")
        activity6 = Activity({7: 2, 8: 4}, "Activity 6")
        activity7 = Activity({11: 4}, "Activity 7")
        activity8 = Activity({11: 1}, "Activity 8")
        activity9 = Activity({10: 1}, "Activity 9")
        activity10 = Activity({11: 4}, "Activity 10")
        activity11 = Activity(None, "Activity 11")

        g = {1: activity1, 2: activity2, 3: activity3, 4: activity4, 5: activity5, 6: activity6, 7: activity7,
             8: activity8, 9: activity9, 10: activity10, 11: activity11}
        graph = Graph(g)
        graph.printG(g)
        print("""All pathes from "1" to "6":""")
        print(graph.slacks_time(1, 6))
        print("""All pathes from "1" to "10":""")
        print(graph.slacks_time(1, 10))

        count =g.__len__()+1

        # newActivity =Activity({11:4,4:2})
        #
        # graph.addActivity(12,newActivity)
        # print(count)

        print("The isolated activities are: ")
        print(graph.find_isolated_activities())