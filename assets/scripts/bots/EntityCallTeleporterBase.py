from RemoteMethod import RemoteMethod, EntityMethodType
class TeleporterBaseEntityCall(object):
    def __init__(self, buffer:list):
        self.callBuffer = buffer


class TeleporterCellEntityCall(object):
    def __init__(self, buffer:list):
        self.callBuffer = buffer

    def doTeleport(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'doTeleport', (arg1, arg2, )))

