# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import sMath

import dataUtils
import gamedecorator
import utils
import gameconst
import CommEventAction
import actionContext
import gameconfig

import Dialog_Dialog as DIALOG_DATA
import gamePlay_gamePlay as GAMEPLAY_DATA
import message_Message_def as MMD
import NPC_NPC as NPC_CONFIG_DATA
import eventAction_Event as EA_ED

class ImpTalk(object):
    def _getTaskCommitCacheKey(self, securityCheckKey):
        return gameconst.SecurityCheckType.TASK_COMMIT_CACHE + str(securityCheckKey)

    def _doTalkToNPC(self, npcEntityID, npcId, taskId, dialogId, idx):
        # npc talk interrupt flag
        isNPCTalkDone = False
        # if the npc talk is not being interrupted, then continue the process
        if not isNPCTalkDone:
            self.doNPCTalk(npcEntityID, npcId, taskId, dialogId, idx)
            LOG_INFO('in _doTalkToNPC, doNPCTalk:', npcEntityID, npcId, taskId, dialogId, idx)

    def makeTalkToNPC(self, npcEntityId, npcId, taskId, dialogId, idx):
        self._doTalkToNPC(npcEntityId, npcId, taskId, dialogId, idx)

    def _checkDialogIdValid(self, npcId, dialogId):
        _commonDialog = NPC_CONFIG_DATA.datas[npcId]['commonDialog']
        return dialogId in DIALOG_DATA.dialogIdMap[_commonDialog]

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def talkToNpc(self, exposed, npcEntityId, taskId, dialogId, idx):
        LOG_INFO('in talkToNpc:', taskId, npcEntityId, dialogId, idx)
        npcId = 0
        if npcEntityId:
            ent = KBEngine.entities.get(npcEntityId)
            if not ent or not ent.IsNpc:
                LOG_WARN('talkToNpc but invalid targetId:', npcEntityId)
                return
            
            if self.spaceNo != ent.spaceNo:
                LOG_WARN('talkToNpc but invalid targetId spaceNo:', npcEntityId)
                return
            
            # 这里判断下和npc的距离，暂定为5把
            if sMath.distance2D(self.position, ent.position) > 5:
                LOG_WARN('talkToNpc but invalid targetId distance:', npcEntityId)
                return

            npcId = ent.npcId

        self.makeTalkToNPC(npcEntityId, npcId, taskId, dialogId, idx)

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def talkToClientNpc(self, exposed, npcId, taskId, dialogId, idx):
        LOG_INFO('in talkToClientNpc:', taskId, npcId, dialogId, idx)
        self.makeTalkToNPC(0, npcId, taskId, dialogId, idx)

    # npc talk
    def doNPCTalk(self, npcEntityId, npcId, taskId, dialogId, idx):
        if taskId > 0:
            taskData = dataUtils.getTaskCfg(taskId)
            if taskData and taskData.get('CheckFollowNPC', False) and taskData.get('TaskFollowNPC', []):
                for followInfo in taskData.get('TaskFollowNPC', []):
                    if followInfo['NpcFollowID'] == npcId:
                        if not self._checkTaskFollowNPC(0, taskId, npcId, dialogId):
                            return

        self._doTaskTalkToNPC(npcEntityId, taskId, npcId, dialogId, idx)

    def _checkDialogEventConfig(self, dialogId, idx):
        dialogData = DIALOG_DATA.datas.get(dialogId, None)
        if dialogData is None:
            return None, None

        event_str = dialogData.get('event')
        event_list = event_str.split('|')

        param_str = dialogData.get('parm')
        param_list = param_str.split('|')
        LOG_INFO('in _checkDialogEventConfig:', event_list, param_list)
        if 0 < len(event_list) < idx:
            LOG_ERR('in _checkDialogEventConfig, event idx error:', idx)
            return None, None

        if 0 < len(param_list) < idx:
            LOG_ERR('in _checkDialogEventConfig, param idx error:', idx)
            return None, None

        eventName = event_list[idx]
        if not eventName:
            LOG_WARN('_checkDialogEventConfig, no eventName, dailog config error:', dialogId)
            return None, None

        return event_list, param_list

    # 检查是否是提交任务
    def _checkGetTaskEvent(self, dialogId, idx):
        event_list, param_list = self._checkDialogEventConfig(dialogId, idx)
        if event_list is None or param_list is None:
            return False
        eventName = event_list[idx]
        # 检查是否是接取任务
        if eventName != "Fnstask":
            return False
        # 检查任务奖励数据
        taskID = param_list[idx]
        if not taskID:
            LOG_WARN('_checkGetTaskEvent, no taskID, dailog config error:', dialogId)
            return False
        return True

    def _checkTaskFollowNPC(self, targetId, taskId, npcId, dialogId):
        talkToNpcData = dataUtils.getTaskCfg(taskId).get('TaskFollowNPC', [])
        for followInfo in talkToNpcData:
            if followInfo['NpcFollowID'] == npcId:
                worldAreaIds = followInfo['WorldAreaID'].split('|')
                if str(self.areaId) in worldAreaIds:
                    # self._doTaskTalkToNPC(targetId, taskId, npcId, dialogId, idx)
                    return True
        LOG_INFO('_checkTaskFollowNPC failed', taskId, npcId, dialogId)
        return False
    
    def _checkEventNpc(self, npcId, eventName):
        _eventData = EA_ED.datas.get(eventName, None)
        if _eventData is None:
            return False
        
        _npcId = _eventData.get('npcId', None)
        if _npcId is None:
            return True
        
        if isinstance(_npcId, int):
            return _npcId == npcId
        
        if isinstance(_npcId, list):
            return npcId in _npcId
        
        return False

    def _doTaskTalkToNPC(self, targetId, taskId, npcId, dialogId, idx):
        event_list, param_list = self._checkDialogEventConfig(dialogId, idx)
        if event_list is None or param_list is None:
            return
        
        eventName = event_list[idx]

        if not self._checkEventNpc(npcId, eventName):
            LOG_ERR('_doTaskTalkToNPC, eventName not match:', eventName, taskId, npcId, dialogId)
            return

        eventArgs, eventKwargs = utils.parseCommEventParams(param_list[idx])
        eventKwargs['_targetId'] = targetId
        eventKwargs['_srcTaskId'] = taskId
        eventKwargs['_npcId'] = npcId
        eventKwargs['_dialogId'] = dialogId

        talkType, actionFunc = CommEventAction.CommEventActionMap[eventName]
        if talkType == CommEventAction.ActionType.CELL:
            actionFunc(self, gameconst.EventActionSrc.SRC_DIALOG, *eventArgs, **eventKwargs)
        else:
            self.base.doBaseCommEvent(gameconst.EventActionSrc.SRC_DIALOG, eventName, eventArgs, eventKwargs)

    def doCellCommEvent(self, eventActionSrc, eventName, eventArgs, eventKwargs):
        actionType, actionFunc = CommEventAction.CommEventActionMap[eventName]
        if actionType != CommEventAction.ActionType.CELL:
            return
        actionFunc(self, eventActionSrc, *eventArgs, **eventKwargs)
        return

    def _eventActionGettask(self, eventActionSrc, *args, **kwargs):
        # claim task
        if len(args) > 0:
            newTaskId = int(args[0])
        else:
            newTaskId = kwargs.get('_srcTaskId')

        self.startClaimTask(newTaskId, taskCtx=actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrcEnum.TASK_SRC_FROM_ACTION))

    def _eventActionAddUltraSkillPower(self, eventActionSrc, *args, **kwargs):
        LOG_INFO('_eventActionAddUltraSkillPower:', eventActionSrc, args, kwargs)

        self.addUltraSkillPower(int(args[0]))
