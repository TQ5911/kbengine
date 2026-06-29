# -*- encoding:utf-8 -*-

from KBEDebug import *
import dropAward
import Mail


class MailInst(object):
    def createObjFromDict(self, dataDict):
        _mailInfo = Mail.Mail()
        _mailInfo.initFromSavedMailDict(dataDict)
        return _mailInfo

    def isSameType(self, obj):
        return isinstance(obj, Mail.Mail)

    def getDictFromObj(self, obj):
        return obj.toMailSavedDict()

mailInstance = MailInst()

class MailAttachInst(object):
    def createObjFromDict(self, dataDict):
        _mailAttach = dropAward.MailAttachVal()
        _mailAttach.fromMailWealthDict(dataDict)
        return  _mailAttach

    def isSameType(self, obj):
        return isinstance(obj, dropAward.MailAttachVal)

    def getDictFromObj(self, obj):
        return obj.toMailWealthDict()

mailAttachInstance = MailAttachInst()


class GlobalMailInst(object):
    def createObjFromDict(self, dataDict):
        _mailInfo = Mail.GlobalMail()
        _mailInfo.fromGlobalMailDict(dataDict)
        return _mailInfo

    def isSameType(self, obj):
        return isinstance(obj, Mail.GlobalMail)

    def getDictFromObj(self, obj):
        return obj.toGlobalMailDict()

globalMailInstance = GlobalMailInst()



