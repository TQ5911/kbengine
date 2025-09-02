
class EntityMethodType(object):
    BASE = 1
    CELL = 2

class RemoteMethod(object):
    def __init__(self, callType:int, methodName:str, args:tuple):
        self.callType = callType
        self.methodName = methodName
        self.args = args

    def __str__(self):
        return '%s:%s(%s)'%(self.callType, self.methodName, self.args)
