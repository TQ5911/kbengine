# coding: utf-8
from KBEDebug import *
import KBEngine
import gameconst
import gameclass
import dropAward
import gameengine
import gameglobal
import gamedecorator
import AuthClsWraper
import utils
import json
import gameconfig
import gametimer
import const_const as CONST
import message_Message_def as MMD
import proto.centralLogin_pb2 as centralLogin
import iWelfareSignIn
import visible_visible as UVVD
import welfare_config as W_CDD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

class IBindPhone(object):
    def __init__(self):
        DEBUG_MSG("IBindPhone init")

    def bindPhoneOnLogin(self):
        DEBUG_MSG("IBindPhone bindPhoneOnLogin", self.accountEntity.phone, self.accountEntity.devicePlatId)
        if self.checkDevicePlatId(self.accountEntity.devicePlatId):
            self.accountEntity.setDefaultPersistentMiscProp(gameconst.AvatarProps.firstPcLoginTimestamp, utils.getNow())
        self.sendClaimPcLoginRewardInfo()

    def sendClaimPcLoginRewardInfo(self):
        firstTimestamp = self.accountEntity.getPersistentMiscProp(gameconst.AvatarProps.firstPcLoginTimestamp, 0)
        claimTimestamp = self.accountEntity.getPersistentMiscProp(gameconst.AvatarProps.claimPcLoginRewardTimestamp, 0)
        DEBUG_MSG("IBindPhone sendClaimPcLoginRewardInfo", firstTimestamp, claimTimestamp, self.accountEntity.devicePlatId)
        self.client.claimPcLoginRewardInfo(firstTimestamp, claimTimestamp)

    def isUnlocked(self, type):
        if not iWelfareSignIn.IWelfareSignIn.checkUnlock(self, iWelfareSignIn.tagClassIDS[type]):
            WARNING_MSG('IBindPhone isUnlocked: not lock', type)
            return False

        return True

    def checkValidPhoneNumber(self, phone):
        '''
        phoneStr = str(phone)
        if len(phoneStr) != 11:
            WARNING_MSG("IBindPhone checkValidPhoneNumber error1", phoneStr)
            self.onMessagePre(MMD.datas.phoneInvalid, [])
            return False
        if phoneStr[0] != '1':
            WARNING_MSG("IBindPhone checkValidPhoneNumber error2", phoneStr)
            self.onMessagePre(MMD.datas.phoneInvalid, [])
            return False 
        return True
        '''
        if 13000000000 <= phone <= 19999999999:
            return True

        WARNING_MSG("IBindPhone checkValidPhoneNumber error", phone)
        self.onMessagePre(MMD.datas.phoneInvalid, [])
        return False

    def controlReqLimit(self):
        now = utils.getNow()
        reqBindPhoneTimestamp = self.getTempMiscProp(gameconst.AvatarProps.reqBindPhoneTimestamp, 0)
        DEBUG_MSG("IBindPhone ", reqBindPhoneTimestamp, now)
        if reqBindPhoneTimestamp > now:
            WARNING_MSG("IBindPhone controlReqLimit warning")
            self.onMessagePre(MMD.datas.web_requestException, [])
            return True
        self.setTempMiscProp(gameconst.AvatarProps.reqBindPhoneTimestamp, now + 3)

        resetTime = self.accountEntity.getPersistentMiscProp(gameconst.AvatarProps.resetBindPhoneCntTime, 0)
        needSet = False
        if resetTime <= now:
            INFO_MSG("IBindPhone controlReqLimit reset")
            self.accountEntity.popPersistentMiscProp(gameconst.AvatarProps.resetBindPhoneCntTime, 0)
            self.accountEntity.popPersistentMiscProp(gameconst.AvatarProps.reqBindPhoneCnt, 0)
            needSet = True

        curCnt = self.accountEntity.getPersistentMiscProp(gameconst.AvatarProps.reqBindPhoneCnt, 0)
        INFO_MSG("IBindPhone controlReqLimit ", curCnt, utils.getTimeStrFromTimeStamp(resetTime))
        maxCnt = CONST.datas['phoneFrequentLockTime']['value']
        if curCnt >= maxCnt:
            WARNING_MSG("IBindPhone controlReqLimit cnt limit", curCnt, maxCnt)
            self.onMessagePre(MMD.datas.login_phoneFrequentLock, [])
            return True
        
        self.accountEntity.setPersistentMiscProp(gameconst.AvatarProps.reqBindPhoneCnt, curCnt + 1)
        if needSet:
            startTimeCron, _ = utils.nextByTimeTupleList([[[0], [5], [], [], [], []]], now)
            nextResetTime = now + startTimeCron
            self.accountEntity.setPersistentMiscProp(gameconst.AvatarProps.resetBindPhoneCntTime, nextResetTime)
            INFO_MSG("IBindPhone controlReqLimit next reset timestamp", curCnt, nextResetTime)

        return False

    def getTempPhone(self):
        return self.getTempMiscProp(gameconst.AvatarProps.tempBindPhone, 0)

    def setTempPhone(self, phone):
        self.setTempMiscProp(gameconst.AvatarProps.tempBindPhone, phone)

    def popTempPhone(self):
        self.popTempMiscProp(gameconst.AvatarProps.tempBindPhone, 0)

    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    @gamedecorator.checkGameconfigEnable(UVVD.datas.get('phoneBind', {}).get('type', 'welfare'))
    def reqBindPhone(self, exposed, phone):
        INFO_MSG("IBindPhone reqBindPhone", phone, self.gbID, self.accountName)
        if self.accountType != centralLogin.ACCOUNT_TAPTAP:
            WARNING_MSG("IBindPhone reqBindPhone channel error", self.accountType, self.accountName, centralLogin.ACCOUNT_TAPTAP)
            return
        if self.accountEntity.phone != 0:
            WARNING_MSG("IBindPhone reqBindPhone alerady bind", self.accountEntity.phone)
            return
        if not self.isUnlocked('phoneBind'):
            return
        if not self.checkValidPhoneNumber(phone):
            return
        if self.controlReqLimit():
            return

        url = gameconfig.tapTapBindPhoneReqUrl()
        message = json.dumps({"phone": str(phone)})
        self.setTempPhone(phone)
        DEBUG_MSG("IBindPhone reqBindPhone url", url, message)
        KBEngine.urlopenv2(url, self._reqBindPhoneResponse, method='POST',
                postData=message.encode('utf-8'),
                headers={"Content-Type": "application/json"},
                timeoutSec=5)

    def _reqBindPhoneResponse(self, httpCode, jsonData, headers, success, *args):
        INFO_MSG("IBindPhone _reqBindPhoneResponse", httpCode, jsonData, headers, success)
        #即便回复了也先限制下
        #self.popTempMiscProp(gameconst.AvatarProps.reqBindPhoneTimestamp, 0)
        if not (httpCode == 200 and success):
            self.onMessagePre(MMD.datas.web_requestException, [])
            ERROR_MSG("IBindPhone _reqBindPhoneResponse failed")
            return

        data = json.loads(jsonData)
        code = data['code']
        if code == 200 or code == 202:
            self.onMessagePre(MMD.datas.smsSentSuccess, [])
        elif code == 1002 or code == 1003:
            curCnt = self.accountEntity.getPersistentMiscProp(gameconst.AvatarProps.reqBindPhoneCnt, 0)
            curCnt = max(int(curCnt - 1), 0)
            self.accountEntity.setPersistentMiscProp(gameconst.AvatarProps.reqBindPhoneCnt, curCnt)
            self.onMessagePre(MMD.datas.login_phoneRepeat, [])
        else:
            WARNING_MSG("IBindPhone _reqBindPhoneResponse exception")
            self.onMessagePre(MMD.datas.web_requestException, [])

    def checkValidVerifyCode(self, code):
        codeStr = str(code)
        if len(codeStr) != 6:
            WARNING_MSG("IBindPhone checkValidVerifyCod error1", codeStr)
            self.onMessagePre(MMD.datas.smsInvalid, [])
            return False

        return True

    def controlVerifyLimit(self):
        INFO_MSG("IBindPhone controlVerifyLimit")
        now = utils.getNow()
        verifyCodeTimestamp = self.getTempMiscProp(gameconst.AvatarProps.verifyCodeTimestamp, 0)
        if verifyCodeTimestamp > now:
            WARNING_MSG("IBindPhone controlVerifyLimit warning")
            self.onMessagePre(MMD.datas.web_frequentRequests, [])
            return True

        self.setTempMiscProp(gameconst.AvatarProps.verifyCodeTimestamp, now + 3)
        return False

    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    @gamedecorator.checkGameconfigEnable(UVVD.datas.get('phoneBind', {}).get('type', 'welfare'))
    def reqVerifyCode(self, exposed, code):
        INFO_MSG("IBindPhone reqVerifyCode", code, self.gbID, self.accountName)
        if self.accountEntity.phone != 0:
            WARNING_MSG("IBindPhone reqVerifyCode alerady bind", self.accountEntity.phone)
            return
        if not self.isUnlocked('phoneBind'):
            return
        if not self.getTempPhone():
            WARNING_MSG("IBindPhone reqVerifyCode reqbind first")
            return
        if not self.checkValidVerifyCode(code):
            return
        if self.controlVerifyLimit():
            return

        url = gameconfig.tapTapBindPhoneVerifyUrl()
        message = json.dumps({"phone": str(self.getTempPhone()), "code": str(code)})
        DEBUG_MSG("IBindPhone reqVerifyCode url", url, message)
        KBEngine.urlopenv2(url, self._reqVerifyCodeResponse, method='POST',
                postData=message.encode('utf-8'),
                headers={"Content-Type": "application/json"},
                timeoutSec=5)

    def _reqVerifyCodeResponse(self, httpCode, jsonData, headers, success, *args):
        INFO_MSG("IBindPhone _reqVerifyCodeResponse", httpCode, jsonData, headers, success)
        # 即便回复了也先限制下
        #self.popTempMiscProp(gameconst.AvatarProps.verifyCodeTimestamp, 0)
        if not (httpCode == 200 and success):
            self.onMessagePre(MMD.datas.web_requestException, [])
            ERROR_MSG("IBindPhone _reqVerifyCodeResponse failed")
            return

        data = json.loads(jsonData)
        code = data['code']
        if code == 200:
            self.accountEntity.phone = self.getTempPhone()
            self.accountEntity.pyWriteToDB()
            self.client.bindPhoneReplay(True, self.accountEntity.phone)
            self.popTempPhone()
            self.onMessagePre(MMD.datas.login_phoneSuccess, [])
        elif code == 1002 or code == 1003:
            self.onMessagePre(MMD.datas.login_phoneRepeat, [])
        else:
            self.onMessagePre(MMD.datas.smsInvalid, [])
#####################################################################################
    def checkDevicePlatId(self, devicePlatId):
        DEBUG_MSG("IBindPhone checkDevicePlatId", devicePlatId)
        return devicePlatId in (gameconst.DevicePlatId.PC_CLIENT, )

    @AuthClsWraper.onlyHost
    @gamedecorator.checkGameconfigEnable(UVVD.datas.get('PcLoginReward', {}).get('type', 'welfare'))
    def reqClaimPcLoginReward(self, exposed):
        INFO_MSG("IBindPhone reqClaimPcLoginReward", self.gbID, self.accountName)
        claimTimestamp = self.accountEntity.getPersistentMiscProp(gameconst.AvatarProps.claimPcLoginRewardTimestamp, 0)
        if claimTimestamp != 0:
            WARNING_MSG("IBindPhone reqClaimPcLoginReward alerady claim", claimTimestamp)
            return
        if not self.isUnlocked('PcLoginReward'):
            return
        if not self.checkDevicePlatId(self.accountEntity.devicePlatId):
            return

        self.accountEntity.setPersistentMiscProp(gameconst.AvatarProps.claimPcLoginRewardTimestamp, utils.getNow())

        rewardId = W_CDD.datas.get('PcLoginReward', {}).get('value', 0)
        if not rewardId:
            WARNING_MSG('IBindPhone reqClaimPcLoginReward: no reward')
            return False

        awardCtx = self._getAvatarAwardCtx(rewardId, None)
        detail = gameclass.AwardDetail(claimTimestamp=claimTimestamp)
        opUUID = KBEngine.genUUID64()
        self.addAwards(AAC_AACDD.datas.BONUS_SRC_WELFARE_SIGN_IN, rewardId, 1, opUUID, detail, awardCtx)

        self.sendClaimPcLoginRewardInfo()
