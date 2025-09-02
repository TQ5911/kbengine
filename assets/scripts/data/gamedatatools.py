# coding: utf-8
# CopyRight CangMing INC 2018-2020

"""
游戏data数据工具集合

日志：
  [2020-11-23]: VarNameDefinedMeta中未定义枚举量报错等级提升至ERROR
"""
# WARNING: DO NOT IMPORT GAME ASSETS MODULE EXCEPT YOU KNOW WHAT YOU ARE DOING!!!
import copy
import collections.abc


class RODict(collections.abc.Mapping):

    def __init__(self, data):
        self._data = data

    def clear(self):
        raise RuntimeError('RODict un-support dict.clear()')

    def copy(self):
        return copy.copy(self)

    def __copy__(self):
        return self.__class__(copy.copy(self._data))

    @staticmethod
    def fromkeys(*args, **kwargs):
        raise RuntimeError('RODict un-support dict.fromkeys()')

    def pop(self, k, d=None):
        raise RuntimeError('RODict un-support dict.pop()')

    def popitem(self):
        raise RuntimeError('RODict un-support dict.popitem()')

    def setdefault(self):
        raise RuntimeError('RODict un-support dict.setdefault()')

    def update(self):
        raise RuntimeError('RODict un-support dict.update()')

    def __delitem__(self, *args, **kwargs):
        raise RuntimeError('RODict un-support del dict[key]')

    def __getitem__(self, item):
        return self._data[item]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return repr(self._data)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.__repr__())

    def __setitem__(self, *args, **kwargs):
        raise RuntimeError('RODict un-support dict[key]=value')

    def __sizeof__(self):
        return super(RODict, self).__sizeof__() + self._data.__sizeof__()


class ROList(collections.abc.Sequence):

    def __init__(self, data):
        self._data = data

    def append(self, p_object):
        raise RuntimeError('ROList un-support list.append()')

    def clear(self):
        raise RuntimeError('ROList un-support list.clear()')

    def copy(self):
        return copy.copy(self)

    def extend(self, iterable):
        raise RuntimeError('ROList un-support list.extend()')

    def insert(self, value, start=None, stop=None):
        raise RuntimeError('ROList un-support list.insert()')

    def pop(self, index=None):
        raise RuntimeError('ROList un-support list.pop()')

    def remove(self, value):
        raise RuntimeError('ROList un-support list.remove()')

    def reverse(self):
        raise RuntimeError('ROList un-support list.reverse()')

    def sort(self, key=None, reverse=None):
        raise RuntimeError('ROList un-support list.sort()')

    def __add__(self, other):
        other_data = other._data if isinstance(other, self.__class__) else other
        return self.__class__(other_data)

    def __delitem__(self, *args, **kwargs):
        raise RuntimeError('ROList un-support del list[index]')

    def __copy__(self):
        return self.__class__(copy.copy(self._data))

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, *args, **kwargs):
        raise RuntimeError('ROLIst un-support list[index]=value')

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.__repr__())

    def __sizeof__(self):
        return super(ROList, self).__sizeof__() + self._data.__sizeof__()

class ROSet(collections.abc.Set):
    def __init__(self, data):
        if not isinstance(data, set):
            raise TypeError('only can init from set')
        self._data = data

    def add(self, val):
        raise RuntimeError('ROSet un-support set.add()')

    def clear(self):
        raise RuntimeError('ROSet un-support set.clear()')

    def discard(self, val):
        raise RuntimeError('ROSet un-support set.discard()')

    def pop(self):
        raise RuntimeError('ROSet un-support set.pop()')

    def remove(self, val):
        raise RuntimeError('ROSet un-support set.remove()')

    def update(self, val):
        raise RuntimeError('ROSet un-support set.update()')

    def symmetric_difference_update(self, val):
        raise RuntimeError('ROSet un-support set.symmetric_difference_update()')

    def intersection_update(self, val):
        raise RuntimeError('ROSet un-support set.intersection_update()')

    def __iter__(self):
        return iter(self._data)

    def __contains__(self, value):
        return value in self._data

    def __len__(self):
        return len(self._data)

class VarNameDefinedMeta(type):
    def __new__(cls, clsname, bases, attrs):
        attrs["__UNKNOWN_SRC__"] = 0
        return type.__new__(cls, clsname, bases, attrs)

    def __getattribute__(cls, item):
        try:
            return type.__getattribute__(cls, item)
        except AttributeError:
            if item == "id":
                raise AttributeError("type object '{}' has no attribute '{}'".format(cls.__name__, item))

            from KBEDebug import ERROR_MSG
            ERROR_MSG("Un-defined varname: {}".format(item))
            return cls.__UNKNOWN_SRC__

