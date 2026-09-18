# coding: utf-8
from KBEDebug import *
import KBEngine
import json
import gameconfig
import gameconst
import gamedecorator
import AuthClsWraper
import dropAward
import mailAssistor
import message_Message_def as MMD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import welfare_config as W_CDD
import welfare_levelReward as W_LRD
import welfare_refundRecharge as W_RRD
import rewardData_rewardData as RD_RDD
import guildAuthorization_authorization as GAZ_AD
import guildAuthorization_authorization_def as GAAD

'''
测试奖励(一测排名/二测充值/二测矿战/二测战力)查询与领取
数据来源于 web 后台统一接口(见 测试奖励接口.txt), 奖励内容不会变化,
查询结果缓存在内存中(不做持久化); 领取为一次性领取全部奖励, 奖励通过邮件下发
'''

# 测试奖励类型(web 后台定义, 固定按 1、2、3、5 排序返回, 可能只有其中某几项)
TEST_REWARD_TYPE_LEVEL_RANK = 1     # 吉日首测排名
TEST_REWARD_TYPE_RECHARGE = 2       # 炽焰测试充值返还
TEST_REWARD_TYPE_MINE_GUILD = 3     # 炽焰测试矿战获胜帮会
TEST_REWARD_TYPE_POWER_RANK = 5     # 炽焰测试战力排行

TEST_REWARD_ALL_TYPES = (
    TEST_REWARD_TYPE_LEVEL_RANK,
    TEST_REWARD_TYPE_RECHARGE,
    TEST_REWARD_TYPE_MINE_GUILD,
    TEST_REWARD_TYPE_POWER_RANK,
)

# ==================== mock 数据, 仅测试用, 测完删除(开始) ====================
# 查询回包: 覆盖四类奖励
# type1 rank5 -> levelReward(condition10) 40000150
# type2 充6000 -> 元宝60000 + 绑元17000 + tierReward 40000206
# type3 副帮主 -> mineBattleReward 40000205
# type5 rank75 -> powerRushReward 40000203
TEST_REWARD_MOCK_QUERY_DATA = json.dumps({
    "code": 200,
    "message": "success",
    "data": {
        "rewards": [
            {
                "rewardType": 1,
                "claimed": False,
                "reward": {"rewardType": 1, "ranking": 5},
            },
            {
                "rewardType": 2,
                "claimed": False,
                "reward": {"rewardType": 2, "rechargeAmount": 6000},
            },
            {
                "rewardType": 3,
                "claimed": False,
                "reward": {"rewardType": 3, "guildTitleId": 2},
            },
            {
                "rewardType": 5,
                "claimed": False,
                "reward": {"rewardType": 5, "ranking": 75},
            },
        ],
    },
    "timestamp": 1699123456789,
})

TEST_REWARD_MOCK_CLAIM_DATA = json.dumps({
    "code": 200,
    "message": "success",
    "data": {
        "claimBatchNo": "mock-batch-001",
        "claimed": True,
        "rewards": [
            {"rewardType": 1, "ranking": 5},
            {"rewardType": 2, "rechargeAmount": 6000},
            {"rewardType": 3, "guildTitleId": 2},
            {"rewardType": 5, "ranking": 75},
        ],
    },
    "timestamp": 1699123456789,
})
# ==================== mock 数据, 仅测试用, 测完删除(结束) ====================


class ITestReward(object):
    def __init__(self):
        LOG_DBG("ITestReward init")
        # {rewardType: [web后台返回的TestRewardQueryVO, ...]}, 每类可能有多条; 内存缓存, 不持久化
        self._testRewardCache = {}

    def _testRewardQueryUrl(self):
        url = gameconfig.webServerDomain()
        return f'{url}/user/api/v1/test-rewards/queryAll'

    def _testRewardClaimUrl(self):
        url = gameconfig.webServerDomain()
        return f'{url}/user/api/v1/test-rewards/claims'

    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    def reqQueryTestReward(self, exposed):
        LOG_INFO("ITestReward::reqQueryTestReward", self.gbID, self.accountName)
        if self._testRewardCache:
            LOG_INFO("ITestReward::reqQueryTestReward hit cache")
            self.client.queryTestRewardReplay(self.buildTestRewardOverview())
            return

        url = self._testRewardQueryUrl()
        if not url:
            LOG_ERR("ITestReward::reqQueryTestReward no url config")
            self.onMessagePre(MMD.datas.web_requestException, [])
            return

        LOG_INFO("ITestReward::reqQueryTestReward url", url)
        KBEngine.urlopenv2(
            url,
            self._reqQueryTestRewardResponse,
            method='GET',
            headers={"Content-Type": "application/json", "satoken": self.accountEntity.webToken},
            timeoutSec=5,
        )

    def _reqQueryTestRewardResponse(self, httpCode, jsonData, headers, success, *args):
        # httpCode, jsonData, success = 200, TEST_REWARD_MOCK_QUERY_DATA, True
        LOG_INFO("ITestReward::_reqQueryTestRewardResponse", httpCode, jsonData, success)
        if not (httpCode == 200 and success):
            LOG_ERR("ITestReward::_reqQueryTestRewardResponse failed", httpCode, success)
            self.onMessagePre(MMD.datas.web_requestException, [])
            return

        data = json.loads(jsonData)
        if data.get('code') != 200:
            LOG_WARN("ITestReward::_reqQueryTestRewardResponse exception", data.get('code'))
            self.onMessagePre(MMD.datas.web_requestException, [])
            return

        # 后台可能只返回部分类型的奖励, 按返回内容缓存; 每类可能有多条
        rewardMap = {}
        for rewardVO in (data.get('data') or {}).get('rewards') or []:
            rewardType = int(rewardVO.get('rewardType', 0))
            if rewardType in TEST_REWARD_ALL_TYPES:
                rewardMap.setdefault(rewardType, []).append(rewardVO)
        self._testRewardCache = rewardMap
        self.client.queryTestRewardReplay(self.buildTestRewardOverview())

    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    def reqClaimTestReward(self, exposed):
        LOG_INFO("ITestReward::reqClaimTestReward")
        if not gameconfig.enableClaimTestReward():
            LOG_INFO("ITestReward::reqClaimTestReward not enable")
            self.onMessagePre(MMD.datas.web_requestException, [])
            return

        url = self._testRewardClaimUrl()
        if not url:
            LOG_ERR("ITestReward::reqClaimTestReward no url config")
            self.onMessagePre(MMD.datas.web_requestException, [])
            self.client.claimTestRewardReplay(False)
            return

        message = json.dumps({
            "userGameRoleId": self.gbID,
        })
        LOG_INFO("ITestReward::reqClaimTestReward url", url, message)
        KBEngine.urlopenv2(
            url,
            self._reqClaimTestRewardResponse,
            method='POST',
            postData=message.encode('utf-8'),
            headers={"Content-Type": "application/json", "satoken": self.accountEntity.webToken},
            timeoutSec=5,
        )

    def _reqClaimTestRewardResponse(self, httpCode, jsonData, headers, success, *args):
        # httpCode, jsonData, success = 200, TEST_REWARD_MOCK_CLAIM_DATA, True
        LOG_INFO("ITestReward::_reqClaimTestRewardResponse", httpCode, jsonData, success)
        if not (httpCode == 200 and success):
            self.onMessagePre(MMD.datas.web_requestException, [])
            LOG_ERR("ITestReward::_reqClaimTestRewardResponse failed")
            self.client.claimTestRewardReplay(False)
            return

        data = json.loads(jsonData)
        if data.get('code') != 200:
            LOG_WARN("ITestReward::_reqClaimTestRewardResponse exception", data.get('code'))
            if data.get('code', 0) == 280401:
                self.onMessagePre(MMD.datas.rewardAlreadyReceived, [])
            elif data.get('code', 0) == 280402:
                self.onMessagePre(MMD.datas.rewardNotFound, [])
            else:
                self.onMessagePre(MMD.datas.web_requestException, [])

            self.client.claimTestRewardReplay(False)
            return

        claimData = data.get('data') or {}
        if not claimData.get('claimed'):
            LOG_WARN("ITestReward::_reqClaimTestRewardResponse not claimed", claimData)
            self.client.claimTestRewardReplay(False)
            return

        self.onClaimTestRewardSuccess(claimData.get('rewards') or [])
        self.client.claimTestRewardReplay(True)

    def onClaimTestRewardSuccess(self, rewardItems):
        LOG_INFO("ITestReward::onClaimTestRewardSuccess", self.gbID, self.accountName, rewardItems)
        # 计算全部奖励内容, 通过邮件下发
        attachVal = dropAward.MailAttachVal()
        hasAttach = False
        for rewardItem in rewardItems:
            rewardType = int(rewardItem.get('rewardType', 0))
            for award in self.calcTestRewardAwards(rewardType, rewardItem):
                self._addAwardToMailAttach(attachVal, award)
                hasAttach = True

            cachedList = self._testRewardCache.setdefault(rewardType, [])
            for cached in cachedList:
                cached['claimed'] = True

        if hasAttach:
            self.sendTestRewardMail(attachVal)
            self.onMessagePre(MMD.datas.returnRewardReceived, [])

    def _addAwardToMailAttach(self, attachVal, award):
        # awardId 为 rewardData 奖励包ID(4开头)时, 需要用 addWealthByRewardId 展开后再加入邮件附件
        awardId = award['awardId']
        count = award['count']
        if awardId in RD_RDD.datas:
            for _ in range(count):
                attachVal.addWealthByRewardId(awardId)
        else:
            attachVal.addWealthByItemId(awardId, count)

    def sendTestRewardMail(self, attachVal):
        mailId = W_CDD.datas.get('rewardReceiveMail', {}).get('value', 0)
        if not mailId:
            LOG_ERR("ITestReward::sendTestRewardMail no mail config")
            return
        LOG_INFO("ITestReward::sendTestRewardMail", self.gbID, mailId, bool(attachVal))
        mailAssistor.sendMailToPlayers(
            [self.gbID],
            mailId,
            extraAttach=attachVal,
            opUUID=KBEngine.genUUID64(),
            srcType=AAC_AACDD.datas.BONUS_SRC_WIPE_REWARD,
            desc='testRewardClaim',
        )

    def buildTestRewardOverview(self):
        # 四类奖励区分开下发, 客户端按类别展示, 每类可能有多条
        return {
            'levelRank': self.buildLevelRankInfoList(),
            'recharge': self.buildRechargeInfoList(),
            'mineGuild': self.buildMineGuildInfoList(),
            'powerRank': self.buildPowerRankInfoList(),
        }

    def buildTestRewardBaseInfo(self, rewardType, rewardVO):
        info = {
            'rewardType': rewardType,
            'claimed': bool(rewardVO.get('claimed', False)),
        }
        return info, rewardVO.get('reward') or {}

    def buildLevelRankInfoList(self):
        # 一测等级排名: 排名 + 奖励列表
        infoList = []
        for rewardVO in self._testRewardCache.get(TEST_REWARD_TYPE_LEVEL_RANK, []):
            info, rewardItem = self.buildTestRewardBaseInfo(TEST_REWARD_TYPE_LEVEL_RANK, rewardVO)
            info['ranking'] = int(rewardItem.get('ranking', 0))
            info['awards'] = self.calcTestRewardAwards(TEST_REWARD_TYPE_LEVEL_RANK, rewardItem)
            infoList.append(info)
        return infoList

    def buildRechargeInfoList(self):
        # 二测充值返还: 充值金额 + 充值奖励列表
        infoList = []
        for rewardVO in self._testRewardCache.get(TEST_REWARD_TYPE_RECHARGE, []):
            info, rewardItem = self.buildTestRewardBaseInfo(TEST_REWARD_TYPE_RECHARGE, rewardVO)
            info['rechargeAmount'] = float(rewardItem.get('rechargeAmount') or 0)
            info['awards'] = self.calcTestRewardAwards(TEST_REWARD_TYPE_RECHARGE, rewardItem)
            infoList.append(info)
        return infoList

    def buildMineGuildInfoList(self):
        # 二测矿战: 帮会职务 + 矿战奖励列表
        infoList = []
        for rewardVO in self._testRewardCache.get(TEST_REWARD_TYPE_MINE_GUILD, []):
            info, rewardItem = self.buildTestRewardBaseInfo(TEST_REWARD_TYPE_MINE_GUILD, rewardVO)
            guildTitleId = rewardItem.get('guildTitleId', 0)
            if not guildTitleId:
                LOG_INFO('buildMineGuildInfoList not win guild:', rewardItem)
                continue
            info['guildJob'] = int(rewardItem.get('guildTitleId', 0))
            info['guildName'] = str(rewardItem.get('guildName', ''))
            info['awards'] = self.calcTestRewardAwards(TEST_REWARD_TYPE_MINE_GUILD, rewardItem)
            infoList.append(info)
        return infoList

    def buildPowerRankInfoList(self):
        # 二测战力排名: 排名 + 排名奖励列表
        infoList = []
        for rewardVO in self._testRewardCache.get(TEST_REWARD_TYPE_POWER_RANK, []):
            info, rewardItem = self.buildTestRewardBaseInfo(TEST_REWARD_TYPE_POWER_RANK, rewardVO)
            info['ranking'] = int(rewardItem.get('ranking', 0))
            info['awards'] = self.calcTestRewardAwards(TEST_REWARD_TYPE_POWER_RANK, rewardItem)
            infoList.append(info)
        return infoList

    def calcTestRewardAwards(self, rewardType, rewardItem):
        # 返回 [{'awardId': xxx, 'count': xxx}, ...]
        if rewardType == TEST_REWARD_TYPE_LEVEL_RANK:
            return self.calcLevelRankAwards(int(rewardItem.get('ranking', 0)))
        if rewardType == TEST_REWARD_TYPE_RECHARGE:
            return self.calcRechargeAwards(float(rewardItem.get('rechargeAmount', 0)))
        if rewardType == TEST_REWARD_TYPE_MINE_GUILD:
            return self.calcMineGuildAwards(int(rewardItem.get('guildTitleId', GAAD.datas.leader)))
        if rewardType == TEST_REWARD_TYPE_POWER_RANK:
            return self.calcPowerRankAwards(int(rewardItem.get('ranking', 0)))
        LOG_WARN("ITestReward::calcTestRewardAwards unknown rewardType", rewardType)
        return []

    @staticmethod
    def calcLevelRankAwards(ranking):
        # 一测等级排名: welfare_levelReward 中 type=2, 取满足 ranking<=condition 的最小档
        if ranking <= 0:
            return []
        best = None
        for row in W_LRD.datas.values():
            if row.get('type') != 2:
                continue
            condition = row.get('condition', 0)
            if ranking <= condition and (best is None or condition < best.get('condition', 0)):
                best = row
        if best is None:
            return []
        return [{'awardId': best.get('rewardID', 0), 'count': 1}]

    @staticmethod
    def calcRechargeAwards(rechargeAmount):
        # 二测充值返还: 充值金额按段切分, 每段按各自比例计算(如(1,100)(101,200), 充200则两段各100),
        # 再叠加 welfare_config tierReward 达标奖励
        if rechargeAmount <= 0:
            return []
        gold = 0
        boundGold = 0
        for row in W_RRD.datas.values():
            rechargeRange = row.get('rechargeRange', ())
            if not rechargeRange:
                continue
            low = rechargeRange[0]
            if rechargeAmount < low:
                continue
            high = rechargeRange[1] if len(rechargeRange) > 1 else None
            segAmount = min(rechargeAmount, high) - low + 1 if high is not None else rechargeAmount - low + 1
            if segAmount <= 0:
                continue
            gold += int(segAmount * row.get('goldRate', 0))
            boundGold += int(segAmount * row.get('boundGoldRate', 0))
        awards = []
        if gold > 0:
            awards.append({'awardId': gameconst.ItemIdEnum.MONEY, 'count': gold})
        if boundGold > 0:
            awards.append({'awardId': gameconst.ItemIdEnum.BIND_MONEY, 'count': boundGold})
        for tier in W_CDD.datas.get('tierReward', {}).get('value', ()):
            if len(tier) != 2:
                continue
            condition, rewardId = tier
            if rechargeAmount >= condition:
                awards.append({'awardId': rewardId, 'count': 1})
        return awards

    @staticmethod
    def calcMineGuildAwards(guildJob):
        # 二测矿战: 固定奖励(rewardData 奖励包ID), 排除帮主
        if guildJob in (0, GAAD.datas.leader):
            return []
        rewardId = W_CDD.datas.get('mineBattleReward', {}).get('value', 0)
        if not rewardId:
            LOG_ERR("ITestReward::calcMineGuildAwards config error", rewardId)
            return []
        return [{'awardId': rewardId, 'count': 1}]

    @staticmethod
    def calcPowerRankAwards(ranking):
        # 二测战力排名: welfare_config powerRushReward 按排名区间划分奖励(rewardData 奖励包ID)
        if ranking <= 0:
            return []
        for entry in W_CDD.datas.get('powerRushReward', {}).get('value', ()):
            if len(entry) != 2:
                continue
            rankRange, rewardId = entry
            if len(rankRange) == 2 and rankRange[0] <= ranking <= rankRange[1]:
                return [{'awardId': rewardId, 'count': 1}]
        return []
