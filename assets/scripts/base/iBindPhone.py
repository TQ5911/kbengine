# coding: utf-8
from KBEDebug import *
import KBEngine
import urllib
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
import redisUtils
import login_set as LSD
import functools
import secondpwd_secondPwdFunction as SP_SPF
import secondpwd_secondPwdConfig as SP_SPC
import visible_visible as V_VD

class IBindPhone(object):
    def __init__(self):
        LOG_DBG("IBindPhone init")
        self.secondaryPwdVerityInfo.setDefault(
            True, 
            True, 
            0, 
            SP_SPF.datas.get(gameconst.SecondaryPasswordCheckType.USE_MONEY, {}).get('isOpen', True), 
            SP_SPC.datas.get('goldCostLimit', {}).get('value', (100, 2000))[0], 
            SP_SPF.datas.get(gameconst.SecondaryPasswordCheckType.USE_BIND_MONEY, {}).get('isOpen', True), 
            SP_SPC.datas.get('boundGoldCostLimit', {}).get('value', (100, 2000))[0], 
            SP_SPF.datas.get(gameconst.SecondaryPasswordCheckType.ITEM_WASH, {}).get('isOpen', True), 
            SP_SPF.datas.get(gameconst.SecondaryPasswordCheckType.ITEM_DISASSEMBLE, {}).get('isOpen', True), 
            SP_SPF.datas.get(gameconst.SecondaryPasswordCheckType.SALE_ITEM, {}).get('isOpen', True), 
            SP_SPF.datas.get(gameconst.SecondaryPasswordCheckType.RENTAL_ITEM, {}).get('isOpen', True)
        )

    def bindPhoneOnLogin(self):
        LOG_DBG("IBindPhone bindPhoneOnLogin", self.accountEntity.phone, self.accountEntity.devicePlatId)
        if self.checkDevicePlatId(self.accountEntity.devicePlatId):
            self.accountEntity.setDefaultPersistentMiscProp(gameconst.EntityPropsEnum.firstPcLoginTimestamp, utils.curTS())
        self.sendRechargeStageRewardInfo()

    def doAllBindPhoneInfo(self):
        LOG_DBG("IBindPhone::doAllBindPhoneInfo")
        now = utils.curTS()
        self.secondaryPwdVerityInfo.updateBeVerity(now, False, SP_SPC.datas.get('pwdFreeVerifyDurationMs', {}).get('value', ()))

        self.sendClaimPcLoginRewardInfo()
        self.sendSecondaryPasswordInfo()
        self.sendSecondaryPasswordVerityInfo()

    def sendClaimPcLoginRewardInfo(self):
        firstTimestamp = self.accountEntity.getPersistentMiscProp(gameconst.EntityPropsEnum.firstPcLoginTimestamp, 0)
        claimTimestamp = self.accountEntity.getPersistentMiscProp(gameconst.EntityPropsEnum.claimPcLoginRewardTimestamp, 0)
        LOG_INFO("IBindPhone sendClaimPcLoginRewardInfo", firstTimestamp, claimTimestamp, self.accountEntity.devicePlatId)
        self.client.claimPcLoginRewardInfo(firstTimestamp, claimTimestamp)

    def sendRechargeStageRewardInfo(self):
        LOG_INFO("IBindPhone sendRechargeStageRewardInfo")
        tierRewardConditionInfo = W_CDD.datas.get('tierRewardCondition', {}).get('value', ())
        num = len(tierRewardConditionInfo)
        if self.accountEntity.hasTempMiscProp(gameconst.EntityPropsEnum.rechargeStageReward):
            rechargeStageRewardInfo = self.accountEntity.getTempMiscProp(gameconst.EntityPropsEnum.rechargeStageReward, [0 for _ in range(num)])
            self.client.rechargeStageRewardInfo(rechargeStageRewardInfo)
        else:
            redisUtils.RedisUtils.getRechargeStageInfo(self.accountName, functools.partial(self.onGetRechargeStageRewardInfoCB, num))

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
        LOG_INFO("IBindPhone reqBindPhone", phone, self.gbID, self.accountName)
        if self.accountEntity.channelId != centralLogin.THIRD_LOGIN_TAPTAP:
            LOG_WARN("IBindPhone reqBindPhone channel error", self.accountType, self.accountName, centralLogin.THIRD_LOGIN_TAPTAP)
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
            self.client.bindPhoneReplay(gameconst.BindPhoneRes.ALERADY_SENT, self.getTempPhone())
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
        return devicePlatId in (gameconst.DevicePlatId.PC_CLIENT, gameconst.DevicePlatId.OSX)
    
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
        queryRechargeTimestamp = self.accountEntity.getTempMiscProp(gameconst.EntityPropsEnum.queryRechargeTimestamp, 0)
        if queryRechargeTimestamp > now:
            LOG_WARN("IBindPhone::controlQueryRechargeLimit cd")
            self.onMessagePre(MMD.datas.frequentRequests_tryLater, [])
            return True

        self.accountEntity.setTempMiscProp(gameconst.EntityPropsEnum.queryRechargeTimestamp, now + 3)
        return False

    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('welfare_refundRecharge')
    def reqQueryRecharge(self, exposed):
        LOG_INFO("IBindPhone::reqQueryRecharge")
        if self.controlQueryRechargeLimit():
            return

        url = gameconfig.queryRechargeUrl()
        _paramDic = {
            'userGameId': self.accountName,
        }
        _param = urllib.parse.urlencode(_paramDic, encoding='utf-8')
        url = f'{url}?{_param}'
        LOG_INFO("IBindPhone::reqQueryRecharge url:", url)
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
            self.accountEntity.setTempMiscProp(gameconst.EntityPropsEnum.rechargeAmount, rechargeAmount)
            LOG_INFO("IBindPhone::_reqQueryRechargeResponse success ", rechargeAmount)
        else:
            self.onMessagePre(MMD.datas.web_requestException, [])
            LOG_WARN("IBindPhone::_reqQueryRechargeResponse exception")

    @gamedecorator.limitcall(1)
    def reqGetRechargeStageReward(self, exposed, stage, rewardId):
        LOG_INFO("IBindPhone::reqGetRechargeStageReward", stage, rewardId, self.accountName)
        tierRewardConditionInfo = W_CDD.datas.get('tierRewardCondition', {}).get('value', ())
        num = len(tierRewardConditionInfo)
        if stage >= num:
            LOG_ERR("IBindPhone::reqGetRechargeStageReward stage error", stage)
            return
        tierRewardCondition = tierRewardConditionInfo[stage]
        if len(tierRewardCondition) != 2:
            LOG_ERR("IBindPhone::reqGetRechargeStageReward tierRewardCondition error")
            return
        condition = tierRewardCondition[0]
        rewards = tierRewardCondition[1]
        if type(rewards) is int:
            rewards = (rewards, )
        LOG_INFO("IBindPhone::reqGetRechargeStageReward condition, rewards", condition, rewards)
        if rewardId not in rewards:
            LOG_ERR("IBindPhone::reqGetRechargeStageReward reward error", rewardId, rewards)
            return

        if not self.accountEntity.hasTempMiscProp(gameconst.EntityPropsEnum.rechargeStageReward):
            LOG_ERR("IBindPhone::reqGetRechargeStageReward no rechargeStageReward data")
            return
        
        rechargeStageRewardInfo = self.accountEntity.getTempMiscProp(gameconst.EntityPropsEnum.rechargeStageReward, [0 for _ in range(num)])
        self.doGetRechargeStageReward(stage, condition, rewardId, rechargeStageRewardInfo, num)

    def onGetRechargeStageRewardInfoCB(self, num, cid, err, res):
        LOG_INFO("IBindPhone::onGetRechargeStageRewardInfoCB", num, cid, err, res)
        if err:
            LOG_ERR("IBindPhone::onGetRechargeStageRewardInfoCB error")
            return

        rechargeStageRewardInfo = [0 for _ in range(num)]
        if res:
            infoValueStr = str(res.decode('utf-8'))
            rechargeStageRewardInfo = self.redisValue2RechargeStageRewardInfo(infoValueStr)
            LOG_INFO("IBindPhone::onGetRechargeStageRewardInfoCB rechargeStageRewardInfo", infoValueStr, rechargeStageRewardInfo)
        LOG_INFO("IBindPhone::onGetRechargeStageRewardInfoCB rechargeStageRewardInfo2", rechargeStageRewardInfo)
        if not self.accountEntity.hasTempMiscProp(gameconst.EntityPropsEnum.rechargeStageReward):
            self.accountEntity.setTempMiscProp(gameconst.EntityPropsEnum.rechargeStageReward, rechargeStageRewardInfo)
        self.client.rechargeStageRewardInfo(rechargeStageRewardInfo)

    def onUpdateRechargeStageRewardInfoCB(self, ok, res):
        LOG_INFO("IBindPhone::onUpdateRechargeStageRewardInfoCB", ok, res)
        if not ok:
            LOG_ERR("IBindPhone::onUpdateRechargeStageRewardInfoCB error")
            return
    
    def doGetRechargeStageReward(self, stage, condition, rewardId, rechargeStageRewardInfo, num):
        LOG_INFO("IBindPhone::doGetRechargeStageReward", stage, condition, rewardId, rechargeStageRewardInfo, num)
        if rechargeStageRewardInfo[stage] != 0:
            LOG_WARN("IBindPhone::doGetRechargeStageReward alerady get stage", stage, rewardId, rechargeStageRewardInfo)
            return

        rechargeAmount = self.accountEntity.getTempMiscProp(gameconst.EntityPropsEnum.rechargeAmount, float(0))
        LOG_INFO("IBindPhone::doGetRechargeStageReward rechargeAmount", rechargeAmount)      
        #queryRechargeTimestamp = self.accountEntity.getTempMiscProp(gameconst.EntityPropsEnum.queryRechargeTimestamp, 0)
        if rechargeAmount < condition:
            LOG_WARN("IBindPhone::doGetRechargeStageReward not enough", rechargeAmount, condition)
            return

        rechargeStageRewardInfo[stage] =  rewardId
        self.accountEntity.setTempMiscProp(gameconst.EntityPropsEnum.rechargeStageReward, rechargeStageRewardInfo)
        redisUtils.RedisUtils.cmdSet(gameconst.RedisKey.RECHARGE_STAGE_INFO + self.accountName, self.rechargeStageRewardInfo2RedisValue(rechargeStageRewardInfo), self.onUpdateRechargeStageRewardInfoCB)
        detail = gameclass.AwardDetailCls()
        srcType = AAC_AACDD.datas.BONUS_SRC_WIPE_RECHARGE_REWARD
        awardVal = dropAward.AwardVal()
        awardVal.addWealthByItemId(rewardId, 1)
        awardCtx = self.getAvatarAwardCtx(0, None)
        self.addWealth(srcType, awardVal, KBEngine.genUUID64(), detail, awardCtx=awardCtx)
        self.client.rechargeStageRewardInfo(rechargeStageRewardInfo)

    @staticmethod
    def redisValue2RechargeStageRewardInfo(infoValueStr):
        info = [int(id) for id in infoValueStr.split(',')]
        return info
     
    @staticmethod
    def rechargeStageRewardInfo2RedisValue(info):
        infoValueStr = ','.join([str(id) for id in info])
        return infoValueStr
#############################################################################
    def controlReqSMSServiceLimit(self, key, cd):
        LOG_INFO("IBindPhone::controlReqSMSServiceLimit", key, cd)
        now = utils.curTS()
        reqSMSServiceTimestamp = self.getTempMiscProp(key, 0)
        if reqSMSServiceTimestamp > now:
            LOG_WARN("IBindPhone::controlReqSMSServiceLimit warning")
            self.onMessagePre(MMD.datas.frequentRequests_tryLater, [])
            return True

        self.setTempMiscProp(key, now + cd)
        return False

    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    def smsServiceSendCode(self, exposed, opType):
        LOG_INFO("IBindPhone::smsServiceSendCode", opType, self.accountEntity.accountType, self.accountName, self.accountEntity.phone)
        if self.accountEntity.accountType != centralLogin.ACCOUNT_OFFICIAL:
            LOG_WARN("IBindPhone::smsServiceSendCode accountType error")
            return
        if self.accountEntity.phone == 0:
            LOG_WARN("IBindPhone::smsServiceSendCode bind phone first")
            return
        if self.controlReqSMSServiceLimit(gameconst.EntityPropsEnum.reqSMSServiceTimestamp, 10):
            return
        checkRes, typeStr = self.preCheckSMSOperationType(opType)
        if not checkRes:
            return

        url = gameconfig.smsServiceReqUrl()
        message = json.dumps({
            "phone"         : str(self.accountEntity.phone),
            "loginType"     : int(self.accountEntity.channelId),
            "gameId"        : str(gameconfig.gameId()),
            "userGameId"    : str(self.accountName),
            "captchaVerifyParam": str(''),
            "deviceId"      : str(self.accountEntity.deviceId),
            "type"          : str(typeStr)
        })
        LOG_INFO("IBindPhone::smsServiceSendCode url", url, message)
        KBEngine.urlopenv2(url, functools.partial(self._smsServiceSendCodeResponse, 1), 
                method='POST',
                postData=message.encode('utf-8'),
                headers={"Content-Type": "application/json", "satoken": self.accountEntity.webToken},
                timeoutSec=5)
        
    def _smsServiceSendCodeResponse(self, sbType, httpCode, jsonData, headers, success, *args):
        LOG_INFO("IBindPhone::_smsServiceSendCodeResponse", httpCode, jsonData, headers, success, *args)
        if not (httpCode == 200 and success):
            self.onMessagePre(MMD.datas.web_requestException, [])
            LOG_ERR("IBindPhone::_smsServiceSendCodeResponse failed")
            return

        data = json.loads(jsonData)
        code = data['code']
        msg = data['message']
        LOG_INFO("IBindPhone::_smsServiceSendCodeResponse code, msg",code, msg)
        if code == 200 or code == 202:
            self.onMessagePre(MMD.datas.smsSentSuccess, [])
            self.client.reqSMSServiceResReplay(gameconst.ReqSMSServiceRes.ALERADY_SENT)
            LOG_INFO("IBindPhone::_smsServiceSendCodeResponse alerady sent")
        elif code == 5005:
            self.client.reqSMSServiceResReplay(gameconst.ReqSMSServiceRes.CHECK_CAPTCHA_VERIFY)
            LOG_INFO("IBindPhone::_smsServiceSendCodeResponse check captcha verify")
        else:
            LOG_WARN("IBindPhone::_smsServiceSendCodeResponse exception")
            self.onMessagePre(MMD.datas.web_requestException, [])

    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    def smsServiceVerifyCode(self, exposed, code, opType):
        LOG_INFO("IBindPhone::smsServiceVerifyCode", code, opType, self.accountEntity.accountType, self.accountName, self.accountEntity.phone)
        if self.accountEntity.accountType != centralLogin.ACCOUNT_OFFICIAL:
            LOG_WARN("IBindPhone::smsServiceVerifyCode accountType error")
            return
        if self.accountEntity.phone == 0:
            LOG_WARN("IBindPhone::smsServiceVerifyCode bind phone first")
            return
        if not self.checkValidVerifyCode(code):
            return
        if self.controlReqSMSServiceLimit(gameconst.EntityPropsEnum.verifySMSServiceTimestamp, 3):
            return
        checkRes, typeStr = self.checkSMSOperationType(opType)
        if not checkRes:
            return

        url = gameconfig.smsServiceVerifyUrl()
        message = json.dumps({
            "phone"         : str(self.accountEntity.phone),
            "gameId"        : str(gameconfig.gameId()),
            "code"          : str(code),
            "type"          : str(typeStr)
        })
        LOG_INFO("IBindPhone::smsServiceVerifyCode url", url, message)
        KBEngine.urlopenv2(url, self._smsServiceVerifyCodeResponse, method='POST',
                postData=message.encode('utf-8'),
                headers={"Content-Type": "application/json", "satoken": self.accountEntity.webToken},
                timeoutSec=5)

    def _smsServiceVerifyCodeResponse(self, httpCode, jsonData, headers, success, *args):
        LOG_INFO("IBindPhone::_smsServiceVerifyCodeResponse", httpCode, jsonData, headers, success)
        if not (httpCode == 200 and success):
            self.onMessagePre(MMD.datas.web_requestException, [])
            LOG_ERR("IBindPhone::_smsServiceVerifyCodeResponse failed")
            return

        data = json.loads(jsonData)
        code = data['code']
        if code == 200:
            self.onMessagePre(MMD.datas.pwdVerifySuccess, [])
            self.client.reqSMSServiceResReplay(gameconst.ReqSMSServiceRes.VERIFY_SUCCESSED)
            LOG_INFO("IBindPhone::_smsServiceVerifyCodeResponse verify success")
            self.grantSMSOperation()
        else:
            LOG_INFO("IBindPhone::_smsServiceVerifyCodeResponse 验证码不存在或已经失效")
            self.onMessagePre(MMD.datas.smsInvalid, [])

    def grantSMSOperation(self):
        self.setTempMiscProp(gameconst.EntityPropsEnum.smsServiceValidTimestamp, utils.curTS() + 300)
        LOG_DBG("IBindPhone::grantSMSOperation", self.getTempMiscProp(gameconst.EntityPropsEnum.smsServiceValidTimestamp, 0))

    def revokeSMSOperation(self):
        self.popTempMiscProp(gameconst.EntityPropsEnum.smsServiceValidTimestamp, 0)

    def checkSMSOperationTypeExpiry(self, opType):
        if opType not in gameconst.SMSOperationType.ALL_VAILD_TYPE:
            LOG_WARN("IBindPhone::checkSMSOperationTypeExpiry opType error")
            return False
        now = utils.curTS()
        smsServiceValidTimestamp = self.getTempMiscProp(gameconst.EntityPropsEnum.smsServiceValidTimestamp, 0)
        if smsServiceValidTimestamp < now:
            LOG_WARN("IBindPhone::checkSMSOperationTypeExpiry no grant")
            self.onMessagePre(MMD.datas.pwdVerifyTimeout, [])
            return False
        
        return True
    
    def preCheckSMSOperationType(self, opType):
        LOG_INFO("IBindPhone::preCheckSMSOperationType", opType)
        typeStr = ''
        if opType not in gameconst.SMSOperationType.ALL_VAILD_TYPE:
            LOG_WARN("IBindPhone::preCheckSMSOperationType opType error")
            return False, typeStr
        
        if opType in gameconst.SMSOperationType.SECONDARY_PWD_VAILD_TYPE:
            if not self.checkSPGameConfigEnable():
                return False, typeStr
            beHas = self.accountEntity.secondaryPwdInfo.hasSecondaryPassword()
            typeStr = gameconst.SMSOperationTypeStr.SECONDARY_PWD
            LOG_INFO("IBindPhone::preCheckSMSOperationType check", beHas)
            if opType == gameconst.SMSOperationType.SECONDARY_PWD_SET:
                #self.onMessagePre(MMD.datas., [])# 提示已经设置了密码
                return not beHas, typeStr
            elif opType == gameconst.SMSOperationType.SECONDARY_PWD_UPDATE:
                return True, typeStr
            elif opType == gameconst.SMSOperationType.SECONDARY_PWD_DELETE:
                #self.onMessagePre(MMD.datas., [])# 提示没有密码无需删除
                return beHas, typeStr
            elif opType == gameconst.SMSOperationType.SECONDARY_PWD_ENABLE:
                #self.onMessagePre(MMD.datas., [])# 提示没有密码无需切换
                return beHas, typeStr
        # 其他业务
        return False, typeStr

    def checkSMSOperationType(self, opType):
        LOG_INFO("IBindPhone::checkSMSOperationType", opType)
        typeStr = ''
        if opType not in gameconst.SMSOperationType.ALL_VAILD_TYPE:
            LOG_WARN("IBindPhone::checkSMSOperationType opType error")
            return False, typeStr

        if opType in gameconst.SMSOperationType.SECONDARY_PWD_VAILD_TYPE:
            if not self.checkSPGameConfigEnable():
                return False, typeStr
            typeStr = gameconst.SMSOperationTypeStr.SECONDARY_PWD
            return True, typeStr
        
        # 其他业务
        return False, typeStr

    def checkSPGameConfigEnable(self):
        if not gameconfig.visibleConfigEnabled('settings_secondPwd'):
            LOG_WARN("IBindPhone::checkSPGameConfigEnable not open")
            return False

        return True
#####################################################################################
    def checkValidSecondaryPassword(self, pwd):
        pwdMinLength = SP_SPC.datas.get('pwdMinLength', {}).get('value', 6)
        pwdMaxLength = SP_SPC.datas.get('pwdMaxLength', {}).get('value', 6)
        pwdMinLength = min(pwdMinLength, pwdMaxLength)
        pwdMaxLength = max(pwdMinLength, pwdMaxLength)
        if len(str(pwd)) < pwdMinLength or pwdMaxLength < len(str(pwd)):
            #self.onMessagePre(MMD.datas., [])# 加一个密码格式无效提示
            LOG_WARN("IBindPhone::checkValidSecondaryPassword pwd len invaild")
            return False
        if not str(pwd).isdigit():
            #self.onMessagePre(MMD.datas., [])# 加一个密码格式无效提示
            LOG_WARN("IBindPhone::checkValidSecondaryPassword pwd not digit")
            return False
        
        return True

    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    @gamedecorator.checkGameconfigEnable('settings_secondPwd')
    def reqSecondaryPasswordSMSOperation(self, exposed, opType, pwd):
        LOG_INFO("IBindPhone::reqSecondaryPasswordSMSOperation", opType, self.accountEntity.accountType, self.accountName, self.accountEntity.phone)
        LOG_DBG("IBindPhone::reqSecondaryPasswordSMSOperation", opType, self.accountEntity.secondaryPwdInfo, self.secondaryPwdVerityInfo)
        now = utils.curTS()
        if opType not in gameconst.SMSOperationType.SECONDARY_PWD_VAILD_TYPE:
            LOG_WARN("IBindPhone::reqSecondaryPasswordSMSOperation opType error")
            return
        if not self.checkSMSOperationTypeExpiry(opType):
            return

        if opType in (gameconst.SMSOperationType.SECONDARY_PWD_SET, gameconst.SMSOperationType.SECONDARY_PWD_UPDATE):
            if not self.checkValidSecondaryPassword(pwd):
                return
            pwdHash = utils.hashPassword(pwd)
            LOG_DBG("IBindPhone::reqSecondaryPasswordSMSOperation pwdHash", pwdHash)
            if opType == gameconst.SMSOperationType.SECONDARY_PWD_SET:
                if self.accountEntity.secondaryPwdInfo.hasSecondaryPassword():
                    #self.onMessagePre(MMD.datas., [])# 提示已经设置了密码
                    LOG_WARN("IBindPhone::reqSecondaryPasswordSMSOperation SECONDARY_PWD_SET alerady set pwdHash")
                    return
                self.accountEntity.secondaryPwdInfo.updateSecondaryPassword(pwdHash)
                self.onMessagePre(MMD.datas.setSecondPwdSuccess, [])
                LOG_INFO("IBindPhone::reqSecondaryPasswordSMSOperation set pwdHash success")
            elif opType == gameconst.SMSOperationType.SECONDARY_PWD_UPDATE:
                if not self.accountEntity.secondaryPwdInfo.hasSecondaryPassword():
                    LOG_WARN("IBindPhone::reqSecondaryPasswordSMSOperation SECONDARY_PWD_UPDATE no pwdHash")
                self.accountEntity.secondaryPwdInfo.updateSecondaryPassword(pwdHash)
                self.onMessagePre(MMD.datas.modifySuccess, [])
                LOG_INFO("IBindPhone::reqSecondaryPasswordSMSOperation update pwdHash success")
        elif opType in (gameconst.SMSOperationType.SECONDARY_PWD_DELETE, gameconst.SMSOperationType.SECONDARY_PWD_ENABLE):
            if opType == gameconst.SMSOperationType.SECONDARY_PWD_DELETE:
                if not self.accountEntity.secondaryPwdInfo.hasSecondaryPassword():
                    LOG_WARN("IBindPhone::reqSecondaryPasswordSMSOperation SECONDARY_PWD_DELETE no pwdHash")
                self.accountEntity.secondaryPwdInfo.delSecondaryPassword()
                LOG_INFO("IBindPhone::reqSecondaryPasswordSMSOperation delete pwdHash success")
            elif opType == gameconst.SMSOperationType.SECONDARY_PWD_ENABLE:
                if not self.accountEntity.secondaryPwdInfo.hasSecondaryPassword():
                    LOG_WARN("IBindPhone::reqSecondaryPasswordSMSOperation SECONDARY_PWD_ENABLE no pwdHash")
                    return
                self.accountEntity.secondaryPwdInfo.enableSecondaryPassword()
                LOG_INFO("IBindPhone::reqSecondaryPasswordSMSOperation switch enable success")

        self.secondaryPwdVerityInfo.updateBeVerity(now, False, SP_SPC.datas.get('pwdFreeVerifyDurationMs', {}).get('value', ()))
        self.accountEntity.cannelSecondaryPwdLockedExpired()
        self.sendSecondaryPasswordInfo()
        self.revokeSMSOperation()
        self.accountEntity.pyWriteToDB()
#####################################################################################
    def checkPopupSecondaryPassword(self, checkList):
        if not checkList:
            return False
        if not self.checkSPGameConfigEnable():
            return False
        LOG_INFO("IBindPhone::checkPopupSecondaryPassword", checkList)
        LOG_DBG("IBindPhone::checkPopupSecondaryPassword", self.accountEntity.secondaryPwdInfo)
        LOG_DBG("IBindPhone::checkPopupSecondaryPassword", self.secondaryPwdVerityInfo)
        now = utils.curTS()
        if not self.accountEntity.secondaryPwdInfo.hasSecondaryPassword():
            LOG_DBG("IBindPhone::checkPopupSecondaryPassword no pwdHash")
            # self.client.notifyPopupSecondaryPassword(gameconst.NotifyPopupSecondaryPasswordType.TO_SET)
            return False
        #if not self.accountEntity.secondaryPwdInfo.getBeEnable():
        if not self.secondaryPwdVerityInfo.getBeEnable():
            LOG_DBG("IBindPhone::checkPopupSecondaryPassword not enable")
            return False
        if self.secondaryPwdVerityInfo.checkBeVerity(now):
            LOG_DBG("IBindPhone::checkPopupSecondaryPassword alerady verity")
            return False
        for checkInfo in checkList:
            LOG_DBG("IBindPhone::checkPopupSecondaryPassword check verity", checkInfo)
            if not len(checkInfo):
                LOG_ERR("IBindPhone::checkPopupSecondaryPassword checkInfo error", checkInfo)
                return True
            if checkInfo[0] not in gameconst.SecondaryPasswordCheckType.VAILD_TYPE:
                LOG_ERR("IBindPhone::checkPopupSecondaryPassword check type error", checkInfo)
                continue
            itemDisassemblyLimit = SP_SPC.datas.get('itemDisassemblyLimit', {}).get('value', 3)
            if not self.secondaryPwdVerityInfo.checkNeedVerity(checkInfo, itemDisassemblyLimit):
                continue
            LOG_INFO("IBindPhone::checkPopupSecondaryPassword need verity", checkInfo)
            self.client.notifyPopupSecondaryPassword(gameconst.NotifyPopupSecondaryPasswordType.TO_VERITY)
            return True

        LOG_INFO("IBindPhone::checkPopupSecondaryPassword end")
        return False
        
    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    @gamedecorator.checkGameconfigEnable('settings_secondPwd')
    def reqSecondaryPasswordVerity(self, exposed, pwd):
        LOG_INFO("IBindPhone::reqSecondaryPasswordVerity")
        LOG_DBG("IBindPhone::reqSecondaryPasswordVerity", self.accountEntity.secondaryPwdInfo)
        LOG_DBG("IBindPhone::reqSecondaryPasswordVerity", self.secondaryPwdVerityInfo)
        now = utils.curTS()
        checkRes = self.secondaryPwdVerity(now, pwd, gameconst.SecondaryPasswordVerityType.VERITY)
        if not checkRes:
            return

        self.secondaryPwdVerityInfo.updateBeVerity(now, True, SP_SPC.datas.get('pwdFreeVerifyDurationMs', {}).get('value', ()))
        LOG_DBG("IBindPhone::reqSecondaryPasswordVerity be verity", self.secondaryPwdVerityInfo)

    def secondaryPwdVerity(self, now, pwd, verityType):
        LOG_INFO("IBindPhone::secondaryPwdVerity", now, verityType)
        if not self.checkValidSecondaryPassword(pwd):
            return False
        if not self.accountEntity.secondaryPwdInfo.hasSecondaryPassword():
            #self.onMessagePre(MMD.datas., [])# 提示还未设置密码
            LOG_WARN("IBindPhone::secondaryPwdVerity no pwdHash")
            return False
        if verityType in (gameconst.SecondaryPasswordVerityType.MODIFY,):
            pass
        elif verityType in (gameconst.SecondaryPasswordVerityType.VERITY,):
            #if not self.accountEntity.secondaryPwdInfo.getBeEnable():
            if not self.secondaryPwdVerityInfo.getBeEnable():
                #self.onMessagePre(MMD.datas., [])# 提示没启用密码当前无需校验
                LOG_WARN("IBindPhone::secondaryPwdVerity not enable")
                return False
            if self.secondaryPwdVerityInfo.checkBeVerity(now):
                #self.onMessagePre(MMD.datas., [])# 提示当前无需再校验
                LOG_WARN("IBindPhone::secondaryPwdVerity alerady verity")
                return False
        if self.accountEntity.secondaryPwdInfo.checkBeVerityLocked(now):
            LOG_INFO("IBindPhone::secondaryPwdVerity be verity locked")
            #self.onMessagePre(MMD.datas., [])# 提示当前处于锁定状态,无法校验
            return False
        if not utils.verifyPassword(pwd, self.accountEntity.secondaryPwdInfo.getSecondaryPassword()):
            LOG_INFO("IBindPhone::secondaryPwdVerity pwd not match")
            continuousWrong = SP_SPC.datas.get('continuousWrong', {}).get('value', [])
            beLocked, msgId = self.accountEntity.secondaryPwdInfo.incrVerityFailedCnt(now, continuousWrong)
            if beLocked:
                self.accountEntity.checkSecondaryPwdLockedExpired(len(continuousWrong))
                self.secondaryPwdVerityInfo.updateBeVerity(now, False, SP_SPC.datas.get('pwdFreeVerifyDurationMs', {}).get('value', ()))
                self.onMessagePre(msgId, [])
            else:
                self.onMessagePre(MMD.datas.continuousWrongPwd, [])

            self.sendSecondaryPasswordInfo()
            LOG_INFO("IBindPhone::secondaryPwdVerity verity failed", beLocked)
            LOG_DBG("IBindPhone::secondaryPwdVerity verity failed", self.accountEntity.secondaryPwdInfo)
            LOG_DBG("IBindPhone::secondaryPwdVerity verity failed", self.secondaryPwdVerityInfo)
            return False
        
        self.accountEntity.secondaryPwdInfo.veritySecondaryPassword()
        self.sendSecondaryPasswordInfo()
        self.onMessagePre(MMD.datas.secondPwdSuccess, [])
        LOG_INFO("IBindPhone::secondaryPwdVerity end")
        return True

    def checkModifySecondaryPwdVerityInfo(self, clientCfg):
        LOG_INFO("IBindPhone::checkModifySecondaryPwdVerityInfo", clientCfg)
        money = clientCfg['money']
        bindMoney = clientCfg['bindMoney']
        accessIdx = clientCfg['accessIdx']
        goldCostLimit = SP_SPC.datas.get('goldCostLimit', {}).get('value', (100, 2000))
        if money < goldCostLimit[0] or goldCostLimit[1] < money:
            #self.onMessagePre(MMD.datas., [])# 提示元宝设置区间不合法
            LOG_WARN("IBindPhone::checkModifySecondaryPwdVerityInfo money")
            return False
        boundGoldCostLimit = SP_SPC.datas.get('boundGoldCostLimit', {}).get('value', (100, 2000))
        if bindMoney < boundGoldCostLimit[0] or boundGoldCostLimit[1] < bindMoney:
            #self.onMessagePre(MMD.datas., [])# 提示绑定元宝设置区间不合法
            LOG_WARN("IBindPhone::checkModifySecondaryPwdVerityInfo bindMoney")
            return False
        pwdFreeVerifyDurationMs = SP_SPC.datas.get('pwdFreeVerifyDurationMs', {}).get('value', ())
        if accessIdx < 0 or len(pwdFreeVerifyDurationMs) < accessIdx:
            #self.onMessagePre(MMD.datas., [])# 提示免密时长设置区间不合法
            LOG_WARN("IBindPhone::checkModifySecondaryPwdVerityInfo accessIdx")
            return False
        
        return True

    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    @gamedecorator.checkGameconfigEnable('settings_secondPwd')
    def reqModifySecondaryPwdVerityInfo(self, exposed, pwd, clientCfg):
        LOG_INFO("IBindPhone::reqModifySecondaryPwdVerityInfo", clientCfg)
        LOG_DBG("IBindPhone::reqModifySecondaryPwdVerityInfo", self.accountEntity.secondaryPwdInfo)
        LOG_DBG("IBindPhone::reqModifySecondaryPwdVerityInfo", self.secondaryPwdVerityInfo)
        if not self.checkModifySecondaryPwdVerityInfo(clientCfg):
            return
        now = utils.curTS()
        checkRes = self.secondaryPwdVerity(now, pwd, gameconst.SecondaryPasswordVerityType.MODIFY)
        if not checkRes:
            return

        updatePropList = self.secondaryPwdVerityInfo.modifyProp(clientCfg)
        LOG_INFO("IBindPhone::reqModifySecondaryPwdVerityInfo updatePropList", updatePropList)
        #self.onMessagePre(MMD.datas., [])# 提示配置修改成功
        if not updatePropList:
            return
        
        if 'accessIdx' in updatePropList or 'beEnable' in updatePropList:
            LOG_INFO("IBindPhone::reqModifySecondaryPwdVerityInfo modify accessIdx")
            self.secondaryPwdVerityInfo.updateBeVerity(now, False, SP_SPC.datas.get('pwdFreeVerifyDurationMs', {}).get('value', ()))
        self.sendSecondaryPasswordVerityInfo()
        LOG_DBG("IBindPhone::reqModifySecondaryPwdVerityInfo modify success", self.secondaryPwdVerityInfo)
        LOG_INFO("IBindPhone::reqModifySecondaryPwdVerityInfo modify success")

    def onSecondaryPwdLockedExpired(self):
        LOG_INFO("IBindPhone::onSecondaryPwdLockedExpired")
        self.sendSecondaryPasswordInfo()

    def onDailyClearPunishmentInfo(self):
        LOG_INFO("IBindPhone::onDailyClearPunishmentInfo")
        self.sendSecondaryPasswordInfo()

    def sendSecondaryPasswordInfo(self):
        LOG_DBG("IBindPhone::sendSecondaryPasswordInfo1", self.accountEntity.secondaryPwdInfo)
        LOG_INFO("IBindPhone::sendSecondaryPasswordInfo2", self.accountEntity.secondaryPwdInfo.toStreamClientDic())
        self.client.sendSecondaryPasswordInfo(self.accountEntity.secondaryPwdInfo.toStreamClientDic())

    def sendSecondaryPasswordVerityInfo(self):
        LOG_DBG("IBindPhone::sendSecondaryPasswordVerityInfo1", self.secondaryPwdVerityInfo)
        LOG_INFO("IBindPhone::sendSecondaryPasswordVerityInfo2", self.secondaryPwdVerityInfo.toStreamClientDic())
        self.client.sendSecondaryPasswordVerityInfo(self.secondaryPwdVerityInfo.toStreamClientDic())
