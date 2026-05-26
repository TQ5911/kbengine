# coding: utf-8
from KBEDebug import *
import KBEngine
import gameconst
import gameclass
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
import visible_visible as UVVD
import LogTrackingMgr
import login_set as LSD
import report_config as RC
import report_report as RR



class reportInfo(object):
    def __init__(self):
        self.reportRoleId = 0
        self.reportRoleName = ''
        self.reportUserGameId = ''
        self.beReportRoleId = 0
        self.beReportRoleName = 0

        self.reportType = 0
        self.chatRef = ''
        self.desc = ''

    def reporter(self, gbId, name, accountName):
        self.reportRoleId = gbId
        self.reportRoleName = name
        self.reportUserGameId = accountName

    def beReporter(self, gbId, name, reportType, chatRef, desc):
        self.beReportRoleId = gbId
        self.beReportRoleName = name

        self.reportType = reportType
        self.chatRef = chatRef
        self.desc = desc

    def dumps(self):
        return json.dumps({
            "reportRoleId": self.reportRoleId,
            "reportRoleName": str(self.reportRoleName),
            "reportUserGameId": str(self.reportUserGameId),
            "beReportRoleId": self.beReportRoleId,
            "beReportRoleName": str(self.beReportRoleName),
            "reportType": ','.join(map(str, self.reportType)),
            "chatRef": self.chatRef,
            "reportReason": self.desc
        }, ensure_ascii=False)

    def __eq__(self, otherReport):
        return self.beReportRoleId == otherReport.beReportRoleId and self.beReportRoleName == otherReport.beReportRoleName and\
              self.reportType == otherReport.reportType and self.chatRef == otherReport.chatRef and self.desc == otherReport.desc 

    def __str__(self):
        return f'reportInfo(beReportRoleId={self.beReportRoleId}, beReportRoleName={self.beReportRoleName}, reportType={self.reportType}, chatRef={self.chatRef}, desc={self.desc})'

    def checkSame(self, otherReport):
        if not otherReport:
            return False
        if not isinstance(otherReport, reportInfo):
            return False
        return otherReport == self

class IReport(object):
    def __init__(self):
        LOG_INFO("IReport::init")

    def reportOnLogin(self):
        LOG_INFO("IReport::reportOnLogin", self.accountEntity.userInfoId, self.accountEntity.accountName)

    def onReportDailyUpdate(self, *args):
        LOG_INFO("IReport::onReportDailyUpdate")
        self.reportCnt = 0

    def checkValidArguments(self, report):
        if not report.beReportRoleId:
            LOG_WARN("IReport::checkValidArguments beReportRoleId")
            return False
        if not report.beReportRoleName:
            LOG_WARN("IReport::checkValidArguments beReportRoleName")
            return False
        if not report.reportType:
            self.onMessagePre(MMD.datas.reportFail_empty, [])
            LOG_WARN("IReport::checkValidArguments reportType")
            return False
        '''
        report.chatRef:
        '''
        maxLength = RC.datas["reportWordLimit"]["value"]
        if len(report.desc) > maxLength:
            LOG_WARN("IReport::checkValidArguments desc")
            self.onMessagePre(MMD.datas.reportFail_wordLimit, [])
            return False
        return True

    def controlReportLimit(self):
        LOG_INFO("IReport::controlReportLimit")
        now = utils.curTS()
        reportTimestamp = self.getTempMiscProp(gameconst.EntityPropsEnum.reportTimestamp, 0)
        if reportTimestamp > now:
            LOG_WARN("IReport::controlReportLimit")
            self.onMessagePre(MMD.datas.petTeamSwitchCD, [])
            return True

        self.setTempMiscProp(gameconst.EntityPropsEnum.reportTimestamp, now + 3)

    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable(UVVD.datas.get('report', {}).get('type', 'report'))
    def reqReport(self, exposed, gbId, name, types, chatRef, desc):
        LOG_INFO("IReport::reqReport", self.gbID, self.characterName, gbId, name, types, chatRef, desc)
        if False:
            LOG_WARN('IReport::reqReport function Limit')
            self.onMessagePre(MMD.datas.reportFail_functionLimit, [])
            return  
        #if not self._isUIVisibleStr('report'):
        needLv = RC.datas["reportLevelLimit"]['value']
        if self.getAvatarLevel() < needLv:
            LOG_WARN('IReport::reqReport not lock')
            self.onMessagePre(MMD.datas.reportLevelLimitTip, [str(needLv)])
            return  
        maxCnt = RC.datas["reportDailyLimit"]['value']
        if self.reportCnt >= maxCnt:
            LOG_WARN("IReport::reqReport cnt limit", self.reportCnt, maxCnt)
            self.onMessagePre(MMD.datas.reportFail_timeLimit, [])
            return
        if self.controlReportLimit():
            return
        
        curReport = reportInfo()
        curReport.beReporter(gbId, name, types, chatRef, desc)
        if not self.checkValidArguments(curReport):
            return
        preReport = self.getTempMiscProp(gameconst.EntityPropsEnum.preReport, None)
        if curReport.checkSame(preReport):
            self.onMessagePre(MMD.datas.reportFail_sameContent, [])
            LOG_WARN("IReport::reqReport checkSame")
            return
        curReport.reporter(self.gbID, self.characterName, self.accountName)
        message = curReport.dumps()
        url = gameconfig.reportUrl()
        LOG_INFO("IReport::reqReport url, message", url, message)

        self.setTempMiscProp(gameconst.EntityPropsEnum.recordPreReport, preReport)
        self.setTempMiscProp(gameconst.EntityPropsEnum.preReport, curReport)
        self.reportCnt += 1
        KBEngine.urlopenv2(url, self._reqReportResponse, method='POST',
                postData=message.encode('utf-8'),
                headers={"Content-Type": "application/json"},
                timeoutSec=5)

    def _reqReportResponse(self, httpCode, jsonData, headers, success, *args):
        LOG_INFO("IReport::_reqReportResponse", httpCode, jsonData, headers, success)
        self.popTempMiscProp(gameconst.EntityPropsEnum.reportTimestamp, 0)
        if not (httpCode == 200 and success):
            self.onMessagePre(MMD.datas.reportFail_serverError, [])
            self.onReportResponseFailed()
            LOG_ERR("IReport::_reqReportResponse failed")
            return

        data = json.loads(jsonData)
        code = data['code']
        if code == 200 or code == 202:
            self.onMessagePre(MMD.datas.reportPass, [])
            self.popTempMiscProp(gameconst.EntityPropsEnum.recordPreReport, None)
            LOG_INFO("IReport::_reqReportResponse success ")
        else:
            self.onMessagePre(MMD.datas.reportFail_serverError, [])
            self.onReportResponseFailed()
            LOG_WARN("IReport::_reqReportResponse exception")

    def onReportResponseFailed(self):
        self.reportCnt = max(0, int(self.reportCnt) - 1)
        recordPreReport = self.popTempMiscProp(gameconst.EntityPropsEnum.recordPreReport, None)
        self.setTempMiscProp(gameconst.EntityPropsEnum.preReport, recordPreReport)