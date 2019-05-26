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

    def print_graph_descending(self):
        for activity in self.__graph_dict.values():
            print(activity.get_name(), activity.print_activity_descending())

    def sum_all_slacks(self):
        sum = 0
        for activity in self.__graph_dict.values():
            sum += activity.sum_all_slacks_activity()
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
        my_graph.print_graph_descending()

        # Question 5
        print("Sum of all slacks: ", my_graph.sum_all_slacks())

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