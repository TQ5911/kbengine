from KBEDebug import *
import gameconst
import dungeonSrc
import tutorConst_newbieStep as TCNSD


class INewbie(object):
    def _initNewbieCell(self):
        ret = self.popTempMiscProp(gameconst.AvatarProps.newbieCreateCellCB)
        if ret is None:
            return

        DEBUG_MSG('_initNewbieCell:', ret)
        for callback, args in ret:
            getattr(self, callback)(*args)

    def destroyFromNewbieDungeon(self, dungeonNo):
        lockNo = self.getNewbieStepDungeonNo()
        INFO_MSG('destroyFromNewbieDungeon', self.gbId, lockNo, dungeonNo, self.getNewbieStepCell())
        if lockNo and lockNo == dungeonNo:
            self.offline(self.id, gameconst.AVATAR_OFFLINE_REASON_NEWBIE_KICKOUT)
            return

        src = dungeonSrc.BasicDungeonSrc()
        self.doLeaveSingleDungeon(dungeonNo, src, 'dungeon timeout')

    def onNewbieStepModify(self, step):
        self.setTempMiscProp(gameconst.AvatarProps.newbieStepCellCache, step)

    def getNewbieStepCell(self):
        return self.getTempMiscProp(gameconst.AvatarProps.newbieStepCellCache, 0)

    def getNewbieStepDungeonNo(self):
        newbieStep = self.getNewbieStepCell()
        stepData = TCNSD.datas.get(newbieStep)
        if not stepData:
            return

        return stepData['lockDun']

    def newbieAllowLeave(self):
        newbieStep = self.getNewbieStepCell()
        stepData = TCNSD.datas.get(newbieStep)
        if not stepData:
            return True

        if not stepData['lockDun']:
            return True

        return stepData['allowleave']

