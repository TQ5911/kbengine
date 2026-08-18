from KBEDebug import *
import KBEngine
import hashlib
import utils
import uuid
import hmac
import json
import base64
from datetime import datetime
import gameconfig
from abc import ABC, abstractmethod


class CloudServicesSDK(object):
    def __init__(self, provider):
        self.provider = provider
        self.textSecurity = 'text_security'
        #print("CloudServicesSDK __init__", self.provider)

    @abstractmethod
    def textSecurityDetect(self, datas, callback):
        return True

class TencentCloudServicesSDK(CloudServicesSDK):
    def __init__(self):
        CloudServicesSDK.__init__(self, 'tencent')
        #print("TencentCloudServicesSDK __init__")

    def textSecurityRequest(self, action, params, callback):

        secret_id = gameconfig.getCloudServicesData(self.provider, self.textSecurity, "secretId")
        secret_key = gameconfig.getCloudServicesData(self.provider, self.textSecurity, "secretKey")
        service = gameconfig.getCloudServicesData(self.provider, self.textSecurity, "service")
        host = gameconfig.getCloudServicesData(self.provider, self.textSecurity, "host")
        endpoint = "https://" + host
        region = gameconfig.getCloudServicesData(self.provider, self.textSecurity, "region")
        version = "2020-12-29"  # 版本为固定值
        algorithm = gameconfig.getCloudServicesData(self.provider, self.textSecurity, "algorithm")
        #print("textSecurityRequest", algorithm)

        timestamp = utils.curTS()
        day = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

        # ************* 步骤 1：拼接规范请求串 *************
        http_request_method = "POST"
        canonical_url = "/"
        canonical_querystring = ""
        ct = "application/json; charset=utf-8"
        payload = json.dumps(params)
        canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
        signed_headers = "content-type;host"
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (
            http_request_method
            + "\n"
            + canonical_url
            + "\n"
            + canonical_querystring
            + "\n"
            + canonical_headers
            + "\n"
            + signed_headers
            + "\n"
            + hashed_request_payload
        )
        #print('textSecurityRequest canonical_request' + canonical_request)

        # ************* 步骤 2：拼接待签名字符串 *************
        credential_scope = day + "/" + service + "/" + "tc3_request"
        hashed_canonical_request = hashlib.sha256(
            canonical_request.encode("utf-8")
        ).hexdigest()
        string_to_sign = (
            algorithm
            + "\n"
            + str(timestamp)
            + "\n"
            + credential_scope
            + "\n"
            + hashed_canonical_request
        )

        #print('textSecurityRequest string_to_sign' + string_to_sign)

        secret_date = self.textSecuritySign(("TC3" + secret_key).encode("utf-8"), day)
        secret_service = self.textSecuritySign(secret_date, service)
        secret_signing = self.textSecuritySign(secret_service, "tc3_request")
        signature = hmac.new(
            secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        #print('textSecurityRequest signature' + signature)

        # ************* 步骤 4：拼接 Authorization *************
        authorization = (
            algorithm
            + " "
            + "Credential="
            + secret_id
            + "/"
            + credential_scope
            + ", "
            + "SignedHeaders="
            + signed_headers
            + ", "
            + "Signature="
            + signature
        )
        #print('textSecurityRequest authorization' + authorization)

        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json; charset=utf-8",
            "Host": host,
            "X-TC-Action": action,
            "X-TC-Timestamp": str(timestamp),
            "X-TC-Version": version,
            "X-TC-Region": region,
        }

        KBEngine.urlopenv2(endpoint, callback, method='POST',
                postData=payload.encode('utf-8'),
                headers=headers,
                timeoutSec=30)

    def textSecuritySign(self, key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def textSecurityDetect(self, datas, callback):
        if not self.checkTextSecurityEnable():
            return False
        
        content = datas.get("text", "")
        idStr = datas.get("id", "")
        bizType = datas.get("bizType", "")
        #print("textSecurityDetect", content, idStr, bizType)
        b4content = base64.b64encode(content.encode()).decode()

        userNode = {
            "UserId"    : str(idStr),
        }
        params = {"BizType": str(bizType), "Content": b4content, "User": userNode}
        #print("textSecurityDetect params", params)
        action = "TextModeration"
        self.textSecurityRequest(action, params, callback)
        return True

    def checkTextSecurityEnable(self):
        enable = gameconfig.getCloudServicesData(self.provider, self.textSecurity, "enable")
        return int(enable) == 1

def checkTextSecurity(datas, callback):
    # 切换
    if True:
        return TencentCloudServicesSDK().textSecurityDetect(datas, callback)