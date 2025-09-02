# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import utils


def checkDBProperty():
    disCheckedPropertyList = ['birthInDB']
    if KBEngine.publish() == 0:
        checkedTypeList = []
        for e in KBEngine.entities.values():
            if e.className == 'Avatar' and e.isTutorialAvatar:
                continue

            if e.className not in checkedTypeList:
                checkedTypeList.append(e.className)
                persistProList = KBEngine.getPersistentProperties(e.className)
                persistProList = [persistPro for persistPro in persistProList if
                                  persistPro not in disCheckedPropertyList]
                if len(persistProList) > 0:
                    persistProList = [persistPro for persistPro in persistProList if hasattr(e, persistPro)]

                if len(persistProList) > 0 and not e.databaseID:
                    sendCheckError(persistProList, e.id, e.className)


def sendCheckError(persistProList, id, typename):
    errMsg = "[{}({})] have persistProperty {} but not in database".format(typename, id, str(persistProList))
    ERROR_MSG(errMsg)
