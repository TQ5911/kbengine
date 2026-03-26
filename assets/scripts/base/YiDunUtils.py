import hashlib
import gameconfig
import KBEngine
import utils
import uuid

class YiDunGen():
    # 签名方法样例
    def __init__(self, platform):
        self.platform = platform
        self.businessId = gameconfig.getYidunData("business_" + self.platform)
        self.secretId = gameconfig.getYidunData("secretId")
        self.secretKey = gameconfig.getYidunData("secretKey")
        self.timestamp = utils.getTimestamp64()
        self.nonce = str(uuid.uuid4().hex)
        self.version = "603"

    def gen_signature(self, params):
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secretKey
        return hashlib.md5(buff.encode("utf8")).hexdigest()
    
    def getData(self):
        return {
            "businessId": self.businessId,
            "secretId": self.secretId,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "version": self.version
        }