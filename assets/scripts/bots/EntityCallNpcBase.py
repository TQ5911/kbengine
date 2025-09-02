from RemoteMethod import RemoteMethod, EntityMethodType
class NpcBaseEntityCall(object):
    def __init__(self, buffer:list):
        self.callBuffer = buffer


class NpcCellEntityCall(object):
    def __init__(self, buffer:list):
        self.callBuffer = buffer

    def cancelChargeSkill(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'cancelChargeSkill', (arg1, )))

    def doDialogEvent(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'doDialogEvent', (arg1, )))

    def getAureoleInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getAureoleInfo', (arg1, )))

    def getBuffInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getBuffInfo', (arg1, )))

