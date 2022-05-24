from collections import defaultdict
from operator import itemgetter


class GraphIterator(object):
    def __init__(self, adj_list):
        self.idx = 0
        self.adj_list = adj_list

    def __iter__(self):
        return self

    def __next__(self):
        """
        This will iterate the keys, which is good for now. We should
        extend this function if we want to iterate the values as well.
        """
        idx = self.idx

        if idx is None or idx >= len(self.adj_list):
            # once we reach the end, all iteration is done, end of.
            self.idx = None
            raise StopIteration()

        value = list(self.adj_list)[idx]
        self.idx = idx + 1
        return value


class Graph(object):
    """
    An adjacency list is the most efficient way to store a graph. It allows
    us to store only edges that are present in a graph.

    The adjacency list takes only n+e elements (n is the number of nodes, e is the
    number of edges).
    The implementation becomes more space-efficient if a graph is not dense (has a
    small number of edges).
    """

    def __init__(self, directed=True):
        self.directed = directed
        self.adj_list = defaultdict(set)

    def add_edge(self, source, destination, weight=1):
        if self.contains_edge(source, destination):
            raise ValueError(f"Edge between ({source}, {destination}) already exists")

        self.adj_list[source].add((destination, weight))

        if not self.directed:
            self.adj_list[destination].add((source, weight))

        return weight

    def contains_edge(self, source, destination):
        # Instant lookup
        if source not in self.adj_list:
            return False

        if not self.directed and destination not in self.adj_list:
            return False

        return self._get_info(source, destination) is not None

    def get_weight(self, source, destination):
        if not self.contains_edge(source, destination):
            return None

        _, weight = self._get_info(source, destination)
        return weight

    def _find_and_set_weight(self, source, destination, weight):
        for node, old_weight in self.adj_list.get(source, set()):
            if node == destination:
                self.adj_list[source].remove((destination, old_weight))
                self.adj_list[source].add((destination, weight))
                return weight

    def set_weight(self, source, destination, weight):
        if not self.contains_edge(source, destination):
            raise ValueError(f"Edge ({source}, {destination}) does not exist in graph.")

        weight = self._find_and_set_weight(source, destination, weight)

        if not self.directed:
            weight_2 = self._find_and_set_weight(destination, source, weight)

            if weight != weight_2:
                raise RuntimeError(
                    f"Something wrong happened processing set_weight in "
                    f"undirected graph: ({source}, {destination}, {weight})."
                )

        return weight

    def get_degree(self, node):
        return len(self.adj_list[node])

    def get_largest_weight(self, node):
        weight = 0
        try:
            weight = max(self.adj_list[node], key=itemgetter(1))[1]
        except ValueError:
            pass

        return weight

    def get_adjacency_list(self, node):
        return self.adj_list[node]

    def _get_info(self, source, destination):
        for node, weight in self.adj_list.get(source):
            if node == destination:
                return (node, weight)

        return None

    def __str__(self):
        output = ""
        for node in self.adj_list.keys():
            output += f"node {node}: {self.adj_list[node]} \n"

        return output

    def __repr__(self) -> str:
        return f"<Graph: {id(self)} nodes={len(self)}>"

    def __len__(self):
        return len(self.adj_list)

    def __iter__(self):
        return GraphIterator(self.adj_list)
