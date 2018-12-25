import sys
from abc import ABC

from pythonds import Graph

from thorup.ds.edge import Edge
from thorup.ds.ufstructure import UnionFindNode, UnionFindStructureTarjan

MAXIMUM_EDGE_WEIGHT = sys.maxsize


class MstAlgorithm(ABC):
    """
    An algorithm for the computation of minimum spanning trees.
    """
    @staticmethod
    def spawn_tree(source_graph: Graph) -> Graph:
        raise NotImplementedError()


class KruskalMstAlgorithm(MstAlgorithm):
    """
     Modified version of Kruskal's algorithm for the computation of msb-minimum spanning trees.
    """

    @staticmethod
    def spawn_tree(source_graph: Graph) -> Graph:
        union_find_nodes = [UnionFindNode(i) for i in range(source_graph.numVertices)]
        sorted_edges = KruskalMstAlgorithm.sorts_edges_by_weights(source_graph)
        msb_minimum_spanning_tree = Graph()

        while sorted_edges:  # msb_minimum_spanning_tree.numVertices < ((source_graph.numVertices - 1) * 2):
            edge = sorted_edges.pop(0)

            source_id = UnionFindStructureTarjan\
                .find(union_find_nodes[edge.source]).item
            target_id = UnionFindStructureTarjan\
                .find(union_find_nodes[edge.target]).item

            if source_id != target_id:
                msb_minimum_spanning_tree.addEdge(source_id, target_id, edge.weight)
                msb_minimum_spanning_tree.addEdge(target_id, source_id, edge.weight)
                UnionFindStructureTarjan.union(union_find_nodes[source_id],
                                               union_find_nodes[target_id])

        return msb_minimum_spanning_tree

    @staticmethod
    def sorts_edges_by_weights(graph: Graph) -> list:
        buckets = [[] for _ in range(get_most_significant_bit(MAXIMUM_EDGE_WEIGHT))]

        for vertex in graph:
            for neighbor in vertex.getConnections():
                if vertex.getId() < neighbor.getId():
                    buckets[get_most_significant_bit(vertex.getWeight(neighbor))]\
                        .append(Edge(vertex.getId(), neighbor.getId(), vertex.getWeight(neighbor)))

        return [edge for bucket in buckets for edge in bucket]


def get_most_significant_bit(x: int) -> int:
    return x.bit_length() - 1
