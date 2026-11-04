# coding: utf-8
from KBEDebug import *
import KBEngine
import gamedecorator
import dropAward
import gameclass
import gameconst
import utils
import LogTrackingMgr
import mailAssistor
import battlePassUtils as BPU
import battlePass_battlePass as BP_BPD
import battlePass_config as BP_CFG
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD


class IBattlePass(object):
    def __init__(self):
        LOG_INFO('IBattlePass::__init__', self.gbID)

    def battlePassOnLogin(self):
        self._checkBattlePassNotice()
        self._settleBattlePass()
        for gid, _ in BPU.iterActive():
            self._ensurePassInfo(gid)
        self.refreshBattlePassPrivileges()
        self.sendBattlePassInfo()
        self.sendBattlePassTasks()
        self.sendBattlePassClaimed()

    def onBattlePassDailyUpdate(self, *args):
        self._checkBattlePassNotice()
        settled = self._settleBattlePass()
        self.refreshBattlePassPrivileges()
        self._resetTasks(BPU.RESET_DAILY)
        if settled:
            self.sendBattlePassInfo()
            self.sendBattlePassTasks()
            self.sendBattlePassClaimed()

    def _checkBattlePassNotice(self):
        for gid, cfg in BPU.iterActive():
            if not BPU.inNoticeWindow(cfg):
                continue
            info = self._ensurePassInfo(gid)
            if info.get('noticeSent'):
                continue
            mailId = int(cfg.get('settleNoticeMailID') or 0)
            if mailId <= 0:
                continue
            mailAssistor.sendMailToPlayers(
                [self.gbID], mailId, despArgs=(BPU.groupName(cfg), BPU.endTimeText(cfg)))
            info['noticeSent'] = 1
            LOG_INFO('battlePass notice', self.gbID, gid, mailId)

    def _settleBattlePass(self):
        now = utils.curTS()
        mailId = BP_CFG.datas['settleMailID']['value']
        maxDays = BP_CFG.datas['offlineSettleMaxDays']['value']
        n = 0
        for gid, info in list(self.battlePassInfos.items()):
            cfg = BPU.getCfg(gid)
            if not cfg or info.get('settled'):
                continue
            _, endTs = BPU.periodRange(cfg)
            if endTs <= 0 or now <= endTs:
                continue
            gid = cfg.get('GroupID')
            if now - endTs <= maxDays * 86400:
                attach = self._settleAwards(gid, cfg, info)
                if attach and mailId:
                    mailAssistor.sendMailToPlayers(
                        [self.gbID], mailId, extraAttach=attach, despArgs=(),
                        opUUID=KBEngine.genUUID64(), srcType=AAC_AACDD.datas.BONUS_SRC_BATTLEPASS_LEVEL_REWARD)
            info['lv'] = info['exp'] = info['weekExp'] = 0
            info['tasks'], info['passIds'], info['claimed'] = {}, [], {}
            info['settled'] = 1
            n += 1
            LOG_INFO('battlePass settle', self.gbID, gid)
        return n

    def _claimableAwards(self, groupId, cfg, info, uptoLv=0):
        awardVal = dropAward.AwardVal()
        marks = []
        lv = int(info.get('lv', 0))
        if uptoLv > 0:
            lv = min(lv, int(uptoLv))
        if lv <= 0:
            return awardVal, marks
        claimed = info.get('claimed') or {}
        for pid in self._unlockedPassIds(groupId, info):
            rgroup = (BP_BPD.datas.get(pid) or {}).get('rewardGroupID')
            got = claimed.get(pid) or claimed.get(str(pid)) or ()
            for n in range(1, lv + 1):
                if n in got:
                    continue
                rid = BPU.rewardId(rgroup, BPU.rewardRow(cfg, n))
                if not rid:
                    continue
                awardVal += dropAward.getAwardOne(rid, self.getAvatarAwardCtx(rid, None))
                marks.append((pid, n))
        return awardVal, marks

    def _settleAwards(self, groupId, cfg, info):
        awardVal, _ = self._claimableAwards(groupId, cfg, info)
        if awardVal.isEmpty():
            return None
        mailVal = dropAward.MailAttachVal()
        mailVal += awardVal
        return mailVal

    def onBattlePassWeeklyUpdate(self, *args):
        for info in self.battlePassInfos.values():
            info['weekExp'] = 0
        self.refreshBattlePassPrivileges()
        self._resetTasks(BPU.RESET_WEEKLY)
        self.sendBattlePassInfo()

    def _getPassInfo(self, groupId):
        infos = self.battlePassInfos
        return infos.get(groupId) or infos.get(str(groupId))

    def _ensurePassInfo(self, groupId):
        info = self._getPassInfo(groupId)
        if info is None:
            info = {'lv': 0, 'exp': 0, 'weekExp': 0, 'tasks': {}, 'passIds': [], 'bagApplied': 0, 'claimed': {}, 'settled': 0}
            self.battlePassInfos[groupId] = info
            return info
        info['lv'] = int(info.get('lv', 0))
        info['exp'] = int(info.get('exp', 0))
        info['weekExp'] = int(info.get('weekExp', 0))
        if 'tasks' not in info:
            info['tasks'] = {}
        if 'passIds' not in info:
            info['passIds'] = []
        if 'bagApplied' not in info:
            info['bagApplied'] = 0
        if 'claimed' not in info:
            info['claimed'] = {}
        if 'settled' not in info:
            info['settled'] = 0
        return info

    def _taskProgress(self, tasks, taskId):
        return int(tasks.get(taskId) or tasks.get(str(taskId)) or 0)

    def getBattlePassLevel(self, groupId):
        info = self._getPassInfo(groupId)
        return int(info.get('lv', 0)) if info else 0

    def addBattlePassExp(self, groupId, exp, ignoreLimit=False, useCatchup=False):
        exp = int(exp)
        if exp <= 0:
            return 0
        cfg = BPU.getCfg(groupId)
        if not cfg or (not ignoreLimit and not BPU.isActive(cfg)):
            LOG_WARN('addBattlePassExp invalid', self.gbID, groupId, exp)
            return 0
        info = self._ensurePassInfo(groupId)
        addExp = exp
        if not ignoreLimit:
            limit = int(cfg.get('weekExpLimit') or 0)
            if limit > 0:
                room = max(0, limit - int(info.get('weekExp', 0)))
                addExp = min(addExp, room)
                if addExp <= 0:
                    return 0
                info['weekExp'] = int(info.get('weekExp', 0)) + addExp
        gained = BPU.applyCatchupExp(cfg, addExp) if useCatchup else addExp
        oldLv = int(info.get('lv', 0))
        info['exp'] = int(info.get('exp', 0)) + gained
        loopCnt = 0
        while True:
            loopCnt += 1
            if loopCnt > 100:
                LOG_ERR('addBattlePassExp loop limit', self.gbID, groupId, info['lv'], info['exp'])
                break
            need = BPU.needExp(cfg, info['lv'])
            if need <= 0 or info['exp'] < need:
                break
            info['exp'] -= need
            info['lv'] += 1
        if info['lv'] != oldLv:
            self._logBattlePassLevelUp(groupId, oldLv, info['lv'], '1')
        LOG_INFO('addBattlePassExp', self.gbID, groupId, addExp, gained, oldLv, info['lv'], info['exp'], useCatchup)
        self.sendBattlePassInfo()
        return gained

    def addBattlePassTaskExp(self, groupId, exp):
        return self.addBattlePassExp(groupId, exp, False, True)

    def gmAddBattlePassExp(self, groupId, exp):
        return self.addBattlePassExp(groupId, exp, True)

    def gmBattlePassCatchup(self, groupId):
        cfg = BPU.getCfg(groupId)
        if not cfg:
            return 'invalid groupId %s' % groupId
        r = BPU.catchupDays(cfg)
        tenths = BPU.catchupMulTenths(cfg)
        return 'groupId=%s enabled=%s designDays=%s R=%s M=%s' % (
            groupId, cfg.get('catchupEnabled'), cfg.get('designTaskDays'), r, tenths / 10.0)

    def buyBattlePassLv(self, groupId, buyCnt, isExchange=False):
        buyCnt = int(buyCnt)
        cfg = BPU.getCfg(groupId)
        if not cfg or not BPU.isActive(cfg) or buyCnt <= 0:
            LOG_WARN('buyBattlePassLv invalid', self.gbID, groupId, buyCnt)
            return False
        info = self._ensurePassInfo(groupId)
        lv = int(info.get('lv', 0))
        maxLv = int(cfg.get('maxLevel') or 0)
        if maxLv <= 0 or lv >= maxLv:
            LOG_WARN('buyBattlePassLv max', self.gbID, groupId, lv, maxLv)
            return False
        buyCnt = min(buyCnt, maxLv - lv)
        deductWealthVal = dropAward.DeductWealthVal()
        for i in range(buyCnt):
            itemId, price = BPU.buyLvCost(cfg, lv + i)
            if itemId <= 0 or price <= 0:
                LOG_WARN('buyBattlePassLv no price', self.gbID, groupId, lv + i)
                return False
            deductWealthVal.addWealthByItemId(itemId, price)
        res = self.canDeductWealth(deductWealthVal, sendMsg=True, allowMoneyCoverBindMoney=isExchange)
        if not res:
            LOG_WARN('buyBattlePassLv wealth', self.gbID, groupId, buyCnt, res())
            return False
        self.deductWealth(AAC_AACDD.datas.BONUS_SRC_BATTLEPASS_BUY_LEVEL_COST, deductWealthVal, KBEngine.genUUID64(), gameclass.AwardDetailCls(), allowMoneyCoverBindMoney=isExchange)
        info['lv'] = lv + buyCnt
        self._logBattlePassLevelUp(groupId, lv, info['lv'], '2')
        LOG_INFO('buyBattlePassLv', self.gbID, groupId, buyCnt, lv, info['lv'], info.get('exp', 0))
        self.sendBattlePassInfo()
        return True

    def claimBattlePassReward(self, groupId, lv):
        cfg = BPU.getCfg(groupId)
        if not cfg or not BPU.isActive(cfg) or lv <= 0:
            LOG_WARN('claimBattlePassReward invalid', self.gbID, groupId, lv)
            return False
        info = self._ensurePassInfo(groupId)
        awardVal, marks = self._claimableAwards(groupId, cfg, info, lv)
        if not marks or awardVal.isEmpty():
            LOG_WARN('claimBattlePassReward empty', self.gbID, groupId, lv)
            return False
        srcType = AAC_AACDD.datas.BONUS_SRC_BATTLEPASS_LEVEL_REWARD
        if not self.canAddWealthVal(srcType, awardVal, bMsg=True):
            LOG_WARN('claimBattlePassReward bag', self.gbID, groupId, lv)
            return False
        claimed = info.setdefault('claimed', {})
        for pid, n in marks:
            claimed.pop(str(pid), None)
            got = list(claimed.get(pid) or ())
            if n not in got:
                got.append(n)
            claimed[pid] = got
        opUUID = KBEngine.genUUID64()
        self.addWealth(srcType, awardVal, opUUID, gameclass.AwardDetailCls(), self.getAvatarAwardCtx(0, None))
        self._logBattlePassReward(groupId, opUUID)
        LOG_INFO('claimBattlePassReward', self.gbID, groupId, lv, info.get('lv', 0), len(marks))
        self.sendBattlePassClaimed()
        return True

    @gamedecorator.limitcall(1)
    def reqBattlePassInfo(self, exposed):
        self.refreshBattlePassPrivileges()
        self.sendBattlePassInfo()
        self.sendBattlePassTasks()
        self.sendBattlePassClaimed()

    @gamedecorator.limitcall(1)
    def reqBuyBattlePassLv(self, exposed, groupId, buyCnt, isExchange=False):
        self.buyBattlePassLv(groupId, buyCnt, isExchange=isExchange)

    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('battlePass')
    def reqClaimBattlePassReward(self, exposed, groupId, lv):
        self.claimBattlePassReward(groupId, lv)

    def sendBattlePassInfo(self):
        if not self.client:
            return
        gids, lvs, exps, weekExps, needExps, catchupMuls, passIds = [], [], [], [], [], [], []
        for gid, cfg in BPU.iterActive():
            info = self._ensurePassInfo(gid)
            lv = int(info.get('lv', 0))
            gids.append(int(gid))
            lvs.append(lv)
            exps.append(int(info.get('exp', 0)))
            weekExps.append(int(info.get('weekExp', 0)))
            needExps.append(BPU.needExp(cfg, lv))
            catchupMuls.append(BPU.catchupMulTenths(cfg))
            passIds.extend(self._unlockedPassIds(gid, info))
        self.client.onBattlePassInfo(
            gids, lvs, exps, weekExps, needExps, catchupMuls, passIds,
            self.getBattlePassStallSlots(), self.getBattlePassBagApplied())

    def sendBattlePassTasks(self, pairs=None):
        if not self.client:
            return
        gids, tids, ps = [], [], []
        if pairs is None:
            for gid, _ in BPU.iterActive():
                tasks = self._ensurePassInfo(gid).get('tasks', {})
                for taskId, _ in BPU.iterTasks(gid):
                    gids.append(int(gid))
                    tids.append(int(taskId))
                    ps.append(self._taskProgress(tasks, taskId))
        else:
            for gid, taskId, progress in pairs:
                gids.append(int(gid))
                tids.append(int(taskId))
                ps.append(int(progress))
        if gids:
            self.client.onBattlePassTaskInfo(gids, tids, ps)

    def sendBattlePassClaimed(self):
        if not self.client:
            return
        pids, lvs = [], []
        for gid, _ in BPU.iterActive():
            claimed = self._ensurePassInfo(gid).get('claimed') or {}
            for pid, got in claimed.items():
                for n in got or ():
                    pids.append(int(pid))
                    lvs.append(int(n))
        if pids:
            self.client.onBattlePassClaimed(pids, lvs)

    def _resetTasks(self, resetType):
        changed = []
        for gid, _ in BPU.iterActive():
            tasks = self._ensurePassInfo(gid).setdefault('tasks', {})
            for taskId, tcfg in BPU.iterTasks(gid):
                if int(tcfg.get('resetType') or 0) != resetType:
                    continue
                if self._taskProgress(tasks, taskId) <= 0:
                    continue
                tasks.pop(str(taskId), None)
                tasks[taskId] = 0
                changed.append((gid, taskId, 0))
        if changed:
            LOG_INFO('resetBattlePassTask', self.gbID, resetType, len(changed))
            self.sendBattlePassTasks(changed)

    def onBattlePassTicketUse(self, activityId, num=1):
        # 任务35只在门票次数实际减少时计，跨服镜像回写本服，不推客户端
        num = int(num or 0)
        activityId = int(activityId or 0)
        if num <= 0 or activityId <= 0:
            return
        if self.isCrossServerInOtherServer:
            self.syncMethodCallToLocalServerBase('onBattlePassTicketUse', (activityId, num))
            return
        self.onBattlePassTask(BPU.TASK_TICKET, num, activityId, 0)

    def onBattlePassTask(self, taskType, num=1, key=0, src=0):
        num = int(num)
        if num <= 0 or not BPU.hasTaskType(taskType):
            return
        # 跨服击杀记在镜像上不落库，回写本服
        if taskType == BPU.TASK_KILL and self.isCrossServerInOtherServer:
            self.syncMethodCallToLocalServerBase('onBattlePassTask', (taskType, num, key, src))
            return
        changed, expAdd = [], {}
        for gid, _ in BPU.iterActive():
            tasks = self._ensurePassInfo(gid).setdefault('tasks', {})
            for taskId, tcfg in BPU.iterTasks(gid, taskType, key):
                if not BPU.matchTask(tcfg, key, src):
                    continue
                target = int(tcfg.get('target') or 0)
                if target <= 0:
                    continue
                old = self._taskProgress(tasks, taskId)
                if old >= target:
                    continue
                new = old + num
                if new > target:
                    new = target
                tasks.pop(str(taskId), None)
                tasks[taskId] = new
                changed.append((gid, taskId, new))
                if old < target <= new:
                    expReward = int(tcfg.get('expReward') or 0)
                    expAdd[gid] = expAdd.get(gid, 0) + expReward
                    self._logBattlePassTaskFinish(gid, taskId, tcfg.get('resetType'), expReward)
        if not changed:
            return
        LOG_INFO('onBattlePassTask', self.gbID, taskType, num, key, src, changed)
        for gid, exp in expAdd.items():
            if exp > 0:
                self.addBattlePassTaskExp(gid, exp)
        self.sendBattlePassTasks(changed)

    def onBattlePassGain(self, srcType, awardVal):
        if not awardVal or not BPU.hasTaskType(BPU.TASK_ITEM):
            return
        srcType = int(srcType or 0)
        for it in awardVal.toBriefList():
            itemId = int(it.get('itemId') or 0)
            n = int(it.get('itemNum') or 0)
            if itemId and n > 0:
                self.onBattlePassTask(BPU.TASK_ITEM, n, itemId, srcType)

    def gmResetBattlePassTask(self, resetType=0):
        resetType = int(resetType or 0)
        if resetType:
            self._resetTasks(resetType)
            return 'reset %s' % resetType
        for rt in (BPU.RESET_DAILY, BPU.RESET_WEEKLY, BPU.RESET_SEASON):
            self._resetTasks(rt)
        return 'reset all'

    def _privOf(self, groupId, idx):
        info = self._getPassInfo(groupId)
        if not info:
            return 0
        n = 0
        for pid in info.get('passIds', []):
            n += BPU.privilege(pid)[idx]
        return n

    def getBattlePassStallSlots(self):
        n = 0
        for gid, _ in BPU.iterActive():
            n += self._privOf(gid, BPU.PRIV_STALL)
        return n

    def getBattlePassBagSlots(self):
        n = 0
        for gid, _ in BPU.iterActive():
            n += self._privOf(gid, BPU.PRIV_BAG)
        return n

    def getBattlePassBagApplied(self):
        n = 0
        for info in self.battlePassInfos.values():
            n += info.get('bagApplied', 0)
        return n

    def refreshBattlePassPrivileges(self):
        self.coinAuctionInfo._privilegeGrids = self.getBattlePassStallSlots()
        self.syncBattlePassBagSlots()

    def tryLockExpiredBattlePassBag(self):
        if self.getBattlePassBagApplied() <= self.getBattlePassBagSlots():
            return
        old = self.getBattlePassBagApplied()
        self.syncBattlePassBagSlots()
        if self.getBattlePassBagApplied() != old:
            self.sendBattlePassInfo()

    def syncBattlePassBagSlots(self):
        bag = self.bagData
        oldCap = bag.capacity
        # bpExtraGrids 不落库，重登后是 0；已写入 capacity 的格数以 bagApplied 为准，避免每次上线再加一遍
        applied = self.getBattlePassBagApplied()
        if bag.bpExtraGrids != applied:
            LOG_INFO('battlePass bagExtra recover', self.gbID, bag.bpExtraGrids, applied, bag.capacity)
            bag.bpExtraGrids = applied
        oldExtra = bag.bpExtraGrids
        for gid, _ in BPU.iterActive():
            info = self._ensurePassInfo(gid)
            target = self._privOf(gid, BPU.PRIV_BAG)
            cur = info.get('bagApplied', 0)
            if target > cur:
                info['bagApplied'] = target
        pending, need = [], 0
        for gid, info in self.battlePassInfos.items():
            cfg = BPU.getCfg(gid)
            target = self._privOf(gid, BPU.PRIV_BAG) if cfg and BPU.isActive(cfg) else 0
            cur = info.get('bagApplied', 0)
            if cur > target:
                pending.append((info, cur - target))
                need += cur - target
        if need > 0:
            used = bag.gridIdToGridObj
            trailing = bag.capacity if not used else max(0, bag.capacity - (max(used) + 1))
            can = min(need, trailing, oldExtra)
            if can > 0:
                for info, n in pending:
                    if can <= 0:
                        break
                    sub = min(n, can)
                    info['bagApplied'] = info.get('bagApplied', 0) - sub
                    can -= sub
        extra = self.getBattlePassBagApplied()
        bag.capacity += extra - oldExtra
        bag.bpExtraGrids = extra
        if bag.capacity != oldCap:
            LOG_INFO('battlePass bagCapacity', self.gbID, oldCap, bag.capacity, extra)
            if self.client:
                self.client.onUnlockGrids(gameconst.BagOPStat.OPERATE_BAG_STAT_OK, bag.capacity)
            if self.isCrossServerInLocalServer and self.otherServerAvatarBox:
                self.syncMethodCallToCrossServerBase('onLocalServerBattlePassBagExtra', (extra, bag.capacity))

    def onLocalServerBattlePassBagExtra(self, extra, capacity):
        self.bagData.bpExtraGrids = extra
        self.bagData.capacity = capacity
        if self.client:
            self.client.onUnlockGrids(gameconst.BagOPStat.OPERATE_BAG_STAT_OK, capacity)

    def _unlockedPassIds(self, groupId, info):
        owned = info.get('passIds', [])
        ids = []
        for pid, _ in BPU.iterPasses(groupId):
            if BPU.isFreePass(pid) or pid in owned:
                ids.append(pid)
        return ids

    def _grantBattlePassActivateReward(self, passId, opUUID):
        rewardId = BPU.activateRewardId(passId)
        if rewardId <= 0:
            LOG_INFO('activateBattlePass no reward cfg', self.gbID, passId)
            return
        detail = gameclass.AwardDetailCls()
        srcType = AAC_AACDD.datas.BONUS_SRC_BATTLEPASS_ACTIVATE_REWARD
        awardVal = dropAward.AwardVal()
        ctx = self.getAvatarAwardCtx(rewardId, None)
        awardVal += dropAward.getAwardOne(rewardId, ctx)
        if awardVal.isEmpty():
            LOG_INFO('activateBattlePass empty reward', self.gbID, passId, rewardId)
            return
        awardCtx = self.getAvatarAwardCtx(0, None)
        self.addWealth(srcType, awardVal, opUUID, detail, awardCtx)

    def activateBattlePass(self, passId, opUUID=None):
        pcfg = BP_BPD.datas.get(passId)
        if not pcfg or not BPU.isPaidPass(passId):
            LOG_WARN('activateBattlePass invalid', self.gbID, passId)
            return False
        groupId = pcfg.get('passGroupID')
        gcfg = BPU.getCfg(groupId)
        if not gcfg or not BPU.isActive(gcfg):
            LOG_WARN('activateBattlePass inactive', self.gbID, passId, groupId)
            return False
        info = self._ensurePassInfo(groupId)
        if passId in info.get('passIds', []):
            LOG_WARN('activateBattlePass already', self.gbID, passId)
            return False
        info.setdefault('passIds', []).append(passId)
        addLv = BPU.privilege(passId)[BPU.PRIV_LV]
        if addLv > 0:
            lv = info.get('lv', 0) + addLv
            maxLv = gcfg.get('maxLevel') or 0
            info['lv'] = min(lv, maxLv) if maxLv > 0 else lv
        self.refreshBattlePassPrivileges()
        opUUID = opUUID or KBEngine.genUUID64()
        self.unlockBag(gameconst.BagTypeEnum.BAG_TYPE_NORMAL, 'unlock by action: activateBattlePass')
        self._grantBattlePassActivateReward(passId, opUUID)
        self._logBattlePassActivate(groupId, passId)
        LOG_INFO('activateBattlePass', self.gbID, groupId, passId, info.get('lv', 0))
        self.sendBattlePassInfo()
        return True

    def addBattlePassByItem(self, passId, itemId, useNum, opUUID, ctx):
        passId = passId or BPU.getPassIdByActivateItem(itemId)
        if not passId or useNum <= 0:
            return False
        ok = self.activateBattlePass(passId, opUUID)
        if ctx is not None:
            ctx.usedCount = 1 if ok else 0
            if (not ctx.fromOrder) and ctx.pendingOpId and self.cell:
                self.cell.onPendingUseItemFinished(ctx.pendingOpId, gameconst.UseItemEnum.TRUE)
        return ok

    def _bpDistinctId(self):
        account = self.accountEntity
        return account.clientDistinctId if account else ''

    def _logBattlePassTaskFinish(self, groupId, taskId, resetType, expReward):
        LogTrackingMgr.LogTrackingMgr.battle_pass_task_finish(
            self.gbID, self._bpDistinctId(), int(groupId), int(taskId),
            int(resetType or 0), int(expReward or 0))

    def _logBattlePassLevelUp(self, groupId, levelBefore, newLevel, upgradeType):
        if int(newLevel) == int(levelBefore):
            return
        LogTrackingMgr.LogTrackingMgr.battle_pass_level_up(
            self.gbID, self._bpDistinctId(), int(groupId), int(newLevel),
            int(levelBefore), upgradeType)

    def _logBattlePassReward(self, groupId, opUUID):
        LogTrackingMgr.LogTrackingMgr.battle_pass_reward(
            self.gbID, self._bpDistinctId(), int(groupId), opUUID)

    def _logBattlePassActivate(self, groupId, passId):
        LogTrackingMgr.LogTrackingMgr.battle_pass_activate(
            self.gbID, self._bpDistinctId(), int(groupId), int(passId), utils.getNowTimeStr())

    def gmActivateBattlePass(self, passId):
        ok = self.activateBattlePass(passId)
        return 'ok' if ok else 'fail'

    def deactivateBattlePass(self, passId):
        pcfg = BP_BPD.datas.get(passId)
        if not pcfg or not BPU.isPaidPass(passId):
            LOG_WARN('deactivateBattlePass invalid', self.gbID, passId)
            return False
        groupId = pcfg.get('passGroupID')
        info = self._getPassInfo(groupId)
        owned = info.get('passIds', []) if info else []
        if passId not in owned:
            LOG_WARN('deactivateBattlePass not owned', self.gbID, passId, groupId)
            return False
        owned.remove(passId)
        self.refreshBattlePassPrivileges()
        self.unlockBag(gameconst.BagTypeEnum.BAG_TYPE_NORMAL, 'unlock by action: deactivateBattlePass')
        LOG_INFO('deactivateBattlePass', self.gbID, groupId, passId, info.get('lv', 0), info.get('bagApplied', 0))
        self.sendBattlePassInfo()
        return True

    @gamedecorator.offlineCallback
    def gmDeactivateBattlePass(self, passId):
        if passId:
            ok = self.deactivateBattlePass(passId)
            return 'ok' if ok else 'fail'
        n = 0
        for info in list(self.battlePassInfos.values()):
            for pid in list(info.get('passIds', [])):
                if self.deactivateBattlePass(pid):
                    n += 1
        return 'ok %s' % n
