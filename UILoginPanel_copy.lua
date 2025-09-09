local UILoginPanel = class("UILoginPanel", require("./Common/UIBase"))

local json = require("Common/json")
local base64 = require("Common/Base64")

function UILoginPanel:Awake()

    --用户协议版本号
    self.LicenseVersion = 2

    -- 上次登录是qq还是微信
    self.m_lastChannelID = -1
    self.m_lastServerTreeNodeCount = -1
    self.m_lastServerLeafNodeCount = -1
    --设置物理同步，当Transform变化的时候更新相关的物理数据
    g_CS:UnityEngine_Physics().autoSyncTransforms = false
    self.useSDK = g_CS:LoadingConfigManager_Instance():UseSDK()
    self.useQueue = g_CS:LoadingConfigManager_Instance():UseQueue()
    self.canLoginWithIOS = g_CS:LoadingConfigManager_Instance():CanLoginWithGuest()

    --判断是否是手游助手模拟器
    self.isAssistGame = g_MSDKDataManager:CheckEmulatorType("Tencent")

    self.isCloudGame = g_MSDKDataManager:CheckEmulatorType("YYX%-CloudMatrix1")

    self.m_friendPanel = self.gameObject.transform:Find("Main/ServerLogin/Friend").gameObject
    self.m_friendPanel:SetActive(false)
    self:InitZoneTable()

    self.ColorTable = {}
    self.StateNameTable = { [0] = "维护", [1] = "流畅", [2] = "拥挤", [3] = "爆满", }
    --排队中
    self.m_isInQueue = false
    self.m_loginCallBack = nil  --排队成功的登录回调（如果不排队直接执行）

    self.m_serverListTable = {}
    self.m_serverListInited = false

    -- 安装app后第一次启动应用 过场动画id
    self.cinemaHistoryID = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableNewbieCreate, "openGameCG", g_ConfigTable.NewbieCretae_Value) or "98100049"
    --self.selectServerId = 0

    local roleIDs = g_ConfigData:GetKeysFromConfigTable(g_ConfigTable.TableCharcter)
    self.TotalRoleCount = #roleIDs

    if g_DataUserInfoManager.CommonTutorOpen == nil then
        g_DataUserInfoManager.CommonTutorOpen = tonumber(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableNewbieCreate, "newRole_isOpen", g_ConfigTable.NewbieCretae_Value)) == 1
    end

    --清空数据
    g_CS:DataUserInfoManager_Instance():ResetData()
    g_CS:NetworkManager_Instance():Reset()

    local colorKeyList = { "color_weihu", "color_kongxian", "color_fanmang", "color_baoman" }
    for i = 1, #colorKeyList do
        local colorId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, colorKeyList[i], g_ConfigTable.Table_Value)
        local colorStr = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableTextColor, colorId, g_ConfigTable.TextColor_color)
        local color = g_LuaUtil:GetColorByTable(colorStr)
        self.ColorTable[i - 1] = color
    end

    --登录场景关闭鹰眼
    --g_LuaUtil:SetHawkeye(false)

    -- 设置依赖于角色位置等信息的渲染相关参数（这个场景非常特殊，没有主角，所以没有RenderConfigByPlayerUpdate.cs来设置和更新角色位置等信息）
    self:SetupRenderConfigByPlayerUpdate()

    self.m_listener = {
        { g_EventDef.EVENT_LOGIN_PASSWORD, self.OnLoginByPassword },
        { g_EventDef.EVENT_LOGIN_EUSDK_LOGIN_CALLBACK, self.OnLoginByEUSDK },
        { g_EventDef.EVENT_LOGIN_LOGIN_SUCESS, self.onLoginSuccessfully },
        { g_EventDef.EVENT_LOGIN_LOGIN_FAIL, self.onLoginFail },
        { g_EventDef.EVENT_LOGIN_GET_SERVERLIST, self.OnGetServerList },
        { g_EventDef.EVENT_LOGIN_SERVER_STATE_CALLBACK, self.OnGetServerState },
        { g_EventDef.EVENT_LOGIN_CHARACTER_INFO_CALLBACK, self.OnGetCharacterInfo },
        { g_EventDef.EVENT_KBE_ONLOGINSUCCESSFULLY, self.onLoginServerSuccessfully },
        { g_EventDef.EVENT_KBE_ONREQAVATARLIST, self.onReqAvatarList },
        { g_EventDef.EVENT_LOGIN_RELOGIN, self.StartLogin },
        { g_EventDef.EVENT_LOGIN_ROLE_RETURN, self.OnRoleReturn },
        { g_EventDef.EVENT_NET_ON_CONNECTION_STATE, self.OnConnectState },
        { g_EventDef.EVENT_KBE_SCRIPT_VERSION_NOT_MATCH, self.OnVersionNotMatch },
        { g_EventDef.EVENT_KBE_ONLOGIN_FAILED, self.OnConnectServerFail },
        { g_EventDef.EVENT_KBE_LOGIN_BASEAPP_FAILED, self.OnConnectServerFail },
        { g_EventDef.EVENT_NET_ONSERVERCHECKCDKEY, self.OnHandleServerCheckCDKey },
        { g_EventDef.EVENT_NET_ONSENDCDKEYRESULT, self.OnHandleActivatedResult },
        { g_EventDef.EVENT_UNITY_LOADSCENEFINISHED, self.OnHandleUnitySceneLoaded },
        { g_EventDef.EVENT_KBE_ON_KICK_ANOTHER_AVATAR, self.OnKickAnotherAvatar },
        { g_EventDef.EVENT_NET_ON_MSDK_LOGIN, self.OnMSDKLogin },
        { g_EventDef.EVENT_NET_ON_MSDK_LOGIN_FAIL, self.OnMSDKLoginFail },
        { g_EventDef.EVENT_KBE_ACCOUNT_BEKICKED, self.OnHandleAccountBeKicked },
        -- { g_EventDef.EVENT_NET_ON_MSDK_JOIN_QUEUE, self.OnHandleMSDKJoinQueue },
        -- { g_EventDef.EVENT_NET_ON_MSDK_EXIT_QUEUE, self.OnHandleMSDKExitQueue },
        -- { g_EventDef.EVENT_NET_ON_MSDK_JOIN_QUEUE_FAIL, self.OnHandleMSDKJoinQueueFail },
        -- { g_EventDef.EVENT_NET_ON_MSDK_EXIT_QUEUE_FAIL, self.OnHandleMSDKExitQueueFail },
        -- { g_EventDef.EVENT_NET_ON_MSDK_QUEUE_ERROR, self.OnHandleMSDKQueueError },
        -- { g_EventDef.EVENT_NET_ON_MSDK_FINISH_QUEUE, self.OnHandleMSDKFinishQueue },
        { g_EventDef.EVENT_UI_REFRESH_MAINCITY, self.OnHandleRefreshUI },
        { g_EventDef.EVENT_MAPLE_QUERY_TREE_FINISHED, self.OnHandleMapleQueryTreeFinished },
        { g_EventDef.EVENT_MAPLE_ON_GET_SERVERLISTDIR, self.OnHandleGetServerlistDir },
        { g_EventDef.EVENT_LOGIN_IN_GAME_FRIEND_INFO_CALLBACK, self.OnHandleOnGetInSameFriend },
        --{ g_EventDef.EVENT_MSDK_DIFFERENT_ACCOUNT_LOGOUT, self.OnHandleDifferentAccountLogout },

        { g_EventDef.EVENT_DID_VERIFY_CALLBACK, self.OnDIDVerifyCallback },
        { g_EventDef.EVENT_DID_SET_SUCESS, self.OnDIDSetSucess },
        { g_EventDef.EVENT_ON_CHECK_CAPTCHA, self.OnHandleCheckCaptcha},
        --{ g_EventDef.EVENT_UI_GET_DID_ACCOUNT_LIST, self.OnGetDidAccountList },
    }

    g_DataUserInfoManager.m_isRealName = false

    --g_DataUserInfoManager.returnLoginType = nil

    self.login_tooBusy_firstWaitTime = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, g_ConfigTable.LoginSet_login_tooBusy_firstWaitTime, g_ConfigTable.Table_Value)
    self.login_tooBusy_secondWaitTime = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, g_ConfigTable.LoginSet_login_tooBusy_secondWaitTime, g_ConfigTable.Table_Value)
    self.login_tooBusy_text = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, g_ConfigTable.LoginSet_login_tooBusy_text, g_ConfigTable.Table_Value)


    --是否不可用版本,跳转到对应商店下载
    if CS.MainStart.IsAbandoned == true then
        local confirmFunc = function()
            local url = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "iosAppStoreUrl", g_ConfigTable.Table_Value)
            g_CS.UnityEngine_Application_OpenURL(url)
            g_CS.UnityEngine_Application_Quit()
        end
        local cancelFunc = function()
            g_CS.UnityEngine_Application_Quit()
        end
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_androidUpdate_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(confirmFunc, cancelFunc, messageId)
        return
    end

--     self:InitCG()
--     self:PlayCG()


end

function UILoginPanel:InitCG()
    self.m_videoPlayer = self.gameObject.transform:Find('Video'):GetComponent(g_Component.VideoPlayer)
    local videoEnd = function()
        self.m_videoPlayer.gameObject:SetActive(false)
    end

    self.m_videoPlayer:loopPointReached('+', videoEnd)

    local btn = self.m_videoPlayer.transform:GetComponent(g_Component.Button)
    self.AddButtonOnClick(btn, self.StopCG)
end

function UILoginPanel:PlayCG()
    self.m_videoPlayer.gameObject:SetActive(true)
    self.m_videoPlayer:Play()
end

function UILoginPanel:StopCG()
    self.m_videoPlayer.gameObject:SetActive(false)
end


function UILoginPanel:Start()

    ------------------第一次玩家测试机型限制------------------------
    local UIDeviceLimit = require("UI/UIDeviceLimit")
    local isLimited = UIDeviceLimit:DeviceLimit()
    ---------------------------------------------------------------

    ----判断是否请求过电话权限，没有的话进行请求
    --if g_CS.MyUtils_IsAndroidDevice() then
    --	if g_CS:UnityEngine_PlayerPrefs().GetInt("requestedReadPhoneState", 0) == 0 then
    --		g_CS:UnityEngine_PlayerPrefs().SetInt("requestedReadPhoneState", 1)
    --		local confirmFunc = function()
    --			local permission = g_GlobalDefine.AndroidPermission.ReadPhoneState
    --        	g_CS.UnityEngine_Android_Permission_RequestUserPermission(permission)
    --    	end
    --		local msgId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "getPhonePermission", g_ConfigTable.Table_Value)
    --		g_UITipsManager:ShowMessage(confirmFunc, nil, msgId)
    --	end
    --end

    print("!!UILoginPanel:Start")

    self.mainObj = g_CS.UnityEngine_GameObject_FindGameObjectWithTag("MainStart")
    if self.mainObj ~= nil then
        self.mainStart = self.mainObj:GetComponent(g_Component.MainStart)
    end

    --关闭应用服网络重连
    if g_CS:NetworkManager_Instance() ~= nil then
        g_CS:NetworkManager_Instance().enabled = false
    end

    self:InitUI()

    self:InitSelectRoleScene()

    self.m_SVNVersionText.text = string.format("svn version: %s", g_CS:LoadingConfigManager_Instance():GetSvnVersion())
    self.m_AppVersionText.text = string.format("app version: %s", g_CS.MainStart_GetAppVersion())
    self.m_LCVersionText.text = string.format("res version: %s", g_CS.MainStart_GetLCVersion())
    self.m_ABVersionText.text = string.format("ab  version: %s", g_CS.MainStart_GetABVersion())

    -- pc包和移动端文字叠在一起了 重新设置一下层级 让layout组件重新工作
    self.m_ABVersionText.transform:SetAsFirstSibling()
    self.m_LCVersionText.transform:SetAsFirstSibling()
    self.m_AppVersionText.transform:SetAsFirstSibling()
    self.m_SVNVersionText.transform:SetAsFirstSibling()

    if self.mainStart.isBanshuVersion == true then
        self.m_SVNVersionText.gameObject:SetActive(false)
    end

    --开始就随机一个名字
    --self:OnClickRandomName()

    g_GlobalDefine.EndGuideTriggerList = nil
    if g_GlobalDefine.MiniChatPanel ~= nil then
        g_CS.UnityEngine_GameObject_Destroy(g_GlobalDefine.MiniChatPanel)
        g_GlobalDefine.MiniChatPanel = nil
    end
    --
    self:ResetLoginClient()
    --self.m_loginClient:connect("192.168.16.201", 2020)





    self.connectDelay = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "connect_ui_delay", g_ConfigTable.Table_Value)

    if g_MSDKDataManager.differentAccount == true then
        if g_MSDKDataManager.loginData.gameData == g_GlobalDefine.MSDKWakeUpGameData.WeChatGameCenter then
            self:LoginWithWX()
        elseif g_MSDKDataManager.loginData.gameData == g_GlobalDefine.MSDKWakeUpGameData.QQGameCenter then
            self:LoginWithQQ()
        end
        g_MSDKDataManager.differentAccount = false
    end

    self.loginCount = 0;

    if g_MSDKDataManager.IDIPPlayerAuthorData == false then
        self:SetAgreementShowState(false, false)
        g_MSDKDataManager.IDIPPlayerAuthorData = true
    end

    if g_CS:LoadingConfigManager_Instance():IsManualSelectServer() then
        if not self.useSDK then
            self:GetServerList()
        else
            g_MSDKDataManager:HasDirInfo(false)
        end
        self:StartLogin()
    else
        local loginType = g_DataUserInfoManager.returnLoginType
        --不可用版本
        if CS.MainStart.IsAbandoned == true or isLimited then
            loginType = 4
        end
        --显示新登陆模块
        self:RefreshLoginModule(loginType)
    end


    g_DataUserInfoManager.returnLoginType = nil
    
    CS.SDKManager.Instance:InitAppDump(CS.MainStart.GetLCVersion(), CS.SDKManager.Channel, CS.MainStart.GetAppVersion())
    CS.SDKManager.Instance:InitCaptcha("db604d47a72143138935bc0505761ff9", false, g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableConst, "graphicCodeTimeLimit", g_ConfigTable.Const_Value) * 1000)
end

-- 设置依赖于角色位置等信息的渲染相关参数
function UILoginPanel:SetupRenderConfigByPlayerUpdate()
    g_CS.UnityEngine_Shader_SetGlobalVector(g_CS:TA_ShaderUtils().PlayerPosID, g_CS.UnityEngine_Vector4(0, 0, 0, 0))
    g_CS.UnityEngine_Shader_SetGlobalFloat(g_CS:TA_ShaderUtils().InteractScaleID, 0.0)
end

function UILoginPanel:ShowUI()
    -- 初始化红点系统
    g_RedDotMgr:InitTree()
    --todo:临时方案 此处对应 UIMainCityPanel 点击背包方法内第一次整理背包
    CS.UnityEngine.PlayerPrefs.DeleteKey("PACK_ARRANGEMENT")

    self:InstallEvents()

    g_CS:GameSceneManager_Singleton():SetCurSceneType(g_CS:GameSceneType().ST_In_Login)

    self.m_loginShadowDistance = tonumber(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableNewbieCreate, "loginShadowDistance", g_ConfigTable.NewbieCretae_Value))
    g_CS:UnityEngine_QualitySettings().shadowDistance = self.m_loginShadowDistance
    self.m_ShadowDistanceID = g_CS.UnityEngine_Shader_PropertyToID("_ShadowDistance")
    g_CS.UnityEngine_Shader_SetGlobalFloat(self.m_ShadowDistanceID, self.m_loginShadowDistance)

    if self.m_3dCamera then
        self.m_3dCamera.gameObject:SetActive(true)
    end
end

function UILoginPanel:HideUI()
    self:UnInstallEvents()

    self:HideMask()

    if self.m_3dCamera then
        self.m_3dCamera.gameObject:SetActive(false)
    end
end

function UILoginPanel:ResetLoginClient()
    if nil ~= self.m_loginClient then
        g_CS.UnityEngine_Object_Destroy(self.m_loginClient)
    end
    self.m_loginClient = self.mainObj:AddComponent(g_Component.LoginClient)
    self.m_loginClient.centerServerList = self.mainStart.m_centerServerList
    -- 重置登录的时候，把循环检测去掉，断开连接有段时间数据是无效的，这个时候执行到检测会出错
    if self.m_getServerListDelayCallId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_getServerListDelayCallId)
        self.m_getServerListDelayCallId = nil
    end
    if self.m_checkActiveDelayCallId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_checkActiveDelayCallId)
        self.m_checkActiveDelayCallId = nil
    end

end

function UILoginPanel:OnDestroy()
    self:HideMask()
    self.m_loginCallBack = nil

    if nil ~= self.delayCallCodeCD then
        g_ScriptEvent:RemoveDelayCall(self.delayCallCodeCD)
    end

    if self.m_didTimeOutDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_didTimeOutDelay)
        self.m_didTimeOutDelay = nil
    end

    if self.m_checkActiveDelayCallId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_checkActiveDelayCallId)
        self.m_checkActiveDelayCallId = nil
    end
    if self.m_getServerListDelayCallId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_getServerListDelayCallId)
        self.m_getServerListDelayCallId = nil
    end

    if self.m_maskDelayCallId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_maskDelayCallId)
        self.m_maskDelayCallId = nil
    end

    if self.m_checkActiveCoro ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_checkActiveCoro)
        self.m_checkActiveCoro = nil
    end

    if self.m_queueDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_queueDelay)
        self.m_queueDelay = nil
    end

    if self.m_queueTimeOutDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_queueTimeOutDelay)
        self.m_queueTimeOutDelay = nil
    end

    g_CS.UnityEngine_Object_Destroy(self.m_loginClient)

    if g_DataUserInfoManager.cinemaParent then
        g_CS.UnityEngine_Object_Destroy(g_DataUserInfoManager.cinemaParent)
    end
    g_DataUserInfoManager.cinemaParent = nil
end

--事件注册
function UILoginPanel:InstallEvents()
    g_EventMgr:RegistListenerBatch(self.m_listener, self)
end

--事件注销
function UILoginPanel:UnInstallEvents()
    g_EventMgr:UnRegistListenerBatch(self.m_listener, self)
end

function UILoginPanel:InitZoneTable()
    self.zoneTable = { ["1"] = { name = "推  荐", servers = {} }, ["2"] = { name = "已有角色", servers = {} } }
    if self.useSDK and g_MSDKDataManager:MSDKPlatformAbilitySwitch() --同玩好友
    then
        self.m_nameLenLimit = 7
        local friendsZoneName = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "msdk_wechatFriendPlayer_areaName", g_ConfigTable.Table_Value)
        self.zoneTable["3"] = { name = friendsZoneName, servers = {} }

        local friendBtn = self.m_friendPanel.transform:GetComponent(g_Component.Button)
        self.AddButtonOnClick(friendBtn, self.OnClickFriendPanel)
    end
end

--初始化UI
function UILoginPanel:InitUI()
    self.m_SVNVersionText = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/Version/SVNVersion"):GetComponent(g_Component.Text)
    self.m_AppVersionText = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/Version/AppVersion"):GetComponent(g_Component.Text)
    self.m_LCVersionText = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/Version/LCVersion"):GetComponent(g_Component.Text)
    self.m_ABVersionText = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/Version/ABVersion"):GetComponent(g_Component.Text)

    self.m_ClickEF = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/ClickEF")

    --user
    self.m_User = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/User")
    self.m_UserNameInputField = g_CS.MyUtils_FindTrans(self.m_User, "UserName"):GetComponent(g_Component.InputField)
    self.m_PassWordInputField = g_CS.MyUtils_FindTrans(self.m_User, "PassWord"):GetComponent(g_Component.InputField)
    self.m_EnterButton = g_CS.MyUtils_FindTrans(self.m_User, "EnterButton"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_EnterButton, self.OnClickEnterBtn)
    ---------------------
    --tencent user
    self.m_txUser = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/UserTX")
    self.m_txUser.gameObject:SetActive(self.useSDK and (not self.canLoginWithIOS) and (not self.isAssistGame) and (not self.isCloudGame))

    self.m_txUserIOS = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/UserTXiOS")

    self.m_txUserIOS.gameObject:SetActive(self.useSDK and self.canLoginWithIOS and (not self.isAssistGame) and (not self.isCloudGame))
    --self.m_User.gameObject:SetActive(not self.useSDK and (not self.isAssistGame)and (not self.isCloudGame))
    self.m_User.gameObject:SetActive(false)

    self.m_guestWindow = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/YkModalWindow")
    self.m_guestWindow.gameObject:SetActive(false)

    --手游助手登录按钮
    self.m_userPC = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/UserPC")
    self.m_userPC.gameObject:SetActive(self.isAssistGame or self.isCloudGame)
    self.m_loginWXIOSPC = g_CS.MyUtils_FindTrans(self.m_userPC, "EnterButtoniOSWeChat"):GetComponent(g_Component.Button)
    self.m_loginQQIOSPC = g_CS.MyUtils_FindTrans(self.m_userPC, "EnterButtoniOSQQ"):GetComponent(g_Component.Button)
    self.m_loginWXAndroidPC = g_CS.MyUtils_FindTrans(self.m_userPC, "EnterButtonAndroidWeChat"):GetComponent(g_Component.Button)
    self.m_loginQQAndroidPC = g_CS.MyUtils_FindTrans(self.m_userPC, "EnterButtonAndroidQQ"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_loginWXIOSPC, self.LoginWithWXIOSPC)
    self.AddButtonOnClick(self.m_loginQQIOSPC, self.LoginWithQQIOSPC)
    self.AddButtonOnClick(self.m_loginWXAndroidPC, self.LoginWithWXAndroidPC)
    self.AddButtonOnClick(self.m_loginQQAndroidPC, self.LoginWithQQAndroidPC)

    self.m_loginWX = g_CS.MyUtils_FindTrans(self.m_txUser, "EnterButtonWX"):GetComponent(g_Component.Button)
    self.m_loginQQ = g_CS.MyUtils_FindTrans(self.m_txUser, "EnterButtonQQ"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_loginWX, self.LoginWithWX)
    self.AddButtonOnClick(self.m_loginQQ, self.LoginWithQQ)
    self.m_loginWXIOS = g_CS.MyUtils_FindTrans(self.m_txUserIOS, "EnterButtonWX"):GetComponent(g_Component.Button)
    self.m_loginWXIOS.gameObject:SetActive(false)
    self.m_loginQQIOS = g_CS.MyUtils_FindTrans(self.m_txUserIOS, "EnterButtonQQ"):GetComponent(g_Component.Button)
    self.m_loginGuestIOS = g_CS.MyUtils_FindTrans(self.m_txUserIOS, "EnterButtonYK"):GetComponent(g_Component.Button)
    self.m_loginAppleIOS = g_CS.MyUtils_FindTrans(self.m_txUserIOS, "EnterButtonApple"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_loginWXIOS, self.LoginWithWX)
    self.AddButtonOnClick(self.m_loginQQIOS, self.LoginWithQQ)
    self.AddButtonOnClick(self.m_loginGuestIOS, self.ShowGuestLoginWindow)
    self.AddButtonOnClick(self.m_loginAppleIOS, self.LoginWithApple)
    self.m_loginGuestIOS.gameObject:SetActive(g_CS.MyUtils_IsInAudit())
    self.m_loginAppleIOS.gameObject:SetActive(g_CS.MyUtils_IsInAudit())
    self.m_loginWXInGuestWindow = g_CS.MyUtils_FindTrans(self.m_guestWindow, "ThirdPanel/Content/EnterButtonWX"):GetComponent(g_Component.Button)
    self.m_loginQQInGuestWindow = g_CS.MyUtils_FindTrans(self.m_guestWindow, "ThirdPanel/Content/EnterButtonQQ"):GetComponent(g_Component.Button)
    self.m_loginGuestCancelBtn = g_CS.MyUtils_FindTrans(self.m_guestWindow, "ThirdPanel/Content/Cancel"):GetComponent(g_Component.Button)
    self.m_loginGuestOKBtn = g_CS.MyUtils_FindTrans(self.m_guestWindow, "ThirdPanel/Content/OkBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_loginWXInGuestWindow, self.LoginWithWX)
    self.AddButtonOnClick(self.m_loginQQInGuestWindow, self.LoginWithQQ)
    self.AddButtonOnClick(self.m_loginGuestCancelBtn, self.HideGuestLoginWindow)
    self.AddButtonOnClick(self.m_loginGuestOKBtn, self.LoginWithGuest)

    --server
    self.m_ServerLogin = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/ServerLogin")
    self.m_ServerLogin.gameObject:SetActive(false)
    self.m_ServerArea = g_CS.MyUtils_FindTrans(self.m_ServerLogin, "Server")
    --self.m_IPAddressInputField = g_CS.MyUtils_FindTrans(self.m_ServerLogin, "IPAddress"):GetComponent(g_Component.InputField)
    self.m_ServerNameText = g_CS.MyUtils_FindTrans(self.m_ServerLogin, "Server/ServerText"):GetComponent(g_Component.Text)
    self.m_ServerNameText.text = "获取中……"
    self.m_ServerStateImage = g_CS.MyUtils_FindTrans(self.m_ServerLogin, "Server/ServerState/Sprite"):GetComponent(g_Component.Image)
    self.m_ServerStateText = g_CS.MyUtils_FindTrans(self.m_ServerLogin, "Server/ServerState/Text"):GetComponent(g_Component.Text)
    self.m_SelectServerBtn = g_CS.MyUtils_FindTrans(self.m_ServerLogin, "Server/SelectServerBtn"):GetComponent(g_Component.Button)
    self.m_SelectServerBtn.gameObject:SetActive(false)
    self.AddButtonOnClick(self.m_SelectServerBtn, self.OnClickSelectServerBtn)
    self.m_LoginBtn = g_CS.MyUtils_FindTrans(self.m_ServerLogin, "LoginButton"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_LoginBtn, self.OnClickLoginBtn)

    --server select
    self.ServerSelect = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/ServerSelect")
    self.m_ServerSelectCloseBtn = g_CS.MyUtils_FindTrans(self.ServerSelect, "CloseButton/ButtonClose2"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_ServerSelectCloseBtn, self.OnClickServerSelectCloseBtn)

    self.ZoneParent = g_CS.MyUtils_FindTrans(self.ServerSelect, "ServerOption/OptionList/Viewport/Content")
    self.ZonePrefab = g_CS.MyUtils_FindTrans(self.ServerSelect, "ServerOption/OptionList/Viewport/Content/prefab").gameObject
    self.ServerParentScroll = g_CS.MyUtils_FindTrans(self.ServerSelect, "ServerScrollRect"):GetComponent(g_Component.ScrollRect)
    self.ServerParentNormal = g_CS.MyUtils_FindTrans(self.ServerSelect, "ServerScrollRect/ViewPort/Grid")
    self.ServerPrefabNormal = g_CS.MyUtils_FindTrans(self.ServerSelect, "ServerPrefab/normalPrefab").gameObject
    self.ServerParentRole = g_CS.MyUtils_FindTrans(self.ServerSelect, "ServerScrollRect/ViewPort/Grid_Role")
    self.ServerPrefabRole = g_CS.MyUtils_FindTrans(self.ServerSelect, "ServerPrefab/rolePrefab").gameObject
    self.ServerParentFriend = g_CS.MyUtils_FindTrans(self.ServerSelect, "ServerScrollRect/ViewPort/Grid_Friend")
    self.ServerPrefabFriend = g_CS.MyUtils_FindTrans(self.ServerSelect, "ServerPrefab/FriendlPrefab").gameObject

    --ButtonArea
    self.ButtonArea = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/ButtonArea")
    self.m_NoticeBtn = g_CS.MyUtils_FindTrans(self.ButtonArea, "AnnounceBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_NoticeBtn, self.OnClickNoticeBtn)
    --审核屏蔽
    if g_CS.MyUtils_IsInAudit() then
        self.m_NoticeBtn.gameObject:SetActive(false)
    end
    self.m_CGBtn = g_CS.MyUtils_FindTrans(self.ButtonArea, "CGBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_CGBtn, self.OnClickCGBtn)
    --审核屏蔽
    if g_CS.MyUtils_IsInAudit() then
        self.m_CGBtn.gameObject:SetActive(false)
    end

    self.m_LogoutBtn = g_CS.MyUtils_FindTrans(self.ButtonArea, "AccountBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_LogoutBtn, self.OnClickLogoutBtn)
    self.m_FixClientBtn = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/ButtonArea/FixBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_FixClientBtn, self.OnClickFixClient)

    --[[
    self.m_loginAccount = g_CS.MyUtils_FindTrans(self.ButtonArea, "AccountBtn/LoginAccount")
    self.m_UserNameText = g_CS.MyUtils_FindTrans(self.m_loginAccount, "Text"):GetComponent(g_Component.Text)
    self.m_QQIcon = g_CS.MyUtils_FindTrans(self.m_loginAccount, "Text/QQIcon")
    self.m_WXIcon = g_CS.MyUtils_FindTrans(self.m_loginAccount, "Text/WXIcon")
    self.m_YKIcon = g_CS.MyUtils_FindTrans(self.m_loginAccount, "Text/YKIcon")
    self.m_AppleIcon = g_CS.MyUtils_FindTrans(self.m_loginAccount, "Text/AppleIcon")
    self.m_KFBtn = g_CS.MyUtils_FindTrans(self.ButtonArea, "KFBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_KFBtn, self.OnClickKFBtn)


    self:ShowUserName(nil)
--]]

    --g_CS.MyUtils_SetLayer(g_CS.MyUtils_FindTrans(self.gameObject.transform, "ModelRoot").gameObject, g_CS.UnityEngine_LayerMask_NameToLayer("3DModel"))
    --self.m_3dCamera = g_CS.MyUtils_FindTrans(self.gameObject.transform, "3DCamera")

    --适龄提示处理
    local ageLimitBtn = self.gameObject.transform:Find("Main/AgeLimitBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(ageLimitBtn, self.OnClickAgeLimitButton)
    self.m_ageLimitWindowObj = self.gameObject.transform:Find("Main/AgeLimitlWindow").gameObject
    local ageLimitWindowCloseBtn = self.gameObject.transform:Find("Main/AgeLimitlWindow/Main/CloseBtn"):GetComponent(g_Component.Button)
    self.ageLimitTextRectTransform = self.m_ageLimitWindowObj.transform:Find("Main/List/Viewport/Text"):GetComponent(g_Component.RectTransform)
    self.AddButtonOnClick(ageLimitWindowCloseBtn, self.OnClickAgeLimitWindowCloseButton)
    self.m_ageLimitWindowObj:SetActive(false)

    --用户协议同意模块
    self.m_agreeMent = g_CS.MyUtils_FindTrans(self.gameObject.transform, "Main/Agreement")
    self.m_agreementToggle = self.m_agreeMent:Find("ToggleBtn"):GetComponent(g_Component.Toggle)
    self.AddToggleOnValueChanged(self.m_agreementToggle, self.OnClickAgreementToggleValueChanged)
    self.m_agreeTipFxObj = self.m_agreeMent:Find("ToggleBtn/FxWhenOff").gameObject
    self:SetAgreementShowState(not self.useSDK, g_CS:UnityEngine_PlayerPrefs().GetInt("clickedAgreePrivacyToggle", 0) == 1)
    local userAgreementBtn = self.m_agreeMent:Find("Text1/OpenLinkBtn"):GetComponent(g_Component.Button)
    local privacyProtectBtn = self.m_agreeMent:Find("Text2/OpenLinkBtn"):GetComponent(g_Component.Button)
    local childPrivacyProtectBtn = self.m_agreeMent:Find("Text3/OpenLinkBtn"):GetComponent(g_Component.Button)
    local thirdInfoShareBtn = self.m_agreeMent:Find("Text4/OpenLinkBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(userAgreementBtn, self.OnClickUserAgreementButton)
    self.AddButtonOnClick(privacyProtectBtn, self.OnClickPrivacyProtectButton)
    self.AddButtonOnClick(childPrivacyProtectBtn, self.OnClickChildPrivacyProtectButton)
    self.AddButtonOnClick(thirdInfoShareBtn, self.OnClick3rdInfoShareButton)

    self.loginLockGo = self.gameObject.transform:Find("Main/ServerLogin/LoginLocked").gameObject
    self.loginLockText = self.gameObject.transform:Find("Main/ServerLogin/LoginLocked/Text"):GetComponent(g_Component.Text)
    self.loginTip = self.gameObject.transform:Find("Main/ServerLogin/LoginTip"):GetComponent(g_Component.CanvasGroup)
    

    --region 新登陆模块

    --用户协议
    self.m_registerRoot = self.gameObject.transform:Find("Main/Register")
    self.m_licenseRoot = self.m_registerRoot:Find("License")
    local licenseAcceptBtn = self.m_licenseRoot:Find("AcceptBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(licenseAcceptBtn, self.OnClickLicenseAcceptBtn)
    local licenseRefuseBtn = self.m_licenseRoot:Find("RefuseBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(licenseRefuseBtn, self.OnClickLicenseRefuseBtn)
    self.m_licenseRefuseConfirm = self.m_licenseRoot:Find("RefuseConfirm")
    local refuseCancelBtn = self.m_licenseRefuseConfirm:Find("CancelBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(refuseCancelBtn, self.OnClickLicenseRefuseCancelBtn)
    local refuseConfirmBtn = self.m_licenseRefuseConfirm:Find("ConfirmBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(refuseConfirmBtn, self.OnClickLicenseRefuseConfirmBtn)
    local xfServerAgreementBtn = self.m_licenseRoot:Find("Scroll View/Viewport/Content/Text/UserBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(xfServerAgreementBtn, self.OnClickLicenseXfServerAgreementBtn)
    local xfPrivacyBtn = self.m_licenseRoot:Find("Scroll View/Viewport/Content/Text/PrivacyBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(xfPrivacyBtn, self.OnClickLicenseXfPrivacyBtn)


    --注册
    self.m_loginRoot = self.m_registerRoot:Find("Login")
    local closeBtn = self.m_loginRoot:Find("ButtonClose2"):GetComponent(g_Component.Button)
    --为了减少操作歧义，先隐藏掉关闭按钮
    closeBtn.gameObject:SetActive(false)
    self.AddButtonOnClick(closeBtn, self.OnClickXFLoginCloseBtn)

    local loginBtn = self.m_loginRoot:Find("LoginBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(loginBtn, self.OnClickXFLoginBtn)

    self.m_xfAgreementToggle = self.m_loginRoot:Find("Toggle"):GetComponent(g_Component.Toggle)
    local agreementInt = g_CS:UnityEngine_PlayerPrefs().GetInt("XFAgreementToggle", 0)
    if agreementInt == 1 then
        self.m_xfAgreementToggle.isOn = true
        self.m_xfAgreement = true
    else
        self.m_xfAgreementToggle.isOn = false
        self.m_xfAgreement = false
    end
    self.AddToggleOnValueChanged(self.m_xfAgreementToggle, self.OnClickXFAgreementToggle)
    local userAgreementBtn = self.m_loginRoot:Find("Toggle/Text/UserBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(userAgreementBtn, self.OnClickUserAgreementBtn)
    local userPrivacyBtn = self.m_loginRoot:Find("Toggle/Text/PrivacyBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(userPrivacyBtn, self.OnClickUserPrivacyBtn)

    self.m_accountInput = self.m_loginRoot:Find("Input/User/Account"):GetComponent(g_Component.InputField)

    self.m_accountExistRoot = self.m_loginRoot:Find("Input/User/Exist")
    self.m_accountAddBtn = self.m_accountExistRoot:Find("AddBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_accountAddBtn, self.OnClickAccountAddBtn)
    self.m_accountSelectBtn = self.m_accountExistRoot:Find("SelectBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_accountSelectBtn, self.OnClickAccountSelectBtn)
    self.m_accountText = self.m_accountExistRoot:Find("SelectBtn/Account"):GetComponent(g_Component.Text)
    self.m_accountSelectPanel = self.m_accountExistRoot:Find("SelectPanel")
    self.m_accountSelectPanelCloseBtn = self.m_accountSelectPanel:GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_accountSelectPanelCloseBtn, self.OnClickAccountSelectPanelCloseBtn)
    self.m_accountSelectList = {}
    for i = 1, 3 do
        local _btn = self.m_accountSelectPanel:Find("Content/" .. i):GetComponent(g_Component.Button)
        self.AddButtonOnClick(_btn, self.OnClickAccountSelectItemBtn)
        local _btn2 = self.m_accountSelectPanel:Find("Content/" .. i .. "/Cancel"):GetComponent(g_Component.Button)
        self.AddButtonOnClick(_btn2, self.OnClickAccountSelectItemRemoveBtn)
        table.insert(self.m_accountSelectList, _btn:GetComponent(g_Component.Text))
    end

    self.m_verificationCode = self.m_loginRoot:Find("Input/User/VerificationCode")
    self.m_codeInput = self.m_verificationCode:Find("Code"):GetComponent(g_Component.InputField)

    self.m_codeGetBtn = self.m_verificationCode:Find("GetBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_codeGetBtn, self.OnClickCodeGetBtn)
    self.m_codeCDRoot = self.m_verificationCode:Find("CD")
    self.m_codeCDText = self.m_codeCDRoot:Find("Text"):GetComponent(g_Component.Text)

    --endregion
    
    -- 游客模式
    self.m_VisitorBtn = self.m_loginRoot:Find("VisitorBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_VisitorBtn,function()
        if g_MarketManager.isH5 then
            g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIH5Market)
        else
            g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIMarket)
        end
    end)
end

------------------------------------------------------------------------------------------------
--region 新登陆模块

--刷新登陆模块
function UILoginPanel:RefreshLoginModule(loginType)
    --为了清除老的token，进入先清除登陆缓存(只一次)
    if g_CS:UnityEngine_PlayerPrefs().GetInt("IsClickSuperR", 0) == 0 then
        g_CS:UnityEngine_PlayerPrefs().SetString("LoginUserList", "")
        g_CS:UnityEngine_PlayerPrefs().SetString("LoginDataJson", "")
        g_CS:UnityEngine_PlayerPrefs().SetInt("IsClickSuperR", 1)
    end

    self.m_registerRoot.gameObject:SetActive(true)
    --注销返回
    if loginType == 3 then
        self:OnClickLicenseAcceptBtn()
        return
    end
    local loginUsersStr = g_CS:UnityEngine_PlayerPrefs().GetString("LoginUserList", "")
    self.m_loginUserList = string.split(loginUsersStr, ',')
    self.m_loginAccount = self.m_loginUserList[1]

    if self.m_loginAccount == "" or string.len(self.m_loginAccount) ~= 11 then
        g_CS:UnityEngine_PlayerPrefs().SetString("LoginUserList", "")
        g_CS:UnityEngine_PlayerPrefs().SetString("LoginDataJson", "")
        self.m_loginUserList = {}
        self.m_loginAccount = ""
        --本地数据为空，走注册流程
        self.m_licenseRoot.gameObject:SetActive(true)
        self.m_loginRoot.gameObject:SetActive(false)
        return
    end

    
    local saveDataStr = g_CS:UnityEngine_PlayerPrefs().GetString("LoginDataJson", "")
    self.saveDataJson = json.decode(saveDataStr)
    local currentData = self.saveDataJson[self.m_loginAccount]
    self.m_token = currentData.token
    self.m_userInfo = currentData.userInfo

    -- if currentData.exp <= os.time() then
    --     --token过期，走注册流程
    --     self.m_accountInput.text = tostring(self.m_loginAccount)
    --     self:OnClickLicenseAcceptBtn()
    --     return
    -- else
    --     --token过期时间小于1天，刷新token
    --     if currentData.exp - os.time() < 86400 then
    --         self:RefreshLoginToken()
    --         return
    --     end
    -- end

    self.m_licenseRoot.gameObject:SetActive(false)
    self.m_loginRoot.gameObject:SetActive(true)

    self.m_accountText.text = string.sub(self.m_loginUserList[1], 1, 3) .. "****" .. string.sub(self.m_loginUserList[1], 8, 11)
    self.m_verificationCode.gameObject:SetActive(false)
    self.m_accountExistRoot.gameObject:SetActive(true)


    --如果用户协议版本号变化，则需弹出用户协议
    if g_CS:UnityEngine_PlayerPrefs().GetInt("LicenseVersion", 0) ~= self.LicenseVersion then
        self.m_licenseRoot.gameObject:SetActive(true)
        self.m_loginRoot.gameObject:SetActive(false)
        loginType = 4
        self.m_licenseReact = true
    end

    if loginType == nil then
        --self:RefreshLoginToken()
        self:OnClickXFLoginBtn()
    end
end


--用户协议 接受按钮
function UILoginPanel:OnClickLicenseAcceptBtn()
    -- 初始化百度安全SDK
    print("lua层调用初始化百度昊天接口")
    CS.SDKManager.Instance:InitHaotian()

    self.m_licenseRoot.gameObject:SetActive(false)
    self.m_loginRoot.gameObject:SetActive(true)

     --保存用户协议版本号
     if g_CS:UnityEngine_PlayerPrefs().GetInt("LicenseVersion", 0) ~= self.LicenseVersion then
        g_CS:UnityEngine_PlayerPrefs().SetInt("LicenseVersion", self.LicenseVersion)
    end

    if self.m_licenseReact == true then
        return
    end

    self.m_xfAgreementToggle.isOn = false
    self.m_verificationCode.gameObject:SetActive(true)
    self.m_accountExistRoot.gameObject:SetActive(false)
end

--用户协议 拒绝按钮
function UILoginPanel:OnClickLicenseRefuseBtn()
    local confirmFunc = function()
        --退出应用
        g_CS.UnityEngine_Application_Quit()
    end
    local cancelFunc = function()
    end
    local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "rejectAgreement_msg", g_ConfigTable.Table_Value)
    g_UITipsManager:ShowMessage(confirmFunc, cancelFunc, messageId)
end

--拒绝用户协议 取消按钮
function UILoginPanel:OnClickLicenseRefuseCancelBtn()
    self.m_licenseRefuseConfirm.gameObject:SetActive(false)
end

--拒绝用户协议 确定按钮
function UILoginPanel:OnClickLicenseRefuseConfirmBtn()
    --退出应用
    g_CS.UnityEngine_Application_Quit()
end

--巽风平台服务协议
function UILoginPanel:OnClickLicenseXfServerAgreementBtn()
    self:OnClickUserAgreementBtn()
end

--巽风隐私协议
function UILoginPanel:OnClickLicenseXfPrivacyBtn()
    self:OnClickUserPrivacyBtn()
end

--用户协议
function UILoginPanel:OnClickUserAgreementBtn()
    local url = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "licenceService", g_ConfigTable.Table_Value)
    g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIWebViewPanel, url)
end

--隐私协议
function UILoginPanel:OnClickUserPrivacyBtn()
    local url = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "privacyProtection", g_ConfigTable.Table_Value)
    g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIWebViewPanel, url)
end

--用户协议 toggle
function UILoginPanel:OnClickXFAgreementToggle(isOn)
    self.m_xfAgreement = isOn
    local saveInt = 0
    if isOn then
        saveInt = 1
    end
    g_CS:UnityEngine_PlayerPrefs().SetInt("XFAgreementToggle", saveInt)
end

function UILoginPanel:AccountAdd()
    self.m_verificationCode.gameObject:SetActive(true)
    self.m_accountExistRoot.gameObject:SetActive(false)
    self.m_accountInput.text = ""
    self.m_codeInput.text = ""
    self.m_loginAccount = ""

    self.m_xfAgreementToggle.isOn = false
end

--添加账号
function UILoginPanel:OnClickAccountAddBtn()
    local confirmFunc = function()
        self:AccountAdd()
    end
    local cancelFunc = function()
    end

    if self:IsAccountChangeLimited() then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "changeFailed_msg", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(confirmFunc, cancelFunc, messageId)
    else
        confirmFunc()
    end
end

--选择账号 按钮
function UILoginPanel:OnClickAccountSelectBtn()
    self.m_accountSelectPanel.gameObject:SetActive(true)

    self:RefreshAccountSelectPanel()
end

--刷新选择账号面板
function UILoginPanel:RefreshAccountSelectPanel()
    for i = 1, 3 do
        if self.m_loginUserList[i] and self.m_loginUserList[i] ~= "" and string.len(self.m_loginUserList[i]) == 11 then
            self.m_accountSelectList[i].gameObject:SetActive(true)
            self.m_accountSelectList[i].text = string.sub(self.m_loginUserList[i], 1, 3) .. "****" .. string.sub(self.m_loginUserList[i], 8, 11)
        else
            self.m_accountSelectList[i].gameObject:SetActive(false)
        end
    end
end

--选择账号面板关闭
function UILoginPanel:OnClickAccountSelectPanelCloseBtn()
    self.m_accountSelectPanel.gameObject:SetActive(false)
end

--选择 某个 账号
function UILoginPanel:OnClickAccountSelectItemBtn(btn)
    local index = tonumber(btn.gameObject.name)
    local confirmFunc = function()
        self.m_loginAccount = self.m_loginUserList[index]
        self.m_accountText.text = self.m_accountSelectList[index].text
    end
    local cancelFunc = function()
    end

    if self:IsAccountChangeLimited() then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "changeFailed_msg", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(confirmFunc, cancelFunc, messageId)
    else
        confirmFunc()
    end

    self.m_accountSelectPanel.gameObject:SetActive(false)
end

--账号切换是否限制
function UILoginPanel:IsAccountChangeLimited()
    local currentUser = g_CS:UnityEngine_PlayerPrefs().GetString("CurrentLoginUserInfo", "")
    local account = ""
    local time = 0
    local count = 1
    if currentUser ~= "" then
        local array = string.split(currentUser, '#')
        account = array[1]
        time = tonumber(array[2])
        count = tonumber(array[3])
    end
    return count >= 2
end

--删除 某个 账号
function UILoginPanel:OnClickAccountSelectItemRemoveBtn(btn)
    local index = tonumber(btn.transform.parent.name)

    local confirmFunc = function()
        table.remove(self.m_loginUserList, index)
        
        local newUserStr = ""
        self:RefreshAccountSelectPanel()
        if #self.m_loginUserList == 0 then
            g_CS:UnityEngine_PlayerPrefs().SetString("LoginUserList", "")
            self:OnClickAccountSelectPanelCloseBtn()
            self:AccountAdd()
        else
            newUserStr = self.m_loginUserList[1]
            local count = 1
            for i = 2, #self.m_loginUserList do
                newUserStr = newUserStr .. "," .. self.m_loginUserList[i]
                count = count + 1
                if count >= 3 then
                    break
                end
            end
        end
        print("UILoginPanel:remove save LoginUserList=", newUserStr)
        g_CS:UnityEngine_PlayerPrefs().SetString("LoginUserList", newUserStr)
    end
    local cancelFunc = function()
    end
    local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "deleteLoginHistory_msg", g_ConfigTable.Table_Value)
    g_UITipsManager:ShowMessage(confirmFunc, cancelFunc, messageId)
end

--登陆 关闭 按钮
function UILoginPanel:OnClickXFLoginCloseBtn()
    self.m_registerRoot.gameObject:SetActive(false)
end

--新登陆按钮
function UILoginPanel:OnClickXFLoginBtn()
    print("UILoginPanel:OnClickXFLoginBtn ", self.m_xfAgreement, self.m_accountInput.text, self.m_codeInput.text)
    if g_CS:UnityEngine_Application().internetReachability == g_CS:UnityEngine_NetworkReachability().NotReachable then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, 99)
        return
    end

    if not self.m_xfAgreement then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "checkProtocol_msg", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
        return
    end


    --如果是已登陆账号，登陆中心服
    if not self.m_verificationCode.gameObject.activeSelf then
        local currentData = self.saveDataJson[self.m_loginAccount]
        self.m_token = currentData.token
        self.m_userInfo = currentData.userInfo
        if currentData.exp <= os.time() then
            --token过期，走注册流程
            self.m_accountInput.text = tostring(self.m_loginAccount)
            self:OnClickLicenseAcceptBtn()
            return
        else
            --token过期时间小于1天，刷新token
            --if currentData.exp - os.time() < 86400 then
                --self:RefreshLoginToken()
            -- else
                 self:LoginCenterServer()
            -- end
        end

        return
    end

    if self.m_accountInput.text == "" or string.len(self.m_accountInput.text) ~= 11 then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "wrongPhoneNumber_msg", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
        return
    end

    if self.m_codeInput.text == "" then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "wrongVerificationCode_msg", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
        return
    end

    self.m_loginAccount = self.m_accountInput.text

    local body = {}
    body.phone = self.m_loginAccount -- 这里应该以登录时输入的手机号为准
    body.code = self.m_codeInput.text
    body.device = g_CS:UnityEngine_SystemInfo().deviceUniqueIdentifier
    body.ts = os.time() * 1000
    body.sign = body.phone .. body.code .. body.device .. body.ts
    g_LuaUtil:HttpPost("/game/verifyLogin", {}, body, self, self.OnVerifyLogin)

    self:DelayShowMask()
end

--手机验证码 获取 按钮
function UILoginPanel:OnClickCodeGetBtn()
    self.m_loginAccount = self.m_accountInput.text
    if self.m_loginAccount == "" or string.len(self.m_loginAccount) ~= 11 then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "wrongPhoneNumber_msg", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
        return
    end

    local body = {}
    body.phone = self.m_loginAccount
    body.ts = os.time() * 1000
    body.sign = body.phone .. body.ts
    g_LuaUtil:HttpPost("/game/identifyingCode", {}, body, self, self.OnGetCode)

    self.m_codeGetBtn.gameObject:SetActive(false)
    self.m_codeCDRoot.gameObject:SetActive(true)
    self.m_codeCDCurrent = 60
    if nil ~= self.delayCallCodeCD then
        g_ScriptEvent:RemoveDelayCall(self.delayCallCodeCD)
    end
    self.delayCallCodeCD = g_ScriptEvent:DelayCall(0, 1000, self.m_codeCDCurrent + 1, self, 'UpdateCodeCDShow')
end

function UILoginPanel:UpdateCodeCDShow()
    if self.m_codeCDCurrent <= 0 then
        self.m_codeGetBtn.gameObject:SetActive(true)
        self.m_codeCDRoot.gameObject:SetActive(false)

        if nil ~= self.delayCallCodeCD then
            g_ScriptEvent:RemoveDelayCall(self.delayCallCodeCD)
        end
    end

    self.m_codeCDText.text = tostring(self.m_codeCDCurrent)

    self.m_codeCDCurrent = self.m_codeCDCurrent - 1
end

function UILoginPanel:OnApplicationFocus(focus)
    if nil == self.delayCallCodeCD then
        return
    end
    if not focus then
        self.m_focusTime = g_ScriptTime:GetServerRealTimeS()
    else
        local pass = g_ScriptTime:GetServerRealTimeS() - self.m_focusTime
        if pass > 0 then
            self.m_codeCDCurrent = self.m_codeCDCurrent - pass
        end
    end
end

--手机验证码 获取 回调
function UILoginPanel:OnGetCode(isSuccess, data)
    print("UILoginPanel:OnGetCode", isSuccess, data)

    if not isSuccess then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, data)
        return
    end

    data = json.decode(data)
    if data.code ~= 0 then
        g_CS.DebugL8_Log("UILoginPanel:OnGetCode Fail {0}  {1}", data.code, data.msg)

        if g_CS:UnityEngine_Application().internetReachability == g_CS:UnityEngine_NetworkReachability().NotReachable then
            local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
            g_UITipsManager:ShowMessage(messageId, 99)
            return
        end

        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        if data.msg ~= "" and data.msg ~= " " then
            messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_phoneBackMsg_msgID", g_ConfigTable.Table_Value)
        end
        g_UITipsManager:ShowMessage(messageId, data.msg)
        return
    end

end

--登陆 回调
function UILoginPanel:OnVerifyLogin(isSuccess, data)
    print("UILoginPanel:OnVerifyLogin", isSuccess, data)
    self:HideMask()

    if not isSuccess then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, data)
        return
    end

    data = json.decode(data)
    if data.code ~= 0 then
        g_CS.DebugL8_Log("UILoginPanel:OnVerifyLogin Fail {0}  {1}", data.code, data.msg)

        if g_CS:UnityEngine_Application().internetReachability == g_CS:UnityEngine_NetworkReachability().NotReachable then
            local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
            g_UITipsManager:ShowMessage(messageId, 99)
            return
        end

        --token错误，走注册流程
        self.m_accountInput.text = tostring(self.m_loginAccount)
        self:OnClickLicenseAcceptBtn()

        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, data.msg)
        return
    end

    self.m_token = data.data.token
    if data.data.user then
        self.m_userInfo = data.data.user
    end
    
    local decodes = string.split(self.m_token, '.')
    local payload = base64.decode(decodes[2])
    --print("UILoginPanel:OnVerifyLogin decodes[2]=",string.sub(payload, -1))
    print("UILoginPanel:OnVerifyLogin payload=", string.len(payload), payload)
    --旧的token最后位是个空字符，新的最后一位正常
    --payload = string.sub(payload, 1, -2)
    payload = g_LuaUtil:filter_spec_char(payload)

    print("UILoginPanel:OnVerifyLogin2 payload=", string.len(payload), payload)
    local tokenInfo = json.decode(payload)

    local saveDataStr = g_CS:UnityEngine_PlayerPrefs().GetString("LoginDataJson", "")
    self.saveDataJson = {}
    if saveDataStr ~= "" then
        self.saveDataJson = json.decode(saveDataStr)
    end

    local account = self.m_loginAccount
    local currentData = {}
    currentData.token = self.m_token
    currentData.exp = tokenInfo.exp
    currentData.userInfo = self.m_userInfo
    self.saveDataJson[account] = currentData

    saveDataStr = json.encode(self.saveDataJson)
    print("UILoginPanel:OnVerifyLogin saveDataStr=", saveDataStr)
    g_CS:UnityEngine_PlayerPrefs().SetString("LoginDataJson", saveDataStr)

    -- print("UILoginPanel:OnVerifyLogin duration = ", currentData.exp - os.time(), currentData.exp, os.time())

    if self.m_loginUserList == nil then
        self.m_loginUserList = {}
    end
    if self.m_loginUserList[1] ~= account then
        local str = account
        local count = 1
        for i = 1, #self.m_loginUserList do
            if self.m_loginUserList[i] ~= account then
                str = str .. "," .. self.m_loginUserList[i]
                count = count + 1
                if count >= 3 then
                    break
                end
            end
        end
        print("UILoginPanel:OnVerifyLogin save LoginUserList=", str)
        g_CS:UnityEngine_PlayerPrefs().SetString("LoginUserList", str)
    end

    LuaAPIManager:onLoginServerSuccessfully(self.m_token)

    self:LoginCenterServer()
end


--登录Token刷新
function UILoginPanel:RefreshLoginToken()
    local header = {}
    header['Authorization'] = self.m_token
    local body = {}
    body.device = g_CS:UnityEngine_SystemInfo().deviceUniqueIdentifier
    body.ts = os.time() * 1000
    body.sign = body.device .. body.ts
    g_LuaUtil:HttpPost("/user/game/refreshLogin", header, body, self, self.OnVerifyLogin)
end

--登录中心服
function UILoginPanel:LoginCenterServer()
    self:ShowMask()

    local currentData = self.saveDataJson[self.m_loginAccount]
    self.m_token = currentData.token
    self.m_userInfo = currentData.userInfo
    --审核
    self.m_userInfo.isAudit = g_CS.MyUtils_IsInAudit()
    self.m_userInfo.deviceId = g_CS:UnityEngine_SystemInfo().deviceUniqueIdentifier
    local userInfo = json.encode(self.m_userInfo)
    print("UILoginPanel:LoginCenterServer", self.m_loginAccount, self.m_token, true, userInfo)
    self.m_loginClient:Login(self.m_loginAccount, self.m_token, true, userInfo)
end

--再登陆
function UILoginPanel:ReturnLogin()
    if g_CS:LoadingConfigManager_Instance():IsManualSelectServer() then
        self:Logout()
    else
        self:ResetLoginClient()
        self:RefreshLoginModule(1)
    end
end

--endregion
-----------------------------------------------------------------------------------------

function UILoginPanel:InitSelectRoleScene()
    local scene = g_CS.UnityEngine_SceneManagement_SceneManager_GetActiveScene()
    if scene.name ~= g_CS:GameSceneManager_Singleton().SceneName_PlayerRole
    then
        -- g_CS:NetworkManager_Instance():ReturnLogin(false)
        if g_CS:LoadingConfigManager_Instance():IsUseAB() then
            g_CS:AssetBundles_AssetBundleManager_Instance():LoadAssetBundle(g_CS:GameSceneManager_Singleton().SceneName_PlayerRole);
        end
        local syncOperation = g_CS.UnityEngine_SceneManagement_SceneManager_LoadSceneAsync(g_CS:GameSceneManager_Singleton().SceneName_PlayerRole)
        syncOperation.allowSceneActivation = true
        --播放登录场景音乐
        g_CS:FMODManager_Instance():PlayMusic(g_CS:GlobalConst().loginSceneMusicId)
        g_CS:FMODManager_Instance():SetFmodSnapShot(g_CS:FMODManager_FmodSnapShotTypeEnum().Normal, true)
    end
end

--获取服务器列表
function UILoginPanel:GetServerList()
    local address = self.mainStart.m_serverListUrl
    --self.m_loginClient:GetServerList(address)
    self:OnGetServerList("")
end

function UILoginPanel:OnGetServerList(result)
    local needInit = true
    -- if result ~= nil and result ~= "" then
    -- 	needInit = true
    -- 	result = string.gsub(result,"\r","")
    -- 	local items = g_LuaUtil:Split(result, "\n")
    -- 	for i = 1, #items do
    -- 		if items[i] ~= "" and items[i] ~= " " then
    -- 			local values = g_LuaUtil:Split(items[i], " ")
    -- 			local id = values[1]
    -- 			local state = 1
    -- 			if values[4] ~= nil then
    -- 				state = tonumber(values[4])
    -- 			end

    -- 			local hide = 0
    -- 			if values[5] ~= nil then
    -- 				hide = tonumber(values[5])
    -- 			end

    -- 			if g_ConfigData:ContainsKey(g_ConfigTable.ServerList, id) then
    -- 				if self.m_serverListTable[id] == nil then
    -- 					self.m_serverListTable[id] = {mode= tonumber(values[2]), ip=values[3], state = 0, defaultState = state}
    -- 				else
    -- 					self.m_serverListTable[id].mode = tonumber(values[2])
    -- 					self.m_serverListTable[id].ip = values[3]
    -- 					self.m_serverListTable[id].defaultState = state

    -- 					if state > 0 and self.m_serverListTable[id].state > 0 then
    -- 						self.m_serverListTable[id].state = state
    -- 					end

    -- 					self.m_serverListTable[id].hide = hide
    -- 				end
    -- 			else
    -- 				print(id.."不在"..g_ConfigTable.ServerList.."配表中")
    -- 			end
    -- 		end
    -- 	end
    -- else
    -- 	local messageId= g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
    -- 	g_UITipsManager:ShowMessage( messageId, 98)
    -- end
    local serverListData = g_ConfigData:GetTableFromConfigTable(g_ConfigTable.ServerList)
    local state = 1
    local mode = 0
    local hide = 0
    for serverId, serverInfo in pairs(serverListData) do
        local ipAddress = serverInfo.gameServer
        if self.m_serverListTable[serverId] == nil then
            self.m_serverListTable[serverId] = { mode = mode, ip = ipAddress, state = 0, defaultState = state }
        else
            self.m_serverListTable[serverId].mode = mode
            self.m_serverListTable[serverId].ip = ipAddress
            self.m_serverListTable[serverId].defaultState = state

            if state > 0 and self.m_serverListTable[serverId].state > 0 then
                self.m_serverListTable[serverId].state = state
            end

            self.m_serverListTable[serverId].hide = hide
        end
    end
    g_DataUserInfoManager.m_serverListTable = self.m_serverListTable

    if needInit and self.m_serverListInited == false then
        self:InitServerList()
        self.m_serverListInited = true
    else
        self:OnGetServerState()
    end

end
--初始化服务器列表
function UILoginPanel:InitServerList()
    if not g_CS:LoadingConfigManager_Instance():UseSDK() then
        for key, value in pairs(self.m_serverListTable) do
            if value.mode == 0 and (value.hide == nil or value.hide == 0) then
                local serverData = value
                local name = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.ServerList, key, g_ConfigTable.ServerList_Name)
                local zoneID = tostring(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.ServerList, key, g_ConfigTable.ServerList_zoneID))
                local zoneName = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.ServerList, key, g_ConfigTable.ServerList_zoneName)
                -- local recommend= tostring(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.ServerList, key, g_ConfigTable.ServerList_recommend))
                -- local hide= g_ConfigData:GetValueFromConfigTable(g_ConfigTable.ServerList, key, g_ConfigTable.ServerList_ifHide)
                serverData.name = name

                if self.zoneTable[zoneID] == nil then
                    self.zoneTable[zoneID] = {}
                end

                local zone = self.zoneTable[zoneID]

                zone.name = zoneName
                zone.hide = hide
                if zone.servers == nil then
                    zone.servers = {}
                end

                table.insert(zone.servers, key)
                -- if recommend == "1" then
                -- 	table.insert(self.zoneTable["1"].servers, key)
                -- end
            end
        end
    else
        if #g_MSDKDataManager.leafInfo > 0 and #g_MSDKDataManager.treeInfo > 0 then
            --self.qqServerList = g_MSDKDataManager:SelectRecommendServers(g_MSDKDataManager.leafInfo, g_GlobalDefine.MSDKChannelID.QQ)
            --self.wxServerList = g_MSDKDataManager:SelectRecommendServers(g_MSDKDataManager.leafInfo, g_GlobalDefine.MSDKChannelID.WeChat)
            --self.wxRecommendServers = {}
            --self.qqRecommendServers = {}
            -- ServerNode
            self.RecommendServerList = g_MSDKDataManager:SelectRecommendServers(g_MSDKDataManager.leafInfo, g_MSDKDataManager.loginData.channelId)
            -- ServerID
            self.RecommendServers = {}
            self:InitZoneTable()
            for i = 1, #g_MSDKDataManager.leafInfo do
                local id = tostring(g_MSDKDataManager.leafInfo[i].id)
                if id ~= nil then
                    if self.m_serverListTable[id].mode == 0 then
                        local name = self.m_serverListTable[id].name
                        local zoneID = tostring(self.m_serverListTable[id].parentId)
                        local zoneName
                        local hide = 0
                        for j = 1, #g_MSDKDataManager.treeInfo do
                            if zoneID == tostring(g_MSDKDataManager.treeInfo[j].id) then
                                zoneName = g_MSDKDataManager.treeInfo[j].name
                                -- hide = g_MSDKDataManager.treeInfo[j].hide
                                break
                            end
                        end
                        local tag = g_MSDKDataManager.leafInfo[i].tag
                        if zoneName ~= nil then
                            if self.zoneTable[zoneID] == nil then
                                self.zoneTable[zoneID] = {}
                            end

                            local zone = self.zoneTable[zoneID]

                            zone.name = zoneName
                            zone.hide = hide
                            if zone.servers == nil then
                                zone.servers = {}
                            end

                            table.insert(zone.servers, id)

                            -- if g_MSDKDataManager:SelectRecommendServerId(self.RecommendServerList, id) == true then
                            -- 	for m = 1, #self.RecommendServerList do
                            -- 		if self.RecommendServerList[m].id == tonumber(id) then
                            -- 			self.RecommendServers[m] = id
                            -- 		end
                            -- 	end
                            -- end
                        end

                        -- if g_MSDKDataManager.mapleRecommendSwitch == false then
                        -- 	if tag == 2 then -- Recommend = 0x02
                        -- 		table.insert(self.zoneTable["1"].servers, id)
                        -- 	end
                        -- end
                    end
                end
            end

            if g_MSDKDataManager.mapleRecommendSwitch == true then
                --if g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.WeChat then
                --	self.zoneTable["1"].servers = self.wxRecommendServers
                --elseif g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.QQ then
                --	self.zoneTable["1"].servers = self.qqRecommendServers
                --end
                self.zoneTable["1"].servers = self.RecommendServers
            end
        end
    end

    local zoneKeyList = {}
    for key, value in pairs(self.zoneTable) do
        if key ~= "nil" then
            table.insert(zoneKeyList, key)
        end
    end
    table.sort(zoneKeyList, function(a, b)
        return tonumber(a) < tonumber(b)
    end)

    --处理页签
    local showZoneCount = 0
    for i = 1, #zoneKeyList do
        local key = zoneKeyList[i]
        local name = self.zoneTable[key].name
        local hide = self.zoneTable[key].hide
        if hide == 0 or hide == nil then
            local itemObj = self.ZonePrefab
            showZoneCount = showZoneCount + 1
            if self.ZoneParent.childCount < showZoneCount then
                itemObj = g_CS.MyUtils_Instantiate(self.ZonePrefab, self.ZoneParent)
            else
                itemObj = self.ZoneParent:GetChild(showZoneCount - 1).gameObject
            end
            itemObj.name = key
            itemObj.transform:Find("Text"):GetComponent(g_Component.Text).text = name
            itemObj.transform:Find("TextSelected"):GetComponent(g_Component.Text).text = name
            local tog = itemObj:GetComponent(g_Component.Toggle)
            self.AddToggleOnValueChanged(tog, self.OnZoneTogValueChange)
            self.zoneTable[key].toggle = tog
            tog.isOn = false
            itemObj:SetActive(true)

            if g_MSDKDataManager.mapleRecommendSwitch == false then
                table.sort(self.zoneTable[key].servers, function(a, b)
                    return tonumber(a) < tonumber(b)
                end)
            end
        end
    end
    --隐藏多余页签
    if self.ZoneParent.childCount > showZoneCount then
        for i = showZoneCount, self.ZoneParent.childCount - 1 do
            self.ZoneParent:GetChild(i).gameObject:SetActive(false)
        end
    end

    self.zoneTable["1"].toggle.isOn = true
    self.currentSelectZoneID = "1"
    self:RefreshZoneServerStateList()
    self:RefreshSelectServerInfo()
end

--刷新当前大区的服务器列表
function UILoginPanel:RefreshZoneServerStateList()
    if self.currentSelectZoneID == "2" then
        --已有角色
        self.ServerParentRole.gameObject:SetActive(true)
        self.ServerParentNormal.gameObject:SetActive(false)
        self.ServerParentFriend.gameObject:SetActive(false)
        self.ServerParentScroll.content = self.ServerParentRole
        for i = 1, self.ServerParentRole.childCount do
            local item = self.ServerParentRole:GetChild(i - 1)
            if item.gameObject.activeSelf then
                local serverId = item.name
                if self.m_serverListTable[serverId] ~= nil then
                    item:Find("ServerState"):GetComponent(g_Component.Image).color = self.ColorTable[self.m_serverListTable[serverId].state]
                end
            end
        end
    elseif self.currentSelectZoneID == "3" then
        --同玩好友
        self.ServerParentRole.gameObject:SetActive(false)
        self.ServerParentNormal.gameObject:SetActive(false)
        self.ServerParentFriend.gameObject:SetActive(true)
        self.ServerParentScroll.content = self.ServerParentFriend

        local gameFriendCount = self:OnRefreshFriendsInfo(self.m_inGameFriends)
        if gameFriendCount ~= 0
        then
            for i = 1, self.ServerParentFriend.childCount do
                local item = self.ServerParentFriend:GetChild(i - 1)
                if item.gameObject.activeSelf
                then
                    local serverId = item.name
                    if self.m_serverListTable[serverId] ~= nil
                    then
                        item:Find("ServerState"):GetComponent(g_Component.Image).color = self.ColorTable[self.m_serverListTable[serverId].state]
                    end
                end
            end
        end
    else
        self.ServerParentRole.gameObject:SetActive(false)
        self.ServerParentNormal.gameObject:SetActive(true)
        self.ServerParentFriend.gameObject:SetActive(false)
        self.ServerParentScroll.content = self.ServerParentNormal
        local zone = self.zoneTable[self.currentSelectZoneID]
        if zone == nil then
            return
        end
        local serverList = {}
        if self.useSDK then
            for i = 1, #zone.servers do
                if self.m_serverListTable[zone.servers[i]].plat == g_MSDKDataManager.loginData.channelId or self.m_serverListTable[zone.servers[i]].plat == 0 then
                    table.insert(serverList, zone.servers[i])
                end
            end
            --if g_MSDKDataManager.mapleRecommendSwitch == true then
            --if g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.WeChat then
            --	self.zoneTable["1"].servers = self.wxRecommendServers
            --elseif g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.QQ then
            --	self.zoneTable["1"].servers = self.qqRecommendServers
            --end
            --end
        else
            serverList = zone.servers
        end

        for i = 1, #serverList do
            local item = nil
            if i <= self.ServerParentNormal.childCount then
                item = self.ServerParentNormal:GetChild(i - 1)
            end
            if item == nil then
                item = g_CS.MyUtils_Instantiate(self.ServerPrefabNormal, self.ServerParentNormal).transform
                self.AddButtonOnClick(item:GetComponent(g_Component.Button), self.ClickServerItem)
            end
            item.gameObject:SetActive(true)
            local serverId = serverList[i]
            item.gameObject.name = serverId
            item:Find("Text"):GetComponent(g_Component.Text).text = self.m_serverListTable[serverId].name
            item:Find("ServerState"):GetComponent(g_Component.Image).color = self.ColorTable[self.m_serverListTable[serverId].state]

            if self.useSDK then
                item:Find("New").gameObject:SetActive(self.m_serverListTable[serverId].tag == 3)
            end
        end
        if self.ServerParentNormal.childCount > #serverList then
            for i = #serverList + 1, self.ServerParentNormal.childCount do
                local item = self.ServerParentNormal:GetChild(i - 1)
                item.gameObject:SetActive(false)
            end
        end
    end
end


--刷新选中服务器信息
function UILoginPanel:RefreshSelectServerInfo(serverId)
    --local ipAddress = ""
    if serverId == nil then
        if self.useSDK then
            if self.m_needRefreshTreeInfo == true then
                serverId = g_CS:UnityEngine_PlayerPrefs().GetString("SelectServerID", "")
            end
        else
            serverId = g_CS:UnityEngine_PlayerPrefs().GetString("SelectServerID", "")
        end
        if serverId == "" or self.m_serverListTable[serverId] == nil then
            if self.useSDK then
                if self.m_needRefreshTreeInfo == true then
                    self.m_needRefreshTreeInfo = false
                    for i = 1, #self.zoneTable["1"].servers do
                        if self.m_serverListTable[self.zoneTable["1"].servers[i]].plat == g_MSDKDataManager.loginData.channelId or self.m_serverListTable[self.zoneTable["1"].servers[i]].plat == 0 then
                            serverId = self.zoneTable["1"].servers[i]
                            break
                        end
                    end
                end
            else
                for sId in pairs(self.m_serverListTable) do
                    serverId = sId
                    break
                end
            end
            --end
        end
        --[[
        ipAddress = g_CS:UnityEngine_PlayerPrefs().GetString("IPAdress", "")
        if ipAddress == "" then
            ipAddress = self.m_serverListTable[serverId].ip
        end
    else
        ipAddress = self.m_serverListTable[serverId].ip
        --]]
    end

    if serverId ~= nil then
        self.selectServerId = serverId
    end

    local server = self.m_serverListTable[self.selectServerId]
    if server == nil then
        return
    end
    --self.m_IPAddressInputField.text= ipAddress

    self.m_ServerNameText.text = server.name
    self.m_ServerNameText.color = self.ColorTable[2]
    self.m_ServerStateImage.color = self.ColorTable[server.state]
    self.m_ServerStateText.text = self.StateNameTable[server.state]
    self.m_ServerStateText.color = self.ColorTable[server.state]
    if not self.m_SelectServerBtn.gameObject.active then
        self.m_ServerArea.gameObject:SetActive(true)
        self.m_SelectServerBtn.gameObject:SetActive(true)
        self:HideMask()
    end
end

--账号/sdk登录
function UILoginPanel:StartLogin()
    self.m_registerRoot.gameObject:SetActive(false)
    self.m_ServerLogin.gameObject:SetActive(false)

    if not self.useSDK then
        self:OnLoginByPassword()
    else

    end
end

--点击事件start----------------------------------------------------------------------------------------------

--点击登录
function UILoginPanel:OnClickEnterBtn(go)

    if g_CS:UnityEngine_Application().internetReachability == g_CS:UnityEngine_NetworkReachability().NotReachable then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, 99)
        return
    end

    if not self.useSDK then
        self.m_userName = self.m_UserNameInputField.text
        self.m_password = self.m_PassWordInputField.text
        if self.m_userName == "" or self.m_password == "" then
            local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_countOrPasswordEmpty_msgID", g_ConfigTable.Table_Value)
            g_UITipsManager:ShowMessage(messageId)
            return
        end

        if g_LuaUtil:IsUserNameLegal(self.m_userName) == false or g_LuaUtil:IsUserNameLegal(self.m_password) == false then
            local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_countOrPasswordIllegal_msgID", g_ConfigTable.Table_Value)
            g_UITipsManager:ShowMessage(messageId)
            return
        end
        self.m_accountType = 1
        g_CS:UnityEngine_PlayerPrefs().SetString("UserName", self.m_userName)
        g_CS:UnityEngine_PlayerPrefs().SetString("Password", self.m_password)

        self.m_loginClient:Login(self.m_userName, self.m_password, false)
    end
    self:DelayShowMask()
end


--登录 服务器
function UILoginPanel:OnClickLoginBtn_old(go)
    --[[
    if self.loginlock then
        g_UITipsManager:ShowMessage(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, g_ConfigTable.LoginSet_login_tooBusy_msgID, g_ConfigTable.Table_Value), math.max(1, self.curLoginLockTime))
        return
    end
    self.loginCount = self.loginCount + 1
    if self.loginCount >= 3 then
        self:StartLoginLock(math.min(self.login_tooBusy_secondWaitTime, math.floor(self.loginCount / 3) * self.login_tooBusy_firstWaitTime))
    end
    --]]
    --点击反馈 特效
    local canvas = self.gameObject:GetComponentInParent(g_Component.Canvas)
    self.m_ClickEF.position = canvas.worldCamera:ScreenToWorldPoint(g_CS:UnityEngine_Input().mousePosition)
    self.m_ClickEF.gameObject:SetActive(false)
    self.m_ClickEF.gameObject:SetActive(true)

    if g_CS:UnityEngine_Application().internetReachability == g_CS:UnityEngine_NetworkReachability().NotReachable then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, 99)
        return
    end

    local canLogin = true
    if self.m_serverListTable == nil or self.m_serverListTable[self.selectServerId] == nil then
        if not self.useSDK then
            self:GetServerList()
        end
        canLogin = false
    end

    if self.m_loginClient.connected == false then
        self.m_loginClient:connect()
        canLogin = false
    end

    --没有服务器列表或者中心服连接失败
    if not canLogin then
        -- 7 代表GPM登录漏斗中：点击进入应用
        return
    end

    if self.useSDK then
        if g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.WeChat then
            g_CS:UnityEngine_PlayerPrefs().SetString("SelectServerID_WX", self.selectServerId)
        elseif g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.QQ then
            g_CS:UnityEngine_PlayerPrefs().SetString("SelectServerID_QQ", self.selectServerId)
        else
            g_CS:UnityEngine_PlayerPrefs().SetString("SelectServerID", self.selectServerId)
        end
    else
        g_CS:UnityEngine_PlayerPrefs().SetString("SelectServerID", self.selectServerId)
    end

    self.m_loginCallBack = function()
        local ipAddress = "192.168.10.161:20013" -- self.m_serverListTable[self.selectServerId].ip
        print(self.m_accountType, self.m_userName, self.m_password, ipAddress, self.loginToken, self.centerServerId)
    
        g_MSDKDataManager.loginData.serverId = self.selectServerId
    
        local password = self.m_password
        local param = {}
        param.token = self.loginToken
        param.loginServerId = self.centerServerId
    
        if self.useSDK then
            local accessToken
            if g_MSDKDataManager.loginData.channelId == 1 then
                --wx
                accessToken = g_MSDKDataManager.loginData.openKey
            elseif g_MSDKDataManager.loginData.channelId == 2 or g_MSDKDataManager.loginData.channelId == 3 then
                --qq guest
                accessToken = g_MSDKDataManager.loginData.token
            end
            local gameData = g_MSDKDataManager.loginData.gameData
            if gameData == nil
            then
                gameData = ""
            end
            param.accessToken = accessToken
            param.gameData = gameData
            password = self.loginToken
        end
    
        if self.m_accountType == 10 then
            g_EventMgr:SendEvent(g_EventDef.EVENT_NET_ON_CLICK_LOGIN, 1, self.m_userName, password, ipAddress, param)
        else
            g_EventMgr:SendEvent(g_EventDef.EVENT_NET_ON_CLICK_LOGIN, self.m_accountType, self.m_userName, password, ipAddress, param)
        end
    
        local info = {}
        info.accountType = self.m_accountType
        info.userName = self.m_userName
        info.password = password
        info.ip = ipAddress
        info.token = self.loginToken
        info.centerServerId = self.centerServerId
    
        g_DataUserInfoManager.m_loginInfo = info
    
        -- 7 代表GPM登录漏斗中：点击进入应用
        g_MSDKDataManager:HasDirInfo(true)
        self:DelayShowMask()
    end

    if g_GlobalDefine.IsNormalQueue then
        self:sendQueueHttp()
        return
    end

    if self.m_loginCallBack then
        self.m_loginCallBack()
        self.m_loginCallBack = nil
    end
end


--登录 服务器
function UILoginPanel:OnClickLoginBtn(go)
    if g_CS:LoadingConfigManager_Instance():IsManualSelectServer() then
        self:OnClickLoginBtn_old()
        return
    end

    if g_CS:UnityEngine_Application().internetReachability == g_CS:UnityEngine_NetworkReachability().NotReachable then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, 99)
        return
    end

    self.m_loginCallBack = function()
        local ipAddress = self.m_centerServerLoginInfo.GameServerHost --self.m_serverListTable[self.selectServerId].ip .. ":20013"
        print(self.m_loginAccount, self.m_centerServerLoginInfo.Token, ipAddress)
    
        local param = {}
        param.token = self.m_centerServerLoginInfo.Token
        param.loginServerId = self.m_centerServerLoginInfo.CentralServerId
        g_EventMgr:SendEvent(g_EventDef.EVENT_NET_ON_CLICK_LOGIN, 2, self.m_userInfo.userId, self.m_centerServerLoginInfo.Token, ipAddress, param)
    
        self:DelayShowMask()
    end

    if g_CS:LoadingConfigManager_Instance().Config.UseQueue then
        if self.m_centerServerLoginInfo and not string.isNilOrEmpty(tostring(self.m_centerServerLoginInfo.QueueServerHost)) then
            self:sendQueueHttp()
            return
        end
    end

    if self.m_loginCallBack then
        self.m_loginCallBack()
        self.m_loginCallBack = nil
    end
end

--发送排队请求
function UILoginPanel:sendQueueHttp()
    if self.m_isInQueue then
        return
    end
    local address = "http://%s/startQueue?accountName=%s&serverId=%s"
    local loginAccount = self.m_loginAccount
    local url = string.format(address,self.m_centerServerLoginInfo.QueueServerHost,loginAccount,self.m_centerServerLoginInfo.ServerId)
    if g_CS:LoadingConfigManager_Instance():IsManualSelectServer() then
        loginAccount = self.m_userName
        url = string.format(address,g_GlobalDefine.QueueServerIp,self.m_userName,self.selectServerId)
    end
    --g_CS.MyUtils_HttpPostForLua(url, {}, {}, self, self.ShowQueuePanel)
    local body = {}
    body.phone = loginAccount
    body.device = g_CS:UnityEngine_SystemInfo().deviceUniqueIdentifier
    body.ts = os.time() * 1000
    body.sign = body.phone .. body.ts
    g_LuaUtil:HttpPost2(url, {}, body, self, self.ShowQueuePanel)
    self.m_isInQueue = true
    if self.m_queueTimeOutDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_queueTimeOutDelay)
        self.m_queueTimeOutDelay = nil
    end
    self.m_queueTimeOutDelay = g_ScriptEvent:DelayCall(15000, 0,1, self, "QueueTimeOutCheck")
end

function UILoginPanel:DelayShowMask()
    if self.m_maskDelayCallId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_maskDelayCallId)
        self.m_maskDelayCallId = nil
    end
    self.m_maskDelayCallId = g_ScriptEvent:DelayCall(self.connectDelay * 1000, 0, 1, self, "ShowMask")
end

function UILoginPanel:HideMask()
    if self.m_maskDelayCallId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_maskDelayCallId)
        self.m_maskDelayCallId = nil
    end
    g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_MASK, false)
end

--显示连接菊花
function UILoginPanel:ShowMask()
    g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_MASK, true)
end

--点击选择服务器
function UILoginPanel:OnClickSelectServerBtn(go)
    self.ServerSelect.gameObject:SetActive(true)
    if self.useSDK then
        g_MSDKDataManager:MapleQueryTree(g_MSDKDataManager.treeId)
    end
end


--关闭选择服务器
function UILoginPanel:OnClickServerSelectCloseBtn(go)
    self.ServerSelect.gameObject:SetActive(false)
end



--点击服务器列表item
function UILoginPanel:ClickServerItem(go)
    self:RefreshSelectServerInfo(go.name)
    self.ServerSelect.gameObject:SetActive(false)
end

--点击大区
function UILoginPanel:OnZoneTogValueChange(isOn, toggle)
    local textTrans = toggle.transform:Find("Text")
    local textSelectedTrans = toggle.transform:Find("TextSelected")
    textTrans.gameObject:SetActive(not isOn)
    textSelectedTrans.gameObject:SetActive(isOn)
    if isOn then
        local dotween = toggle.transform:Find("CheckMark"):GetComponent(g_Component.DOTweenAnimation)
        if dotween then
            dotween:DORestart()
        end
        local key = toggle.gameObject.name
        self.currentSelectZoneID = key
        self:RefreshZoneServerStateList()
    end
end

--点击公告按钮
function UILoginPanel:OnClickNoticeBtn(go)
    --审核屏蔽
    if g_CS.MyUtils_IsInAudit() then
        return
    end

    if self.noticeObj == nil then
        local prefab = g_CS.ResLoad_LoadResources("Assets/Res/ui/prefab/UIAnnouncePanel.prefab", g_Component.GameObject)
    else
        self.noticeObj:SetActive(true)
    end
end

--加载Notice预制体
function UILoginPanel:LoadNoticePrefabAsyn(prefab)
    if prefab == nil then
        return
    end
    if g_CS.MyUtils_UnityObjectIsNull(self.gameObject) then
        return
    end
    self.noticeObj = g_CS.MyUtils_Instantiate(prefab, self.gameObject.transform)
end

--点击CG按钮
function UILoginPanel:OnClickCGBtn(go)
    --self:AsyncLoadCinemaHistory(true)
    self:PlayCG()
end

--点击登出按钮
function UILoginPanel:OnClickLogoutBtn(go)
    --[[
    if self.loginToken == nil then
        return
    end
    self:Logout()
    --]]

    self:ReturnLogin()
end

--点击修复客户端
function UILoginPanel:OnClickFixClient(go)
    local unBindMatConfirmFunc = function()
        g_CS.MainStart_FixClient(nil)
    end
    local msgID = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "clientFix_msgID", "value")
    g_UITipsManager:ShowMessage(unBindMatConfirmFunc, nil, msgID)
end

--点击客服按钮
function UILoginPanel:OnClickKFBtn(go)
    local link = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCustomerServiceConst, "level1_login", g_ConfigTable.CustomerServiceConst_Value)
    g_MSDKDataManager:OpenKF(link)
end

--点击事件end-------------------------------------------------------------------------------------------



--其他方法---------------------------------------------------------------------------------------------------------

--密码登录
function UILoginPanel:OnLoginByPassword()
    self.m_UserNameInputField.text = g_CS:UnityEngine_PlayerPrefs().GetString("UserName", "")
    self.m_PassWordInputField.text = g_CS:UnityEngine_PlayerPrefs().GetString("Password", "")
    self.m_User.gameObject:SetActive(true)
end

--eusdk登录
function UILoginPanel:OnLoginByEUSDK(param)
    if param.Count == 0 then
        return
    end
    local _, userID = param:TryGetValue("userID")
    local _, token = param:TryGetValue("token")
    self.m_userName = userID
    self.m_password = ""
    self.m_accountType = 2

    self.m_loginClient:Login(userID, token, true)
    --self.m_loginClient:loginByYXMToken(param["userID"], param["token"])
end

--登录成功回调
--loginInfo:{Result, Token, CentralServerId, ServerId, GameServerHost, QueueServerHost}
function UILoginPanel:onLoginSuccessfully(loginInfo)
    print("~~~~~~ UILoginPanel:onLoginSuccessfully ", loginInfo.Result, loginInfo.Token, loginInfo.CentralServerId, loginInfo.ServerId, loginInfo.GameServerHost, loginInfo.QueueServerHost)
    --g_UITipsManager:ShowMessage( "54000041")
    --self.selectServerId = loginInfo.ServerId

    self.m_centerServerLoginInfo = loginInfo
    self.m_registerRoot.gameObject:SetActive(false)
    self.m_ServerLogin.gameObject:SetActive(true)
    self:HideMask()

    if g_CS:LoadingConfigManager_Instance():IsManualSelectServer() then
        self:RefreshUserOfPassword(loginInfo)
    else
        if self.m_loginUserList[1] ~= self.m_loginAccount then
            local str = self.m_loginAccount
            local count = 1
            for i = 1, #self.m_loginUserList do
                if self.m_loginUserList[i] ~= self.m_loginAccount then
                    str = str .. "," .. self.m_loginUserList[i]
                    count = count + 1
                    if count >= 3 then
                        break
                    end
                end
            end
            print("UILoginPanel:onLoginSuccessfully save LoginUserList=", str)
            g_CS:UnityEngine_PlayerPrefs().SetString("LoginUserList", str)
        end
    end

    local loginUsersStr = g_CS:UnityEngine_PlayerPrefs().GetString("LoginUserList", "")
    if loginUsersStr ~= "" then
        local info = string.split(loginUsersStr, ',')
        local saveDataStr = g_CS:UnityEngine_PlayerPrefs().GetString("LoginDataJson", "")
        local saveDataJson = json.decode(saveDataStr)
        local currentData = saveDataJson[info[1]]
        LuaAPIManager:onLoginServerSuccessfully(currentData.token)
    end
    
    
    if self.m_checkActiveDelayCallId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_checkActiveDelayCallId)
        self.m_checkActiveDelayCallId = nil
    end
    self.m_checkActiveDelayCallId = g_ScriptEvent:DelayCall(0, 10 * 1000, -1, self, "checkCentralServerActive")

    -------公告只有在第一个开应用时候或者有新的公告时候才自动弹出
    local localHashCode = g_CS:UnityEngine_PlayerPrefs().GetInt("NoticeHashCode", 0)
    local currentHashCode = g_CS.MyUtils_GetHashCode(self.mainStart.m_noticeContent)
    if localHashCode ~= currentHashCode then
        g_CS:UnityEngine_PlayerPrefs().SetInt("NoticeHashCode", currentHashCode)
    end

    local nowTime = g_ScriptTime:GetStrFromUnixTimeYMD()
    local savedTime = g_CS:UnityEngine_PlayerPrefs().GetString("NoticeSavedTime", "0")
    local noticeUnopen = g_CS:UnityEngine_PlayerPrefs().GetInt("NoticeUnopen", 0)
    g_CS:UnityEngine_PlayerPrefs().SetString("NoticeSavedTime", nowTime)
    if localHashCode ~= currentHashCode or nowTime ~= savedTime or (nowTime == savedTime and noticeUnopen == 0) then
        self:OnClickNoticeBtn()
        return
    end
    -----------------------------------------------------------

    if not g_CS:LoadingConfigManager_Instance():IsManualSelectServer() then
        --自动登陆应用服
        self:OnClickLoginBtn()
    end

end

function UILoginPanel:RefreshUserOfPassword(loginInfo)
    if (not self.useSDK) then
        self:ShowUserName(self.m_UserNameInputField.text)
    end

    self.m_inGameFriends = nil
    self.loginToken = loginInfo.Token
    self.centerServerId = loginInfo.CentralServerId
    self.m_User.gameObject:SetActive(false)
    self.m_txUser.gameObject:SetActive(false)
    self.m_txUserIOS.gameObject:SetActive(false)
    self.m_userPC.gameObject:SetActive(false)
    self.m_guestWindow.gameObject:SetActive(false)
    self.m_ServerLogin.gameObject:SetActive(true)
    g_CS:UnityEngine_PlayerPrefs().SetInt("clickedAgreePrivacyToggle", 1)
    self:SetAgreementShowState(true, true)

    if self.m_checkActiveDelayCallId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_checkActiveDelayCallId)
        self.m_checkActiveDelayCallId = nil
    end
    if self.m_getServerListDelayCallId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_getServerListDelayCallId)
        self.m_getServerListDelayCallId = nil
    end

    self.m_checkActiveDelayCallId = g_ScriptEvent:DelayCall(0, 10 * 1000, -1, self, "checkCentralServerActive")
    -- if self.useSDK then
    -- 	self.m_getServerListDelayCallId = g_ScriptEvent:DelayCall(0, 30*1000, -1, self, "GetServerStateList")
    -- else
    -- 	self.m_getServerListDelayCallId = g_ScriptEvent:DelayCall(0, 30*1000, -1, self, "GetServerStateList")
    -- end

    self.m_LogoutBtn.gameObject:SetActive(true)
    --self.m_KFBtn.gameObject:SetActive(g_MSDKDataManager:MSDKPlatformAbilitySwitch())

    self:SetAgreementShowState(true, false)
end
--登录失败回调
function UILoginPanel:onLoginFail(failCode, date)
    print('onLoginFail ', failCode)
    self:HideMask()

    local logout = function()
        self:ReturnLogin()
    end

    if g_CS:UnityEngine_Application().internetReachability == g_CS:UnityEngine_NetworkReachability().NotReachable then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, 99)
        return
    end

    --服务器没有准备好,正在启动中, 正在关闭中
    if failCode == 1 or failCode == 13 or failCode == 20 then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_serverInMaintenance_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
        return
    end

    if failCode == 4 or failCode == 5 or failCode == 6 then
        if g_CS:LoadingConfigManager_Instance():UseSDK() then
            local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_authTimeout", g_ConfigTable.Table_Value)
            g_UITipsManager:ShowMessage(logout, messageId)
        else
            local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_countOrPasswordError_msgID", g_ConfigTable.Table_Value)
            g_UITipsManager:ShowMessage(messageId)
            logout()
        end
        return
    end

    --2 是 LoginReply.Types.LoginResult.LoginTokenError 的值
    if failCode == 2 then
        local reLogin = function()
            --token过期，走注册流程
            self.m_accountInput.text = tostring(self.m_loginAccount)
            self:OnClickLicenseAcceptBtn()
        end

        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(reLogin, messageId, failCode)
        return
    end

    --提示操作过于繁忙
    if failCode == 8 then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_tooBusyWithoutCD_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
        return
    end

    --27 是 被封禁
    if failCode == 27 then
        print("账号被封禁", date)
        local leftTime = tostring(date)
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "idip_accountBanned_client_msg", g_ConfigTable.Table_Value)
        local bannedUserAppealLink = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "bannedUserAppealLink", g_ConfigTable.Table_Value)
        local confirmFun = function()
            --local url = "http://welk.co/8UkFR6i6ow"
            local url = string.format(bannedUserAppealLink, self.m_loginAccount)
            g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIWebViewPanel, url)
        end
        g_UITipsManager:ShowMessage(confirmFun, messageId, leftTime)
        return
    elseif failCode == 28 then
        --顶号操作过于频繁
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "frequent_dinghao_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
        return
    elseif failCode == 29 then
        --注册人数达到上限
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "regLimited_serverFull_msg", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
        return
    elseif failCode == 30 then
        --已注销
        local reLogin = function()
            local loginUsersStr = g_CS:UnityEngine_PlayerPrefs().GetString("LoginUserList", "")
            self.m_loginUserList = string.split(loginUsersStr, ',')
            local loginAccount = self.m_loginUserList[1]
            table.remove(self.m_loginUserList, 1)
            local newStr = ""
            if #self.m_loginUserList > 0 then
                newStr = self.m_loginUserList[1]
                for i = 2, #self.m_loginUserList, 1 do
                    newStr = newStr .. "," .. self.m_loginUserList[i]
                end
            end
            g_CS:UnityEngine_PlayerPrefs().SetString("LoginUserList", newStr)
            self.m_accountInput.text = tostring(loginAccount)
            self:OnClickLicenseAcceptBtn()
        end

        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "accountCancellation", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(reLogin, messageId)
        return
    elseif failCode == 1005 then
        --同设备24小时内只能切换一次账号
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "loginFailed_msg", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
        return
    end

    local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
    g_UITipsManager:ShowMessage(logout, messageId, failCode)

    if self.useSDK then
        if g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.Guest then
            self:ShowUserName("游客")
        elseif g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.AppleId then
            self:ShowUserName(g_MSDKDataManager.loginData.appleFullName)
        else
            self:ShowUserName(g_MSDKDataManager.loginData.userName)
        end
        self.m_YKIcon.gameObject:SetActive(g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.Guest)
        self.m_AppleIcon.gameObject:SetActive(g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.AppleId)
    end
end

--登出
function UILoginPanel:Logout()

    --退出登录取消实名
    g_DataUserInfoManager.m_isRealName = false

    --3 是MSDK
    if self.useSDK then
        self.m_User.gameObject:SetActive(false)

        if self.isAssistGame or self.isCloudGame then
            self.m_userPC.gameObject:SetActive(true)
        elseif self.canLoginWithIOS then
            self.m_txUserIOS.gameObject:SetActive(true)
        else
            self.m_txUser.gameObject:SetActive(true)
        end
        g_CS:UnityEngine_PlayerPrefs().SetInt("clickedAgreePrivacyToggle", 0)
        self:SetAgreementShowState(false, false)
    else
        --self.m_txUserIOS.gameObject:SetActive(false)
        --self.m_txUser.gameObject:SetActive(false)
        --self.m_userPC.gameObject:SetActive(false)
        self.m_User.gameObject:SetActive(true)
        self:SetAgreementShowState(true, g_CS:UnityEngine_PlayerPrefs().GetInt("clickedAgreePrivacyToggle", 0) == 1)
    end
    self.m_ServerLogin.gameObject:SetActive(false)
    self.m_guestWindow.gameObject:SetActive(false)
    self:ResetLoginClient()
    self:ShowUserName(nil)
    --self.m_QQIcon.gameObject:SetActive(false)
    --self.m_WXIcon.gameObject:SetActive(false)
    --self.m_YKIcon.gameObject:SetActive(false)
    --self.m_AppleIcon.gameObject:SetActive(false)
    self:HideMask()

    --[[
    if self.m_inGameFriends ~= nil
    then
        self.m_inGameFriends:Clear()
        self:OnHandleOnGetInSameFriend(self.m_inGameFriends)
    end
    --]]
    self.m_characterList = nil
end

--心跳包，10秒发一次
function UILoginPanel:checkCentralServerActive()
    self.m_loginClient:checkCentralServerActive()
end

--获取服务器状态列表，30秒发一次
function UILoginPanel:GetServerStateList()
    if not self.useSDK then
        self:GetServerList()
        self.m_loginClient:GetServerStateList()
    else
        if self.useSDK then
            g_MSDKDataManager:MapleQueryTree(g_MSDKDataManager.treeId)
        end
    end
end

--初始化服务器列表
--0=维护, 1=流畅 ，2=拥挤， 3=爆满
function UILoginPanel:OnGetServerState(dic)

    if dic ~= nil then
        for key, value in pairs(self.m_serverListTable) do
            value.state = 0 --默认是维护（不下发的也是维护）
            if dic:ContainsKey(key) then
                --local _,_state = dic:TryGetValue(key)
                value.state = value.defaultState
            end
        end
    end

    self:RefreshZoneServerStateList()
    self:RefreshSelectServerInfo(self.selectServerId)
end

function UILoginPanel:OnGetCharacterInfo(list)
    self.m_characterList = list
    self:RefreshCharacterUI(list)
end

function UILoginPanel:RefreshCharacterUI(list)
    if list == nil then
        return
    end
    local servers = {}
    if list.Count > 0 then
        local index = 0
        for i = 1, list.Count do
            local info = list[i - 1]
            if self.m_serverListTable[info.serverId] then
                if (not self.useSDK) or (self.useSDK and (self.m_serverListTable[info.serverId].plat == g_MSDKDataManager.loginData.channelId or self.m_serverListTable[info.serverId].plat == 0)) then
                    table.insert(servers, info.serverId)
                    local item = nil
                    if index < self.ServerParentRole.childCount then
                        item = self.ServerParentRole:GetChild(index)
                    end
                    if item == nil then
                        item = g_CS.MyUtils_Instantiate(self.ServerPrefabRole, self.ServerParentRole).transform
                        self.AddButtonOnClick(item:GetComponent(g_Component.Button), self.ClickServerItem)
                    end
                    item.gameObject:SetActive(true)

                    item.gameObject.name = info.serverId
                    item:Find("Text"):GetComponent(g_Component.Text).text = self.m_serverListTable[info.serverId].name
                    item:Find("ServerState"):GetComponent(g_Component.Image).color = self.ColorTable[self.m_serverListTable[info.serverId].state]
                    item:Find("Name"):GetComponent(g_Component.Text).text = info.name .. "[" .. info.level .. "级]"
                    item:Find("Job"):GetComponent(g_Component.Text).text = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharcter, info.school, g_ConfigTable.Character_Name)
                    item:Find("Time"):GetComponent(g_Component.Text).text = g_CS.KBEngineTime_GetServerDateTime(info.lastLoginTime * 1000):ToString("yyyy-MM-dd")

                    local dataId = info.school .. info.sex
                    local iconPath = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, dataId, g_ConfigTable.TableCharRoleData_MainAvatar)
                    self:SetSprite(item:Find("Avatar/Icon"):GetComponent(g_Component.Image), iconPath)
                    index = index + 1
                end
            end
        end

        if self.ServerParentRole.childCount > #servers then
            for i = 1, self.ServerParentRole.childCount do
                local item = self.ServerParentRole:GetChild(i - 1)
                item.gameObject:SetActive(false)
            end
            for i = 1, #servers do
                if servers[i] == list[i - 1].serverId then
                    local item = self.ServerParentRole:GetChild(i - 1)
                    item.gameObject:SetActive(true)
                end
            end
        end

        if #servers > 0 then
            for key, value in pairs(self.zoneTable) do
                if value.toggle then
                    value.toggle.isOn = false
                end
            end
            if self.zoneTable["2"].toggle then
                self.zoneTable["2"].toggle.isOn = true
            end

            self.currentSelectZoneID = "2"
        end

        self:RefreshZoneServerStateList()
    else
        for i = 1, self.ServerParentRole.childCount do
            local item = self.ServerParentRole:GetChild(i - 1)
            item.gameObject:SetActive(false)
        end
        self.ServerPrefabRole.gameObject:SetActive(false)
    end
end

function UILoginPanel:OnRefreshFriendsInfo(friends)
    if friends == nil or friends.Count == 0
    then
        self.ServerParentFriend.gameObject:SetActive(false)
        return 0
    end

    local count = 0
    for i = 0, friends.Count - 1 do
        local info = friends[i]
        --print(info.UserName .. " ServerId " .. tostring(info.ServerId) .. " ".. tostring(self.m_serverListTable[tostring(info.ServerId)] == nil))
        if self.m_serverListTable[tostring(info.ServerId)]
        then
            local item = nil
            if count < self.ServerParentFriend.childCount
            then
                item = self.ServerParentFriend:GetChild(count)
            end

            if item == nil
            then
                item = g_CS.MyUtils_Instantiate(self.ServerPrefabFriend, self.ServerParentFriend).transform
                self.AddButtonOnClick(item:GetComponent(g_Component.Button), self.ClickServerItem)
            end
            item.gameObject:SetActive(true)
            item.gameObject.name = info.ServerId

            local nameLen = g_LuaUtil:SubStringGetTotalIndex(info.UserName)
            if nameLen > self.m_nameLenLimit
            then
                item:Find("Name"):GetComponent(g_Component.Text).text = g_LuaUtil:SubStringUTF8(info.UserName, 1, self.m_nameLenLimit - 1) .. '...'
            else
                item:Find("Name"):GetComponent(g_Component.Text).text = info.UserName
            end

            item:Find("Level"):GetComponent(g_Component.Text).text = info.Level .. "级"
            item:Find("ServerName"):GetComponent(g_Component.Text).text = self.m_serverListTable[tostring(info.ServerId)].name
            item:Find("ServerState"):GetComponent(g_Component.Image).color = self.ColorTable[self.m_serverListTable[tostring(info.ServerId)].state]

            if info.IsOnline == 1 or info.OfflineTime == 0  --在线
            then
                item:Find("Time"):GetComponent(g_Component.Text).text = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "msdk_wechatFriendPlayer_InGameText", g_ConfigTable.Table_Value)
            else
                item:Find("Time"):GetComponent(g_Component.Text).text = g_CS.KBEngineTime_GetServerDateTime(info.OfflineTime * 1000):ToString("yyyy-MM-dd")
            end

            local schoolPath = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharcter, info.School, g_ConfigTable.Character_IconName)
            self:SetSprite(item:Find("ClassImg"):GetComponent(g_Component.Image), schoolPath)

            local picUrl
            if g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.WeChat
            then
                picUrl = info.PictureUrl .. "/46"
            else
                picUrl = info.PictureUrl .. "40"
            end
            g_CS.MyUtils_ShowUrlImage(item:Find("Portrait"):GetComponent(g_Component.Image), picUrl)
            count = count + 1
        end

        if self.ServerParentFriend.childCount > count
        then
            for i = count + 1, self.ServerParentFriend.childCount do
                local item = self.ServerParentFriend:GetChild(i - 1)
                item.gameObject:SetActive(false)
            end
        end
    end

    return count
end

--登录成功回调
function UILoginPanel:onLoginServerSuccessfully()
    print 'UILoginPanel:onLoginServerSuccessfully'
    if self.m_loginClient ~= nil then
        print 'set NeedCheckState fasle'
        self.m_loginClient.NeedCheckState = false
    end

    --self:HideMask()
    --g_UITipsManager:ShowMessage( "54000041")
    --[[
    if g_CS:KBEngine_KBEngineApp().app.entity_type == "Account" then
        local account = g_CS:KBEngine_KBEngineApp().app:player()
        if account ~= nil then
            self.ui_avatarList = account.avatars
        end
    end
    --]]
end

--拉取角色列表回调
function UILoginPanel:onReqAvatarList(gbid)
    self.loginCount = 0
    self.m_avatarGbId = gbid
    self:SetLockLogin(false)
    print('UILoginPanel:onReqAvatarList')
    if self.m_loginClient ~= nil then
        print 'set NeedCheckState fasle'
        self.m_loginClient.NeedCheckState = false
    end

    --[[
    local newUserGuide = g_CS:GameConfig().enableNewbieGuide

    if newUserGuide == false or avatarList.Count > 0 then
        g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIPlayerRolesPanel, avatarList)
    else
        g_EventMgr:SendEvent(g_EventDef.EVENT_KBE_REQCREATEAVATAR)
    end
    --]]

    local hasDID = 0

    if g_CS:LoadingConfigManager_Instance():IsManualSelectServer() then
        hasDID = 1
    end

    if g_DataUserInfoManager.accountLua.did ~= "" then
        hasDID = 1
    else
        local token, account = g_DataUserInfoManager.accountLua:GetUserLoginToken()
        if self.m_didData ~= nil and self.m_didData.account == account and self.m_didData.did ~= "" then
            g_DataUserInfoManager.accountLua:reqSetDidInfo(self.m_didData.name, self.m_didData.idCardNumber, self.m_didData.did)
            hasDID = 2
        end
    end

    --[[
    if hasDID == 1 then
        self:EnterCreateRole()
    elseif hasDID == 0 then
        self:DIDVerify()
    end
    --]]

    self:EnterCreateRole()
end

--检查是否需要设置did
function UILoginPanel:CheckDidNeedSelect()
    --local accountList = g_DataUserInfoManager:GetAccountList()
    --if not accountList or #accountList <= 0 then
    --    return false
    --end
    --
    --if #accountList == 1 then
    --    if g_DataUserInfoManager.accountLua then
    --        g_DataUserInfoManager.accountLua:reqSetDidLimitItems(accountList[1].realAccount)
    --    end
    --    return false
    --end

    local mainAccount = g_DataUserInfoManager:GetDidMainAccount()
    if string.isNilOrEmpty(mainAccount) then
        return true
    end

    return false
end

--成功拉取did账号列表进入设置
function UILoginPanel:OnGetDidAccountList()
    if self.m_didTimeOutDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_didTimeOutDelay)
        self.m_didTimeOutDelay = nil
    end
    local accountList = g_DataUserInfoManager:GetAccountList()
    if not accountList or #accountList <= 0 then
        return
    end

    local func = function()
        if self.m_avatarGbId ~= 0 then
            print('g_DataUserInfoManager.accountLua:selectAvatarGame()')
            g_DataUserInfoManager.accountLua:selectAvatarGame()
        else
            --self:LoadFirstCharModel()
            print('create role')
            g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_MASK, false)
            g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIRoleCreatePanel)
        end
    end

    local openFunc = function()
        g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIDidSelectPanel,{confirmFunc = func,selectModel = 1})
    end
    local msgId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableItemSet, "mainAccountChoose", g_ConfigTable.TableItemSet_Value)
    g_UITipsManager:ShowMessage(openFunc,nil,msgId)
end

function UILoginPanel:didTimeOutHandler()
    if self.m_didTimeOutDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_didTimeOutDelay)
        self.m_didTimeOutDelay = nil
        
        local msgId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableItemSet, "noAccountInfo", g_ConfigTable.TableItemSet_Value)
        g_UITipsManager:ShowMessage(openFunc,nil,msgId)
    end
end

function UILoginPanel:EnterCreateRole()
    if self.m_avatarGbId ~= 0 then
        print('g_DataUserInfoManager.accountLua:selectAvatarGame()')
        g_DataUserInfoManager.accountLua:selectAvatarGame()
    else
        --self:LoadFirstCharModel()
        print('create role')
        g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_MASK, false)
        g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIRoleCreatePanel)
    end
    local extraParams = {
        userid = g_DataUserInfoManager.accountLua.accountName or "",
        gbid   = tostring(g_DataUserInfoManager.playerEntityLua and g_DataUserInfoManager.playerEntityLua.gbId or ""),
        ver    = g_CS.MainStart_GetAppVersion(),
        brand  = CS.SDKManager.Instance:GetDeviceBrand(),
        model  = g_CS:UnityEngine_SystemInfo().deviceModel

    }
    -- local func = function()
    --     if self.m_avatarGbId ~= 0 then
    --         print('g_DataUserInfoManager.accountLua:selectAvatarGame()')
    --         g_DataUserInfoManager.accountLua:selectAvatarGame()
    --     else
    --         --self:LoadFirstCharModel()
    --         print('create role')
    --         g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_MASK, false)
    --         g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIRoleCreatePanel)
    --     end
    -- end
    --
    -- local gbid = self.m_avatarGbId
    -- local key = "didAccountCount".. tostring(gbid)
    -- local accountCount = g_LuaUtil:GetPlayerPrefs(key,1)
    -- if not accountCount or accountCount == 1 or accountCount == 0 then
    --     func()
    --     return
    -- end
    --if not g_DataUserInfoManager.didAccountInit then
    --    g_DataUserInfoManager.accountLua:reqDidMultiAccounts()
    --    if self.m_didTimeOutDelay then
    --        g_ScriptEvent:RemoveDelayCall(self.m_didTimeOutDelay)
    --        self.m_didTimeOutDelay = nil
    --    end
    --    self.m_didTimeOutDelay = g_ScriptEvent:DelayCall(15000, 0,1, self, "didTimeOutHandler")
    --else
    --    self:OnGetDidAccountList()
    --end
     --
     --local callBack = function()
     --    local result = self:CheckDidNeedSelect()
     --    if not result then
     --        func()
     --    else
     --        self:HideMask()
     --        local openFunc = function()
     --            g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIDidSelectPanel,{confirmFunc = func,selectModel = 1})
     --        end
     --        local msgId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableItemSet, "mainAccountChoose", g_ConfigTable.TableItemSet_Value)
     --        g_UITipsManager:ShowMessage(openFunc,nil,msgId)
     --    end
     --end
     --g_LuaUtil:SendDidLimitHttp(callBack)
end

--region DID
--实名认证
function UILoginPanel:DIDVerify()
    self:HideMask()
    local confirmFun = function()

        self.didTime = g_ScriptTime:GetRealtimeSinceStartup()

        local url = g_LuaUtil:GetMallAPIUrlWithoutSlash() .. "/did"
        local token, account = g_DataUserInfoManager.accountLua:GetUserLoginToken()
        if g_LuaUtil.MallUrlForPrerelease == true then
            CS.SDKManager.Instance:DIDVerify(url, account, token, false)
        else
            CS.SDKManager.Instance:DIDVerify(url, account, token, g_CS:LoadingConfigManager_Instance():isTestUrl())
        end
    end
    local cancelFun = function()
    end

    local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "realNameApprove", g_ConfigTable.Table_Value)
    g_UITipsManager:ShowMessage(confirmFun, cancelFun, messageId)

end

--认证 回调
function UILoginPanel:OnDIDVerifyCallback(dataStr)
    print("UILoginPanel:OnDIDVerifyCallback() ", dataStr)
    local didTable = json.decode(dataStr)
    if didTable.errorCode == 0 then
        local token, account = g_DataUserInfoManager.accountLua:GetUserLoginToken()
        self.m_didData = didTable
        self.m_didData.account = account
        g_DataUserInfoManager.accountLua:reqSetDidInfo(didTable.name, didTable.idCardNumber, didTable.did)
        --self:DIDComparison(didTable.did)
        --self:EnterCreateRole()

        local currentTime = g_ScriptTime:GetRealtimeSinceStartup()
        local passTime = currentTime - self.didTime
        print("UILoginPanel:OnDIDVerifyCallback passTime=", passTime)
        if passTime >= 20 then --如果did认证超过20秒，服务器以及断连，需要重新登陆中心服
            self:ResetLoginClient()
            self:LoginCenterServer()
        end
    end
end

--认证 设置返回
function UILoginPanel:OnDIDSetSucess(resCode)
    print("UILoginPanel:OnDIDSetSucess() ",resCode)
    if resCode == 0 then
        self:EnterCreateRole()
    elseif resCode == 2 then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "needTheSameRealName", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
    else
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "didAccountNumTips", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
    end
end

---@since 小茅运信息 是否领取过瑞羽
---@param did string_当前用户did
function UILoginPanel:DIDComparison(did)
    if g_DataUserInfoManager.accountLua.mtExchangeTime ~= 0 then
        return
    end
end


--endregion

--返回登录
function UILoginPanel:OnRoleReturn(avatarList)
    print 'UILoginPanel:OnRoleReturn'
    if self.m_loginClient ~= nil then
        print 'set NeedCheckState true'
        self.m_loginClient.NeedCheckState = true
    end
end

--连接应用服 状态【【结拜】在结拜结缘界面点击前往后，退出与NPC对话界面，无法再次选中结拜结缘NPC】
--https://www.tapd.cn/57153713/bugtrace/bugs/view/1157153713001025717
function UILoginPanel:OnConnectState(isSuccess, isNetValid)

    if isSuccess == false then
        self:HideMask()
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, 97)
    else
        if not g_CS:NetworkManager_Instance().enabled then
            g_CS:NetworkManager_Instance().enabled = true
        end
    end
end

--版本不匹配
function UILoginPanel:OnVersionNotMatch(clientVersion, serverVersion, clientScriptVersion, curServerScriptVersion, serverEntitydefMD5, curServerEntitydefMD5)
    print("OnVersionNotMatch    " .. " clientVersion=" .. clientVersion .. " serverVersion=" .. serverVersion .. " clientScriptVersion=" .. clientScriptVersion .. " curServerScriptVersion=" .. curServerScriptVersion .. " serverEntitydefMD5=" .. serverEntitydefMD5 .. " curServerEntitydefMD5=" .. curServerEntitydefMD5)

    --[[
    --如果能判断出服务器处于维护中，则弹维护中的message
    local server = self.m_serverListTable[self.selectServerId]
    if server.state == 0 then
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_serverInMaintenance_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(quit, messageId)
        self:HideMask()
        return
    end
    --]]

    local quit = function()
        --g_CS.UnityEngine_Application_Quit()
    end

    local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_digestNotMatch", g_ConfigTable.Table_Value)
    g_UITipsManager:ShowMessage(quit, messageId)
    self:HideMask()
end

--登录loginapp失败了
function UILoginPanel:OnConnectServerFail(failCode, date)
    self:HideMask()

    if failCode == 1 or failCode == 13 or failCode == 20 then
        --服务器没有准备好,正在启动中, 正在关闭中
        self:onLoginFail(failCode)
    elseif failCode == 4 or failCode == 5 or failCode == 6 then
        --用户名或者密码错误
        self:onLoginFail(failCode)
    elseif failCode == 8 then
        --提示操作过于繁忙
        self:onLoginFail(failCode)
    elseif failCode == 25 then
        --错误码为25时是和中心服断开了
        self:onLoginFail(failCode)
    elseif failCode == 26 then
        --不在白名单
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "accountNotWhitelisted", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId)
    elseif failCode == 27 then
        --错误码为27时是账号被封禁
        self:onLoginFail(failCode, date)
    elseif failCode == 28 then
        --顶号操作过于频繁
        self:onLoginFail(failCode)
    elseif failCode == 29 then
        --注册人数达到上限
        self:onLoginFail(failCode)
    elseif failCode == 30 then
        --已注销
        self:onLoginFail(failCode)
    else
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, failCode)
    end
end

--服务器需要验证激活码
function UILoginPanel:OnHandleServerCheckCDKey()
    if self.m_checkActiveCoro ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_checkActiveCoro)
        self.m_checkActiveCoro = nil
    end
    self.m_checkActiveCoro = g_ScriptEvent:DelayCall(0, 10 * 1000, -1, self, "checkCentralServerActive")
end

function UILoginPanel:OnHandleCheckCaptcha()
    if self.m_checkActiveCoro ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.m_checkActiveCoro)
        self.m_checkActiveCoro = nil
    end
    self.m_checkActiveCoro = g_ScriptEvent:DelayCall(0, 10 * 1000, -1, self, "checkCentralServerActive")
end

--激活结果，1--success,2--used,3--invalid
function UILoginPanel:OnHandleActivatedResult(result)
    if result == 1 then
        if self.m_checkActiveCoro ~= nil then
            g_ScriptEvent:RemoveDelayCall(self.m_checkActiveCoro)
            self.m_checkActiveCoro = nil
        end
    end
end

--如果没有显示过过场动画 异步加载
function UILoginPanel:AsyncLoadCinemaHistory(bForce)
    local historyPlayState = g_CS:UnityEngine_PlayerPrefs().GetInt("CinemaHistoryState", 0)
    if historyPlayState == 0 then
        -- 5 代表GPM登录漏斗中：看开场视频
        g_CS:UnityEngine_PlayerPrefs().SetInt("FirstWatchCinemaHistoryState", 1)
    end
    if historyPlayState == 0 or bForce then
        if not g_LuaUtil:UnityObjectIsNil(g_DataUserInfoManager.cinemaParent) then
            local cinemaObj = g_DataUserInfoManager.cinemaParent.transform:Find(self.cinemaHistoryID)
            if cinemaObj then
                -- MainStart.cs 里面成功加载了
                cinemaObj.gameObject:SetActive(true)
                g_CS:UnityEngine_PlayerPrefs().SetInt("CinemaHistoryState", 1)
                return
            end
        end

        -- 避免手机上异步加载未完成的时候玩家疯狂点击导致重复加载
        if self.isLoadingCinemaRes then
            return
        end
        self.isLoadingCinemaRes = true

        --if math.floor(self.cinemaHistoryID / 100000) == 989 then
        --	g_CS.ResLoad_AsyncLoadAssetForLua("Assets/Res/design/video/Cinema_VideoPlay.prefab", self, "ShowCinemaHistory", g_Component.GameObject)
        --else
        --	-- 没有找到资源重新加载
        --	local showPath = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCinemaPlay, self.cinemaHistoryID, g_ConfigTable.CinemaPlay_resource)
        --
        --	g_CS.ResLoad_AsyncLoadAssetForLua(showPath, self, "ShowCinemaHistory", g_Component.GameObject, nil)
        --end
    end
end

--显示过场动画
function UILoginPanel:ShowCinemaHistory(asynLoadResult)
    self.isLoadingCinemaRes = false
    if g_LuaUtil:UnityObjectIsNil(asynLoadResult.m_oAssetObject) then
        return
    end
    if g_CS.MyUtils_UnityObjectIsNull(self.gameObject) then
        return
    end

    g_CS:UnityEngine_PlayerPrefs().SetInt("CinemaHistoryState", 1)
    -- 和c# MainStart.cs 统一不然逻辑操作有问题
    g_DataUserInfoManager.cinemaParent = g_CS.UnityEngine_GameObject()
    g_DataUserInfoManager.cinemaParent.name = self.cinemaHistoryID

    self.cinema_history = g_CS.MyUtils_Instantiate(asynLoadResult.m_oAssetObject, g_DataUserInfoManager.cinemaParent.transform)
    self.cinema_history.name = self.cinemaHistoryID
    self.cinema_history:SetActive(true)
end


--unity加载场景完毕
function UILoginPanel:OnHandleUnitySceneLoaded(scene)
    if scene.name == g_CS:GameSceneManager_Singleton().SceneName_PlayerRole then
        --self.MainCamera =g_CS:MainCamera().Instance
        --self.MainCamera.gameObject:AddComponent(g_Component.RenderToRT)

        --self:AsyncLoadCinemaHistory()
    end
end

-----------------------------------------------提前异步加载四个预览模型----------------------------------------------------

--加载第一个角色模型
function UILoginPanel:LoadFirstCharModel()
    if self.m_avatarList == nil or g_LuaUtil:GetTableSize(self.m_avatarList) == 0 or g_DataUserInfoManager.accountLua.m_commonTutorialCompleted then
        self:LoadHighModel()
    else
        local gbIdList = {}
        for i, v in pairs(self.m_avatarList) do
            table.insert(gbIdList, i)
        end

        --按上次在线时间排序，最近的排上面
        table.sort(gbIdList, function(gbId1, gbId2)
            return self.m_avatarList[gbId1].tLastOnline > self.m_avatarList[gbId2].tLastOnline
        end)

        local oldModelRootName = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableNewbieCreate, "newbieModelRoot_oldChar", g_ConfigTable.NewbieCretae_Value)
        local oldModelRoot = g_CS.UnityEngine_GameObject_Find(oldModelRootName).transform
        local model = oldModelRoot:Find(tostring(gbIdList[1]))
        if g_LuaUtil:UnityObjectIsNil(model) == false then
            self:ModelLoadAll()
            return
        end

        local avatarInfo = self.m_avatarList[gbIdList[1]]

        local roleId = self:GetRoleID(avatarInfo.school, avatarInfo.sex)
        local path = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_ResourcePath)
                .. g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_Resource) .. ".prefab"
        g_CS.ResLoad_AsyncLoadAssetForLua(path, self, "AsynLoadAvatarModel", g_Component.GameObject, avatarInfo)
    end
end

function UILoginPanel:AsynLoadAvatarModel(asynLoadResult)
    local prefab = asynLoadResult.m_oAssetObject
    if g_LuaUtil:UnityObjectIsNil(self.gameObject) or g_LuaUtil:UnityObjectIsNil(prefab) then
        return
    end

    g_CS:GameSceneManager_Singleton():SetCurSceneType(g_CS:GameSceneType().ST_In_SelectRole)
    local avatarInfo = asynLoadResult.m_oParam
    local oldModelRootName = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableNewbieCreate, "newbieModelRoot_oldChar", g_ConfigTable.NewbieCretae_Value)
    local oldModelRoot = g_CS.UnityEngine_GameObject_Find(oldModelRootName).transform
    local modelObj = g_CS.MyUtils_Instantiate(prefab, oldModelRoot)
    modelObj.name = tostring(avatarInfo.gbId)
    local animator = modelObj:GetComponent(g_Component.Animator)
    animator:Play(g_CS:AniName().idleNormal)
    animator.cullingMode = g_CS:UnityEngine_AnimatorCullingMode().AlwaysAnimate
    g_CS.MyUtils_SetLayer(modelObj, oldModelRoot.gameObject.layer)

    local roleId = self:GetRoleID(avatarInfo.school, avatarInfo.sex)
    local ViewAvatar = modelObj:AddComponent(g_Component.ViewEntity)
    ViewAvatar:ChangeAnimator(animator)
    ViewAvatar.isPlayer = true
    ViewAvatar.m_LoadAll = true
    ViewAvatar:SetLoadAllCallback(self, self.ModelLoadAll)
    ViewAvatar:LoadAppearance(roleId, avatarInfo.charAppearance)
end

function UILoginPanel:GetRoleID(school, sex)
    local roleOpenState = {
        Close = 0, -- 未开放
        Open = 1, -- 开放
        Waitting = 2 -- 暂未开放
    }
    local allSchoolMap = {}                                    --{school, list:roleId}
    local roleOpenStateList = {}
    local roleIDs = g_ConfigData:GetKeysFromConfigTable(g_ConfigTable.TableCharRoleData)
    for i = 1, #roleIDs do
        local roleId = tonumber(roleIDs[i])
        local isOpen = tonumber(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_IsOpen))
        roleOpenStateList[roleId] = isOpen
        if isOpen ~= roleOpenState.Close then
            local schoolID = tonumber(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_CharID))
            if allSchoolMap[schoolID] == nil then
                allSchoolMap[schoolID] = {}
            end

            table.insert(allSchoolMap[schoolID], roleId)
        end
    end
    local roleIdList = allSchoolMap[school]
    for i = 1, #roleIdList do
        local tmpSex = tonumber(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleIdList[i], g_ConfigTable.TableCharRoleData_Sex))
        if tmpSex == sex then
            return roleIdList[i]
        end
    end
end

--异步加载高模
function UILoginPanel:LoadHighModel()
    --g_CS:GameSceneManager_Singleton():SetCurSceneType(g_CS:GameSceneType().ST_In_CreateRole)
    local root_1001 = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableNewbieCreate, "newbiePreviewRoot_1001", g_ConfigTable.NewbieCretae_Value)
    root_1001 = g_CS.UnityEngine_GameObject_Find(root_1001)
    if g_LuaUtil:UnityObjectIsNil(root_1001) == false and root_1001.transform.childCount ~= 0 then
        self.m_loadHighModelCount = self.TotalRoleCount
    end
    if self.m_loadHighModelCount == self.TotalRoleCount then
        g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIRoleCreatePanel, self.m_avatarList)
        return
    end
    -- 对应character-roledata 中 isOpen字段
    local roleOpenState = {
        Close = 0, -- 未开放
        Open = 1, -- 开放
        Waitting = 2 -- 暂未开放
    }
    self.m_loadHighModelCount = 0
    self:ShowMask()

    local schoolIDArr = g_ConfigData:GetKeysFromConfigTable(g_ConfigTable.TableCharcter)
    for i = 1, #schoolIDArr do
        local root = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableNewbieCreate, "newbiePreviewRoot_" .. schoolIDArr[i], g_ConfigTable.NewbieCretae_Value)
        local defaultSex = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharcter, schoolIDArr[i], g_ConfigTable.Character_defaultSex)
        local roleId = self:GetRoleID(tonumber(schoolIDArr[i]), tonumber(defaultSex))
        local path = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_ResourcePath)
                .. g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_Resource) .. "_show.prefab"
        local param = {}
        param.root = root
        param.roleId = tonumber(roleId)
        g_CS.ResLoad_AsyncLoadAssetForLua(path, self, "AsynLoadPreviewModel", g_Component.GameObject, param)
    end
end

--加载预览模型
function UILoginPanel:AsynLoadPreviewModel(asynLoadResult)
    if g_LuaUtil:UnityObjectIsNil(asynLoadResult.m_oAssetObject) then
        return
    end
    if g_CS.MyUtils_UnityObjectIsNull(self.gameObject) then
        return
    end
    -- 对应character-roledata 中 isOpen字段
    local roleOpenState = {
        Close = 0, -- 未开放
        Open = 1, -- 开放
        Waitting = 2 -- 暂未开放
    }
    local allSchoolMap = {}                                    --{school, list:roleId}
    local roleOpenStateList = {}
    local availableRoleIDs = {}
    local roleIDs = g_ConfigData:GetKeysFromConfigTable(g_ConfigTable.TableCharRoleData)
    for i = 1, #roleIDs do
        local roleId = tonumber(roleIDs[i])
        local isOpen = tonumber(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_IsOpen))
        roleOpenStateList[roleId] = isOpen
        if isOpen ~= roleOpenState.Close then
            local schoolID = tonumber(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_CharID))
            if allSchoolMap[schoolID] == nil then
                allSchoolMap[schoolID] = {}
            end

            table.insert(allSchoolMap[schoolID], roleId)
            table.insert(availableRoleIDs, roleId)
        end
    end

    local roleFaceData = {}
    local shapingId, roleId, shapeData, shapeId
    local shapingKeys = g_ConfigData:GetKeysFromConfigTable(g_ConfigTable.TableShapingResource)

    for i = 1, #availableRoleIDs do
        roleId = availableRoleIDs[i]
        roleFaceData[roleId] = {}
        roleFaceData[roleId].hair = {}
        roleFaceData[roleId].face = {}
        roleFaceData[roleId].eye = {}
        roleFaceData[roleId].scar = {}
        roleFaceData[roleId].suit = {}
        local hairBaseId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_Hair)
        local faceBaseId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_Face)
        local eyeBaseId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_Pupil)
        local scarBaseId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_Decoration)
        local suitBaseId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableCharRoleData, roleId, g_ConfigTable.TableCharRoleData_CreatSet)
        for j = 1, #shapingKeys do
            shapingId = tonumber(shapingKeys[j])
            if math.floor(shapingId / 1000) == hairBaseId then
                table.insert(roleFaceData[roleId].hair, shapingId)
            elseif math.floor(shapingId / 1000) == faceBaseId then
                table.insert(roleFaceData[roleId].face, shapingId)
                roleFaceData[roleId].eye[shapingId] = {}
                local eyes = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableShapingResource, shapingId, g_ConfigTable.TableCharRoleData_Eyes)
                for i = 1, #eyes do
                    table.insert(roleFaceData[roleId].eye[shapingId], tonumber(eyes[i]))
                end
                --elseif math.floor(shapingId / 1000) == eyeBaseId then
                --table.insert(roleFaceData[roleId].eye, shapingId)
            elseif math.floor(shapingId / 100) == suitBaseId then
                table.insert(roleFaceData[roleId].suit, shapingId)
            end
        end
    end

    local param = asynLoadResult.m_oParam
    local parent = g_CS.UnityEngine_GameObject_Find(param.root).transform
    local model = g_CS.MyUtils_Instantiate(asynLoadResult.m_oAssetObject, parent)
    local viewEntity = model:AddComponent(g_Component.ViewEntity)
    viewEntity.m_LoadAll = true
    viewEntity:SetLoadAllCallback(self, self.HighModelLoadAll)
    viewEntity.isPlayer = true
    viewEntity.m_isCreateState = true
    viewEntity:ChangeAnimator(viewEntity:GetComponent(g_Component.Animator))

    local _, shapeId = g_LuaUtil:GetSchoolAndSexByRoleID(param.roleId)
    local hairId = roleFaceData[param.roleId].hair[1]
    local faceId = roleFaceData[param.roleId].face[1]
    local eyeId = roleFaceData[param.roleId].eye[faceId][1]
    local hairColorId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableShapingResource, hairId, g_ConfigTable.ShapingResource_hairColor)[1]
    local scarId = 0
    local suitId = roleFaceData[param.roleId].suit[1]

    local equipParts1 = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableShapingResource, suitId, g_ConfigTable.ShapingResource_Resource)
    --local equipParts2 = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableShapingResource, suitId, g_ConfigTable.ShapingResource_Resource2)
    viewEntity:LoadBody(param.roleId, equipParts1)
    --viewEntity:LoadWeapon(param.roleId, equipParts2)

    viewEntity:LoadHair(hairId, hairColorId)
    --viewEntity:LoadEye(eyeId)
    viewEntity:LoadFace(faceId, eyeId, true)

    model:SetActive(false)
end

--高模各部件全部加载完毕
function UILoginPanel:HighModelLoadAll()
    self.m_loadHighModelCount = self.m_loadHighModelCount + 1
    if self.m_loadHighModelCount == self.TotalRoleCount then
        g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_MASK, false)
        g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIRoleCreatePanel, self.m_avatarList)
    end
end

--模型加载完毕
function UILoginPanel:ModelLoadAll()
    g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_MASK, false)
    g_EventMgr:SendEvent(g_EventDef.EVENT_UI_SHOW_UI, g_GlobalDefine.UINameConst.UIRoleCreatePanel, self.m_avatarList)
end

--获取默认颜色值
function UILoginPanel:GetDefaultColorValue(prefab)
    local color = {}
    local min = prefab[1][1]
    local max = prefab[1][2]
    color[1] = (prefab[1][3] - min) / (max - min) * 100
    min = prefab[2][1]
    max = prefab[2][2]
    color[2] = (prefab[2][3] - min) / (max - min) * 100
    min = prefab[3][1]
    max = prefab[3][2]
    color[3] = (prefab[3][3] - min) / (max - min) * 100

    return color
end


--异步加载模型
function UILoginPanel:AsynLoadModel(asynLoadResult)
    if g_LuaUtil:UnityObjectIsNil(asynLoadResult.m_oAssetObject) then
        return
    end
    local parent = g_CS.UnityEngine_GameObject_Find(asynLoadResult.m_oParam).transform
    local model = g_CS.MyUtils_Instantiate(asynLoadResult.m_oAssetObject, parent)
    model:SetActive(false)
end
-----------------------------------------------提前异步加载四个预览模型----------------------------------------------------

--顶号
function UILoginPanel:OnKickAnotherAvatar()
    self:HideMask()
    local confirmFun = function()
        --g_EventMgr:SendEvent(g_EventDef.EVENT_KBE_KICK_ANOTHER_AVATAR, true)
        g_DataUserInfoManager.accountLua:kickAnotherAvatar(1)
    end
    local cancelFun = function()
        --g_EventMgr:SendEvent(g_EventDef.EVENT_KBE_KICK_ANOTHER_AVATAR, false)
        g_DataUserInfoManager.accountLua:kickAnotherAvatar(0)
    end

    local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_dinghaoConfirm_msgID", g_ConfigTable.Table_Value)
    g_UITipsManager:ShowMessage(confirmFun, cancelFun, messageId)
end

-- 被顶号
function UILoginPanel:OnHandleAccountBeKicked()
    self:ReturnLogin()
end

function UILoginPanel:LoginWithQQ()
    if self:StopLoginByDontAgreeUserAgreement() then
        return
    end
    if self:CheckLoginFailInterval() == false then
        g_MSDKDataManager.loginQQ = true
    end
end

function UILoginPanel:LoginWithWX()
    if self:StopLoginByDontAgreeUserAgreement() then
        return
    end
    if self:CheckLoginFailInterval() == false then
    end
end

function UILoginPanel:LoginWithGuest()
    if self:StopLoginByDontAgreeUserAgreement() then
        return
    end
    if self:CheckLoginFailInterval() == false then
    end
end

function UILoginPanel:LoginWithApple()
    if self:StopLoginByDontAgreeUserAgreement() then
        return
    end
    if self:CheckLoginFailInterval() == false then
    end
end

--手游助手登录
function UILoginPanel:LoginWithWXIOSPC()
    if self:StopLoginByDontAgreeUserAgreement() then
        return
    end
    if self:CheckLoginFailInterval() == false then
        g_MSDKDataManager.assistGamePlatform = g_GlobalDefine.AssistGamePlatform.IOS
    end
end

function UILoginPanel:LoginWithQQIOSPC()
    if self:StopLoginByDontAgreeUserAgreement() then
        return
    end
    if self:CheckLoginFailInterval() == false then
        g_MSDKDataManager.assistGamePlatform = g_GlobalDefine.AssistGamePlatform.IOS
        g_MSDKDataManager.loginQQ = true
    end
end

function UILoginPanel:LoginWithWXAndroidPC()
    if self:StopLoginByDontAgreeUserAgreement() then
        return
    end
    if self:CheckLoginFailInterval() == false then
        g_MSDKDataManager.assistGamePlatform = g_GlobalDefine.AssistGamePlatform.Android
    end
end

function UILoginPanel:LoginWithQQAndroidPC()
    if self:StopLoginByDontAgreeUserAgreement() then
        return
    end
    if self:CheckLoginFailInterval() == false then
        g_MSDKDataManager.assistGamePlatform = g_GlobalDefine.AssistGamePlatform.Android
        g_MSDKDataManager.loginQQ = true
    end
end


--MSDK登录成功，触发应用登录
function UILoginPanel:OnMSDKLogin(openId, token, channelId, userName, isManual)

    --登录成功就认证已实名
    g_DataUserInfoManager.m_isRealName = true

    if isManual then
        --如果是手动登录，需要弹msg"用实名信息登录的提示"
        local clickCallBack = function()
            self:OnMSDKLoginSuccess(openId, token, channelId, userName)
        end
        local msgId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "realNameMsg", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(clickCallBack, msgId)
    else
        self:OnMSDKLoginSuccess(openId, token, channelId, userName)
    end
end

--MSDK登录成功后，触发应用登录流程
function UILoginPanel:OnMSDKLoginSuccess(openId, token, channelId, userName)
    self.m_userName = openId
    self.m_password = token
    --3 是指MSDK登录

    self.m_loginClient:Login(self.m_userName, self.m_password, true, channelId)
    self:DelayShowMask()

    local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableConst, "accountAuthSuccess", g_ConfigTable.Table_Value)
    g_UITipsManager:ShowMessage(messageId)
    g_CS:UnityEngine_PlayerPrefs().SetInt("LoginFailTimes", 0)
    g_CS:UnityEngine_PlayerPrefs().SetInt("LoginFailRealTimeS", 0)
end

function UILoginPanel:OnMSDKLoginFail(type)
    self:HideMask()

    if type == "Fail" then
        local loginFailTimes = g_CS:UnityEngine_PlayerPrefs().GetInt("LoginFailTimes", 0)
        g_CS:UnityEngine_PlayerPrefs().SetInt("LoginFailTimes", loginFailTimes + 1)
        g_CS:UnityEngine_PlayerPrefs().SetInt("LoginFailRealTimeS", os.time())
    end
    self:SetAgreementShowState(false, false)
end

function UILoginPanel:ShowGuestLoginWindow()
    self.m_guestWindow.gameObject:SetActive(true)
end

function UILoginPanel:HideGuestLoginWindow()
    self.m_guestWindow.gameObject:SetActive(false)
end

function UILoginPanel:ShowUserName(username)
    --[[
    if username == nil then
        self.m_UserNameText.text = ""
        self.m_loginAccount.gameObject:SetActive(false)
        self.m_LogoutBtn.gameObject:SetActive(false)
        self.m_KFBtn.gameObject:SetActive(false)
    else
        self.m_UserNameText.text = tostring(username)
        self.m_loginAccount.gameObject:SetActive(true)
        self.m_LogoutBtn.gameObject:SetActive(true)
        self.m_KFBtn.gameObject:SetActive(g_MSDKDataManager:MSDKPlatformAbilitySwitch())
    end
    --]]
end

--检查登录是否在冷却时间内
function UILoginPanel:CheckLoginFailInterval()
    local loginFailTimes = g_CS:UnityEngine_PlayerPrefs().GetInt("LoginFailTimes", 0)
    local loginFailRealTimeS = g_CS:UnityEngine_PlayerPrefs().GetInt("LoginFailRealTimeS", 0)
    local level1CooldownInterval = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "level1Cooldown", "value")
    local level2CooldownInterval = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "level2Cooldown", "value")
    local nowRealTimeS = os.time() - loginFailRealTimeS

    local msgId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "connectCooldownMsg", "value")

    if loginFailTimes < g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "level1CooldownTrigger", "value") then
        return false
    elseif loginFailTimes < g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "level2CooldownTrigger", "value") then
        if level1CooldownInterval - nowRealTimeS > 0 then
            g_UITipsManager:ShowMessage(msgId, level1CooldownInterval - nowRealTimeS)
            return true
        end
        return false
    else
        if level2CooldownInterval - nowRealTimeS > 0 then
            g_UITipsManager:ShowMessage(msgId, level2CooldownInterval - nowRealTimeS)
            return true
        end
        return false
    end
end

--显示排队界面
function UILoginPanel:ShowQueuePanel(isSuccess,data)
    print("UILoginPanel:onStartQueue", isSuccess, data)
    if self.m_queueTimeOutDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_queueTimeOutDelay)
        self.m_queueTimeOutDelay = nil
    end
    if not isSuccess then
        -- local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        -- g_UITipsManager:ShowMessage(messageId, data)
        self:QueueSuccess()
        return
    end
    local data = json.decode(data)
    local state = data.state or 0
    if tonumber(state) ~= 1 then
        self:QueueSuccess()
        return
    end
    self.m_queueFirstWaitTime = data.waitTime or 0
    self.m_queueFirstWaitPos = data.queueId or 0
    if self.m_queuePanel == nil then
        g_CS.ResLoad_AsyncLoadAssetForLua("Assets/Res/ui/prefab/common/UIQueuePanel.prefab", self, "LoadQueuePrefabAsyn", g_Component.GameObject, nil)
    else
        self.m_queuePanel.gameObject:SetActive(true)
        if tonumber(self.m_queueFirstWaitPos) <= 8000 then
            self.m_queuePosText.text = tostring(self.m_queueFirstWaitPos)
        else
            self.m_queuePosText.text = "> 8000"
        end

        self.m_queueTimeText.text = tostring(math.modf(tonumber(self.m_queueFirstWaitTime) / 60)) .. "分钟"
        local queueTime = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "loginQueueWaitTimeRefresh", g_ConfigTable.Table_Value)
        local firstTime = math.min(self.m_queueFirstWaitTime,queueTime)
        self.m_queueDelay = g_ScriptEvent:DelayCall(firstTime * 1000, queueTime*1000, -1, self, "ReqQueueInfo")
    end
end

--http请求超时处理（暂定十秒）
function UILoginPanel:QueueTimeOutCheck()
    if self.m_queueTimeOutDelay then
        self:QueueSuccess()
        g_ScriptEvent:RemoveDelayCall(self.m_queueTimeOutDelay)
        self.m_queueTimeOutDelay = nil
    end
end

--加载排队预制体
function UILoginPanel:LoadQueuePrefabAsyn(asynLoadResult)
    local prefab = asynLoadResult.m_oAssetObject
    if prefab == nil then
        return
    end
    if g_CS.MyUtils_UnityObjectIsNull(self.gameObject) then
        return
    end
    self.m_queuePanel = g_CS.MyUtils_Instantiate(prefab, self.gameObject.transform)
    self.m_queueQuitBtn = self.m_queuePanel.transform:Find("Main/ModalWindow/QuitBtn"):GetComponent(g_Component.Button)
    self.AddButtonOnClick(self.m_queueQuitBtn, self.OnClickQueueQuitBtn)
    self.m_queuePosText = self.m_queuePanel.transform:Find("Main/ModalWindow/TextVal1"):GetComponent(g_Component.Text)
    self.m_queueTimeText = self.m_queuePanel.transform:Find("Main/ModalWindow/TextVal2"):GetComponent(g_Component.Text)

    if self.m_queueFirstWaitPos then
        if tonumber(self.m_queueFirstWaitPos) <= 8000 then
            self.m_queuePosText.text = tostring(self.m_queueFirstWaitPos)
        else
            self.m_queuePosText.text = "> 8000"
        end
    end

    local queueTime = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "loginQueueWaitTimeRefresh", g_ConfigTable.Table_Value)
    local firstTime = queueTime
    if self.m_queueFirstWaitTime then
        self.m_queueTimeText.text = tostring(math.modf(tonumber(self.m_queueFirstWaitTime) / 60)) .. "分钟"
        firstTime = math.min(self.m_queueFirstWaitTime,queueTime)
    end
    
    self.m_queueDelay = g_ScriptEvent:DelayCall(firstTime * 1000, queueTime * 1000, -1, self, "ReqQueueInfo")
end

--请求排队信息
function UILoginPanel:ReqQueueInfo()
    if not self.m_centerServerLoginInfo then
        return
    end
    
    local address = "http://%s/getQueueInfo?accountName=%s&serverId=%s"
    local loginAccount = self.m_loginAccount
    local url = string.format(address,self.m_centerServerLoginInfo.QueueServerHost,loginAccount,self.m_centerServerLoginInfo.ServerId)
    --g_CS.MyUtils_HttpPostForLua(url, {}, {}, self, self.RefreshQueueInfo)
    if g_CS:LoadingConfigManager_Instance():IsManualSelectServer() then
        loginAccount = self.m_userName
        url = string.format(address,g_GlobalDefine.QueueServerIp,self.m_userName,self.selectServerId)
    end
    local body = {}
    body.phone = loginAccount
    body.device = g_CS:UnityEngine_SystemInfo().deviceUniqueIdentifier
    body.ts = os.time() * 1000
    body.sign = body.phone .. body.ts
    g_LuaUtil:HttpPost2(url, {}, body, self, self.RefreshQueueInfo)
    self.m_isReqQueueInfo = true
    
    if self.m_queueTimeOutDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_queueTimeOutDelay)
        self.m_queueTimeOutDelay = nil
    end
    self.m_queueTimeOutDelay = g_ScriptEvent:DelayCall(15000, 0,1, self, "QueueTimeOutCheck")
end

--请求排队信息成功
function UILoginPanel:RefreshQueueInfo(isSuccess,data)
    print("UILoginPanel:onGetQueueInfo", isSuccess, data)
    self.m_isReqQueueInfo = false
    if self.m_queueTimeOutDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_queueTimeOutDelay)
        self.m_queueTimeOutDelay = nil
    end
    if not isSuccess then
        self:QueueSuccess()
        return
    end
    data = json.decode(data)
    local waitState = data.state or 0
    local waitPos = data.queueId or 0
    local waitTime = data.waitTime or 0
    if tonumber(waitPos) <= 8000 then
        self.m_queuePosText.text = tostring(waitPos)
    else
        self.m_queuePosText.text = "> 8000"
    end
    
    self.m_queueTimeText.text = tostring(math.modf(tonumber(waitTime) / 60)) .. "分钟"

    if tonumber(waitState) ~= 1 then
        self:QueueSuccess()
    end
end


--排队成功登录服务器
function UILoginPanel:QueueSuccess()
    if not self.m_isInQueue then
        return
    end
    self.m_isInQueue = false
    self.m_isReqQueueInfo = false
    if self.m_queueTimeOutDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_queueTimeOutDelay)
        self.m_queueTimeOutDelay = nil
    end
    if self.m_queuePanel then
        self.m_queuePanel.gameObject:SetActive(false)
    end
    if self.m_queueDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_queueDelay)
        self.m_queueDelay = nil
    end
    self.m_queueFirstWaitPos = nil
    self.m_queueFirstWaitTime = nil
    if self.m_loginCallBack then
        self.m_loginCallBack()
        self.m_loginCallBack = nil
    end
end


--点击退出排队按钮
function UILoginPanel:OnClickQueueQuitBtn()
    --g_CS:GCloudQueueManager_Instance():ExitQueue()
    self.m_isInQueue = false
    self.m_isReqQueueInfo = false
    print("exit queue")
    self.m_queueFirstWaitPos = nil
    self.m_queueFirstWaitTime = nil
    if self.m_queueTimeOutDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_queueTimeOutDelay)
        self.m_queueTimeOutDelay = nil
    end
    self.m_queuePanel.gameObject:SetActive(false)
    if self.m_queueDelay then
        g_ScriptEvent:RemoveDelayCall(self.m_queueDelay)
        self.m_queueDelay = nil
    end
    self.m_queueFirstWaitTime = nil
end

-- --收到成功进入排队的回调
-- function UILoginPanel:OnHandleMSDKJoinQueue(curPosition, estimatedTime)
--     self.m_isInQueue = true
--     self:ShowQueuePanel()
--     if curPosition == nil then
--         self.m_queuePosText.text = "0"
--     else
--         self.m_queuePosText.text = curPosition
--     end
--     self.m_queueTimeText.text = tostring(math.modf(estimatedTime / 60)) .. "分钟"
-- end

-- --收到成功退出排队的回调
-- function UILoginPanel:OnHandleMSDKExitQueue()
--     self.m_isInQueue = false
--     print("OnHandleMSDKExitQueue")
--     self.m_queuePanel.gameObject:SetActive(false)
-- end

-- --收到进入排队失败的回调
-- function UILoginPanel:OnHandleMSDKJoinQueueFail(result, statusInfo)
--     g_CS.DebugL8_Log("JoinQueue Fail, ErrorCode:{0}, ErrorMsg:{1}", statusInfo.ErrCode, statusInfo.ErrMsg);
-- end

-- --收到退出排队失败的回调
-- function UILoginPanel:OnHandleMSDKExitQueueFail(result, statusInfo)
--     g_CS.DebugL8_Log("ExitQueue, ErrorCode:{0}, ErrorMsg:{1}", statusInfo.ErrCode, statusInfo.ErrMsg);
--     if g_CS.System_Convert_ToUInt32(statusInfo.ErrCode) == 200 or g_CS.System_Convert_ToUInt32(statusInfo.ErrCode) == 201 then
--         if self.m_queuePanel ~= nil then
--             self.m_queuePanel.gameObject:SetActive(false)
--         end
--     end
-- end

-- --收到排队错误的回调
-- function UILoginPanel:OnHandleMSDKQueueError()
--     print("OnHandleMSDKQueueError")
-- end

-- --收到排队完成的回调
-- function UILoginPanel:OnHandleMSDKFinishQueue(queueToken, joinTime, passTime)
--     print("OnHandleMSDKFinishQueue queueToken:" .. queueToken .. " joinTime:" .. joinTime .. " passTime:" .. passTime)
--     self.m_isInQueue = false
--     if self.m_queuePanel ~= nil then
--         self.m_queuePanel.gameObject:SetActive(false)
--     end
--     local accessToken
--     if g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.WeChat then
--         accessToken = g_MSDKDataManager.loginData.openKey
--     elseif g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.QQ or g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.Guest then
--         accessToken = g_MSDKDataManager.loginData.token
--     end
--     local ip = self.m_serverListTable[self.selectServerId].ip
--     local gameData = g_MSDKDataManager.loginData.gameData
--     if gameData == nil
--     then
--         gameData = ""
--     end

--     local password = self.loginToken
--     local param = {}
--     param.token = self.loginToken
--     param.loginServerId = self.centerServerId
--     param.accessToken = accessToken
--     param.gameData = gameData

--     local Dictionary_String_String = g_CS.System_Collections_Generic_Dictionary(CS.System.String, CS.System.String)
--     local dic = Dictionary_String_String()
--     dic:Add('token', tostring(queueToken))
--     dic:Add('jointime', tostring(joinTime))
--     dic:Add('passtime', tostring(passTime))
--     param.queue = dic

--     g_EventMgr:SendEvent(g_EventDef.EVENT_NET_ON_CLICK_LOGIN, self.m_accountType, self.m_userName, password, ip, param)

--     local info = {}
--     info.accountType = self.m_accountType
--     info.userName = self.m_userName
--     info.password = password
--     info.ip = ip
--     info.token = self.loginToken
--     info.centerServerId = self.centerServerId

--     g_DataUserInfoManager.m_loginInfo = info

--     -- 7 代表GPM登录漏斗中：点击进入应用
--     self:DelayShowMask()
-- end

function UILoginPanel:OnHandleRefreshUI()
    if self.m_isInQueue == true then
        g_CS:GCloudQueueManager_Instance():ExitQueue()
    end
    if self.m_queuePanel ~= nil then
        self.m_queuePanel.gameObject:SetActive(false)
    end
end

--拉取服务器信息完毕
function UILoginPanel:OnHandleMapleQueryTreeFinished()
    self.m_serverListTable = {}
    if #g_MSDKDataManager.leafInfo > 0 and #g_MSDKDataManager.treeInfo > 0 then
        for i = 1, #g_MSDKDataManager.leafInfo do
            local id = tostring(g_MSDKDataManager.leafInfo[i].id)
            if self.m_serverListTable[id] == nil then
                self.m_serverListTable[id] = {}
            end
            local curLeafInfo = g_MSDKDataManager.leafInfo[i]
            local curServerInfo = self.m_serverListTable[id]

            curServerInfo.mode = 0
            curServerInfo.ip = curLeafInfo.url
            curServerInfo.defaultState = curLeafInfo.flag
            curServerInfo.state = curLeafInfo.flag
            curServerInfo.parentId = curLeafInfo.parentId
            curServerInfo.name = curLeafInfo.name
            curServerInfo.tag = curLeafInfo.tag
            curServerInfo.plat = curLeafInfo.plat
            curServerInfo.hide = curLeafInfo.hide
            curServerInfo.day = curLeafInfo.day
            curServerInfo.startTime = curLeafInfo.startTime
        end
    else
        local messageId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "login_enterServerError_msgID", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(messageId, 96)
    end

    g_DataUserInfoManager.m_serverListTable = self.m_serverListTable

    -- if g_MSDKDataManager.treeId ~= self.curTreeId then
    -- 	self:InitServerList()
    -- 	self.curTreeId = g_MSDKDataManager.treeId
    -- else
    -- 	self:OnGetServerState()
    -- end

    if self.m_lastChannelID ~= g_MSDKDataManager.loginData.channelId or self.m_lastServerLeafNodeCount ~= #g_MSDKDataManager.leafInfo or self.m_lastServerTreeNodeCount ~= #g_MSDKDataManager.treeInfo then
        self.m_needRefreshTreeInfo = true
        self.m_lastChannelID = g_MSDKDataManager.loginData.channelId
        self.m_lastServerLeafNodeCount = #g_MSDKDataManager.leafInfo
        self.m_lastServerTreeNodeCount = #g_MSDKDataManager.treeInfo
        self:InitServerList()
        self:RefreshCharacterUI(self.m_characterList)
    else
        self:OnGetServerState()
    end

    if self.useSDK
    then
        if self.m_inGameFriends == nil and g_MSDKDataManager:MSDKPlatformAbilitySwitch()
        then
            --请求同玩好友
            self.m_loginClient:GetWXFriendInfo(g_MSDKDataManager.loginData.openId, g_MSDKDataManager.loginData.token, g_MSDKDataManager.loginData.channelId)
        end
    end
end

--收到中心服服务器列表支持
function UILoginPanel:OnHandleGetServerlistDir(isMaple, serverListInfo)
    if isMaple == true then
        if g_CS:DolphinGlobalDefine().isAuditProgramVersion == true then
            g_MSDKDataManager.treeId = 4
        else
            g_MSDKDataManager.treeId = tonumber(serverListInfo)
        end

        g_MSDKDataManager:MapleQueryTree(g_MSDKDataManager.treeId)
    end
end

--同玩好友
function UILoginPanel:OnHandleOnGetInSameFriend(friends)
    if self.m_friendIconTab == nil
    then
        local friendPanel = self.gameObject.transform:Find("Main/ServerLogin/Friend/Content")
        self.m_friendIconTab = {}
        for i = 0, friendPanel.childCount - 1 do
            local icon = friendPanel:GetChild(i):GetComponent(g_Component.Image)
            table.insert(self.m_friendIconTab, icon)
        end
    end

    self.m_inGameFriends = friends
    local count = 0
    local showCount = #self.m_friendIconTab
    for i = 0, friends.Count - 1 do
        local info = friends[i]
        --print(info.UserName .. " ServerId " .. tostring(info.ServerId) .. " ".. tostring(self.m_serverListTable[tostring(info.ServerId)] == nil))
        if self.m_serverListTable[tostring(info.ServerId)]
        then
            if count < showCount
            then
                self.m_friendIconTab[count + 1].gameObject:SetActive(true)
                local picUrl
                if g_MSDKDataManager.loginData.channelId == g_GlobalDefine.MSDKChannelID.WeChat
                then
                    picUrl = friends[i].PictureUrl .. "/46"
                else
                    picUrl = friends[i].PictureUrl .. "40"
                end
                g_CS.MyUtils_ShowUrlImage(self.m_friendIconTab[count + 1], picUrl)
                count = count + 1
            else
                break
            end
        end
    end

    self.m_friendPanel:SetActive(count > 0)

    if count > 0
    then
        for i = count + 1, #self.m_friendIconTab do
            self.m_friendIconTab[i].gameObject:SetActive(false)
        end
    end

    print("同玩好友数量总数 " .. tostring(friends.Count) .. " 实际数量 " .. tostring(count))
    if self.currentSelectZoneID == "3"
    then
        self:RefreshZoneServerStateList()
    end
end

function UILoginPanel:OnClickFriendPanel(arg)
    self:OnClickSelectServerBtn()
    self.zoneTable["3"].toggle.isOn = true
end

--[[
--异账号退出登录并自动登录
function UILoginPanel:OnHandleDifferentAccountLogout()
    g_MSDKDataManager:HasDirInfo(false)
    self:Logout()
    if g_MSDKDataManager.loginData.gameData == g_GlobalDefine.MSDKWakeUpGameData.WeChatGameCenter then
        self:LoginWithWX()
    elseif g_MSDKDataManager.loginData.gameData == g_GlobalDefine.MSDKWakeUpGameData.QQGameCenter then
        self:LoginWithQQ()
    end
end
--]]

--region 适龄提示处理

function UILoginPanel:OnClickAgeLimitButton(go)
    self.ageLimitTextRectTransform.anchoredPosition = g_CS.UnityEngine_Vector2.zero
    self.m_ageLimitWindowObj:SetActive(true)
end

function UILoginPanel:OnClickAgeLimitWindowCloseButton(go)
    self.m_ageLimitWindowObj:SetActive(false)
end

--endregion

--region 用户协议同意处理

function UILoginPanel:OnClickAgreementToggleValueChanged(isOn)
    self.m_agreeTipFxObj:SetActive(not isOn)
end

function UILoginPanel:SetAgreementShowState(hideAgreement, toggleValue)
    self.m_agreeMent.gameObject:SetActive(not hideAgreement)
    self.m_agreementToggle.isOn = toggleValue
end

function UILoginPanel:StopLoginByDontAgreeUserAgreement()
    if self.m_agreementToggle.isOn == false then
        local msgId = g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, "checkAgreementTips", g_ConfigTable.Table_Value)
        g_UITipsManager:ShowMessage(msgId)
        return true
    end
    return false
end

function UILoginPanel:OnClickUserAgreementButton(go)
    g_LuaUtil:OnClickUserAgreementButton(go)
end

function UILoginPanel:OnClickPrivacyProtectButton(go)
    g_LuaUtil:OnClickPrivacyProtectButton(go)
end

function UILoginPanel:OnClickChildPrivacyProtectButton(go)
    g_LuaUtil:OnClickChildPrivacyProtectButton(go)
end

function UILoginPanel:OnClick3rdInfoShareButton(go)
    g_LuaUtil:OnClick3rdInfoShareButton(go)
end

function UILoginPanel:SetLockLogin(lock)
    if self.startLoginLockId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.startLoginLockId)
        self.startLoginLockId = nil
    end
    self.loginLockGo:SetActive(lock)
    self.loginlock = lock
    --self.m_LoginBtn.enabled = not lock
    self.loginTip.alpha = lock and 0 or 1.0
end

function UILoginPanel:StartLoginLock(time)
    if self.startLoginLockId ~= nil then
        g_ScriptEvent:RemoveDelayCall(self.startLoginLockId)
        self.startLoginLockId = nil
    end
    self:SetLockLogin(true)
    self.curLoginLockTime = math.floor(time + 0.01)
    g_UITipsManager:ShowMessage(g_ConfigData:GetValueFromConfigTable(g_ConfigTable.TableLoginSet, g_ConfigTable.LoginSet_login_tooBusy_msgID, g_ConfigTable.Table_Value), self.curLoginLockTime)
    self.startLoginLockId = g_ScriptEvent:DelayCall(0, 1000, self.curLoginLockTime + 1, self, "ShowLoginLock")
end

function UILoginPanel:ShowLoginLock()
    self.loginLockText.text = string.gsub(self.login_tooBusy_text, "{0}", tostring(self.curLoginLockTime))
    self.curLoginLockTime = self.curLoginLockTime - 1
    if self.curLoginLockTime <= -1 then
        self:SetLockLogin(false)
    end
end

--endregion

return UILoginPanel
