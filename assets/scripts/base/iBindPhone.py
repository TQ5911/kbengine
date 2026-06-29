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
import LogTrackingMgr
import login_set as LSD

class IBindPhone(object):
    def __init__(self):
        LOG_DBG("IBindPhone init")

    def bindPhoneOnLogin(self):
        LOG_DBG("IBindPhone bindPhoneOnLogin", self.accountEntity.phone, self.accountEntity.devicePlatId)
        if self.checkDevicePlatId(self.accountEntity.devicePlatId):
            self.accountEntity.setDefaultPersistentMiscProp(gameconst.EntityPropsEnum.firstPcLoginTimestamp, utils.curTS())
        self.sendClaimPcLoginRewardInfo()

    def sendClaimPcLoginRewardInfo(self):
        firstTimestamp = self.accountEntity.getPersistentMiscProp(gameconst.EntityPropsEnum.firstPcLoginTimestamp, 0)
        claimTimestamp = self.accountEntity.getPersistentMiscProp(gameconst.EntityPropsEnum.claimPcLoginRewardTimestamp, 0)
        LOG_INFO("IBindPhone sendClaimPcLoginRewardInfo", firstTimestamp, claimTimestamp, self.accountEntity.devicePlatId)
        self.client.claimPcLoginRewardInfo(firstTimestamp, claimTimestamp)

    def isUnlocked(self, type):
        if not iWelfareSignIn.IWelfareSignIn.checkUnlock(self, iWelfareSignIn.tagClassIDS[type]):
            LOG_WARN('IBindPhone isUnlocked: not lock', type)
            return False

        return True

    def checkValidPhoneNumber(self, phone):
        '''
        phoneStr = str(phone)
        if len(phoneStr) != 11:
            LOG_WARN("IBindPhone checkValidPhoneNumber error1", phoneStr)
            self.onMessagePre(MMD.datas.phoneInvalid, [])
            return False
        if phoneStr[0] != '1':
            LOG_WARN("IBindPhone checkValidPhoneNumber error2", phoneStr)
            self.onMessagePre(MMD.datas.phoneInvalid, [])
            return False 
        return True
        '''
        if 13000000000 <= phone <= 19999999999:
            return True

        LOG_WARN("IBindPhone checkValidPhoneNumber error", phone)
        self.onMessagePre(MMD.datas.phoneInvalid, [])
        return False

    def controlReqLimit(self):
        now = utils.curTS()
        reqBindPhoneTimestamp = self.getTempMiscProp(gameconst.EntityPropsEnum.reqBindPhoneTimestamp, 0)
        LOG_DBG("IBindPhone ", reqBindPhoneTimestamp, now)
        if reqBindPhoneTimestamp > now:
            LOG_WARN("IBindPhone controlReqLimit warning")
            self.onMessagePre(MMD.datas.web_requestException, [])
            return True
        # 放宽频率
        self.setTempMiscProp(gameconst.EntityPropsEnum.reqBindPhoneTimestamp, now + 1)

        resetTime = self.accountEntity.getPersistentMiscProp(gameconst.EntityPropsEnum.resetBindPhoneCntTime, 0)
        needSet = False
        if resetTime <= now:
            LOG_INFO("IBindPhone controlReqLimit reset")
            self.accountEntity.popPersistentMiscProp(gameconst.EntityPropsEnum.resetBindPhoneCntTime, 0)
            self.accountEntity.popPersistentMiscProp(gameconst.EntityPropsEnum.reqBindPhoneCnt, 0)
            needSet = True

        # 加大上限值
        curCnt = self.accountEntity.getPersistentMiscProp(gameconst.EntityPropsEnum.reqBindPhoneCnt, 0)
        LOG_INFO("IBindPhone controlReqLimit ", curCnt, utils.getCommonTimeStrFromTimeStamp(resetTime))
        maxCnt = LSD.datas['phoneFrequentLockTime']['value']
        if curCnt >= maxCnt:
            LOG_WARN("IBindPhone controlReqLimit cnt limit", curCnt, maxCnt)
            self.onMessagePre(MMD.datas.login_phoneFrequentLock, [])
            return True
        
        self.accountEntity.setPersistentMiscProp(gameconst.EntityPropsEnum.reqBindPhoneCnt, curCnt + 1)
        if needSet:
            startTimeCron, _ = utils.nextByCronTupleList([[[0], [5], [], [], [], []]], now)
            nextResetTime = now + startTimeCron
            self.accountEntity.setPersistentMiscProp(gameconst.EntityPropsEnum.resetBindPhoneCntTime, nextResetTime)
            LOG_INFO("IBindPhone controlReqLimit next reset timestamp", curCnt, nextResetTime)

        return False

    def getTempPhone(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.tempBindPhone, 0)

    def setTempPhone(self, phone):
        self.setTempMiscProp(gameconst.EntityPropsEnum.tempBindPhone, phone)

    def popTempPhone(self):
        self.popTempMiscProp(gameconst.EntityPropsEnum.tempBindPhone, 0)

    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    @gamedecorator.checkGameconfigEnable(UVVD.datas.get('phoneBind', {}).get('type', 'welfare'))
    def reqBindPhone(self, exposed, phone, verifyParam):
        LOG_INFO("IBindPhone reqBindPhone", phone, self.gbID, self.accountName, self.accountEntity.webToken)
        if self.accountType != centralLogin.ACCOUNT_TAPTAP:
            LOG_WARN("IBindPhone reqBindPhone channel error", self.accountType, self.accountName, centralLogin.ACCOUNT_TAPTAP)
            return
        if self.accountEntity.phone != 0:
            LOG_WARN("IBindPhone reqBindPhone alerady bind", self.accountEntity.phone)
            return
        if not self.isUnlocked('phoneBind'):
            return
        if not self.checkValidPhoneNumber(phone):
            return
        if self.controlReqLimit():
            return

        url = gameconfig.tapTapBindPhoneReqUrl()
        message = json.dumps({
            "phone"         : str(phone),
            "loginType"     : int(centralLogin.THIRD_LOGIN_TAPTAP),
            "gameId"        : str(gameconfig.gameId()),
            "userGameId"    : str(self.accountName),
            "captchaVerifyParam": str(verifyParam),
            "deviceId"      : str(self.accountEntity.deviceId)
        })
        self.setTempPhone(phone)
        LOG_INFO("IBindPhone reqBindPhone url", url, message)
        KBEngine.urlopenv2(url, self._reqBindPhoneResponse, method='POST',
                postData=message.encode('utf-8'),
                headers={"Content-Type": "application/json", "satoken": self.accountEntity.webToken},
                timeoutSec=5)

    def _reqBindPhoneResponse(self, httpCode, jsonData, headers, success, *args):
        LOG_INFO("IBindPhone _reqBindPhoneResponse", httpCode, jsonData, headers, success)
        #即便回复了也先限制下
        #self.popTempMiscProp(gameconst.EntityPropsEnum.reqBindPhoneTimestamp, 0)
        if not (httpCode == 200 and success):
            self.onMessagePre(MMD.datas.web_requestException, [])
            LOG_ERR("IBindPhone _reqBindPhoneResponse failed")
            return

        data = json.loads(jsonData)
        code = data['code']
        if code == 200 or code == 202:
            self.onMessagePre(MMD.datas.smsSentSuccess, [])
            LOG_INFO("IBindPhone _reqBindPhoneResponse success ", self.getTempPhone())
        elif code == 1002 or code == 1003:
            curCnt = self.accountEntity.getPersistentMiscProp(gameconst.EntityPropsEnum.reqBindPhoneCnt, 0)
            curCnt = max(int(curCnt - 1), 0)
            self.accountEntity.setPersistentMiscProp(gameconst.EntityPropsEnum.reqBindPhoneCnt, curCnt)
            self.onMessagePre(MMD.datas.login_phoneRepeat, [])
        elif code == 4005:
            curCnt = self.accountEntity.getPersistentMiscProp(gameconst.EntityPropsEnum.reqBindPhoneCnt, 0)
            curCnt = max(int(curCnt - 1), 0)
            self.accountEntity.setPersistentMiscProp(gameconst.EntityPropsEnum.reqBindPhoneCnt, curCnt)
            self.client.bindPhoneReplay(gameconst.BindPhoneRes.CHECK_CAPTCHA_VERIF, self.getTempPhone())
        else:
            LOG_WARN("IBindPhone _reqBindPhoneResponse exception")
            self.onMessagePre(MMD.datas.web_requestException, [])

    def checkValidVerifyCode(self, code):
        codeStr = str(code)
        if len(codeStr) != 6:
            LOG_WARN("IBindPhone checkValidVerifyCod error1", codeStr)
            self.onMessagePre(MMD.datas.smsInvalid, [])
            return False

        return True

    def controlVerifyLimit(self):
        LOG_INFO("IBindPhone controlVerifyLimit")
        now = utils.curTS()
        verifyCodeTimestamp = self.getTempMiscProp(gameconst.EntityPropsEnum.verifyCodeTimestamp, 0)
        if verifyCodeTimestamp > now:
            LOG_WARN("IBindPhone controlVerifyLimit warning")
            self.onMessagePre(MMD.datas.web_frequentRequests, [])
            return True

        self.setTempMiscProp(gameconst.EntityPropsEnum.verifyCodeTimestamp, now + 3)
        return False

    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    @gamedecorator.checkGameconfigEnable(UVVD.datas.get('phoneBind', {}).get('type', 'welfare'))
    def reqVerifyCode(self, exposed, code):
        LOG_INFO("IBindPhone reqVerifyCode", code, self.gbID, self.accountName)
        if self.accountEntity.phone != 0:
            LOG_WARN("IBindPhone reqVerifyCode alerady bind", self.accountEntity.phone)
            return
        if not self.isUnlocked('phoneBind'):
            return
        if not self.getTempPhone():
            LOG_WARN("IBindPhone reqVerifyCode reqbind first")
            return
        if not self.checkValidVerifyCode(code):
            return
        if self.controlVerifyLimit():
            return

        url = gameconfig.tapTapBindPhoneVerifyUrl()
        message = json.dumps({
            "phone"         : str(self.getTempPhone()),
            "code"          : str(code),
            "loginType"     : int(centralLogin.THIRD_LOGIN_TAPTAP),
            "gameId"        : str(gameconfig.gameId()),
        })
        LOG_INFO("IBindPhone reqVerifyCode url", url, message)
        KBEngine.urlopenv2(url, self._reqVerifyCodeResponse, method='POST',
                postData=message.encode('utf-8'),
                headers={"Content-Type": "application/json", "satoken": self.accountEntity.webToken},
                timeoutSec=5)

    def _reqVerifyCodeResponse(self, httpCode, jsonData, headers, success, *args):
        LOG_INFO("IBindPhone _reqVerifyCodeResponse", httpCode, jsonData, headers, success)
        # 即便回复了也先限制下
        #self.popTempMiscProp(gameconst.EntityPropsEnum.verifyCodeTimestamp, 0)
        if not (httpCode == 200 and success):
            self.onMessagePre(MMD.datas.web_requestException, [])
            LOG_ERR("IBindPhone _reqVerifyCodeResponse failed")
            return

        data = json.loads(jsonData)
        code = data['code']
        if code == 200:
            self.accountEntity.phone = self.getTempPhone()
            self.accountEntity.pyWriteToDB()
            self.client.bindPhoneReplay(gameconst.BindPhoneRes.BIND_SUCCESSED, self.accountEntity.phone)
            self.popTempPhone()
            self.onMessagePre(MMD.datas.login_phoneSuccess, [])
            LOG_INFO("IBindPhone _reqVerifyCodeResponse success ", self.accountEntity.phone)
        elif code == 1002 or code == 1003:
            self.onMessagePre(MMD.datas.login_phoneRepeat, [])
        else:
            self.onMessagePre(MMD.datas.smsInvalid, [])
#####################################################################################
    def checkDevicePlatId(self, devicePlatId):
        LOG_INFO("IBindPhone checkDevicePlatId", devicePlatId)
        return devicePlatId in (gameconst.DevicePlatId.PC_CLIENT, )
    
    @AuthClsWraper.onlyHost
    @gamedecorator.checkGameconfigEnable('welfare_pcLogin')
    def reqClaimPcLoginReward(self, exposed):
        LOG_INFO("IBindPhone reqClaimPcLoginReward", self.gbID, self.accountName)
        claimTimestamp = self.accountEntity.getPersistentMiscProp(gameconst.EntityPropsEnum.claimPcLoginRewardTimestamp, 0)
        if claimTimestamp != 0:
            LOG_WARN("IBindPhone reqClaimPcLoginReward alerady claim", claimTimestamp)
            return
        if not self.isUnlocked('PcLoginReward'):
            return
        if not self.checkDevicePlatId(self.accountEntity.devicePlatId):
            return

        claimTimestamp = utils.curTS()
        self.accountEntity.setPersistentMiscProp(gameconst.EntityPropsEnum.claimPcLoginRewardTimestamp, claimTimestamp)

        self.sendClaimPcLoginRewardInfo()

        opUUID = KBEngine.genUUID64()
        LogTrackingMgr.LogTrackingMgr.Welfare_PcDrainage(
            self.gbID,
            self.accountEntity.clientDistinctId,
            self.accountName,
            self.gbID,
            self.accountEntity.devicePlatId,
            claimTimestamp,
            opUUID,
        )

        rewardId = W_CDD.datas.get('PcLoginReward', {}).get('value', 0)
        if not rewardId:
            LOG_ERR('IBindPhone reqClaimPcLoginReward: no reward')
            return

        awardCtx = self.getAvatarAwardCtx(rewardId, None)
        detail = gameclass.AwardDetailCls(claimTimestamp=claimTimestamp)
        self.addAwards(AAC_AACDD.datas.BONUS_SRC_WELFARE_PCDRAINAGE, rewardId, 1, opUUID, detail, awardCtx)
#####################################################################################
    def controlQueryRechargeLimit(self):
        LOG_INFO("IBindPhone::controlQueryRechargeLimit")
        now = utils.curTS()
        queryRechargeTimestamp = self.getTempMiscProp(gameconst.EntityPropsEnum.queryRechargeTimestamp, 0)
        if queryRechargeTimestamp > now:
            LOG_WARN("IBindPhone::controlQueryRechargeLimit")
            self.onMessagePre(MMD.datas.frequentRequests_tryLater, [])
            return True

        self.setTempMiscProp(gameconst.EntityPropsEnum.queryRechargeTimestamp, now + 3)
        return False

    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('welfare_refundRecharge')
    def reqQueryRecharge(self, exposed):
        LOG_INFO("IBindPhone::reqQueryRecharge")
        if self.controlQueryRechargeLimit():
            return

        url = gameconfig.queryRechargeUrl()
        params = "?userGameId=" + str(self.accountName)
        url += params
        LOG_INFO("IBindPhone::reqQueryRecharge url, message", url)
        KBEngine.urlopenv2(url, self._reqQueryRechargeResponse, method='GET',
                headers={"satoken": self.accountEntity.webToken},
                timeoutSec=5)

    def _reqQueryRechargeResponse(self, httpCode, jsonData, headers, success, *args):
        LOG_INFO("IBindPhone::_reqQueryRechargeResponse", httpCode, jsonData, headers, success)
        if not (httpCode == 200 and success):
            self.onMessagePre(MMD.datas.web_requestException, [])
            LOG_ERR("IBindPhone::_reqQueryRechargeResponse failed")
            return

        data = json.loads(jsonData)
        code = data['code']
        if code == 0:
            rechargeAmount = float(data['data'])
            self.client.queryRechargeAmountReplay(rechargeAmount)
            LOG_INFO("IBindPhone::_reqQueryRechargeResponse success ", rechargeAmount)
        else:
            self.onMessagePre(MMD.datas.web_requestException, [])
            LOG_WARN("IBindPhone::_reqQueryRechargeResponse exception")