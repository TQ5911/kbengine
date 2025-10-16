# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    # --auto genterate mark--
    pass
def refreshBase():
    import actionContext
    import gameconst
    import iAchievement
    def _checkAchieveDailyRefresh(self, *args):
        DEBUG_MSG('ZTQ takeAchievementRewards:')
        self.achievementInfo.triggerAchieveByType(self, gameconst.AchieveType.LOGIN_DAYS, actionContext.AchievementCtx())
    iAchievement.IAchievement._checkAchieveDailyRefresh = _checkAchieveDailyRefresh
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
