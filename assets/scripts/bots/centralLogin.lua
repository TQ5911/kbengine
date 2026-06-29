-- Auto generated from _pb2.py, do not edit.

local M = {}

M.CentralServer = {
    -- CentralServer
    getLoginKey = 0,
    loginByPassword = 1,
    loginByToken = 2,
    getCharaterInfo = 3,
    listServers = 4,
    activeTick = 5,
    checkCDkey = 6,
    getServerListDir = 7,
    captchaValidate = 8,
    loginByThird = 9,
}

M.CentralServerArgs = {
    -- method -> input message name (one arg per method)
    getLoginKey = "LoginKeyRequest",
    loginByPassword = "PasswordLogin",
    loginByToken = "TokenLogin",
    getCharaterInfo = "Void",
    listServers = "Void",
    activeTick = "Void",
    checkCDkey = "CheckCDKeyRequest",
    getServerListDir = "ServerListRequest",
    captchaValidate = "CaptchaValidateRequest",
    loginByThird = "ThirdLogin",
}

M.CentralServerMethod = {
    -- method -> { input, output }
    getLoginKey = { input = "LoginKeyRequest", output = "Void" },
    loginByPassword = { input = "PasswordLogin", output = "Void" },
    loginByToken = { input = "TokenLogin", output = "Void" },
    getCharaterInfo = { input = "Void", output = "Void" },
    listServers = { input = "Void", output = "Void" },
    activeTick = { input = "Void", output = "Void" },
    checkCDkey = { input = "CheckCDKeyRequest", output = "Void" },
    getServerListDir = { input = "ServerListRequest", output = "Void" },
    captchaValidate = { input = "CaptchaValidateRequest", output = "Void" },
    loginByThird = { input = "ThirdLogin", output = "Void" },
}

M.GameClient = {
    -- GameClient
    onGetLoginKey = 0,
    onLoginReply = 1,
    onGetCharacterInfo = 2,
    onListServers = 3,
    activeTickCallback = 4,
    onCheckCDKey = 5,
    onGetServerListDir = 6,
    onCaptchaValidate = 7,
    onCheckCaptcha = 8,
}

M.GameClientArgs = {
    -- method -> input message name (one arg per method)
    onGetLoginKey = "LoginKeyResponse",
    onLoginReply = "LoginReply",
    onGetCharacterInfo = "CharacterInfo",
    onListServers = "ServerInfo",
    activeTickCallback = "Void",
    onCheckCDKey = "CheckCDKeyReply",
    onGetServerListDir = "ServerListReply",
    onCaptchaValidate = "CaptchaValidateResponse",
    onCheckCaptcha = "CheckCaptchaNotify",
}

M.GameClientMethod = {
    -- method -> { input, output }
    onGetLoginKey = { input = "LoginKeyResponse", output = "Void" },
    onLoginReply = { input = "LoginReply", output = "Void" },
    onGetCharacterInfo = { input = "CharacterInfo", output = "Void" },
    onListServers = { input = "ServerInfo", output = "Void" },
    activeTickCallback = { input = "Void", output = "Void" },
    onCheckCDKey = { input = "CheckCDKeyReply", output = "Void" },
    onGetServerListDir = { input = "ServerListReply", output = "Void" },
    onCaptchaValidate = { input = "CaptchaValidateResponse", output = "Void" },
    onCheckCaptcha = { input = "CheckCaptchaNotify", output = "Void" },
}

M.byFullName = {
    ["CentralServer.getLoginKey"] = 0,
    ["CentralServer.loginByPassword"] = 1,
    ["CentralServer.loginByToken"] = 2,
    ["CentralServer.getCharaterInfo"] = 3,
    ["CentralServer.listServers"] = 4,
    ["CentralServer.activeTick"] = 5,
    ["CentralServer.checkCDkey"] = 6,
    ["CentralServer.getServerListDir"] = 7,
    ["CentralServer.captchaValidate"] = 8,
    ["CentralServer.loginByThird"] = 9,
    ["GameClient.onGetLoginKey"] = 0,
    ["GameClient.onLoginReply"] = 1,
    ["GameClient.onGetCharacterInfo"] = 2,
    ["GameClient.onListServers"] = 3,
    ["GameClient.activeTickCallback"] = 4,
    ["GameClient.onCheckCDKey"] = 5,
    ["GameClient.onGetServerListDir"] = 6,
    ["GameClient.onCaptchaValidate"] = 7,
    ["GameClient.onCheckCaptcha"] = 8,
}

M.byFullNameArgs = {
    ["CentralServer.getLoginKey"] = "LoginKeyRequest",
    ["CentralServer.loginByPassword"] = "PasswordLogin",
    ["CentralServer.loginByToken"] = "TokenLogin",
    ["CentralServer.getCharaterInfo"] = "Void",
    ["CentralServer.listServers"] = "Void",
    ["CentralServer.activeTick"] = "Void",
    ["CentralServer.checkCDkey"] = "CheckCDKeyRequest",
    ["CentralServer.getServerListDir"] = "ServerListRequest",
    ["CentralServer.captchaValidate"] = "CaptchaValidateRequest",
    ["CentralServer.loginByThird"] = "ThirdLogin",
    ["GameClient.onGetLoginKey"] = "LoginKeyResponse",
    ["GameClient.onLoginReply"] = "LoginReply",
    ["GameClient.onGetCharacterInfo"] = "CharacterInfo",
    ["GameClient.onListServers"] = "ServerInfo",
    ["GameClient.activeTickCallback"] = "Void",
    ["GameClient.onCheckCDKey"] = "CheckCDKeyReply",
    ["GameClient.onGetServerListDir"] = "ServerListReply",
    ["GameClient.onCaptchaValidate"] = "CaptchaValidateResponse",
    ["GameClient.onCheckCaptcha"] = "CheckCaptchaNotify",
}

return M
