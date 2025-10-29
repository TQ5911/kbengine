# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    # --auto genterate mark--
    pass
def refreshBase():
    import iCollectible
    def _checkInUnavailableClass(self, info, collectID):
        unavailableClass = info.get('unavailableClass', [])
        school = self.getAvatarSchool()
        if school in unavailableClass:
            WARNING_MSG('in _checkInUnavailableClass, school in unavailableClass:', collectID, school, unavailableClass)
            return True
        return False
    iCollectible.ICollectible._checkInUnavailableClass = _checkInUnavailableClass
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
