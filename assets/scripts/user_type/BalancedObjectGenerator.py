
class BalancedObjectGenerator(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._beBroken = False

    def popitems(self, maxObjectNum, breakKey=None):
        results = []

        if not self:
            return results, 0

        if self._beBroken:
            results.append(self.pop())
            self._beBroken = False
            return results, 1

        for i in range(maxObjectNum):
            if not self:
                break

            item = self.pop()

            if callable(breakKey) and breakKey(item):
                self._beBroken = True
                self.append(item)
                break

            results.append(item)

        return results, len(results)
