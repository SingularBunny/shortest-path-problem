import unittest

from pythonds import Graph

from thorup.algs.mstalgorithm import KruskalMstAlgorithm
from thorup.algs.thorup import ThorupModel
from thorup.util.graphgenerator import RandomGraphGenerator


class TestFindPass(unittest.TestCase):
    def test_model(self):
        number_of_vertices, maximum_edge_weight, edges_per_vertex = (10, 10, 3)
        # graph = RandomGraphGenerator.generate_connected_weighted_undirected_graph(number_of_vertices,
        #                                                                     maximum_edge_weight,
        #                                                                     edges_per_vertex)

        graph = Graph()
        graph.addEdge(0, 1, 1)
        graph.addEdge(1, 0, 1)
        graph.addEdge(0, 2, 2)
        graph.addEdge(2, 0, 2)


        thorup = ThorupModel(graph)

        thorup.construct_minimum_spanning_tree(KruskalMstAlgorithm)
        thorup.construct_other_data_structures()
        result = thorup.find_shortest_paths(0)
        self.assertEquals([0,1,2], result)

if __name__ == '__main__':
    unittest.main()