from typing import TypeVar, List, Generic

from thorup.ds.ackermanntable import AckermannTable
from thorup.ds.doublylinkedlist import ElementContainer, DoublyLinkedList

T = TypeVar('T')


class SplitFindminStructureGabow(Generic[T]):
    """
    Implementation of Harold N. Gabow's split-findmin structure, using superelements and sublists.
    """

    def __init__(self,
                 elements_number: int = None,
                 decreasecosts_number: int = None,
                 ackermann_table: AckermannTable = None,
                 list_index: int = None) -> None:
        super().__init__()
        self.elements: DoublyLinkedList[Element[T]] = DoublyLinkedList()
        self.singleton_elements: DoublyLinkedList[Element[T]] = DoublyLinkedList()
        self.singleton_superelements: DoublyLinkedList[Superelement[T]] = DoublyLinkedList()
        self.sublists: DoublyLinkedList[SplitFindminStructureGabow[Superelement[T]]] = DoublyLinkedList()
        self.containing_list: SplitFindminStructureGabow = None
        self.ackermann_table: AckermannTable = ackermann_table if ackermann_table else AckermannTable(elements_number)
        self.containing_container_sublists: ElementContainer[SplitFindminStructureGabow[T]] = None
        self.list_index: int = list_index if list_index \
            else self.ackermann_table.get_inverse(decreasecosts_number, elements_number)
        self.cost: float = 0

    def is_sublist(self) -> bool:
        return bool(self.containing_list)

    def add(self, item: T, cost: float) -> 'Element[T]':
        element = Element(item, cost)
        container = self.elements.append(element)
        element.containing_container = container
        return element

    def initialize_head(self) -> None:
        current = self.elements.last_container

        self.cost = float("inf")
        size = 0

        while current is not self.elements.left_sentinel:
            size += 1
            self.cost = min(self.cost, current.item.cost)
            current = current.predecessor

        current = self.elements.last_container
        processed_elements = 0
        superelements_in_current_sublist = 0
        most_recent_superelement = None
        current_superelement = None
        current_level_sublist = SplitFindminStructureGabow(ackermann_table=self.ackermann_table,
                                                           list_index=self.list_index - 1)
        while (size - processed_elements) > 3:
            level = self.ackermann_table.get_inverse(self.list_index, size - processed_elements)

            current_superelement = Superelement(level)
            current_superelement.cost = float("inf")

            number_of_elements = 2 * self.ackermann_table.get_value(self.list_index, level)

            current_superelement.last_containing = current.item

            for _ in range(number_of_elements):
                current.item.superelement = current_superelement
                current_superelement.cost = min(current_superelement.cost, current.item.cost)
                current = current.predecessor

            current_superelement.first_containing = current.successor.item

            if most_recent_superelement and most_recent_superelement.level != level:
                if superelements_in_current_sublist > 1:
                    container = self.sublists.append_first(current_level_sublist)
                    current_level_sublist.containing_container_sublists = container
                    current_level_sublist.containing_list = self
                else:
                    container = self.singleton_superelements.append_first(most_recent_superelement)
                    most_recent_superelement.containing_container_singleton_superelements = container

                    most_recent_superelement.containing_list = self
                    most_recent_superelement.sublist_element = None
                    most_recent_superelement.containing_sublist = None

                current_level_sublist = SplitFindminStructureGabow(ackermann_table=self.ackermann_table,
                                                                   list_index=self.list_index - 1)
                superelements_in_current_sublist = 0

            element = current_level_sublist.add_first(current_superelement, current_superelement.cost)
            current_superelement.sublist_element = element
            current_superelement.containing_sublist = current_level_sublist
            superelements_in_current_sublist += 1

            processed_elements += number_of_elements
            most_recent_superelement = current_superelement

        if superelements_in_current_sublist > 1:
            container = self.sublists.append_first(current_level_sublist)
            current_level_sublist.containing_container_sublists = container
            current_level_sublist.containing_list = self
        else:
            if most_recent_superelement:
                container = self.singleton_superelements.append_first(most_recent_superelement)
                most_recent_superelement.containing_container_singleton_superelements = container

                most_recent_superelement.containing_list = self
                most_recent_superelement.sublist_element = None
                most_recent_superelement.containing_sublist = None

        while current is not self.elements.left_sentinel:
            container = self.singleton_elements.append_first(current.item)
            current.item.containing_container_singleton_elements = container
            current.item.containing_list = self
            current = current.predecessor

        for sublist in self.sublists:
            sublist.initialize_head()

    def initializeTail(self) -> None:
        current = self.elements.left_sentinel.successor
        self.cost = float("inf")
        size = 0

        while current is not None:
            size += 1
            self.cost = min(self.cost, current.item.cost)
            current = current.successor = self.elements.left_sentinel.successor
            processed_elements = 0
            superelements_in_current_sublist = 0
            most_recent_superelement = None
            current_superelement = None
            current_level_sublist = SplitFindminStructureGabow(ackermann_table=self.ackermann_table,
                                                               list_index=self.list_index - 1)
        while (size - processed_elements) > 3:
            level = self.ackermann_table.get_inverse(self.list_index, size - processed_elements)

            current_superelement = Superelement(level)
            current_superelement.cost = float("inf")

            number_of_elements = 2 * self.ackermann_table.get_value(self.list_index, level)

            current_superelement.first_containing = current.item

            for _ in range(number_of_elements):
                current.item.superelement = current_superelement
                current_superelement.cost = min(current_superelement.cost, current.item.cost)
                current = current.successor

            current_superelement.last_containing = current.predecessor.item

            if most_recent_superelement and most_recent_superelement.level != level:
                if superelements_in_current_sublist > 1:
                    container = self.sublists.append(current_level_sublist)
                    current_level_sublist.containing_container_sublists = container
                    current_level_sublist.containing_list = self
                else:
                    container = self.singleton_superelements.append(most_recent_superelement)
                    most_recent_superelement.containing_container_singleton_superelements = container

                    most_recent_superelement.containing_list = self
                    most_recent_superelement.sublist_element = None
                    most_recent_superelement.containing_sublist = None

                current_level_sublist = SplitFindminStructureGabow(ackermann_table=self.ackermann_table,
                                                                   list_index=self.list_index - 1)
                superelements_in_current_sublist = 0

            element = current_level_sublist.add(current_superelement, current_superelement.cost)
            current_superelement.sublist_element = element
            current_superelement.containing_sublist = current_level_sublist
            superelements_in_current_sublist += 1

            processed_elements += number_of_elements
            most_recent_superelement = current_superelement

        if superelements_in_current_sublist > 1:
            container = self.sublists.append(current_level_sublist)
            current_level_sublist.containing_container_sublists = container
            current_level_sublist.containing_list = self
        else:
            if most_recent_superelement:
                container = self.singleton_superelements.append(most_recent_superelement)
                most_recent_superelement.containing_container_singleton_superelements = container

                most_recent_superelement.containing_list = self
                most_recent_superelement.sublist_element = None
                most_recent_superelement.containing_sublist = None

        while current is not self.elements.left_sentinel:
            container = self.singleton_elements.append(current.item)
            current.item.containing_container_singleton_elements = container
            current.item.containing_list = self
            current = current.successor

        for sublist in self.sublists:
            sublist.initialize_tail()

    def initialize_head_between(self,
                                first_element_container: ElementContainer['Element[T]'],
                                last_element_container: ElementContainer['Element[T]'],
                                new_singleton_elements: DoublyLinkedList['Element[T]'],
                                new_singleton_superelements: DoublyLinkedList['Superelement[T]'],
                                new_sublists: DoublyLinkedList['SplitFindminStructureGabow[Superelement[T]]']) -> None:
        current = last_element_container

        size = 0

        while current is not first_element_container.predecessor:
            size += 1
            current = current.predecessor

        current = last_element_container
        processed_elements = 0
        superelements_in_current_sublist = 0
        most_recent_superelement = None
        current_superelement = None
        current_level_sublist = SplitFindminStructureGabow(ackermann_table=self.ackermann_table,
                                                           list_index=self.list_index - 1)
        while (size - processed_elements) > 3:
            level = self.ackermann_table.get_inverse(self.list_index, size - processed_elements)

            current_superelement = Superelement(level)
            current_superelement.cost = float("inf")

            number_of_elements = 2 * self.ackermann_table.get_value(self.list_index, level)

            current_superelement.last_containing = current.item

            for _ in range(number_of_elements):
                current.item.superelement = current_superelement
                current_superelement.cost = min(current_superelement.cost, current.item.cost)
                current = current.predecessor

            current_superelement.first_containing = current.successor.item

            if most_recent_superelement and most_recent_superelement.level != level:
                if superelements_in_current_sublist > 1:
                    container = new_sublists.append_first(current_level_sublist)
                    current_level_sublist.containing_container_sublists = container
                    current_level_sublist.containing_list = self
                else:
                    container = new_singleton_superelements.append_first(most_recent_superelement)
                    most_recent_superelement.containing_container_singleton_superelements = container

                    most_recent_superelement.containing_list = self
                    most_recent_superelement.sublist_element = None
                    most_recent_superelement.containing_sublist = None

                current_level_sublist = SplitFindminStructureGabow(ackermann_table=self.ackermann_table,
                                                                   list_index=self.list_index - 1)
                superelements_in_current_sublist = 0

            element = current_level_sublist.add_first(current_superelement, current_superelement.cost)
            current_superelement.sublist_element = element
            current_superelement.containing_sublist = current_level_sublist
            superelements_in_current_sublist += 1

            processed_elements += number_of_elements
            most_recent_superelement = current_superelement

        if superelements_in_current_sublist > 1:
            container = new_sublists.append_first(current_level_sublist)
            current_level_sublist.containing_container_sublists = container
            current_level_sublist.containing_list = self
        else:
            if most_recent_superelement:
                container = new_singleton_superelements.append_first(most_recent_superelement)
                most_recent_superelement.containing_container_singleton_superelements = container

                most_recent_superelement.containing_list = self
                most_recent_superelement.sublist_element = None
                most_recent_superelement.containing_sublist = None

        while current is not first_element_container.predecessorl:
            container = new_singleton_elements.append_first(current.item)
            current.item.containing_container_singleton_elements = container
            current.item.containing_list = self
            current.item.superelement = None
            current = current.predecessor

        for sublist in new_sublists:
            sublist.initialize_head()

    def initialize_tail_between(self,
                                first_element_container: ElementContainer['Element[T]'],
                                last_element_container: ElementContainer['Element[T]'],
                                new_singleton_elements: DoublyLinkedList['Element[T]'],
                                new_singleton_superelements: DoublyLinkedList['Superelement[T]'],
                                new_sublists: DoublyLinkedList['SplitFindminStructureGabow[Superelement[T]]']) -> None:
        current = first_element_container

        size = 0

        while current is not last_element_container.successor:
            size += 1
            current = current.successor

        current = first_element_container
        processed_elements = 0
        superelements_in_current_sublist = 0
        most_recent_superelement = None
        current_superelement = None
        current_level_sublist = SplitFindminStructureGabow(ackermann_table=self.ackermann_table,
                                                           list_index=self.list_index - 1)
        while (size - processed_elements) > 3:
            level = self.ackermann_table.get_inverse(self.list_index, size - processed_elements)

            current_superelement = Superelement(level)
            current_superelement.cost = float("inf")

            number_of_elements = 2 * self.ackermann_table.get_value(self.list_index, level)

            current_superelement.first_containing = current.item

            for _ in range(number_of_elements):
                current.item.superelement = current_superelement
                current_superelement.cost = min(current_superelement.cost, current.item.cost)
                current = current.successor

            current_superelement.last_containing = current.predecessor.item

            if most_recent_superelement and most_recent_superelement.level != level:
                if superelements_in_current_sublist > 1:
                    container = new_sublists.append(current_level_sublist)
                    current_level_sublist.containing_container_sublists = container
                    current_level_sublist.containing_list = self
                else:
                    container = new_singleton_superelements.append(most_recent_superelement)
                    most_recent_superelement.containing_container_singleton_superelements = container

                    most_recent_superelement.containing_list = self
                    most_recent_superelement.sublist_element = None
                    most_recent_superelement.containing_sublist = None

                current_level_sublist = SplitFindminStructureGabow(ackermann_table=self.ackermann_table,
                                                                   list_index=self.list_index - 1)
                superelements_in_current_sublist = 0

            element = current_level_sublist.add(current_superelement, current_superelement.cost)
            current_superelement.sublist_element = element
            current_superelement.containing_sublist = current_level_sublist
            superelements_in_current_sublist += 1

            processed_elements += number_of_elements
            most_recent_superelement = current_superelement

        if superelements_in_current_sublist > 1:
            container = new_sublists.append(current_level_sublist)
            current_level_sublist.containing_container_sublists = container
            current_level_sublist.containing_list = self
        else:
            if most_recent_superelement:
                container = new_singleton_superelements.append(most_recent_superelement)
                most_recent_superelement.containing_container_singleton_superelements = container

                most_recent_superelement.containing_list = self
                most_recent_superelement.sublist_element = None
                most_recent_superelement.containing_sublist = None

        while current is not last_element_container.successor:
            container = new_singleton_elements.append(current.item)
            current.item.containing_container_singleton_elements = container
            current.item.containing_list = self
            current.item.superelement = None
            current = current.successor

        for sublist in new_sublists:
            sublist.initialize_tail()

    def add_first(self, item: T, cost: float) -> 'Element[T]':
        element = Element(item, cost)
        container = self.elements.append_first(element)
        element.containing_container = container
        return element

    def get_cost(self) -> float:
        if self.containing_list:
            return self.containing_list.cost
        else:
            return self.cost

class Element(Generic[T]):
    """
    An element of Harold N. Gabow's split-findmin structure.
    """

    def __init__(self, item: T, cost: float) -> None:
        super().__init__()
        self.cost: float = cost
        self.item: T = item
        self.superelement: Superelement[T] = None
        self.containing_list: List['SplitFindminStructureGabow'] = None
        self.containing_container: ElementContainer[Superelement[T]] = None
        self.containing_container_singleton_elements: ElementContainer[Element[T]] = None

    def is_singleton(self) -> bool:
        return self.containing_list or (self.superelement and self.superelement.is_singleton())

    def decrease_cost(self, new_cost: float) -> 'SplitFindminStructureGabow[T]':
        if self.is_singleton():
            # update c(x)
            self.cost = min(self.cost, new_cost)

            if self.superelement:  # x is contained by a singleton superelement
                self.superelement.cost = min(self.superelement.cost, new_cost)  # update c(e(x))
                self.superelement.containing_list.cost = \
                    min(self.superelement.containing_list.cost, new_cost)  # update c(L(x))
                return self.superelement.containing_list  # return L(x)
            else:  # x is a left-over
                self.containing_list.cost = min(self.containing_list.cost, new_cost)  # update c(L(x))

                return self.containing_list  # return L(x)
        else:  # x is contained by a superelement in a sublist
            sublist = self.superelement\
                .sublist_element.decrease_cost(new_cost)  # call A_{i-1} to do decreasecost(e(x), d)
            self.superelement.cost = min(self.superelement.cost, new_cost)  # update c(e(x))
            self.cost = min(self.cost, new_cost)  # update c(x)
            list = sublist.containing_list  # find L(x)
            list.cost = min(list.cost, new_cost)  # update c(L(x))

            return list  # return L(x)

    def split(self) -> 'SplitFindminStructureGabow[T]':
        first_structure = None
        second_structure = None
        if self.is_singleton():  # this element is a left-over
            if not self.superelement:
                first_structure = self.containing_list
                second_structure = SplitFindminStructureGabow(ackermann_table=first_structure.ackermann_table,
                                                              list_index=first_structure.list_index)
                second_structure.singleton_elements = first_structure.singleton_elements\
                    .cut(self.containing_container_singleton_elements)

                current = self.containing_container.predecessor

                while current is not first_structure.elements.left_sentinel:
                    se = current.item.superelement

                    if se and se.is_singleton():
                        second_structure.singleton_superelements = first_structure.singleton_superelements\
                            .cut(se.containing_container_singleton_superelements)
                        break

                    current = current.predecessor

                if current is first_structure.elements.left_sentinel:
                    second_structure.singleton_superelements = first_structure.singleton_superelements
                    first_structure.singleton_superelements = DoublyLinkedList()

                current = self.containing_container.predecessor

                while current is not first_structure.elements.left_sentinel:
                    se = current.item.superelement

                    if se and not se.is_singleton():
                        second_structure.sublists = first_structure.sublists\
                            .cut(se.containing_sublist.containing_container_sublists)
                        break

                    current = current.predecessor

                if not self.superelement and current == first_structure.elements.left_sentinel:
                        second_structure.sublists = first_structure.sublists
                        first_structure.sublists = DoublyLinkedList()
            else:
                first_structure = self.superelement.containing_list
                second_structure = SplitFindminStructureGabow(first_structure.ackermann_table,
                                                              first_structure.list_index)
                if self is self.superelement.last_containing:
                    current = self.containing_container.predecessor

                    while current is not first_structure.elements.left_sentinel:
                        element = current.item

                        if element.is_singleton() and not element.superelement:
                            second_structure.singleton_elements = first_structure.singleton_elements\
                                .cut(element.containing_container_singleton_elements)
                            break

                        current = current.predecessor

                    if current is first_structure.elements.left_sentinel:
                        second_structure.singleton_elements = first_structure.singleton_elements
                        first_structure.singleton_elements = DoublyLinkedList()

                    second_structure.singleton_superelements = first_structure.singleton_superelements\
                        .cut(self.superelement.containing_container_singleton_superelements)

                    current = self.containing_container.predecessor

                    while current is not first_structure.elements.left_sentinel:
                        se = current.item.superelement

                        if se and not se.is_singleton():
                            second_structure.sublists = first_structure.sublists\
                                .cut(se.containing_sublist.containing_container_sublists)
                            break

                        current = current.predecessor

                    if current == first_structure.elements.left_sentinel:
                        second_structure.sublists = first_structure.sublists
                        first_structure.sublists = DoublyLinkedList()
                else:
                    last_singleton_element = None
                    current = self.containing_container.predecessor

                    while current is not first_structure.elements.left_sentinel:
                        element = current.item

                        if element.is_singleton() and not element.superelement:
                            last_singleton_element = element.containing_container_singleton_elements
                            break

                        current = current.predecessor

                    if current == first_structure.elements.left_sentinel:
                        last_singleton_element = first_structure.singleton_elements.left_sentinel

                    last_singleton_superelement = self.superelement.containing_container_singleton_superelements
                    last_sublist = None
                    current = self.containing_container.predecessor

                    while current is not first_structure.elements.left_sentinel:
                        se = current.item.superelement

                        if se and not se.is_singleton():
                            last_sublist = se.containing_sublist.containing_container_sublists
                            break

                        current = current.predecessor

                    if current == first_structure.elements.left_sentinel:
                        last_sublist = first_structure.sublists.left_sentinel

                    last_singleton_superelement = first_structure.singleton_superelements\
                        .remove(last_singleton_superelement)

                    new_singleton_elements = DoublyLinkedList()
                    new_singleton_superelements = DoublyLinkedList()
                    new_sublists = DoublyLinkedList()

                    old_superelement = self.superelement

                    first_structure.initialize_head_between(self.superelement.first_containing.containing_container,
                                                            self.containing_container,
                                                            new_singleton_elements,
                                                            new_singleton_superelements,
                                                            new_sublists)

                    last_singleton_element = first_structure.singleton_elements\
                        .insert_list(last_singleton_element, new_singleton_elements)
                    last_singleton_superelement = first_structure.singleton_superelements\
                        .insert_list(last_singleton_superelement, new_singleton_superelements)
                    last_sublist = first_structure.sublists.insert_list(last_sublist, new_sublists)

                    second_structure.singleton_elements = first_structure.singleton_elements\
                        .cut(last_singleton_element)
                    second_structure.singleton_superelements = first_structure.singleton_superelements\
                        .cut(last_singleton_superelement)
                    second_structure.sublists = first_structure.sublists.cut(last_sublist)

                    new_singleton_elements = DoublyLinkedList()
                    new_singleton_superelements = DoublyLinkedList()
                    new_sublists = DoublyLinkedList()

                    first_structure.initialize_tail_between(self.containing_container.successor,
                                                            old_superelement.last_containing.containing_container,
                                                            new_singleton_elements,
                                                            new_singleton_superelements,
                                                            new_sublists)

                    new_singleton_elements.extend(second_structure.singleton_elements)
                    new_singleton_superelements.extend(second_structure.singleton_superelements)
                    new_sublists.extend(second_structure.sublists)

                    second_structure.singleton_elements = new_singleton_elements
                    second_structure.singletonSuperelements = new_singleton_superelements
                    second_structure.sublists = new_sublists
        else:
            first_structure = self.superelement.containing_sublist.containing_list
            second_structure = SplitFindminStructureGabow(first_structure.ackermann_table,
                                                          first_structure.list_index)
            container_to_insert_after = self.superelement.containing_sublist.containing_container_sublists

            sublist2 = None
            sublist3 = self.superelement.sublist_element.split()

            for element in sublist3.elements:
                se = element.item
                se.containing_sublist = sublist3

            if self.superelement.sublist_element.containing_container.predecessor.item:
                sublist2 = self.superelement.sublist_element.containing_container.predecessor.item.split()

                for element in sublist2.elements:
                    se = element.item
                    se.containing_sublist = sublist2

            if sublist2:
                container_to_insert_after = first_structure.sublists.insert(container_to_insert_after, sublist2)
                sublist2.containing_container_sublists = container_to_insert_after
                sublist2.containing_list = first_structure

            container_to_insert_after = first_structure.sublists.insert(container_to_insert_after, sublist3)
            sublist3.containing_container_sublists = container_to_insert_after
            sublist3.containing_list = first_structure

            if self is self.superelement.last_containing:
                current = self.containing_container.predecessor

                while current is not first_structure.elements.left_sentinel:
                    element = current.item

                    if element.is_singleton() and not element.superelement:
                        second_structure.singleton_elements = first_structure.singleton_elements\
                            .cut(element.containing_container_singleton_elements)
                        break

                    current = current.predecessor

                if current == first_structure.elements.left_sentinel:
                    second_structure.singleton_elements = first_structure.singleton_elements
                    first_structure.singleton_elements = DoublyLinkedList()

                current = self.containing_container.predecessor

                while current is not first_structure.elements.left_sentinel:
                    se = current.item.superelement

                    if se and se.is_singleton():
                        second_structure.singleton_superelements = first_structure.singleton_superelements\
                            .cut(se.containing_container_singleton_superelements)
                        break

                    current = current.predecessor

                if current is first_structure.elements.left_sentinel:
                    second_structure.singleton_superelements = first_structure.singleton_superelements
                    first_structure.singleton_superelements = DoublyLinkedList()

                if sublist2:
                    second_structure.sublists = first_structure.sublists\
                        .cut(sublist2.containing_container_sublists)
                else:
                    second_structure.sublists = first_structure.sublists\
                        .cut(self.superelement.containing_sublist.containing_container_sublists)
            else:
                last_singleton_element = None
                current = self.containing_container.predecessor

                while current is not first_structure.elements.left_sentinel:
                    element = current.item

                    if element.is_singleton() and not element.superelement:
                        last_singleton_element = element.containing_container_singleton_elements
                        break

                    current = current.predecessor

                if current == first_structure.elements.left_sentinel:
                    last_singleton_element = first_structure.singleton_elements.left_sentinel

                current = self.containing_container.predecessor

                while current is not first_structure.elements.left_sentinel:
                    se = current.item.superelement

                    if se and se.is_singleton():
                        last_singleton_superelement = se.containing_container_singleton_superelements
                        break

                    current = current.predecessor

                if current is first_structure.elements.left_sentinel:
                    last_singleton_superelement = first_structure.singleton_superelements.left_sentinel

                last_sublist = self.superelement.containing_sublist.containing_container_sublists.predecessor

                new_singleton_elements = DoublyLinkedList()
                new_singleton_superelements = DoublyLinkedList()
                new_sublists = DoublyLinkedList()

                old_superelement = self.superelement

                first_structure.initialize_head_between(self.superelement.first_containing.containing_container,
                                                        self.containing_container,
                                                        new_singleton_elements,
                                                        new_singleton_superelements,
                                                        new_sublists)

                last_singleton_element = first_structure.singleton_elements \
                    .insert_list(last_singleton_element, new_singleton_elements)
                last_singleton_superelement = first_structure.singleton_superelements \
                    .insert_list(last_singleton_superelement, new_singleton_superelements)
                last_sublist = first_structure.sublists.insert_list(last_sublist, new_sublists)

                second_structure.singleton_elements = first_structure.singleton_elements \
                    .cut(last_singleton_element)
                second_structure.singleton_superelements = first_structure.singleton_superelements \
                    .cut(last_singleton_superelement)
                second_structure.sublists = first_structure.sublists.cut(last_sublist)

                second_structure.sublists = second_structure.sublists\
                    .cut(second_structure.sublists.left_sentinel.successor)

                new_singleton_elements = DoublyLinkedList()
                new_singleton_superelements = DoublyLinkedList()
                new_sublists = DoublyLinkedList()

                first_structure.initialize_tail_between(self.containing_container.successor,
                                                        old_superelement.last_containing.containing_container,
                                                        new_singleton_elements,
                                                        new_singleton_superelements,
                                                        new_sublists)

                new_singleton_elements.extend(second_structure.singleton_elements)
                new_singleton_superelements.extend(second_structure.singleton_superelements)
                new_sublists.extend(second_structure.sublists)

                second_structure.singleton_elements = new_singleton_elements
                second_structure.singletonSuperelements = new_singleton_superelements
                second_structure.sublists = new_sublists

        second_structure.elements = first_structure.elements.cut(self.containing_container)
        second_structure.containing_list = first_structure.containing_list

        first_structure.cost = float("inf")
        second_structure.cost = float("inf")

        for element in first_structure.singleton_elements:
            first_structure.cost = min(first_structure.cost, element.cost)

        for superelement in first_structure.singleton_superelements:
            first_structure.cost = min(first_structure.cost, superelement.cost)

        for sublist in first_structure.sublists:
            first_structure.cost = min(first_structure.cost, sublist.cost)

        for element in second_structure.singleton_elements:
            element.containing_list = second_structure
            second_structure.cost = min(second_structure.cost, element.cost)

        for superelement in second_structure.singleton_superelements:
            superelement.containing_list = second_structure
            second_structure.cost = min(second_structure.cost, superelement.cost)

        for sublist in second_structure.sublists:
            self.deep_set_pointers(sublist, second_structure)
            second_structure.cost = min(second_structure.cost, sublist.cost)

        return second_structure

    def get_list_cost(self) -> float:
        if self.is_singleton():
            if self.containing_list:
                return self.containing_list.cost
            else:
                return self.superelement.cost
        else:
            return self.superelement.containing_sublist.get_cost()

    def deep_set_pointers(self,
                          sublist: SplitFindminStructureGabow['Superelement[T]'],
                          containing_list: SplitFindminStructureGabow) -> None:
        sublist.containing_list = containing_list

        for subsublist in sublist.sublists:
            self.deep_set_pointers(subsublist, sublist)


class Superelement(Generic[T]):
    """
    Superelemtn of Harold N. Gabow's split-findmin structure.
    """

    def __init__(self, level: int) -> None:
        super().__init__()
        self.level: int = level
        self.first_containing: 'Element[T]' = None
        self.last_containing: 'Element[T]' = None
        self.cost: float = None
        self.containing_list: List['SplitFindminStructureGabow'] = None
        self.containing_container_singleton_superelements: ElementContainer[Superelement[T]] = None
        self.sublist_element: 'Element'[Superelement[T]] = None
        self.containing_sublist: 'SplitFindminStructureGabow'[Superelement[T]] = None

    def is_singleton(self) -> bool:
        return bool(self.containing_list)
