#coding:utf-8
from KBEDebug import *



class IEventBase(object):
    def createTempEvent(self, eventKey):
        if self.getTempMiscProp(eventKey):
            LOG_ERR("IEventBase::createTempEvent tempMiscProp is not empty", _eventKey)
            return

        self.setTempMiscProp(eventKey, [])

    def registerTempEvent(self, eventKey, func, args):
        _eventList = self.getTempMiscProp(eventKey, None)
        if _eventList is None:
            LOG_ERR("IEventBase::registerTempEvent tempMiscProp is None", eventKey, func)
            return

        _eventList.append((func, args))

    def triggerTempEvent(self, eventKey):
        _eventList = self.popTempMiscProp(eventKey, [])
        for _func, _args in _eventList:
            getattr(self, _func)(*_args)


