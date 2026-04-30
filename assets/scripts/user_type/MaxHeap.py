# coding: utf-8
import copy

import userType


class MaxHeap(userType.UserSingleType):
    def __init__(self, array: list=None):
        self._data = copy.copy(array) if array is not None else []
        self.rebuild()

    def reset(self, newArry):
        self._data = copy.copy(newArry)
        self.rebuild()

    def clear(self):
        self._data.clear()

    def rebuild(self):
        pCount = self.size // 2
        while pCount >= 1:
            self.shiftdown(pCount)
            pCount -= 1

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    @property
    def maximum(self):
        if self.size:
            return self._data[0]

    def getDataKey(self, data):
        return data

    @property
    def size(self):
        return len(self._data)

    def copy(self):
        return self.__class__(self._data)

    def isEmpty(self):
        return bool(not self.size)

    def insert(self, item):
        self._data.append(item)
        self.shiftup(self.size)

    def shiftup(self, count):
        while count > 1 and self.getDataKey(self._data[count//2-1]) < self.getDataKey(self._data[count-1]):
            self._data[count//2-1], self._data[count-1] = self._data[count-1], self._data[count//2-1]
            count //= 2

    def pop(self, *default):
        if self.size > 0:
            ret = self._data[0]
            self._data[0], self._data[self.size-1] = \
                self._data[self.size-1], self._data[0]
            self._data.pop()
            self.shiftdown(1)
            return ret

        if len(default) == 1:
            return default[0]
        raise IndexError('Pop from empty MaxHeap')

    def shiftdown(self, count):
        while 2 * count <= self.size:
            cCount = 2 * count
            if cCount + 1 <= self.size:
                if self.getDataKey(self._data[cCount]) > self.getDataKey(self._data[cCount-1]):
                    cCount += 1
            if self.getDataKey(self._data[count-1]) >= self.getDataKey(self._data[cCount-1]):
                break
            # exchange
            self._data[count-1], self._data[cCount-1] = \
                self._data[cCount-1], self._data[count-1]
