from typing import TypeVar, Generic

T = TypeVar('T')

class UnionFindStructureTarjan():
    """ Implementation of Tarjan's union-find structure, using
        union with size and find with path compression.
    """

    @staticmethod
    def find(node: 'UnionFindNode'):

        root = UnionFindStructureTarjan._get_root(node)
        current = node
        next_ = None

        while current is not root:
            next_ = current.parent
            current.parent = root
            current = next_

        return root

    @staticmethod
    def _get_root(node: 'UnionFindNode'):
        root = node
        while root.parent is not None:
            root = root.parent
        return root

    @staticmethod
    def union(first_node: 'UnionFindNode', second_node: 'UnionFindNode'):
        first_node_root = UnionFindStructureTarjan.find(first_node)
        second_node_root = UnionFindStructureTarjan.find(second_node)

        if first_node is not second_node:

            if first_node_root.subtree_size < second_node_root.subtree_size:
                first_node_root.parent = second_node_root
                second_node_root.subtree_size += first_node_root.subtree_size
            else:
                second_node_root.parent = first_node_root
                first_node_root.subtree_size += second_node_root.subtree_size


class UnionFindNode(Generic[T]):
    """  Node of Tarjan's union-find structure. """

    def __init__(self, item: T, parent: 'UnionFindNode' = None):
        super(UnionFindNode, self).__init__()
        self.item: T = item
        self.parent: UnionFindNode = parent
        self.subtree_size: int = 1
