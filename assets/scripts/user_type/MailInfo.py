# -*- encoding:utf-8 -*-

from KBEDebug import *
import Mail
import dropAward


class MailInst(object):
    def createObjFromDict(self, dataDict):
        mailInfo = Mail.Mail()
        mailInfo.initFromSavedMailDict(dataDict)
        return mailInfo

    def getDictFromObj(self, obj):
        return obj.toMailSavedDict()

    def isSameType(self, obj):
        return isinstance(obj, Mail.Mail)

mailInstance = MailInst()

class MailAttachInst(object):
    def createObjFromDict(self, dataDict):
        mailAttach = dropAward.MailAttachVal()
        mailAttach.fromMailWealthDict(dataDict)
        return  mailAttach

    def getDictFromObj(self, obj):
        return obj.toMailWealthDict()

    def isSameType(self, obj):
        return isinstance(obj, dropAward.MailAttachVal)

mailAttachInstance = MailAttachInst()


class GlobalMailInst(object):
    def createObjFromDict(self, dataDict):
        mailInfo = Mail.GlobalMail()
        mailInfo.fromGlobalMailDict(dataDict)
        return mailInfo

    def getDictFromObj(self, obj):
        return obj.toGlobalMailDict()

    def isSameType(self, obj):
        return isinstance(obj, Mail.GlobalMail)

globalMailInstance = GlobalMailInst()



