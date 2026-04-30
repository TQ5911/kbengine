# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *

import utils
import dataUtils
import userType
import dropAward
import gameconst
import _pickle as cPickle
import mailAssistor

import LogTrackingMgr

import mail_config as MACF


class GlobalMail(userType.UserSingleType):
    def __init__(self):
        self.globalMailGBID = 0
        self.mailId = 0
        self.despArgs = []
        self.createTime = 0
        self.expiredTime = 0
        self.minRoleTime = 0
        self.maxRoleTime = 0
        self.dueTime = 0
        self.minRoleLevel = 0
        self.maxRoleLevel = 0
        self.extraAttach = dropAward.MailWealthVal()
        self.title = ''
        self.cont = ''
        self.channel = 0
        self.srcType = 0

    def _lateReload(self):
        super(GlobalMail, self)._lateReload()
        self.extraAttach.reloadScript()
        return

    def initNewGlobalMail(self, mailId, extraAttach:dropAward.MailWealthVal, despArgs, title, cont, 
                          minRoleTime, maxRoleTime, dueTime, minRoleLevel, maxRoleLevel, channel, srcType):
        self.globalMailGBID = KBEngine.genUUID64()
        self.mailId = mailId
        self.despArgs = despArgs if despArgs else []
        self.createTime = utils.curTS()
        self.minRoleTime = minRoleTime
        self.maxRoleTime = maxRoleTime
        self.dueTime = dueTime
        self.minRoleLevel = minRoleLevel
        self.maxRoleLevel = maxRoleLevel
        self.expiredTime = mailAssistor.calcMailExpiredTime(mailId, utils.curTS())
        self.extraAttach = extraAttach if extraAttach else dropAward.MailWealthVal()
        self.title = title
        self.cont = cont
        self.channel = channel
        self.srcType = srcType

    def fromGlobalMailDict(self, dataDic):
        self.globalMailGBID = dataDic['globalMailGBID']
        self.mailId = dataDic['mailId']
        self.despArgs = dataDic.get('despArgs', [])
        self.createTime = dataDic['createTime']
        self.expiredTime = dataDic['expiredTime']
        self.minRoleTime = dataDic['minRoleTime']
        self.maxRoleTime = dataDic['maxRoleTime']
        self.dueTime = dataDic.get('dueTime', 0)
        self.minRoleLevel = dataDic['minRoleLevel']
        self.maxRoleLevel = dataDic['maxRoleLevel']
        self.extraAttach = dataDic.get('extraAttach', None)
        if self.extraAttach is None:
            self.extraAttach = dropAward.MailWealthVal()
        self.title = dataDic.get('title', '')
        self.cont = dataDic.get('cont', '')
        self.channel = dataDic.get('channel', 0)
        self.srcType = dataDic.get('srcType', 0)
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
            'dueTime':self.dueTime,
            'minRoleLevel':self.minRoleLevel,
            'maxRoleLevel':self.maxRoleLevel,
            'extraAttach':self.extraAttach,
            'title':self.title,
            'cont':self.cont,
            'channel': self.channel,
            'srcType': self.srcType,
        }

    def isExpired(self):
        return self.expiredTime <= utils.curTS()

    def isTracebackTimeOut(self):
        # 后创建账号也都能收到的邮件，需要考虑追溯期
        return dataUtils.checkMailType(self.mailId, gameconst.MailType.GLOBAL_MAIL_INCLUDE_NEW_PLAYERS)
    
    def isForOldPlayer(self):
        # 只给已创建账号的老玩家发
        return dataUtils.checkMailType(self.mailId, gameconst.MailType.GLOBAL_MAIL_EXCLUDE_NEW_PLAYERS)

class MailCacheData(userType.UserSingleType):
    def __init__(self):
        self.lastGlobalMailTime = 0
        self.mails = {}
        self.globalMailsMap = {}
        self.lastPlayerMailTime = 0

    def _lateReload(self):
        super(MailCacheData, self)._lateReload()
        for v in self.mails.values():
            v.reloadScript()
        return

    def resetMailCache(self):
        self.lastGlobalMailTime = 0
        self.globalMailsMap.clear()
        self.lastPlayerMailTime = 0
        self.mails.clear()

    def isEmpty(self):
        return len(self.mails) == 0

    def mailGBIDListAtNewestCreateTime(self, isGlobal):
        rets = []
        for mail in self.mails.values():
            if isGlobal:
                if mail.globalMailGBID > 0 and mail.createTime == self.lastGlobalMailTime:
                    rets.append(mail.mailGBID)
            else:
                if mail.globalMailGBID == 0 and mail.createTime == self.lastPlayerMailTime:
                    rets.append(mail.mailGBID)
        return rets

    def playerMailSpaceLeft(self):
        maxPlayerMailNum = MACF.datas['mailNumMax']['value']
        return maxPlayerMailNum - (len(self.mails) - len(self.globalMailsMap))
    
    def systemMailSpaceLeft(self):
        globalMailCount = len(self.globalMailsMap)
        maxSystemMailNum = MACF.datas['mailNumMax2']['value']
        return maxSystemMailNum - globalMailCount

    def getLastGlobalMailTime(self):
        return self.lastGlobalMailTime

    def setLastGlobalMailTime(self, lastMailTime):
        if lastMailTime > self.lastGlobalMailTime:
            self.lastGlobalMailTime = lastMailTime
        return
    
    def setLastPlayerMailTime(self, lastMailTime):
        if lastMailTime > self.lastPlayerMailTime:
            self.lastPlayerMailTime = lastMailTime
        return
    
    def addNewMailCache(self, owner, mail):
        if mail.mailGBID in self.mails:
            return False
        if mail.isExpired() or not mail.isInLoginWindow(owner.tLoginBase):
            return False
        
        mail.clearDueTime()

        self.mails[mail.mailGBID] = mail

        if mail.globalMailGBID > 0:
            self.globalMailsMap[mail.globalMailGBID] = mail.mailGBID
            self.setLastGlobalMailTime(mail.createTime)
        else:
            self.setLastPlayerMailTime(mail.createTime)
        return True

    def deleteMailsCache(self, mailGBIDList):
        rmMails ={}
        for mailGBID in mailGBIDList:
            mVal = self.mails.pop(mailGBID, None)
            if not mVal:
                continue
            rmMails[mailGBID] = mVal
            if mVal.globalMailGBID <=0:
                continue
            self.globalMailsMap.pop(mVal.globalMailGBID, None)

        return rmMails

    def getMailByGBID(self, mailGBID):
        return self.mails.get(mailGBID)

    def readMail(self, avatar, mailGBID):
        mail = self.getMailByGBID(mailGBID)
        if not mail:
            return
        mail.setReadState(gameconst.MailReadState.HasRead)
        LogTrackingMgr.LogTrackingMgr.Mail_Read(avatar.gbID, mail.fromGBID, mail.mailId, mail.mailGBID, mail.globalMailGBID, mail.srcType, mail.srcSubType, mail.opUUID, mail.source, mail.attach)
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

    def getReplaceMailList(self, isGlobal):
        if isGlobal:
            num = self.systemMailSpaceLeft()
        else:
            num = self.playerMailSpaceLeft()

        if num >= 0:
            return []
        
        num = abs(num)
         
        globalMail = []
        playerMail = []
        mailSortList = sorted(list(self.mails.values()), key=lambda mail: (-1*mail.attachStat, -1*mail.readStat, mail.createTime))
        for mail in mailSortList:
            if mail.globalMailGBID > 0:
                globalMail.append(mail)
            else:
                playerMail.append(mail)

        if isGlobal:
            mailSortList = globalMail
        else:
            mailSortList = playerMail
                   
        rmGBIDList = []
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
            if oneMail.attachStat == gameconst.MailAttachState.NotGet:
                continue
            if oneMail.readStat == gameconst.MailReadState.NotRead:
                continue
            deleteMailGBIDList.append(oneMail.mailGBID)
        return deleteMailGBIDList

    def getClientMailList(self):
        mailList = []
        playerMailCount = 0
        globalMailCount = 0
        playerMailMaxNum = MACF.datas['mailNumMax']['value']
        globalMailMaxNum = MACF.datas['mailNumMax2']['value']
        mailSortList = sorted(list(self.mails.values()), key=lambda mail: (mail.attachStat, mail.readStat, -1*mail.createTime))
        for oneMail in mailSortList:
            if playerMailCount >= playerMailMaxNum \
                and globalMailCount >= globalMailMaxNum:
                break
            if oneMail.globalMailGBID > 0:
                if globalMailCount < globalMailMaxNum:
                    globalMailCount += 1
                    mailList.append(oneMail.toMailClientDict())
            else:
                if playerMailCount < playerMailMaxNum:
                    playerMailCount += 1
                    mailList.append(oneMail.toMailClientDict())
        return mailList

class Mail(userType.UserSingleType):
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
        self.dueTime = 0
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
        self.dueTime = int(dbMailRowData[5].decode())
        self.createTime = int(dbMailRowData[6].decode())
        self.expiredTime = int(dbMailRowData[7].decode())
        self.fromGBID = int(dbMailRowData[8].decode())
        # 对原先的旧数据格式做下兼容
        datas = cPickle.loads(dbMailRowData[9])
        if type(datas) is dict:
            mailAttach = dropAward.MailWealthVal()
            mailAttach.fromMailWealthDict(datas)
            self.attach = mailAttach
        else:
            self.attach = datas
        self.attachStat = int(dbMailRowData[10].decode())
        self.despArgs = cPickle.loads(dbMailRowData[11])
        self.title = dbMailRowData[12].decode()
        self.cont = dbMailRowData[13].decode()
        self.opUUID = int(dbMailRowData[14].decode())
        self.srcType = int(dbMailRowData[15].decode())
        self.srcSubType = int(dbMailRowData[16].decode())
        self.desc = dbMailRowData[17].decode()
        self.source = int(dbMailRowData[18].decode())

    def initFromSavedMailDict(self, dataDic):
        #LOG_DBG('in init initFromSavedMailDict:', dataDic)
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
        self.dueTime = dataDic.get('dueTime', 0)
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
            'dueTime':self.dueTime,
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
        return self.expiredTime <= utils.curTS()
    
    def isInLoginWindow(self, loginTime):
        if self.dueTime > 0 and loginTime > self.dueTime:
            return False
        return True

    def setReadState(self, state):
        self.readStat = state

    def setAttachState(self, state):
        if state != self.attachStat and state == gameconst.MailAttachState.NotGet:
            LOG_IFO('mail attach state reset not get:', self.toMailSavedDict())
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

    def clearDueTime(self):
        self.dueTime = 0

    def getDueTime(self):
        return self.dueTime