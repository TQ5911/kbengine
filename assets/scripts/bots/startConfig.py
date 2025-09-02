class StartConfig:
    rps = 100
    maxNum = 100
    index = 0

    def __init__(self, rps: int, maxNum: int, index: int):
        self.rps = rps
        self.maxNum = maxNum
        self.index = index

    def getStartSleepTime(self):
        if self.rps == 0:
            self.rps = 100
        return (self.index // self.rps) + 1

    def getRunSleepTime(self):
        if self.rps == 0:
            self.rps = 100
        return (self.maxNum // self.rps) - self.getStartSleepTime() + 1
