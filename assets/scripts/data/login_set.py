# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: login/set
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "returnToLoginConfirmMsg": _tools.RODict({
        "ID": "returnToLoginConfirmMsg",
        "value": 54000042,
    }),
    "ExitGameConfirmMsg": _tools.RODict({
        "ID": "ExitGameConfirmMsg",
        "value": 54000043,
    }),
    "login_digestNotMatch": _tools.RODict({
        "ID": "login_digestNotMatch",
        "value": 54000016,
    }),
    "login_serverClosed": _tools.RODict({
        "ID": "login_serverClosed",
        "value": 54000015,
    }),
    "SEVER_CAN_NOT_CONNECT": _tools.RODict({
        "ID": "SEVER_CAN_NOT_CONNECT",
        "value": 54000017,
    }),
    "connect_ui_delay": _tools.RODict({
        "ID": "connect_ui_delay",
        "value": 0.5,
    }),
    "clientFix_msgID": _tools.RODict({
        "ID": "clientFix_msgID",
        "value": 54001097,
    }),
    "login_dinghao_msgID": _tools.RODict({
        "ID": "login_dinghao_msgID",
        "value": 54000014,
    }),
    "login_enterServerError_msgID": _tools.RODict({
        "ID": "login_enterServerError_msgID",
        "value": 54000797,
    }),
    "login_serverInMaintenance_msgID": _tools.RODict({
        "ID": "login_serverInMaintenance_msgID",
        "value": 54000798,
    }),
    "login_countOrPasswordError_msgID": _tools.RODict({
        "ID": "login_countOrPasswordError_msgID",
        "value": 54000023,
    }),
    "login_tooBusyWithoutCD_msgID": _tools.RODict({
        "ID": "login_tooBusyWithoutCD_msgID",
        "value": 54002069,
    }),
    "login_failed_msgID": _tools.RODict({
        "ID": "login_failed_msgID",
        "value": 54000068,
    }),
    "login_dinghaoConfirm_msgID": _tools.RODict({
        "ID": "login_dinghaoConfirm_msgID",
        "value": 54001434,
    }),
    "idip_accountBanned_msg": _tools.RODict({
        "ID": "idip_accountBanned_msg",
        "value": 54001560,
    }),
    "idip_accountBanned_msg2": _tools.RODict({
        "ID": "idip_accountBanned_msg2",
        "value": 54001562,
    }),
    "accountNotWhitelisted": _tools.RODict({
        "ID": "accountNotWhitelisted",
        "value": 54000798,
    }),
    "frequent_dinghao_msgID": _tools.RODict({
        "ID": "frequent_dinghao_msgID",
        "value": 54001588,
    }),
    "realNameAuthInfoEmpty_msgID": _tools.RODict({
        "ID": "realNameAuthInfoEmpty_msgID",
        "value": 54002006,
    }),
    "realNameAuthFailed_msgID": _tools.RODict({
        "ID": "realNameAuthFailed_msgID",
        "value": 54002007,
    }),
    "usernameRegex": _tools.RODict({
        "ID": "usernameRegex",
        "value": "[a-zA-Z0-9]{3,12}",
    }),
    "passwordRegex": _tools.RODict({
        "ID": "passwordRegex",
        "value": "[a-zA-Z0-9]{6,18}",
    }),
    "userNameLenMismatch_msgID": _tools.RODict({
        "ID": "userNameLenMismatch_msgID",
        "value": 54002008,
    }),
    "passWordLenMismatch_msgID": _tools.RODict({
        "ID": "passWordLenMismatch_msgID",
        "value": 54002009,
    }),
    "protocolText": _tools.RODict({
        "ID": "protocolText",
        "value": "我已详细阅读并同意<msg=54002010,label=\"《许可及服务协议》\">、<msg=54002011,label=\"《隐私政策》\">、<msg=54002012,label=\"《儿童信息及隐私保护政策》\">",
    }),
    "serverClosedText": _tools.RODict({
        "ID": "serverClosedText",
        "value": "[维护]",
    }),
    "regLimited_serverFull_msg": _tools.RODict({
        "ID": "regLimited_serverFull_msg",
        "value": 54001683,
    }),
    "foreverText": _tools.RODict({
        "ID": "foreverText",
        "value": "永久",
    }),
    "accountCancellation": _tools.RODict({
        "ID": "accountCancellation",
        "value": 54920002,
    }),
    "color_baoman": _tools.RODict({
        "ID": "color_baoman",
        "value": 116,
    }),
    "color_fanmang": _tools.RODict({
        "ID": "color_fanmang",
        "value": 117,
    }),
    "color_kongxian": _tools.RODict({
        "ID": "color_kongxian",
        "value": 118,
    }),
    "color_weihu": _tools.RODict({
        "ID": "color_weihu",
        "value": 84,
    }),
    "login_iOSUpdate_msgID": _tools.RODict({
        "ID": "login_iOSUpdate_msgID",
        "value": 54000789,
    }),
    "login_androidUpdate_msgID": _tools.RODict({
        "ID": "login_androidUpdate_msgID",
        "value": 54000790,
    }),
    "login_packageUpdateFinished_msgID": _tools.RODict({
        "ID": "login_packageUpdateFinished_msgID",
        "value": 54000791,
    }),
    "login_networkError_msgID": _tools.RODict({
        "ID": "login_networkError_msgID",
        "value": 54000792,
    }),
    "login_getPatchListNetError_msgID": _tools.RODict({
        "ID": "login_getPatchListNetError_msgID",
        "value": 54000793,
    }),
    "login_downloadPatchNetError_msgID": _tools.RODict({
        "ID": "login_downloadPatchNetError_msgID",
        "value": 54000794,
    }),
    "login_ifDownloadPatch_msgID": _tools.RODict({
        "ID": "login_ifDownloadPatch_msgID",
        "value": 54000795,
    }),
    "login_phoneBackMsg_msgID": _tools.RODict({
        "ID": "login_phoneBackMsg_msgID",
        "value": 54000796,
    }),
    "login_serverNotOpen_msgID": _tools.RODict({
        "ID": "login_serverNotOpen_msgID",
        "value": 54000799,
    }),
    "login_countOrPasswordEmpty_msgID": _tools.RODict({
        "ID": "login_countOrPasswordEmpty_msgID",
        "value": 54000021,
    }),
    "login_countOrPasswordIllegal_msgID": _tools.RODict({
        "ID": "login_countOrPasswordIllegal_msgID",
        "value": 54000022,
    }),
    "login_authTimeout": _tools.RODict({
        "ID": "login_authTimeout",
        "value": 54001909,
    }),
    "login_getNoticeError_msgID": _tools.RODict({
        "ID": "login_getNoticeError_msgID",
        "value": 54001664,
    }),
    "loginOnlineNum": _tools.RODict({
        "ID": "loginOnlineNum",
        "value": 4000,
    }),
    "loginQueueNumShowDetail": _tools.RODict({
        "ID": "loginQueueNumShowDetail",
        "value": 2000,
    }),
    "loginQueueNumShowTime": _tools.RODict({
        "ID": "loginQueueNumShowTime",
        "value": 8000,
    }),
    "loginSpeed": _tools.RODict({
        "ID": "loginSpeed",
        "value": 300,
    }),
    "loginQueueWaitTimeRefresh": _tools.RODict({
        "ID": "loginQueueWaitTimeRefresh",
        "value": 5,
    }),
    "idip_accountBanned_client_msg": _tools.RODict({
        "ID": "idip_accountBanned_client_msg",
        "value": 54001874,
    }),
    "idip_roleBanned_msg": _tools.RODict({
        "ID": "idip_roleBanned_msg",
        "value": 54001561,
    }),
    "level1CooldownTrigger": _tools.RODict({
        "ID": "level1CooldownTrigger",
        "value": 3,
    }),
    "level1Cooldown": _tools.RODict({
        "ID": "level1Cooldown",
        "value": 10,
    }),
    "level2CooldownTrigger": _tools.RODict({
        "ID": "level2CooldownTrigger",
        "value": 4,
    }),
    "level2Cooldown": _tools.RODict({
        "ID": "level2Cooldown",
        "value": 60,
    }),
    "connectCooldownMsg": _tools.RODict({
        "ID": "connectCooldownMsg",
        "value": 54001563,
    }),
    "queueFail_networkFail_msg": _tools.RODict({
        "ID": "queueFail_networkFail_msg",
        "value": 54001582,
    }),
    "frequent_dinghao_time": _tools.RODict({
        "ID": "frequent_dinghao_time",
        "value": 600,
    }),
    "frequent_dinghao_num": _tools.RODict({
        "ID": "frequent_dinghao_num",
        "value": 10,
    }),
    "login_tooBusy_firstWaitTime": _tools.RODict({
        "ID": "login_tooBusy_firstWaitTime",
        "value": 10,
    }),
    "login_tooBusy_secondWaitTime": _tools.RODict({
        "ID": "login_tooBusy_secondWaitTime",
        "value": 20,
    }),
    "login_tooBusy_msgID": _tools.RODict({
        "ID": "login_tooBusy_msgID",
        "value": 54002040,
    }),
    "login_tooBusy_text": _tools.RODict({
        "ID": "login_tooBusy_text",
        "value": "登录频繁，{0}秒后再试",
    }),
    "officialAnnounce_picWidthLimit": _tools.RODict({
        "ID": "officialAnnounce_picWidthLimit",
        "value": 1274,
    }),
    "serverInMaintainanceMsg": _tools.RODict({
        "ID": "serverInMaintainanceMsg",
        "value": 54000798,
    }),
    "loginPopUp_announceLevelLimit": _tools.RODict({
        "ID": "loginPopUp_announceLevelLimit",
        "value": 12,
    }),
    "scrollingMessagePullInterval": _tools.RODict({
        "ID": "scrollingMessagePullInterval",
        "value": 60,
    }),
    "serverRegLimit": _tools.RODict({
        "ID": "serverRegLimit",
        "value": 10000,
    }),
    "regSwitchDefault": _tools.RODict({
        "ID": "regSwitchDefault",
        "value": 1,
    }),
    "login_kickedByServer_window": _tools.RODict({
        "ID": "login_kickedByServer_window",
        "value": 54001920,
    }),
    "fakeOnlineTime": _tools.RODict({
        "ID": "fakeOnlineTime",
        "value": 300,
    }),
    "mapleFilterOn": _tools.RODict({
        "ID": "mapleFilterOn",
        "value": 0,
    }),
    "voiceChat_micBanFail_voiceChatClose": _tools.RODict({
        "ID": "voiceChat_micBanFail_voiceChatClose",
        "value": 54001972,
    }),
    "sdk_login_networkLoss": _tools.RODict({
        "ID": "sdk_login_networkLoss",
        "value": 54002024,
    }),
    "dolphin_downloadPatch_msgID": _tools.RODict({
        "ID": "dolphin_downloadPatch_msgID",
        "value": 54000795,
    }),
    "dolphin_downloadApk_wifi_msgID": _tools.RODict({
        "ID": "dolphin_downloadApk_wifi_msgID",
        "value": 54001843,
    }),
    "dolphin_downloadApk_msgID": _tools.RODict({
        "ID": "dolphin_downloadApk_msgID",
        "value": 54001844,
    }),
    "dolphin_downloadIpa_msgID": _tools.RODict({
        "ID": "dolphin_downloadIpa_msgID",
        "value": 54001845,
    }),
    "dolphin_downloadNetChange_msgID": _tools.RODict({
        "ID": "dolphin_downloadNetChange_msgID",
        "value": 54001846,
    }),
    "dolphin_checkPackText": _tools.RODict({
        "ID": "dolphin_checkPackText",
        "value": "检测包体更新",
    }),
    "dolphin_downloadPackText": _tools.RODict({
        "ID": "dolphin_downloadPackText",
        "value": "更新包体过程中请不要关闭游戏，正在{0}， 速度{1}",
    }),
    "dolphin_checkPatchText": _tools.RODict({
        "ID": "dolphin_checkPatchText",
        "value": "检测资源更新",
    }),
    "dolphin_downloadPatchText": _tools.RODict({
        "ID": "dolphin_downloadPatchText",
        "value": "更新资源过程中请不要关闭游戏，正在{0}， 速度{1}",
    }),
    "dolphin_decompressionPackTitle": _tools.RODict({
        "ID": "dolphin_decompressionPackTitle",
        "value": "正在从设备存储空间中加载资源，此过程需要下载0KB文件，请耐心等待。",
    }),
    "dolphin_decompressionPackText": _tools.RODict({
        "ID": "dolphin_decompressionPackText",
        "value": "资源加载中（{0}/{1}）",
    }),
    "dolphin_decompressionPackOver": _tools.RODict({
        "ID": "dolphin_decompressionPackOver",
        "value": "更新成功！",
    }),
    "ageAppropriateTips": _tools.RODict({
        "ID": "ageAppropriateTips",
        "value": "提示说明：\\n\\n1）需要补充失灵",
    }),
    "checkAgreementTips": _tools.RODict({
        "ID": "checkAgreementTips",
        "value": 54920003,
    }),
    "licenceService": _tools.RODict({
        "ID": "licenceService",
        "value": "https://xwindlab.com/agreement.html",
    }),
    "privacyProtection": _tools.RODict({
        "ID": "privacyProtection",
        "value": "https://xwindlab.com/privacy.html",
    }),
    "kidPrivacyProtection": _tools.RODict({
        "ID": "kidPrivacyProtection",
        "value": "",
    }),
    "informationShare": _tools.RODict({
        "ID": "informationShare",
        "value": "",
    }),
    "realNameMsg": _tools.RODict({
        "ID": "realNameMsg",
        "value": 54920001,
    }),
    "accountCancelOfficial": _tools.RODict({
        "ID": "accountCancelOfficial",
        "value": "",
    }),
    "accountCancelTest": _tools.RODict({
        "ID": "accountCancelTest",
        "value": "",
    }),
    "privacyAssistantEntrance": _tools.RODict({
        "ID": "privacyAssistantEntrance",
        "value": "",
    }),
    "goMobilePayment": _tools.RODict({
        "ID": "goMobilePayment",
        "value": 54920004,
    }),
    "getStoragePermission": _tools.RODict({
        "ID": "getStoragePermission",
        "value": 54920005,
    }),
    "getMicrophonePermission": _tools.RODict({
        "ID": "getMicrophonePermission",
        "value": 54920006,
    }),
    "getPhonePermission": _tools.RODict({
        "ID": "getPhonePermission",
        "value": 54920007,
    }),
    "getLocationPermission": _tools.RODict({
        "ID": "getLocationPermission",
        "value": 54920008,
    }),
    "localTimeCalibration": _tools.RODict({
        "ID": "localTimeCalibration",
        "value": 54002106,
    }),
    "androidCloseLocation": _tools.RODict({
        "ID": "androidCloseLocation",
        "value": "（关闭此功能请前往手机应用管理关闭位置信息权限）",
    }),
    "iosCloseLocation": _tools.RODict({
        "ID": "iosCloseLocation",
        "value": "（关闭此功能请前往设置关闭位置权限）",
    }),
    "needLocationPermission": _tools.RODict({
        "ID": "needLocationPermission",
        "value": "（需要开启位置权限）",
    }),
    "locationIsOpen": _tools.RODict({
        "ID": "locationIsOpen",
        "value": "已开启",
    }),
    "recommendServer": _tools.RODict({
        "ID": "recommendServer",
        "value": 1,
    }),
    "recommendServerNum": _tools.RODict({
        "ID": "recommendServerNum",
        "value": 6,
    }),
    "recommendServerDay": _tools.RODict({
        "ID": "recommendServerDay",
        "value": 2,
    }),
    "noRecommendServer": _tools.RODict({
        "ID": "noRecommendServer",
        "value": 10,
    }),
    "iosAppStoreUrl": _tools.RODict({
        "ID": "iosAppStoreUrl",
        "value": "https://s.xwindlab.com/h5_xf/index.html",
    }),
    "superRIsOpen": _tools.RODict({
        "ID": "superRIsOpen",
        "value": 0,
    }),
    "tinyIsOpen": _tools.RODict({
        "ID": "tinyIsOpen",
        "value": 0,
    }),
    "cloudGame_goMobilePayment_msg": _tools.RODict({
        "ID": "cloudGame_goMobilePayment_msg",
        "value": 54002223,
    }),
    "cloudGame_goMobileShare_msg": _tools.RODict({
        "ID": "cloudGame_goMobileShare_msg",
        "value": 54002330,
    }),
    "changeAccountRefreshTime": _tools.RODict({
        "ID": "changeAccountRefreshTime",
        "value": 5,
    }),
    "changeAccountRefreshCD": _tools.RODict({
        "ID": "changeAccountRefreshCD",
        "value": 86400,
    }),
    "changeAccountLimit": _tools.RODict({
        "ID": "changeAccountLimit",
        "value": 1,
    }),
    "accountDisplayMaxNum": _tools.RODict({
        "ID": "accountDisplayMaxNum",
        "value": 3,
    }),
    "rejectAgreement_msg": _tools.RODict({
        "ID": "rejectAgreement_msg",
        "value": 54980001,
    }),
    "wrongPhoneNumber_msg": _tools.RODict({
        "ID": "wrongPhoneNumber_msg",
        "value": 54980002,
    }),
    "wrongVerificationCode_msg": _tools.RODict({
        "ID": "wrongVerificationCode_msg",
        "value": 54980003,
    }),
    "loginSuccessful_msg": _tools.RODict({
        "ID": "loginSuccessful_msg",
        "value": 54980004,
    }),
    "deleteLoginHistory_msg": _tools.RODict({
        "ID": "deleteLoginHistory_msg",
        "value": 54980005,
    }),
    "changeFailed_msg": _tools.RODict({
        "ID": "changeFailed_msg",
        "value": 54980006,
    }),
    "loginFailed_msg": _tools.RODict({
        "ID": "loginFailed_msg",
        "value": 54980007,
    }),
    "checkProtocol_msg": _tools.RODict({
        "ID": "checkProtocol_msg",
        "value": 54980008,
    }),
    "connectionTimedOut_msg": _tools.RODict({
        "ID": "connectionTimedOut_msg",
        "value": 54980009,
    }),
    "forceLogout": _tools.RODict({
        "ID": "forceLogout",
        "value": 54980011,
    }),
    "changeAccountExplanation": _tools.RODict({
        "ID": "changeAccountExplanation",
        "value": "当日早5点至次日早5点间，只能切换一次账号进入。",
    }),
    "inputTelephoneNum": _tools.RODict({
        "ID": "inputTelephoneNum",
        "value": "请输入手机号",
    }),
    "inputVerificationCode": _tools.RODict({
        "ID": "inputVerificationCode",
        "value": "请输入验证码",
    }),
    "loginWaiting": _tools.RODict({
        "ID": "loginWaiting",
        "value": "账号登录中...",
    }),
    "realNameApprove": _tools.RODict({
        "ID": "realNameApprove",
        "value": 54990035,
    }),
    "accountLogout": _tools.RODict({
        "ID": "accountLogout",
        "value": 54990036,
    }),
    "announcementURL": _tools.RODict({
        "ID": "announcementURL",
        "value": "http://meta-patch.xwindlab.com/notice.jpg",
    }),
    "announcementNoticeURL": _tools.RODict({
        "ID": "announcementNoticeURL",
        "value": "https://mall-res.xwindlab.com/prod/operationFile/pro/notice.json",
    }),
    "iWantLogout": _tools.RODict({
        "ID": "iWantLogout",
        "value": "我要注销该账号",
    }),
    "enterWrongTips": _tools.RODict({
        "ID": "enterWrongTips",
        "value": 54990091,
    }),
    "enterEmptyTips": _tools.RODict({
        "ID": "enterEmptyTips",
        "value": 54990092,
    }),
    "didAccountNumTips": _tools.RODict({
        "ID": "didAccountNumTips",
        "value": 54990097,
    }),
    "simulatorloginForbidMsg": _tools.RODict({
        "ID": "simulatorloginForbidMsg",
        "value": 54980010,
    }),
    "announcementInfoURL": _tools.RODict({
        "ID": "announcementInfoURL",
        "value": "http://meta-patch.xwindlab.com/Announcement.json",
    }),
    "testPublishAnnouncementInfoURL": _tools.RODict({
        "ID": "testPublishAnnouncementInfoURL",
        "value": "https://testmall-res.xwindlab.com/test/operationFile/pro/notice.json",
    }),
    "testTestAnnouncementInfoURL": _tools.RODict({
        "ID": "testTestAnnouncementInfoURL",
        "value": "https://testmall-res.xwindlab.com/test/operationFile/test/notice.json",
    }),
    "publishAnnouncementInfoURL": _tools.RODict({
        "ID": "publishAnnouncementInfoURL",
        "value": "https://mall-res.xwindlab.com/prod/operationFile/pro/notice.json",
    }),
    "testAnnouncementInfoURL": _tools.RODict({
        "ID": "testAnnouncementInfoURL",
        "value": "https://mall-res.xwindlab.com/prod/operationFile/test/notice.json",
    }),
    "needTheSameRealName": _tools.RODict({
        "ID": "needTheSameRealName",
        "value": 54990174,
    }),
    "bannedUserAppealLink": _tools.RODict({
        "ID": "bannedUserAppealLink",
        "value": "https://xfkjgzyxgs.dingwei.netease.com/survey/45yosj/paper?uid=%s",
    }),
    "patchMessage": _tools.RODict({
        "ID": "patchMessage",
        "value": 54990180,
    }),
    "userServiceAgreement": _tools.RODict({
        "ID": "userServiceAgreement",
        "value": "用户服务协议",
    }),
    "privacyPolicy": _tools.RODict({
        "ID": "privacyPolicy",
        "value": "隐私政策",
    }),
    "privacyPolicySummary": _tools.RODict({
        "ID": "privacyPolicySummary",
        "value": "隐私政策摘要",
    }),
    "personalInformationList": _tools.RODict({
        "ID": "personalInformationList",
        "value": "个人信息清单",
    }),
    "personalInformationSharingChecklist": _tools.RODict({
        "ID": "personalInformationSharingChecklist",
        "value": "第三方个人信息分享清单",
    }),
    "noReasonForReturn": _tools.RODict({
        "ID": "noReasonForReturn",
        "value": "退换货规则",
    }),
    "intellectualProperty": _tools.RODict({
        "ID": "intellectualProperty",
        "value": "知识产权侵权投诉指引",
    }),
    "notice": _tools.RODict({
        "ID": "notice",
        "value": "关于《退换货规则》公开征求意见",
    }),
    "notice2": _tools.RODict({
        "ID": "notice2",
        "value": "关于《知识产权侵权投诉指引》公开征求意见",
    }),
    "intellectualMailNotice": _tools.RODict({
        "ID": "intellectualMailNotice",
        "value": "关于受理知识产权侵权投诉邮箱变更的公告",
    }),
    "yuanBeiRulesNotice": _tools.RODict({
        "ID": "yuanBeiRulesNotice",
        "value": "关于《积分获取及使用规则》调整公开征求意见",
    }),
    "yuanBeiRulesNotice2": _tools.RODict({
        "ID": "yuanBeiRulesNotice2",
        "value": "积分获取及使用规则",
    }),
    "digitalWorldCommunityRules": _tools.RODict({
        "ID": "digitalWorldCommunityRules",
        "value": "社区规则",
    }),
    "digitalWorldCommunityRulesNotice": _tools.RODict({
        "ID": "digitalWorldCommunityRulesNotice",
        "value": "关于《社区规则》公开征求意见",
    }),
    "userAgreementNotice": _tools.RODict({
        "ID": "userAgreementNotice",
        "value": "关于《用户服务协议》公开征求意见",
    }),
    "pleaseReadAll": _tools.RODict({
        "ID": "pleaseReadAll",
        "value": 54990252,
    }),
    "readingTimeHasNotEnded": _tools.RODict({
        "ID": "readingTimeHasNotEnded",
        "value": 54990253,
    }),
    "withdrawalOfConsent": _tools.RODict({
        "ID": "withdrawalOfConsent",
        "value": 54990267,
    }),
    "queuingWhiteList": _tools.RODict({
        "ID": "queuingWhiteList",
        "value": 0,
    }),
    "accountsDinghao": _tools.RODict({
        "ID": "accountsDinghao",
        "value": 54001589,
    }),
    "login_greenPasswordError": _tools.RODict({
        "ID": "login_greenPasswordError",
        "value": 54001591,
    }),
    "login_areaPlayerFull": _tools.RODict({
        "ID": "login_areaPlayerFull",
        "value": 54001592,
    }),
    "agreementUnchecked": _tools.RODict({
        "ID": "agreementUnchecked",
        "value": 54002070,
    }),
    "phoneEmpty": _tools.RODict({
        "ID": "phoneEmpty",
        "value": 54002071,
    }),
    "phoneInvalid": _tools.RODict({
        "ID": "phoneInvalid",
        "value": 54002072,
    }),
    "smsSentSuccess": _tools.RODict({
        "ID": "smsSentSuccess",
        "value": 54002073,
    }),
    "smsEmpty": _tools.RODict({
        "ID": "smsEmpty",
        "value": 54002074,
    }),
    "smsInvalid": _tools.RODict({
        "ID": "smsInvalid",
        "value": 54002075,
    }),
    "smsExpired": _tools.RODict({
        "ID": "smsExpired",
        "value": 54002076,
    }),
    "nameEmpty": _tools.RODict({
        "ID": "nameEmpty",
        "value": 54002077,
    }),
    "nameFormatInvalid": _tools.RODict({
        "ID": "nameFormatInvalid",
        "value": 54002078,
    }),
    "idCardEmpty": _tools.RODict({
        "ID": "idCardEmpty",
        "value": 54002079,
    }),
    "idCardFormatInvalid": _tools.RODict({
        "ID": "idCardFormatInvalid",
        "value": 54002080,
    }),
    "authProcessing": _tools.RODict({
        "ID": "authProcessing",
        "value": 54002081,
    }),
    "authSuccess": _tools.RODict({
        "ID": "authSuccess",
        "value": 54002082,
    }),
    "authFailed": _tools.RODict({
        "ID": "authFailed",
        "value": 54002083,
    }),
    "minorAuth": _tools.RODict({
        "ID": "minorAuth",
        "value": 54002084,
    }),
    "policeApiError": _tools.RODict({
        "ID": "policeApiError",
        "value": 54002085,
    }),
    "infoMismatch": _tools.RODict({
        "ID": "infoMismatch",
        "value": 54002086,
    }),
    "realNameAuth": _tools.RODict({
        "ID": "realNameAuth",
        "value": 54002087,
    }),
    "authUnfinished": _tools.RODict({
        "ID": "authUnfinished",
        "value": 54002088,
    }),
    "phoneRepeat": _tools.RODict({
        "ID": "phoneRepeat",
        "value": 54002089,
    }),
    "phoneSuccess": _tools.RODict({
        "ID": "phoneSuccess",
        "value": 54002090,
    }),
    "phoneFrequentTime": _tools.RODict({
        "ID": "phoneFrequentTime",
        "value": 10,
    }),
    "phoneFrequent": _tools.RODict({
        "ID": "phoneFrequent",
        "value": 54002091,
    }),
    "phoneFrequentLockTime": _tools.RODict({
        "ID": "phoneFrequentLockTime",
        "value": 25,
    }),
    "phoneFrequentLock": _tools.RODict({
        "ID": "phoneFrequentLock",
        "value": 54002092,
    }),
    "webRequestException": _tools.RODict({
        "ID": "webRequestException",
        "value": 54002093,
    }),
    "webFrequentRequests": _tools.RODict({
        "ID": "webFrequentRequests",
        "value": 54002094,
    }),
    "underageBlock": _tools.RODict({
        "ID": "underageBlock",
        "value": 54002095,
    }),
    "agreementContent": _tools.RODict({
        "ID": "agreementContent",
        "value": "我已详细阅读并同意<link url label=《用户协议》 url=https://api.yunxingu.com/mobile/index.html/#/privacy?index=0>、<link url label=《隐私政策》 url=https://api.yunxingu.com/mobile/index.html/#/privacy?index=1>和<link url label=《儿童隐私保护政策》 url=https://api.yunxingu.com/mobile/index.html/#/privacy?index=2>。",
    }),
    "loginFailed_msgLogin": _tools.RODict({
        "ID": "loginFailed_msgLogin",
        "value": 54002101,
    }),
    "loginFailed_checkSim": _tools.RODict({
        "ID": "loginFailed_checkSim",
        "value": 54002102,
    }),
    "loginFailed_checkNet": _tools.RODict({
        "ID": "loginFailed_checkNet",
        "value": 54002103,
    }),
    "loginFailed_wrongOperator": _tools.RODict({
        "ID": "loginFailed_wrongOperator",
        "value": 54002104,
    }),
    "inMaintenance_msgLogin": _tools.RODict({
        "ID": "inMaintenance_msgLogin",
        "value": 54002105,
    }),
    "frequentRequests_tryLater": _tools.RODict({
        "ID": "frequentRequests_tryLater",
        "value": 54002106,
    }),
    "codeFailed_checkNet": _tools.RODict({
        "ID": "codeFailed_checkNet",
        "value": 54002107,
    }),
    "loginExpired_relogin": _tools.RODict({
        "ID": "loginExpired_relogin",
        "value": 54002108,
    }),
    "authFailed_checkInfo": _tools.RODict({
        "ID": "authFailed_checkInfo",
        "value": 54002109,
    }),
    "authFailed_checkNet": _tools.RODict({
        "ID": "authFailed_checkNet",
        "value": 54002110,
    }),
    "codeFailed_isLimited": _tools.RODict({
        "ID": "codeFailed_isLimited",
        "value": 54002111,
    }),
    "serverUnlockTimeMsg": _tools.RODict({
        "ID": "serverUnlockTimeMsg",
        "value": 54002164,
    }),
    "TaptaploginAnomaly": _tools.RODict({
        "ID": "TaptaploginAnomaly",
        "value": 54481007,
    }),
    "activationPass": _tools.RODict({
        "ID": "activationPass",
        "value": 54002067,
    }),
    "activationFail": _tools.RODict({
        "ID": "activationFail",
        "value": 54002068,
    }),
    "authFailed_tooManyAccounts": _tools.RODict({
        "ID": "authFailed_tooManyAccounts",
        "value": 54002112,
    }),
    "greenCode_wrong": _tools.RODict({
        "ID": "greenCode_wrong",
        "value": 54002120,
    }),
    "greenCode_invalid": _tools.RODict({
        "ID": "greenCode_invalid",
        "value": 54002121,
    }),
    "patchUpdate_restart": _tools.RODict({
        "ID": "patchUpdate_restart",
        "value": 54002130,
    }),
    "patchUpdate_launcher": _tools.RODict({
        "ID": "patchUpdate_launcher",
        "value": 54002131,
    }),
    "fullUpdate_download": _tools.RODict({
        "ID": "fullUpdate_download",
        "value": 54002132,
    }),
    "register_blockNumbers": _tools.RODict({
        "ID": "register_blockNumbers",
        "value": ([17000000000, 170999999999], [17100000000, 171999999999], [16500000000, 165999999999], [16700000000, 167999999999], [16200000000, 162999999999]),
    }),
    "register_blockNumbersMsg": _tools.RODict({
        "ID": "register_blockNumbersMsg",
        "value": 54980012,
    })
})