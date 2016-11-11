import itertools
import operator

from models import Course, Student, ScheduleConfig

import networkx as nx


class CoursesGraph(object):

    def __init__(self):
        """
        Initializes the graph students, courses, their relations (
        edges weights), and initial scheduling configurations
        """
        self.graph = nx.Graph()

        self.courses = Course.objects.all()
        self.students = Student.objects.all()
        self.schedule_configs = ScheduleConfig.objects.get(id=1)

        self._initialize_nodes()
        self._initialize_colors()
        self._create_weighted_edges()

        self._schedule()

    def node_degree(self, node):
        """
        :return: a node degree in the graph
        """
        return self.graph.degree(node)

    def nodes_degree(self):
        """
        :return: a list of every node degree in the graph
        """
        return self.graph.degree()

    def _initialize_nodes(self):
        """
        Create a node from each course in the graph.

        TODO: Mark nodes from user selected courses
        TODO: Check if it is good to store a course as node in terms
              of space.
        """
        self.graph.add_nodes_from(self.courses)

    def _initialize_colors(self):
        """
        The coloring scheme for the problem uses a double indexed
        color R[i][j], where the index (i) represents the day of the
        exam and (j) represents the exam time slot on a given day.

        - The range of (j), i.e., the number of exam time slots is
          determined by the registrar and/or the faculty
        - The range of the index (i) is a parameter generated as an
          outcome by the algorithm
        :return:
        """

    def _create_weighted_edges(self):
        """
        Iterates over each student and add an edge between her
        courses or increase the weight of the edge if an edge
        already exists.
        """
        for student in self.students:
            student_courses = student.courses.all()

            # permutations of 2 for every course in student's schedule
            courses_permutations = \
                itertools.permutations(student_courses, 2)

            for source, dist in courses_permutations:
                if self.graph.has_edge(source, dist):
                    self.graph[source][dist]['weight'] += 1
                else:
                    self.graph.add_edge(source, dist, weight=1)

    def _sort_bunch(self, full_list, start, end):
        """
        Sorts a bunch of nodes using the weight criteria.

        :param full_list: The list we want to sort its nodes
        :param start: The start index
        :param end: The end position (last index + 1)

        :return: Nothing since list object in python are mutable
        """
        partial = full_list[start:end]

        sorted_chunk = sorted(
            self.graph.degree_iter(nbunch=partial, weight='weight'),
            key=operator.itemgetter(1),
            reverse=True
        )

        full_list[start:end] = [c for c, _ in sorted_chunk]

    def _sort_graph(self):
        """
        - Sorts the nodes in the weight matrix in a descending order
          based on the degree of nodes.
        - Nodes with similar degrees are ordered based on the
          largest weight w in its adjacency list.
        - Nodes with similar degrees d and weights w are ordered based
          on their node ID (smallest ID first).

        :return: A list of sorted nodes
        """

        # Sort in a descending order based on the degree of the nodes
        sorted_nodes_degree = sorted(
            self.graph.degree_iter(),
            key=operator.itemgetter(1),
            reverse=True
        )
        # The original result will be: (Course, x) while x is the degree
        # I want to keep the courses only in the list
        sorted_nodes = [course for course, _ in sorted_nodes_degree]

        # Nodes with similar degrees are ordered based on the largest
        # weight w in its adjacency list.
        start = 0
        similar_degrees = 0
        for i, (node, degree) in enumerate(sorted_nodes_degree):
            # If the current degree equals the previous one
            if i > -1 and degree == sorted_nodes_degree[i-1][1]:
                # Increment the similar degrees and set the start
                # index to i-1 if it's the first similar degree
                similar_degrees += 1
                if similar_degrees == 1:
                    start = i-1
            # If the previous check failed and there are similar degrees
            elif similar_degrees > 0:
                # export the end position and reset the similar degrees
                end = start + similar_degrees + 1
                similar_degrees = 0

                # And also sort the bunch of founded nodes. No need
                # to assign a list back because lists in python are
                # mutable
                self._sort_bunch(sorted_nodes, start, end)

        return sorted_nodes

    def _schedule(self):
        """
        :return:
        """
        sorted_nodes = self._sort_graph()
        colored_courses = []

        for i, course in enumerate(sorted_nodes):  # Begin1
            if len(colored_courses) == len(self.graph):
                # exit the loop and finish
                break

            if course not in colored_courses: #Begin 2
                if i == 0:  # Begin 3
                    pass
