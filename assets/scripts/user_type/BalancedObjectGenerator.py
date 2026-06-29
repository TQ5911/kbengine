
class BalancedObjectGenerator(list):
    def __init__(self, *args, **keywordArgs):
        super().__init__(*args, **keywordArgs)
        self._beBroken = False

    def popitems(self, maxObjectNum, breakKey=None):
        _results = []

        if not self:
            return _results, 0

        if self._beBroken:
            _results.append(self.pop())
            self._beBroken = False
            return _results, 1

        for _ in range(maxObjectNum):
            if not self:
                break

            _item = self.pop()

            if callable(breakKey) and breakKey(_item):
                self._beBroken = True
                self.append(_item)
                break

            _results.append(_item)

        return _results, len(_results)
