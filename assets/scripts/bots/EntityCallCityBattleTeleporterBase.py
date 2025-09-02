from RemoteMethod import RemoteMethod, EntityMethodType
class CityBattleTeleporterBaseEntityCall(object):
    def __init__(self, buffer:list):
        self.callBuffer = buffer


class CityBattleTeleporterCellEntityCall(object):
    def __init__(self, buffer:list):
        self.callBuffer = buffer

    def doTeleport(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'doTeleport', ()))

