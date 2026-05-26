

class MineGlobalData(object):
    MINE_STATE_PREPARE = 1
    MINE_STATE_START = 2
    MINE_STATE_END = 3

    def __init__(self, mineWarState=MINE_STATE_END):
        self.mineWarState = mineWarState

    def clone(self):
        return MineGlobalData(
            self.mineWarState,
        )


