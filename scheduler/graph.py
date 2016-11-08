from itertools import permutations

from models import Course, Student

import networkx as nx


class CoursesGraph(object):

    def __init__(self):
        """
        Initializes the graph students, courses and their relations (
        edeges weights)
        """
        self.graph = nx.Graph()

        self.courses = Course.objects.all()
        self.students = Student.objects.all()

        self._initialize_nodes()
        self._create_weighted_edges()

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

    def _create_weighted_edges(self):
        """
        Iterates over each student and add an edge between her
        courses or increase the weight of the edge if an edge
        already exists.
        """
        for student in self.students:
            student_courses = student.courses.all()

            # permutations of 2 for every course in student's schedule
            courses_permutations = permutations(student_courses, 2)

            for source, dist in courses_permutations:
                if self.graph.has_edge(source, dist):
                    self.graph[source][dist]['weight'] += 1
                else:
                    self.graph.add_edge(source, dist, weight=1)
