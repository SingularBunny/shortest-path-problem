from math import floor
from typing import Dict


class AckermannTable:
    """
    Table that allows accessing the values of Ackermann's function A(i, j) that are n or less for a given n.
    """
    def __init__(self, maximum_table_value) -> None:
        super().__init__()
        self.table: Dict[int, Dict[int, int]] = {}
        self._init_table(maximum_table_value)

    def _init_table(self, maximum_table_value) -> None:
        i = 1
        j = 2

        self.set_value(1, 1, 2)

        while True:
            new_value = -1

            if i == 1:
                new_value = self.get_value(i, j - 1) * 2
            else:
                new_value = self.get_value(i - 1, self.get_value(i, j - 1))

            if new_value > maximum_table_value or new_value == -1:
                if j == 1:
                    return
                else:
                    i += 1
                    j = 1
            else:
                self.set_value(i, j, new_value)
                j += 1

    def get_value(self, i: int, j: int) -> int:
        if j == 0:
            return 2
        else:
            if i in self.table:
                row_i = self.table[i]
                if j in row_i:
                    return row_i[j]
                else:
                    return -1
            else:
                return -1

    def get_inverse(self, m: int, n: int) -> int:
        if n >= 4:
            j = 0

            while ((2 * self.get_value(m, j)) <= n) and (self.get_value(m, j) != -1):
                j += 1

            return j - 1
        elif m >= n:
            i = 1

            while self.get_value(i, int(floor(m / n))) != -1:
                i += 1

            return i

        return -1

    def set_value(self, i: int, j: int, value: int) -> None:

        self.table.setdefault(i, {})[j] = value
