# coding: utf-8


class SStack(list):
    """ Sinple Stack Structure

    Include operations:
        extend(iter)
        pop()
        push()
        clear()

    >>> SStack([1,2,3])
    [1, 2, 3]

    >>> # ------------------------
    >>> # test extend out of range
    >>> SStack(range(1000), 4)
    Traceback (most recent call last):
        ...
    IndexError: out of stack max size 4

    >>> # ---------------
    >>> # test pop & push
    >>> SStack([1]).pop()
    1
    >>> _ = SStack([1])
    >>> _.push(1)
    >>> assert _ == [1, 1]

    >>> # ---------------------
    >>> # test push out of size
    >>> _ = SStack([1,2,3], 3)
    >>> _.push(2)
    Traceback (most recent call last):
        ...
    IndexError: this stack is full

    >>> # ----------
    >>> # test clear
    >>> _ = SStack([1,2,3,4])
    >>> _.clear()
    >>> assert _ == []
    """

    def __init__(self, items: list, maximum=8):
        super().__init__()
        self.maximum = maximum
        # extend objects
        self.extend(items)

    @property
    def depth(self):
        return len(self)

    def is_full(self):
        return True if self.depth >= self.maximum else False

    def resize(self, new_size):
        if self.depth > new_size:
            raise RuntimeError('can\'t resize, stack depth > new size')

        self.maximum = new_size

    def extend(self, iterable):
        """ push multi items in stack

        :raise IndexError: stack is full
        """
        super().extend(self._extend(iterable))

    def _extend(self, iterable):
        for idx, item in enumerate(iterable):
            if idx > self.maximum:
                raise IndexError(
                    'out of stack max size {}'.format(self.maximum))

            yield item

    def pop(self):
        """ get one item from stack

        :return: pop item
        :raise IndexError: stack is empty
        """
        return super().pop()

    def push(self, item):
        """ push one item in stack

        :raise IndexError: stack is full
        """
        if self.depth >= self.maximum:
            raise IndexError('this stack is full')

        self.append(item)

    def clear(self):
        """ clear pool """
        super().clear()


class SStackMgr(dict):

    def createStack(self, key, items, maximum=8, replaceable=True):
        """ create new stack in stack manager

        :param key: stack's identity key, it should be hashable
        :param maximum: stack max size
        :param replaceable: if set False, func will raise exc
                            when key repeated

        :return: new created stack
        :raise KeyError: when replaceable turn False and key repeated
        :raise IndexError: when items out of stack maximum size
        """
        if replaceable and key in self:
            raise KeyError('key "{}" already exist'.format(key))

        _s = SStack(items, maximum=maximum)
        self[key] = _s

        return _s

    def addStack(self, key, stack: SStack, replaceable=True):
        """ add exist stack in stack manager

        :param key: stack's identity key
        :param stack: an exist stack
        :param replaceable: if set False, func will raise exc
                            when key repeated

        :raise KeyError: when replaceable turn False and key repeated
        """
        if replaceable and key in self:
            raise KeyError('key "{}" already exist'.format(key))

        self[key] = stack

    def removeStack(self, key):
        """ remove special stack from pool dict """
        if key in self:
            del self[key]

    def clearStack(self, key):
        if key in self:
            self[key].clear()

    def getStack(self, key, default=None):
        """ get specail stack from pool dict """
        return self.get(key, default)

    def pushInStack(self, key, item):
        """ push item to special stack

        :raise IndexError: when stack is full
        :raise KeyError: key not found in stack
        """
        self[key].push(item)

    def popFromStack(self, key, item):
        """" pop item from specail stack

        :raise IndexError: when stak is empty
        :raise KeyError: key not found in stack
        """
        return self[key].pop(item)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)