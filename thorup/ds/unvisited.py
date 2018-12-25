from typing import List

from thorup.ds.componenttree import ComponentTree, ComponentTreeNode
from thorup.ds.splitfindmin import SplitFindminStructureGabow, Element


class UnvisitedDataStructure:
    """
    Unvisited data structure used by Thorup's algorithm
    for maintaining the chaning set of roots of a component tree.
    """

    def __init__(self, vertices_number: int, component_tree: ComponentTree) -> None:
        super().__init__()
        self.vertex_index: List[int] = [None for _ in range(vertices_number)]
        self.containers: List[Element[int]] = [None for _ in range(vertices_number)]

        self.initialize_mapping(component_tree.root, 0)
        self.split_findmin_structure = SplitFindminStructureGabow(vertices_number, vertices_number)

        for i in range(vertices_number):
            self.containers[i] = self.split_findmin_structure.add(i, float("inf"))

        self.split_findmin_structure.initialize_head()

    def get_min_dvi_minus(self, node: ComponentTreeNode) -> int:
        cost = self.containers[node.maximum_unvisited_vertex_index].get_list_cost()
        return -1 if cost == float("inf") else cost

    def decreases_super_distance(self, vertex_index: int, new_lower_super_distance) -> None:
        self.containers[self.vertex_index[vertex_index]].decrease_cost(new_lower_super_distance)

    def get_super_distance(self, vertex_index: int) -> int:
        return int(self.containers[self.vertex_index[vertex_index]].cost)

    def get_unvisited_root(self, component_tree: ComponentTree, leaf_index: int) -> ComponentTreeNode:
        current = component_tree.leafs[leaf_index]

        while not current.parent.visited:
            current = current.parent

        return current

    def delete_root(self, node: ComponentTreeNode) -> None:
        for child in node.children:
            if child is not node.children[-1]:
                self.containers[child.maximum_unvisited_vertex_index].split()

    def initialize_mapping(self, node: ComponentTreeNode, next_node_index: int) -> int:
        if not node.children:
            self.vertex_index[node.index] = next_node_index
            node.maximum_unvisited_vertex_index = next_node_index
            return next_node_index + 1

        else:
            next_index = next_node_index

            for child in node.children:
                next_index = self.initialize_mapping(child, next_index)

            node.maximum_unvisited_vertex_index = next_index - 1

            return next_index
