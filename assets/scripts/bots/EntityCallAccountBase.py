from RemoteMethod import RemoteMethod, EntityMethodType
class AccountBaseEntityCall(object):
    def __init__(self, buffer:list):
        self.callBuffer = buffer

    def getAvatarDetailForAccount(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getAvatarDetailForAccount', (arg1, )))

    def kickAnotherAvatar(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'kickAnotherAvatar', (arg1, )))

    def logBeforeLogin(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'logBeforeLogin', (arg1, arg2, )))

    def reqCreateAvatar(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqCreateAvatar', (arg1, arg2, arg3, arg4, arg5, )))

    def reqCreateBot(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqCreateBot', (arg1, arg2, )))

    def reqRemoveAvatar(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqRemoveAvatar', (arg1, )))

    def selectAvatarGame(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'selectAvatarGame', (arg1, )))


class AccountCellEntityCall(object):
    def __init__(self, buffer:list):
        self.callBuffer = buffer

