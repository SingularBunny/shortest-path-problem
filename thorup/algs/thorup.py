import sys
from math import ceil
from typing import List

from pythonds import Graph

from thorup.algs.mstalgorithm import MstAlgorithm, get_most_significant_bit, MAXIMUM_EDGE_WEIGHT, KruskalMstAlgorithm
from thorup.ds.componenttree import ComponentTree, ComponentTreeNode
from thorup.ds.edge import Edge
from thorup.ds.splitfindmin import SplitFindminStructureGabow
from thorup.ds.ufstructure import UnionFindNode, UnionFindStructureTarjan
from thorup.ds.unvisited import UnvisitedDataStructure


class ThorupModel(object):
    """
    An implementation of Thorup's single-source shortest paths
    algorithm.
    """

    def __init__(self, source_graph: Graph) -> None:
        super().__init__()
        self.source_vertex: int = None
        self.source_graph: Graph = source_graph
        self.visited_vertices: List[bool] = [False] * source_graph.numVertices
        self.msb_minimum_spanning_tree: Graph = None
        self.component_tree: ComponentTree = None
        self.unvisited_data_structure: UnvisitedDataStructure = None

    def construct_minimum_spanning_tree(self, msb_minimum_spanning_tree_algorithm: MstAlgorithm) -> None:
        self.msb_minimum_spanning_tree = msb_minimum_spanning_tree_algorithm.spawn_tree(self.source_graph)

    def construct_other_data_structures(self) -> None:
        self.component_tree = self.construct_component_tree()
        self.unvisited_data_structure = UnvisitedDataStructure(self.source_graph.numVertices,
                                        self.component_tree)

    def construct_component_tree(self):
        """
        Constructing the component tree (Algorithm G).
        :return: component tree
        """
        uf = UnionFindStructureTarjan()
        uf_nodes = [UnionFindNode(i) for i in range(self.source_graph.numVertices)]
        eis = KruskalMstAlgorithm.sorts_edges_by_weights(self.msb_minimum_spanning_tree)

        c = [0 for _ in range(self.source_graph.numVertices)]
        s = [0 for _ in range(self.source_graph.numVertices)]
        component_tree = ComponentTree(self.source_graph.numVertices)

        new_c = [0 for _ in range(self.source_graph.numVertices)]
        represents_internal_node = [False for _ in range(self.source_graph.numVertices)]

        # G.1.
        for v in range(self.source_graph.numVertices):
            c[v] = v
            s[v] = 0

        # G.2.
        comp = 0
        x = set()

        # G.3.
        for i in range(len(eis) - 1):
            # G.3.1.
            ei = eis[i]

            # G.3.2.
            x.add(uf.find(uf_nodes[ei.source]).item)
            x.add(uf.find(uf_nodes[ei.target]).item)

            # G.3.3.
            new_s = s[uf.find(uf_nodes[ei.source]).item] + \
                    s[uf.find(uf_nodes[ei.target]).item] + \
                    ei.weight

            # G.3.4.
            uf.union(uf_nodes[ei.source], uf_nodes[ei.target])

            # G.3.5.
            s[uf.find(uf_nodes[ei.source]).item] = new_s

            # G.3.6.
            if get_most_significant_bit(ei.weight) < get_most_significant_bit(eis[i + 1].weight):
                # G.3.6.1.
                new_x = set()
                for v in x:
                    new_x.add(uf.find(uf_nodes[v]).item)

                # G.3.6.2.
                for v in new_x:
                    comp += 1
                    new_c[v] = comp

                # G.3.6.3.
                for v in x:
                    if not represents_internal_node[v]:
                        component_tree.set_parent_of_leaf(c[v], new_c[uf.find(uf_nodes[v]).item])
                    else:
                        component_tree.set_parent_of_internal_node(c[v], new_c[uf.find(uf_nodes[v]).item])

                # G.3.6.4
                for v in new_x:
                    c[v] = new_c[v]
                    represents_internal_node[v] = True
                    component_tree \
                        .set_buckets_internal_node_number(c[v], int(ceil(
                        s[v] / pow(2, get_most_significant_bit(ei.weight)))))
                    component_tree.set_component_hierarchy_level(c[v],
                                                                      get_most_significant_bit(ei.weight) + 1)
                # G.3.6.5
                x.clear()

        i = len(eis) - 1

        # G.3.1.
        ei = eis[i]

        # G.3.2.
        x.add(uf.find(uf_nodes[ei.source]).item)
        x.add(uf.find(uf_nodes[ei.target]).item)

        # G.3.4.
        uf.union(uf_nodes[ei.source], uf_nodes[ei.target])

        # G.3.6.
        if get_most_significant_bit(ei.weight) < get_most_significant_bit(sys.maxsize):
            # G.3.6.1.
            new_x = set()
            for v in x:
                new_x.add(uf.find(uf_nodes[v]).item)

            # G.3.6.2.
            for v in new_x:
                comp += 1
                new_c[v] = comp

            # G.3.6.3.
            for v in x:
                if not represents_internal_node[v]:
                    component_tree.set_parent_of_leaf(c[v], new_c[uf.find(uf_nodes[v]).item])
                else:
                    component_tree.set_parent_of_internal_node(c[v], new_c[uf.find(uf_nodes[v]).item])

            # G.3.6.4
            for v in new_x:
                c[v] = new_c[v]
                represents_internal_node[v] = True
                component_tree \
                    .set_buckets_internal_node_number(c[v], int(ceil(
                    s[v] / pow(2, get_most_significant_bit(ei.weight)))))
                component_tree.set_component_hierarchy_level(c[v],
                                                                  get_most_significant_bit(ei.weight) + 1)
            # G.3.6.5
            x.clear()

        return component_tree

    def find_shortest_paths(self, source_vertex: int) -> List[int]:
        if source_vertex < 0 or source_vertex >= self.source_graph.numVertices:
            raise AttributeError('{} is no valid source vertex.'.format(str(source_vertex)))

        # B.1.
        self.source_vertex = source_vertex
        self.visited_vertices[source_vertex] = True

        for vertex, weight in self.source_graph.getVertex(source_vertex).connectedTo.items():
            self.unvisited_data_structure.decreases_super_distance(vertex.getId(), weight)

        # B.3.
        self.visit_node(self.component_tree.root)

        # B.4.
        d = [0] * self.source_graph.numVertices

        for i in range(self.source_graph.numVertices):
            d[i] = self.unvisited_data_structure.get_super_distance(i)

        # B.2.
        d[source_vertex] = 0

        return d

    def expand(self, node: ComponentTreeNode) -> None:
        node.lowest_bucket_index = self.unvisited_data_structure.get_min_dvi_minus(node) >> (node.component_hierarchy_level -1)
        node.highest_bucket_index = node.lowest_bucket_index + node.delta

        node.initialize_buckets()
        self.unvisited_data_structure.delete_root(node)

        for wh in node.children:
            minimum = self.unvisited_data_structure.get_min_dvi_minus(wh)

            if minimum != -1:
                if wh.children or not wh.index == self.source_vertex:
                    node.inserts_tree_node_to_bucket_by_index(wh, minimum >> (node.component_hierarchy_level - 1))
                else:
                    current = node

                    while current is not None:
                        current.unvisited_vertices_number -= 1
                        current = current.parent

        node.visited = True

    def visit(self, vertex: int) -> None:
        if vertex != self.source_vertex:
            self.visited_vertices[vertex] = True
            for vrtx, weight in self.source_graph.getVertex(vertex).connectedTo.items():
                new_d_value = self.unvisited_data_structure.get_super_distance(vertex) + weight

                if new_d_value > 0 and new_d_value < self.unvisited_data_structure.get_super_distance(vrtx.getId()):
                    wh = self.unvisited_data_structure.get_unvisited_root(self.component_tree, vrtx.getId())
                    wi = wh.parent

                    old_value = self.unvisited_data_structure.get_min_dvi_minus(wh) >> (wi.index - 1)
                    self.unvisited_data_structure.decreases_super_distance(vrtx.getId(), new_d_value)
                    new_value = self.unvisited_data_structure.get_min_dvi_minus(wh) >> (wi.index - 1)

                    if old_value == -1 or new_value < old_value:
                        wh.move_to_bucket(wi, self.unvisited_data_structure.get_min_dvi_minus(wh) >> (wi.index - 1))

    def visit_node(self, vi: ComponentTreeNode) -> None:
        vj = vi.parent
        j = None

        if vj is None:
            j = get_most_significant_bit(sys.maxsize)
        else:
            j = vj.component_hierarchy_level

        # F.1.
        if vi.component_hierarchy_level == 0:
            # F.1.1.
            self.visit(vi.index)

            current = vi.parent
            while current is not None:
                current.unvisited_vertices_number -= 1
                current = current.parent

            # F.1.2.
            vi.remove_from_parent_bucket()

            # F.1.3.
            return


        # F.2
        if not vi.visited:
            self.expand(vi)
            vi.next_bucket_index = vi.lowest_bucket_index

        # F.3
        old_shifted_index = vi.next_bucket_index >> (j - vi.component_hierarchy_level)

        while vi.unvisited_vertices_number > 0 and (vi.next_bucket_index >> (j - vi.component_hierarchy_level)) == old_shifted_index:
            # F.3.1.
            while vi.get_bucket(vi.next_bucket_index):
                # F.3.1.1.
                wh = vi.get_bucket(vi.next_bucket_index)[0]

                # F.3.1.2.
                self.visit_node(wh)

            # F.3.2.
            vi.next_bucket_index += 1

        # F.4.
        if vi.unvisited_vertices_number > 0:
            vi.move_to_bucket(vj, vj.next_bucket_index >> (j - vi.component_hierarchy_level))
        else:
            #F.5.
            if vi.parent is not None:
                vi.remove_from_parent_bucket()

    def clean_up_between_queries(self):
        sf = SplitFindminStructureGabow(self.source_graph.numVertices, self.source_graph.numVertices)
        self.visited_vertices = []
        self.deep_clean_up_nodes(self.component_tree.root)
        self.unvisited_data_structure.containers = []

        for i in range(self.source_graph.numVertices):
            self.unvisited_data_structure[i] = sf.add(i, float("inf"))

        sf.initialize_head()

    def deep_clean_up_nodes(self, node: ComponentTreeNode) -> None:
        node.unvisited_vertices_number = node.unvisited_vertices_initial_number
        node.visited = False

        for child in node.children:
            self.deep_clean_up_nodes(child)
