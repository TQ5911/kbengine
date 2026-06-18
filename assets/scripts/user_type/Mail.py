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
        self.mailId = 0
        self.globalMailGBID = 0
        self.despArgs = []
        self.createTime = 0
        self.expiredTime = 0
        self.maxRoleTime = 0
        self.minRoleTime = 0
        self.dueTime = 0
        self.maxRoleLevel = 0
        self.minRoleLevel = 0
        self.extraAttach = dropAward.MailAttachVal()
        self.title = ''
        self.cont = ''
        self.channel = 0
        self.srcType = 0
        self.mailTag = 0

    def _lateReload(self):
        super(GlobalMail, self)._lateReload()
        self.extraAttach.reloadScript()

    def initNewGlobalMail(self, mailId, extraAttach:dropAward.MailAttachVal, despArgs, title, cont, 
                          minRoleTime, maxRoleTime, dueTime, minRoleLevel, maxRoleLevel, channel, srcType,
                          mailTag=0):
        self.mailId = mailId
        self.globalMailGBID = KBEngine.genUUID64()
        self.despArgs = despArgs if despArgs else []
        self.createTime = utils.curTS()
        self.maxRoleTime = maxRoleTime
        self.minRoleTime = minRoleTime
        self.dueTime = dueTime
        self.minRoleLevel = minRoleLevel
        self.maxRoleLevel = maxRoleLevel
        self.expiredTime = mailAssistor.calcMailExpiredTime(mailId, utils.curTS())
        self.extraAttach = extraAttach if extraAttach else dropAward.MailAttachVal()
        self.title = title
        self.cont = cont
        self.channel = channel
        self.srcType = srcType
        self.mailTag = mailTag

    def fromGlobalMailDict(self, dataDic):
        self.mailId = dataDic['mailId']
        self.globalMailGBID = dataDic['globalMailGBID']
        self.createTime = dataDic['createTime']
        self.despArgs = dataDic.get('despArgs', [])
        self.expiredTime = dataDic['expiredTime']
        self.maxRoleTime = dataDic['maxRoleTime']
        self.minRoleTime = dataDic['minRoleTime']
        self.dueTime = dataDic.get('dueTime', 0)
        self.minRoleLevel = dataDic['minRoleLevel']
        self.maxRoleLevel = dataDic['maxRoleLevel']
        _extraAttach = dataDic.get('extraAttach', None)
        if _extraAttach is None:
            self.extraAttach = dropAward.MailAttachVal()
        else:
            self.extraAttach = dropAward.MailAttachVal().fromMailWealthDict(_extraAttach)

        self.title = dataDic.get('title', '')
        self.cont = dataDic.get('cont', '')
        self.channel = dataDic.get('channel', 0)
        self.srcType = dataDic.get('srcType', 0)
        self.mailTag = dataDic.get('mailTag', 0)
        return

    def toGlobalMailDict(self):
        return {
            'mailId':self.mailId,
            'globalMailGBID':self.globalMailGBID,
            'despArgs':self.despArgs,
            'expiredTime':self.expiredTime,
            'createTime':self.createTime,
            'minRoleTime':self.minRoleTime,
            'maxRoleTime':self.maxRoleTime,
            'dueTime':self.dueTime,
            'minRoleLevel':self.minRoleLevel,
            'maxRoleLevel':self.maxRoleLevel,
            'extraAttach':self.extraAttach.toMailWealthDict(),
            'title':self.title,
            'cont':self.cont,
            'channel': self.channel,
            'srcType': self.srcType,
            "mailTag": self.mailTag
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
        for _v in self.mails.values():
            _v.reloadScript()

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
        _rmMails ={}
        for mailGBID in mailGBIDList:
            mVal = self.mails.pop(mailGBID, None)
            if not mVal:
                continue
            _rmMails[mailGBID] = mVal
            if mVal.globalMailGBID <=0:
                continue
            self.globalMailsMap.pop(mVal.globalMailGBID, None)

        return _rmMails

    def getMailByGBID(self, mailGBID):
        return self.mails.get(mailGBID)

    def readMail(self, avatar, mailGBID):
        _mail = self.getMailByGBID(mailGBID)
        if not _mail:
            return
        _mail.setReadState(gameconst.MailReadState.HasRead)
        LogTrackingMgr.LogTrackingMgr.Mail_Read(
            avatar.gbID, 
            avatar.accountEntity.clientDistinctId, 
            avatar.gbID, 
            _mail.fromGBID, 
            _mail.mailId, 
            _mail.mailGBID, 
            _mail.globalMailGBID, 
            _mail.srcType, 
            _mail.srcSubType, 
            _mail.opUUID, 
            _mail.source, 
            _mail.attach)

    def setAttachHasGet(self, mailGBID):
        _mail = self.getMailByGBID(mailGBID)
        if _mail:
            _mail.setAttachState(gameconst.MailAttachState.HasGET)

    def getMailsWithAttachHasNotGet(self):
        attachMails = []
        for _mail in self.mails.values():
            if not _mail.coudlGetAttach():
                continue
            attachMails.append(_mail)
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
                   
        _rmGBIDList = []
        cordinateList = []
        for _mail in mailSortList:
            if _mail.readStat == gameconst.MailReadState.HasRead or _mail.attachStat == gameconst.MailAttachState.HasGET:
                _rmGBIDList.append(_mail.mailGBID)
            else:
                cordinateList.append(_mail.mailGBID)
            if len(_rmGBIDList) == num:
                return _rmGBIDList

        return _rmGBIDList + cordinateList[:num-len(_rmGBIDList)]

    def getMailListCanDelete(self):
        deleteMailGBIDList = []
        for _oneMail in self.mails.values():
            if _oneMail.attachStat == gameconst.MailAttachState.NotGet:
                continue
            if _oneMail.readStat == gameconst.MailReadState.NotRead:
                continue
            deleteMailGBIDList.append(_oneMail.mailGBID)
        return deleteMailGBIDList

    def getClientMailList(self):
        mailList = []
        playerMailCount = 0
        globalMailCount = 0
        playerMailMaxNum = MACF.datas['mailNumMax']['value']
        globalMailMaxNum = MACF.datas['mailNumMax2']['value']
        mailSortList = sorted(list(self.mails.values()), key=lambda mail: (mail.attachStat, mail.readStat, -1*mail.createTime))
        for _oneMail in mailSortList:
            if playerMailCount >= playerMailMaxNum \
                and globalMailCount >= globalMailMaxNum:
                break
            if _oneMail.globalMailGBID > 0:
                if globalMailCount < globalMailMaxNum:
                    globalMailCount += 1
                    mailList.append(_oneMail.toMailClientDict())
            else:
                if playerMailCount < playerMailMaxNum:
                    playerMailCount += 1
                    mailList.append(_oneMail.toMailClientDict())
        return mailList

class Mail(userType.UserSingleType):
    def __init__(self):
        self.mailId = 0
        self.toGBID = 0
        self.mailGBID = 0
        self.globalMailGBID = 0
        self.readStat = gameconst.MailReadState.NotRead
        self.expiredTime = 0
        self.createTime = 0
        self.fromGBID = 0
        self.attach = dropAward.MailAttachVal()
        self.despArgs = []
        self.attachStat = gameconst.MailAttachState.NotGet
        self.title = ''
        self.cont = ''
        self.opUUID = 0
        self.srcSubType = 0
        self.srcType = 0
        self.desc = ''
        self.source = 0
        self.dueTime = 0

    def _lateReload(self):
        super(Mail, self)._lateReload()
        self.attach.reloadScript()

    def setDespArgs(self, despArgsList):
        self.despArgs = [str(arg) for arg in despArgsList]

    def initFromDBMailData(self, mailRowData):
        self.toGBID = int(mailRowData[0].decode())
        self.mailId = int(mailRowData[1].decode())
        self.mailGBID = int(mailRowData[2].decode())
        self.globalMailGBID = int(mailRowData[3].decode())
        self.readStat = int(mailRowData[4].decode())
        self.dueTime = int(mailRowData[5].decode())
        self.createTime = int(mailRowData[6].decode())
        self.expiredTime = int(mailRowData[7].decode())
        self.fromGBID = int(mailRowData[8].decode())
        # 对原先的旧数据格式做下兼容
        datas = cPickle.loads(mailRowData[9])
        if type(datas) is dict:
            mailAttach = dropAward.MailAttachVal()
            mailAttach.fromMailWealthDict(datas)
            self.attach = mailAttach
        else:
            self.attach = datas
        self.attachStat = int(mailRowData[10].decode())
        self.despArgs = cPickle.loads(mailRowData[11])
        self.title = mailRowData[12].decode()
        self.cont = mailRowData[13].decode()
        self.opUUID = int(mailRowData[14].decode())
        self.srcType = int(mailRowData[15].decode())
        self.srcSubType = int(mailRowData[16].decode())
        self.desc = mailRowData[17].decode()
        self.source = int(mailRowData[18].decode())

    def initFromSavedMailDict(self, dataDic):
        #LOG_DBG('in init initFromSavedMailDict:', dataDic)
        self.mailId = dataDic['mailId']
        self.mailGBID = dataDic['mailGBID']
        self.toGBID = dataDic['toGBID']
        self.globalMailGBID = dataDic['globalMailGBID']
        self.fromGBID = dataDic['fromGBID']
        self.attach = dataDic['attach']
        if self.attach is None:
            self.attach = dropAward.MailAttachVal()
        self.attachStat = dataDic['attachStat']
        self.readStat = dataDic['readStat']
        self.expiredTime = dataDic['expiredTime']
        self.createTime = dataDic['createTime']
        self.despArgs = dataDic.get('despArgs', [])
        self.cont = dataDic.get('cont', '')
        self.title = dataDic.get('title', '')
        self.srcType = dataDic['srcType']
        self.opUUID = dataDic['opUUID']
        self.srcSubType = dataDic['srcSubType']
        self.desc = dataDic['desc']
        self.dueTime = dataDic.get('dueTime', 0)
        self.source = dataDic['source']

    def toMailSavedDict(self):
        return {
            'mailId':self.mailId,
            'mailGBID':self.mailGBID,
            'toGBID':self.toGBID,
            'fromGBID':self.fromGBID,
            'attach':self.attach,
            'globalMailGBID':self.globalMailGBID,
            'readStat':self.readStat,
            'createTime':self.createTime,
            'attachStat':self.attachStat,
            'expiredTime':self.expiredTime,
            'despArgs':self.despArgs,
            'opUUID':self.opUUID,
            'title':self.title,
            'srcType':self.srcType,
            'srcSubType':self.srcSubType,
            'source':self.source,
            'desc':self.desc,
            'dueTime':self.dueTime,
        }

    def toMailClientDict(self):
        return {
            'mailId':self.mailId,
            'mailGBID':self.mailGBID,
            'toGBID':self.toGBID,
            'fromGBID':self.fromGBID,
            'attach':self.attach,
            'globalMailGBID':self.globalMailGBID,
            'readStat':self.readStat,
            'attachStat':self.attachStat,
            'createTime':self.createTime,
            'despArgs':self.despArgs,
            'expiredTime':self.expiredTime,
            'title': self.title,
            'cont': self.cont,
        }

    def isExpired(self):
        return self.expiredTime <= utils.curTS()
    
    def isInLoginWindow(self, loginTime):
        if self.dueTime > 0 and loginTime > self.dueTime:
            return False
        return True

    def setAttachState(self, state):
        if state != self.attachStat and state == gameconst.MailAttachState.NotGet:
            LOG_INFO('mail attach state reset not get:', self.toMailSavedDict())
        self.attachStat = state

    def setReadState(self, state):
        self.readStat = state

    def canDeleteMail(self):
        if self.coudlGetAttach():
            #有附件未领取，不能删除
            return False
        if self.readStat == gameconst.MailReadState.HasRead:
            #邮件尚未读取
            return False
        return True

    def coudlGetAttach(self):
        return not self.isExpired() and self.attachStat == gameconst.MailAttachState.NotGet

    def clearDueTime(self):
        self.dueTime = 0

    def getDueTime(self):
        return self.dueTime
