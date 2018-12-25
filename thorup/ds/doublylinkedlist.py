from typing import TypeVar, Generic, Iterator

T = TypeVar('T')


class DoublyLinkedList(Generic[T]):

    def __init__(self) -> None:
        super().__init__()
        self.left_sentinel: ElementContainer[T] = ElementContainer(None, None, None)
        self.last_container: ElementContainer[T] = self.left_sentinel

    def __iter__(self) -> Iterator[T]:
        return DoublyLinkedListIterator(self.left_sentinel)

    def is_empty(self):
        return self.left_sentinel is self.last_container

    def append(self, item: T) -> 'ElementContainer[T]':
        self.last_container.insert_after(item)
        self.last_container = self.last_container.successor
        return self.last_container

    def append_first(self, item: T) -> 'ElementContainer[T]':
        self.left_sentinel.insert_after(item)

        if self.left_sentinel is self.last_container:
            self.last_container = self.left_sentinel.successor

        return self.left_sentinel.successor

    def remove(self, container: 'ElementContainer[T]') -> 'ElementContainer[T]':
        if container is self.last_container:
            self.last_container = self.last_container.predecessor

        return container.remove()

    def insert(self, container_to_insert_after: 'ElementContainer[T]', item: T) -> 'ElementContainer[T]':
        container_to_insert_after.insert_after(item)

        if container_to_insert_after is self.last_container:
            self.last_container = container_to_insert_after.successor

        return container_to_insert_after.successor

    def cut(self, container: 'ElementContainer[T]') -> 'DoublyLinkedList[T]':
        if container is self.last_container:
            return DoublyLinkedList()
        else:
            new_list = DoublyLinkedList()
            new_list.left_sentinel.successor = container.successor
            container.successor.predecessor = new_list.left_sentinel
            new_list.last_container = self.last_container

            container.successor = None
            self.last_container = container
            return new_list

    def insert_list(self, position: 'ElementContainer[T]', lst: 'DoublyLinkedList[T]') -> 'ElementContainer[T]':
        if lst.is_empty():
            return position
        else:
            if position.successor:
                position.successor.predecessor = lst.last_container
                lst.last_container.successor = position.successor

            position.successor = lst.left_sentinel.successor
            lst.left_sentinel.successor.predecessor = position

            if position is self.last_container:
                self.last_container = lst.last_container

            return lst.last_container

    def extend(self, lst: 'DoublyLinkedList[T]'):
        if not lst.is_empty():
            self.last_container.successor = lst.left_sentinel.successor
            lst.left_sentinel.successor.predecessor = self.last_container
            self.last_container = lst.last_container


class ElementContainer(Generic[T]):

    def __init__(self, item: T, predecessor: 'ElementContainer[T]', successor: 'ElementContainer[T]') -> None:
        super().__init__()
        self.item: T = item
        self.predecessor: ElementContainer[T] = predecessor
        self.successor: ElementContainer[T] = successor

    def insert_after(self, item: T) -> 'ElementContainer[T]':
        new_container = ElementContainer(item, self, self.successor)

        if self.successor:
            self.successor.predecessor = new_container

        self.successor = new_container
        return new_container

    def remove(self) -> 'ElementContainer[T]':
        self.predecessor.successor = self.successor

        if self.successor:
            self.successor.predecessor = self.predecessor

        return self.predecessor


class DoublyLinkedListIterator:
    def __init__(self, left_sentinel: ElementContainer[T]):
        self.current = left_sentinel

    def __iter__(self):
        return self

    def __next__(self):
        if self.current.successor:
            item = self.current.successor.item
            self.current = self.current.successor
            return item
        else:
            raise StopIteration()
