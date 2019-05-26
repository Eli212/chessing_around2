# Majdi Abu Salah - 311468326
# Eli Bunimovich - 312474786


maxSum = 0
critical_path = []

maxSum_copy = 0
critical_path_copy = []

class Activity:
    def __init__(self, name, related=None):
        if related is None:
            related = {}
        self._related = related
        self.name = name

    def get_related(self):
        return self._related

    def get_name(self):
        return self.name

    def update_related(self, valuee):
        self._related.update(valuee)

    def print_activity_descending(self):
        arr = []
        for i in self.get_related().values():
            arr.append(i)
        arr.sort(reverse=True)
        return arr

    def sum_all_slacks_activity(self):
        sum = 0
        for i in self.get_related().values():
            sum += i
        return sum

    def max_slacks_activity(self):
        return max(self.get_related().values()) if self.get_related() else 0

    def __str__(self):
        most_weeks = 0
        if self.get_related() is not None:
            for activity in self._related.values():
                if activity > most_weeks:
                    most_weeks = activity
            return self.name + " takes " + repr(most_weeks) + " weeks"
            # return str


class Graph:
    def __init__(self, graph_dict=None):
            if graph_dict is None:
                graph_dict = {}
            self.__graph_dict = graph_dict
            self.__paths_list_EE = []
            self.__paths_list_LE = []
            self.next_iter = 0

    def get_graph_dict(self):
        return self.__graph_dict

    def add_activity(self, number, activity):
        self.__graph_dict.update({number: activity})
        return

    def find_isolated_activities(self):
        isolated_activities = []
        for activity in self.__graph_dict.values():
            if len(activity.get_related()) == 0:
                isolated_activities.append(activity)
        return isolated_activities

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start to
            end in graph """
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex].get_related():
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,
                                                     end_vertex,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
        return paths

    def slacks_time(self):
        paths_start_to_end = self.find_all_paths(list(self.__graph_dict.keys())[0], list(self.__graph_dict.keys())[-1])
        original_path_list = []
        for path in paths_start_to_end:
            temp = {}
            temp_for_original = {}
            last_slack = 0
            for node in path:
                temp[node] = last_slack
                for k, v in self.__graph_dict[node].get_related().items():
                    if k in path:
                        temp_for_original[k] = v
                        temp[k] = last_slack + v
                        last_slack = temp[k]
                        break
            original_path_list.append(temp_for_original)
            self.__paths_list_EE.append(temp)
        critical_value = 0
        for path in self.__paths_list_EE:
            if list(path.keys())[-1] > critical_value:
                critical_value = list(path.values())[-1]

        self.__paths_list_LE = self.__paths_list_EE[:]

        sum_arr = []
        for index in range(len(self.__paths_list_LE)):
            temp_arr = {len(self.__graph_dict): critical_value}
            temp_num = critical_value
            # counter = len(self.__paths_list_LE[index].keys()) - 1
            keys = list(self.__paths_list_LE[index].keys()).copy()
            keys.reverse()
            for key in range(0, len(keys) - 1, 1):
                # print(original_path_list[index])
                if keys[key] in original_path_list[index]:
                    temp_num -= original_path_list[index][keys[key]]
                    temp_arr.update({keys[key+1]: temp_num})
            sum_arr.append(temp_arr)

        EE_dict = {}
        for i in range(1, len(self.__graph_dict) + 1, 1):
            min = critical_value
            for j in range(0, len(temp_arr), 1):
                if i in list(sum_arr[j].keys()) and sum_arr[j].get(i) < min:
                    min = sum_arr[j].get(i)
            EE_dict.update({i: min})

        LE_dict = {}
        for path in self.__paths_list_LE:
            for node in path.keys():
                if node in LE_dict:
                    LE_dict[node] = max(LE_dict[node], path[node])
                else:
                    LE_dict[node] = path[node]

        slacks = {}
        for i in range(1, len(LE_dict) + 1, 1):
            slacks.update({i: EE_dict.get(i) - LE_dict.get(i)})

        return slacks

    def sum_all_slacks(self, slacks):
        sum = 0
        for activity in slacks.values():
            sum += activity
        return sum

    def __str__(self):
        str = "This graph has " + repr(len(self.__graph_dict)) + " activities:\n"
        # print("This graph has", len(self.__graph_dict), "activities")
        for activity in self.__graph_dict.values():
            str += repr(activity.__str__())
            str += "\n"
        return str

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_iter <= len(self.__graph_dict):
            self.next_iter += 1
            return self.__graph_dict.get(self.next_iter - 1)
        else:
            raise StopIteration

    def get_critical_path(self):
        global maxSum
        global critical_path
        global critical_paths

        maxSum = 0
        critical_path = []
        critical_paths = []

        self.recursive_critical_path(len(self.__graph_dict), 0, 0, [], len(self.__graph_dict), [])
        critical_path.append(1)
        critical_path.reverse()

    def recursive_critical_path(self, start, end, sum, cr_path, search, dont_search_in):
        global maxSum
        global critical_path

        for i in range(start, end, -1):
            # self.__graph_dict.get(i + 1).__str__()
            # print(i)
            for activity in self.__graph_dict.get(i).get_related().keys():
                if activity == search and activity not in dont_search_in:
                    cr_copy = cr_path.copy()
                    cr_copy.append(activity)
                    dont_search_in_copy = dont_search_in.copy()
                    dont_search_in_copy.append(activity)
                    critical_paths.append(cr_path)
                    self.recursive_critical_path(start, end, sum + self.__graph_dict.get(i).get_related().get(activity),
                                                 cr_copy, i, dont_search_in_copy)
        if sum > maxSum:
            maxSum = sum
            critical_path = cr_path

    def recursive_critical_path_copy(self, start, end, sum, cr_path, search, dont_search_in, graph):
        global maxSum_copy
        global critical_path_copy

        for i in range(start, end, -1):
            # self.__graph_dict.get(i + 1).__str__()
            # print(i)
            for activity in graph.get(i).get_related().keys():
                if activity == search and activity not in dont_search_in:
                    cr_copy = cr_path.copy()
                    cr_copy.append(activity)
                    dont_search_in_copy = dont_search_in.copy()
                    dont_search_in_copy.append(activity)
                    # critical_path_copy.append(cr_path)
                    self.recursive_critical_path_copy(start, end, sum + graph.get(i).get_related().get(activity),
                                                 cr_copy, i, dont_search_in_copy, graph)
        if sum > maxSum_copy:
            maxSum_copy = sum
            critical_path_copy = cr_path

    def q9(self):
        global maxSum_copy
        global critical_path_copy

        graph_copy = self.__graph_dict.copy()
        perfect = {}
        for i in range(0, len(critical_path) - 1, 1):
            breaks_cr = False
            while graph_copy.get(critical_path[i]).get_related().get(critical_path[i+1]) > 1 and breaks_cr is False:
                graph_copy.get(critical_path[i]).update_related({critical_path[i+1]: graph_copy.get(critical_path[i])
                                                                .get_related().get(critical_path[i+1]) - 1})

                maxSum_copy = 0
                critical_path_copy = []

                self.recursive_critical_path_copy(len(graph_copy), 0, 0, [], len(graph_copy), [], graph_copy)
                critical_path_copy.append(1)
                critical_path_copy.reverse()

                if critical_path_copy != critical_path:
                    breaks_cr = True
                    graph_copy.get(critical_path[i]).update_related({critical_path[i + 1]: graph_copy
                                                                    .get(critical_path[i]).get_related()
                                                                    .get(critical_path[i + 1]) + 1})
                    # perfect[critical_path[i]] = graph_copy.get(critical_path[i]).get_related().get(critical_path[i+1])
            perfect[critical_path[i]] = graph_copy.get(critical_path[i]).get_related().get(critical_path[i + 1])
        return perfect

    #
    #
    #

if __name__ == '__main__':
        # Question 1 + 2
        my_graph = Graph()
        # This is the 1st Graph in the homework file
        my_graph.add_activity(1, Activity("Activity 1", {2: 6}))
        my_graph.add_activity(2, Activity("Activity 2", {3: 4, 4: 3, 6: 6}))
        my_graph.add_activity(3, Activity("Activity 3", {5: 2}))
        my_graph.add_activity(4, Activity("Activity 4", {9: 4}))
        my_graph.add_activity(5, Activity("Activity 5", {6: 3}))
        my_graph.add_activity(6, Activity("Activity 6", {7: 2, 8: 4}))
        my_graph.add_activity(7, Activity("Activity 7", {11: 4}))
        my_graph.add_activity(8, Activity("Activity 8", {11: 1}))
        my_graph.add_activity(9, Activity("Activity 9", {10: 1}))
        my_graph.add_activity(10, Activity("Activity 10", {11: 4}))
        my_graph.add_activity(11, Activity("Activity 11", None))

        # This is the 3rd Graph in the homework file
        # my_graph.add_activity(1, Activity("Activity 1", {2: 4, 3: 6, 4: 5}))
        # my_graph.add_activity(2, Activity("Activity 2", {3: 0}))
        # my_graph.add_activity(3, Activity("Activity 3", {5: 2}))
        # my_graph.add_activity(4, Activity("Activity 4", {6: 4}))
        # my_graph.add_activity(5, Activity("Activity 5", {4: 0, 6: 0, 7: 5, 8: 2, 9: 8}))
        # my_graph.add_activity(6, Activity("Activity 6", {9: 6}))
        # my_graph.add_activity(7, Activity("Activity 7", {6: 0, 9: 5}))
        # my_graph.add_activity(8, Activity("Activity 8", {9: 0}))
        # my_graph.add_activity(9, Activity("Activity 9", None))


        # Question 3 - Isolated Activities
        print("The isolated activities are: ")
        for activity in my_graph.find_isolated_activities():
            print(activity.get_name())

        # Question 4
        slacks = my_graph.slacks_time()
        print(slacks)

        # Question 5
        print("Sum of all slacks: ", my_graph.sum_all_slacks(slacks))

        # Question 6
        my_graph.__str__()

        # Question 7
        for activity in my_graph:
            activity.__str__()

        # Question 8
        my_graph.get_critical_path()
        print("Critical path is:", critical_path, "Time:", maxSum, "weeks")

        # Question 9
        print(my_graph.q9())
