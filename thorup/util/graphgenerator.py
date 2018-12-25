from random import choices, randrange

from pythonds import Graph


class RandomGraphGenerator(object):

    @staticmethod
    def generate_connected_weighted_undirected_graph(number_of_vertices: int,
                                                     maximum_edge_weight: int,
                                                     edges_per_vertex: int):
        graph = Graph()

        indexes = [index for index in range(number_of_vertices)]

        for index in indexes:
            for neighbor_vertex_index in choices(indexes, k=randrange(1, min(number_of_vertices, edges_per_vertex))):
                graph.addEdge(index, neighbor_vertex_index, randrange(1, maximum_edge_weight))
                graph.addEdge(neighbor_vertex_index, index, randrange(1, maximum_edge_weight))

        return graph
