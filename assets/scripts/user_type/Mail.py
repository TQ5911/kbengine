# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *
import utils
import userType
import dropAward
import dataUtils
import gameconst
import _pickle as cPickle
import mailAssistor
import mail_mail as MAMAD
import mail_config as MACF


class GlobalMail(userType.UserSoleType):
    def __init__(self):
        self.globalMailGBID = 0
        self.mailId = 0
        self.despArgs = []
        self.createTime = 0
        self.expiredTime = 0
        self.minRoleTime = 0
        self.maxRoleTime = 0
        self.minRoleLevel = 0
        self.maxRoleLevel = 0
        self.extraAttach = dropAward.MailWealthVal()
        self.title = ''
        self.cont = ''

    def _lateReload(self):
        super(GlobalMail, self)._lateReload()
        self.extraAttach.reloadScript()
        return

    def initNewGlobalMail(self, mailId, extraAttach:dropAward.MailWealthVal, despArgs, title, cont, minRoleTime,
                          maxRoleTime, minRoleLevel, maxRoleLevel):
        self.globalMailGBID = KBEngine.genUUID64()
        self.mailId = mailId
        self.despArgs = despArgs if despArgs else []
        self.createTime = utils.getNow()
        self.minRoleTime = minRoleTime
        self.maxRoleTime = maxRoleTime
        self.minRoleLevel = minRoleLevel
        self.maxRoleLevel = maxRoleLevel
        self.expiredTime = mailAssistor.calcMailExpiredTime(mailId, utils.getNow())
        self.extraAttach = extraAttach if extraAttach else dropAward.MailWealthVal()
        self.title = title
        self.cont = cont
        return

    def fromGlobalMailDict(self, dataDic):
        self.globalMailGBID = dataDic['globalMailGBID']
        self.mailId = dataDic['mailId']
        self.despArgs = dataDic.get('despArgs', [])
        self.createTime = dataDic['createTime']
        self.expiredTime = dataDic['expiredTime']
        self.minRoleTime = dataDic['minRoleTime']
        self.maxRoleTime = dataDic['maxRoleTime']
        self.minRoleLevel = dataDic['minRoleLevel']
        self.maxRoleLevel = dataDic['maxRoleLevel']
        self.extraAttach = dataDic.get('extraAttach', None)
        if self.extraAttach is None:
            self.extraAttach = dropAward.MailWealthVal()
        self.title = dataDic.get('title', '')
        self.cont = dataDic.get('cont', '')
        return

    def toGlobalMailDict(self):
        return {
            'globalMailGBID':self.globalMailGBID,
            'mailId':self.mailId,
            'despArgs':self.despArgs,
            'createTime':self.createTime,
            'expiredTime':self.expiredTime,
            'minRoleTime':self.minRoleTime,
            'maxRoleTime':self.maxRoleTime,
            'minRoleLevel':self.minRoleLevel,
            'maxRoleLevel':self.maxRoleLevel,
            'extraAttach':self.extraAttach,
            'title':self.title,
            'cont':self.cont,
        }

    def isExpired(self):
        return self.expiredTime <= utils.getNow()

    def isTracebackTimeOut(self):
        # 后创建账号也都能收到的邮件，需要考虑追溯期
        mailData = MAMAD.datas[self.mailId]
        if mailData['type'] != gameconst.MailType.GLOBAL_MAIL_INCLUDE_NEW_PLAYERS:
            return False

        return False


class MailCacheData(userType.UserSoleType):
    def __init__(self):
        self.lastGlobalMailTime = 0
        self.mails = {}
        self.globalMailsMap = {}
        self.newestMailCreateTime = 0

    def _lateReload(self):
        super(MailCacheData, self)._lateReload()
        for v in self.mails.values():
            v.reloadScript()
        return

    def resetMailCache(self):
        self.lastGlobalMailTime = 0
        self.globalMailsMap.clear()
        self.newestMailCreateTime = 0
        self.mails.clear()

    def isEmpty(self):
        return len(self.mails) == 0

    def mailGBIDListAtNewestCreateTime(self):
        return [mail.mailGBID for mail in self.mails.values() if mail.createTime == self.newestMailCreateTime]

    def mailSpaceLeft(self):
        mailMaxNum = MACF.datas['mailNumMax']['value']
        return mailMaxNum - len(self.mails)

    def getLastGlobalMailTime(self):
        return self.lastGlobalMailTime

    def setLastGlobalMailTime(self, lastGBMailTime):
        if lastGBMailTime > self.lastGlobalMailTime:
            self.lastGlobalMailTime = lastGBMailTime
        return

    def addNewMailCache(self, mail):
        if mail.mailGBID in self.mails:
            return False
        if mail.isExpired():
            return False

        self.mails[mail.mailGBID] = mail
        if mail.createTime > self.newestMailCreateTime:
            self.newestMailCreateTime = mail.createTime
        if mail.globalMailGBID > 0:
            self.globalMailsMap[mail.globalMailGBID] = mail.mailGBID
            if mail.createTime > self.lastGlobalMailTime:
                self.setLastGlobalMailTime(mail.createTime)
        return True

    def deleteMailsCache(self, mailGBIDList):
        rmMails ={}
        for mailGBID in mailGBIDList:
            mVal = self.mails.pop(mailGBID, None)
            if mVal:
                rmMails[mailGBID] = mVal

        return rmMails

    def getMailByGBID(self, mailGBID):
        return self.mails.get(mailGBID)

    def readMail(self, mailGBID):
        mail = self.getMailByGBID(mailGBID)
        if not mail:
            return
        mail.setReadState(gameconst.MailReadState.HasRead)
        return

    def setAttachHasGet(self, mailGBID):
        mail = self.getMailByGBID(mailGBID)
        mail and mail.setAttachState(gameconst.MailAttachState.HasGET)

    def getMailsWithAttachHasNotGet(self):
        attachMails = []
        for mail in self.mails.values():
            if not mail.canGetAttach():
                continue
            attachMails.append(mail)
        attachMails = sorted(attachMails, key=lambda mail:mail.createTime)
        return attachMails

    def getReplaceMailList(self, num):
        rmGBIDList = []
        mailSortList = sorted(list(self.mails.values()), key=lambda mail: (-1*mail.attachStat, -1*mail.readStat, mail.createTime))
        cordinateList = []
        for mail in mailSortList:
            if mail.readStat == gameconst.MailReadState.HasRead or mail.attachStat == gameconst.MailAttachState.HasGET:
                rmGBIDList.append(mail.mailGBID)
            else:
                cordinateList.append(mail.mailGBID)
            if len(rmGBIDList) == num:
                return rmGBIDList

        return rmGBIDList + cordinateList[:num-len(rmGBIDList)]

    def getMailListCanDelete(self):
        deleteMailGBIDList = []
        for oneMail in self.mails.values():
            if oneMail.isExpired():
                deleteMailGBIDList.append(oneMail.mailGBID)
                continue
            if oneMail.attachStat == gameconst.MailAttachState.NotGet:
                continue
            if oneMail.readStat == gameconst.MailReadState.NotRead:
                continue
            deleteMailGBIDList.append(oneMail.mailGBID)
        return deleteMailGBIDList

    def getClientMailList(self):
        mailList = []
        for oneMail in self.mails.values():
            mailList.append(oneMail.toMailClientDict())
        mailList = sorted(mailList, key=lambda oneMail: -1*oneMail['createTime'])
        mailMaxNum = MACF.datas['mailNumMax']['value']
        if len(mailList) > mailMaxNum:
            mailList = mailList[:mailMaxNum]
        return mailList


class Mail(userType.UserSoleType):
    def __init__(self):
        self.toGBID = 0
        self.mailId = 0
        self.mailGBID = 0
        self.globalMailGBID = 0
        self.readStat = gameconst.MailReadState.NotRead
        self.createTime = 0
        self.expiredTime = 0
        self.fromGBID = 0
        self.attach = dropAward.MailWealthVal()
        self.attachStat = gameconst.MailAttachState.NotGet
        self.despArgs = []
        self.title = ''
        self.cont = ''
        self.opUUID = 0
        self.srcType = 0
        self.srcSubType = 0
        self.desc = ''
        self.source = 0
        return

    def _lateReload(self):
        super(Mail, self)._lateReload()
        self.attach.reloadScript()
        return

    def setDespArgs(self, despArgsList):
        self.despArgs = [str(arg) for arg in despArgsList]
        return

    def initFromDBMailData(self, dbMailRowData):
        self.toGBID = int(dbMailRowData[0].decode())
        self.mailId = int(dbMailRowData[1].decode())
        self.mailGBID = int(dbMailRowData[2].decode())
        self.globalMailGBID = int(dbMailRowData[3].decode())
        self.readStat = int(dbMailRowData[4].decode())
        self.createTime = int(dbMailRowData[5].decode())
        self.expiredTime = int(dbMailRowData[6].decode())
        self.fromGBID = int(dbMailRowData[7].decode())
        self.attach = cPickle.loads(dbMailRowData[8])
        self.attachStat = int(dbMailRowData[9].decode())
        self.despArgs = cPickle.loads(dbMailRowData[10])
        self.title = dbMailRowData[11].decode()
        self.cont = dbMailRowData[12].decode()
        self.opUUID = int(dbMailRowData[13].decode())
        self.srcType = int(dbMailRowData[14].decode())
        self.srcSubType = int(dbMailRowData[15].decode())
        self.desc = dbMailRowData[16].decode()
        self.source = int(dbMailRowData[17].decode())

    def initFromSavedMailDict(self, dataDic):
        #DEBUG_MSG('in init initFromSavedMailDict:', dataDic)
        self.mailGBID = dataDic['mailGBID']
        self.mailId = dataDic['mailId']
        self.toGBID = dataDic['toGBID']
        self.fromGBID = dataDic['fromGBID']
        self.globalMailGBID = dataDic['globalMailGBID']
        self.attach = dataDic['attach']
        if self.attach is None:
            self.attach = dropAward.MailWealthVal()
        self.readStat = dataDic['readStat']
        self.attachStat = dataDic['attachStat']
        self.createTime = dataDic['createTime']
        self.expiredTime = dataDic['expiredTime']
        self.despArgs = dataDic.get('despArgs', [])
        self.title = dataDic.get('title', '')
        self.cont = dataDic.get('cont', '')
        self.opUUID = dataDic['opUUID']
        self.srcType = dataDic['srcType']
        self.srcSubType = dataDic['srcSubType']
        self.desc = dataDic['desc']
        self.source = dataDic['source']
        return

    def toMailSavedDict(self):
        return {
            'mailGBID':self.mailGBID,
            'mailId':self.mailId,
            'toGBID':self.toGBID,
            'fromGBID':self.fromGBID,
            'globalMailGBID':self.globalMailGBID,
            'attach':self.attach,
            'readStat':self.readStat,
            'attachStat':self.attachStat,
            'createTime':self.createTime,
            'expiredTime':self.expiredTime,
            'despArgs':self.despArgs,
            'title':self.title,
            'opUUID':self.opUUID,
            'srcType':self.srcType,
            'srcSubType':self.srcSubType,
            'desc':self.desc,
            'source':self.source,
        }

    def toMailClientDict(self):
        return {
            'mailGBID':self.mailGBID,
            'mailId':self.mailId,
            'toGBID':self.toGBID,
            'fromGBID':self.fromGBID,
            'globalMailGBID':self.globalMailGBID,
            'attach':self.attach,
            'readStat':self.readStat,
            'attachStat':self.attachStat,
            'createTime':self.createTime,
            'expiredTime':self.expiredTime,
            'despArgs':self.despArgs,
            'title': self.title,
            'cont': self.cont,
        }

    def isExpired(self):
        return self.expiredTime <= utils.getNow()

    def setReadState(self, state):
        self.readStat = state

    def setAttachState(self, state):
        if state != self.attachStat and state == gameconst.MailAttachState.NotGet:
            INFO_MSG('mail attach state reset not get:', self.toMailSavedDict())
        self.attachStat = state

    def canGetAttach(self):
        return not self.isExpired() and self.attachStat == gameconst.MailAttachState.NotGet

    def canDeleteMail(self):
        if self.canGetAttach():
            #有附件未领取，不能删除
            return False
        if self.readStat == gameconst.MailReadState.HasRead:
            #邮件尚未读取
            return False
        return True
