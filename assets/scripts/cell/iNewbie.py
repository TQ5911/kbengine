from KBEDebug import *
import gameconst
import dungeonSrc
import tutorConst_newbieStep as TCNSD


class INewbie(object):
    def _initNewbieCell(self):
        ret = self.popTempMiscProp(gameconst.EntityPropsEnum.newbieCreateCellCB)
        if ret is None:
            return

        LOG_DBG('_initNewbieCell:', ret)
        for callback, args in ret:
            getattr(self, callback)(*args)

    def destroyFromNewbieDungeon(self, dungeonNo):
        lockNo = self.getNewbieStepDungeonNo()
        LOG_INFO('destroyFromNewbieDungeon', self.gbId, lockNo, dungeonNo, self.getNewbieStepCell())
        if lockNo:
            self.offline(self.id, gameconst.OFFLINE_REASON_NEWBIE_KICKOUT)
            return

        src = dungeonSrc.BasicDungeonSrc()
        self.doLeaveSingleDungeon(dungeonNo, src, 'dungeon timeout')

    def onNewbieStepModify(self, step):
        self.setTempMiscProp(gameconst.EntityPropsEnum.newbieStepCellCache, step)

    def getNewbieStepCell(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.newbieStepCellCache, 0)

    def getNewbieStepDungeonNo(self):
        _newbieStep = self.getNewbieStepCell()
        _stepData = TCNSD.datas.get(_newbieStep)
        if not _stepData:
            return

        return _stepData['lockDun']

    def newbieAllowLeave(self):
        newbieStep = self.getNewbieStepCell()
        stepData = TCNSD.datas.get(newbieStep)
        if not stepData:
            return True

        if not stepData['lockDun']:
            return True

        return stepData['allowleave']

