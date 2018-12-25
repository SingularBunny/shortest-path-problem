from typing import List


class ComponentTree:
    """
    A component tree of a weighted, undirected graph with positive integer edge weights.
    """

    def __init__(self, vertices_number: int) -> None:
        super().__init__()
        self.leafs: List[ComponentTreeNode] = [ComponentTreeNode(i) for i in range(vertices_number)]
        self.internal_nodes: List[ComponentTreeNode] = [None for _ in range(vertices_number)]
        self.root: ComponentTreeNode = None

    def set_buckets_internal_node_number(self, internal_node_index: int, buckets_number: int) -> None:
        self.internal_nodes[internal_node_index].delta = buckets_number

    def set_component_hierarchy_level(self, internal_node_index: int, component_hierarchy_level: int):
        self.internal_nodes[internal_node_index].component_hierarchy_level = component_hierarchy_level

    def set_parent_of_leaf(self, leaf: int, parent: int):
        if not self.internal_nodes[parent]:
            self.internal_nodes[parent] = ComponentTreeNode(parent)
            self.root = self.internal_nodes[parent]

        self.leafs[leaf].set_parent(self.internal_nodes[parent])
        self.internal_nodes[parent].unvisited_vertices_number += 1
        self.internal_nodes[parent].unvisited_vertices_initial_number += 1

    def set_parent_of_internal_node(self, internal_node: int, parent: int):
        if not self.internal_nodes[parent]:
            self.internal_nodes[parent] = ComponentTreeNode(parent)
            self.root = self.internal_nodes[parent]

        self.internal_nodes[internal_node].set_parent(self.internal_nodes[parent])
        self.internal_nodes[parent].unvisited_vertices_number += \
            self.internal_nodes[internal_node].unvisited_vertices_number
        self.internal_nodes[parent].unvisited_vertices_initial_number += \
            self.internal_nodes[internal_node].unvisited_vertices_initial_number


class ComponentTreeNode:


    def __init__(self, index: int) -> None:
        super().__init__()
        self.index: int = index
        self.delta: int = None
        self.lowest_bucket_index: int = None
        self.component_hierarchy_level: int = None
        self.visited: bool = None
        self.bucket_index_offset: int = None
        self.highest_bucket_index: int = None
        self.next_bucket_index: int = None
        self.maximum_unvisited_vertex_index: int = None
        self.unvisited_vertices_number: int = 0
        self.unvisited_vertices_initial_number: int = 0
        self.parent: ComponentTreeNode = None

        self.children: List['ComponentTreeNode'] = []
        self.buckets: List[List['ComponentTreeNode']] = []
        self.containing_bucket: List['ComponentTreeNode'] = None

    def remove_from_parent_bucket(self) -> None:
        self.containing_bucket.remove(self)

    def move_to_bucket(self, parent: 'ComponentTreeNode', index: int) -> None:
        if self.containing_bucket:
            self.remove_from_parent_bucket()

        parent.inserts_tree_node_to_bucket_by_index(self, index)

    def inserts_tree_node_to_bucket_by_index(self, tree: 'ComponentTreeNode', index: int) -> None:
        if index - self.bucket_index_offset < len(self.buckets):
            self.buckets[index - self.bucket_index_offset].append(tree)
            tree.containingBucket = self.buckets[index - self.bucket_index_offset]

    def get_bucket(self, index: int) -> List['ComponentTreeNode']:
        return self.buckets[index - self.bucket_index_offset]

    def set_parent(self, parent: 'ComponentTreeNode') -> None:
        self.parent = parent
        parent.children.append(self)

    def initialize_buckets(self) -> None:
        self.bucket_index_offset = self.lowest_bucket_index
        bucket_size = self.maximum_unvisited_vertex_index - self.lowest_bucket_index + 1
        buckets = []
        for i in range(bucket_size):
            buckets[i] = []
