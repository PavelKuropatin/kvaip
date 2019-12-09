from typing import Union, List

from utils.constants import F_ALL, DC


class Cube:

    def __init__(self, x: List[int], f: int, m: Union[List[int], int], parent: List = ()):
        from utils.utils import as_str
        self.__x = x
        self.__sum_x = sum([_ for _ in x if _ not in F_ALL])
        self.__f = f
        self.__m = m
        self.__str_f = as_str(f)
        self.__parent = parent

    @property
    def x(self):
        return self.__x

    @property
    def sum_x(self):
        return self.__sum_x

    @property
    def f(self):
        return self.__f

    @property
    def m(self):
        return self.__m

    @x.setter
    def x(self, value):
        self.__x = value

    @f.setter
    def f(self, value):
        self.__f = value

    @m.setter
    def m(self, value):
        self.__m = value

    def has_m(self, m):
        if isinstance(self.__m, list):
            return m in self.__m
        return m == self.__m

    def is_match(self, other):
        """
        compare array by value sequentially
        return false if count of mistached values is more then 1
        """
        diff = 0
        for i in range(len(self.__x)):
            if self.__x[i] != other.x[i]:
                diff += 1
            if diff == 2:
                return False
        return True

    def values(self, f=True):
        if f:
            end = [self.__str_f, set(self.__m)] if isinstance(self.__m, list) else [self.__str_f, self.__m]
        else:
            end = [set(self.__m)] if isinstance(self.__m, list) else [{self.__m}]
        return self.__x + end

    def is_covered(self, parent):
        if isinstance(self.__m, list):
            if isinstance(parent.m, list):
                return not set(self.__m).difference(set(parent.m))
            return parent.m not in self.__m
        if isinstance(parent.m, list):
            return False
        return self.__m == parent.m

    @classmethod
    def merge(cls, c1, c2):
        joined_m = []
        joined_m += c1.m if isinstance(c1.m, list) else [c1.m]
        joined_m += c2.m if isinstance(c2.m, list) else [c2.m]
        joined_m = list(set(joined_m))

        joined_x = [
            DC if c1.x[i] != c2.x[i] else c1.x[i]
            for i in range(len(c1.x))
        ]
        return Cube(joined_x, DC, joined_m)

    def __eq__(self, other):
        if not isinstance(other, Cube):
            return False
        return all([
            self.__x == other.x,
            set(self.__m) == set(other.m),
            self.__f == other.f
        ])

    def __repr__(self):
        return self.__class__.__name__ + "(x = %s, f = %s, m = %s)" % (str(self.__x), self.__str_f, str(self.__m))
