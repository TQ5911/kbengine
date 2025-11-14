# -*- coding: utf-8 -*-

class ActionType(object):
    BASE = 0
    CELL = 1


CommEventActionMap = {
    'Gettask': (ActionType.CELL,
                lambda self, eventActionSrc, *args, **kwargs: self._eventActionGettask(eventActionSrc, *args,
                                                                                       **kwargs)),
    'Fnstalk': (ActionType.BASE,
                lambda self, eventActionSrc, *args, **kwargs: self._eventActionFnstalk(eventActionSrc, *args,
                                                                                       **kwargs)),
    'Fnstask': (ActionType.BASE,
                lambda self, eventActionSrc, *args, **kwargs: self._eventActionFnstask(eventActionSrc, *args,
                                                                                       **kwargs)),
    'Failtask': (ActionType.BASE,
                 lambda self, eventActionSrc, *args, **kwargs: self._eventActionFailtask(eventActionSrc, *args,
                                                                                         **kwargs)),
    'enterSence': (ActionType.CELL, lambda self, eventActionSrc, *args, **kwargs: self.enterLineByNpc(*args, **kwargs)),

    'taskRepeat': (ActionType.BASE,
                   lambda self, eventActionSrc, *args, **kwargs: self._eventActionTaskRepeat(eventActionSrc, *args,
                                                                                             **kwargs)),
    'setVariableNoCharProp': (ActionType.BASE,
                              lambda self, eventActionSrc, *args, **kwargs: self._eventActionSetVariableNoCharProp(
                                  eventActionSrc, *args, **kwargs)),
    'addEquipWashAnima': (ActionType.BASE,
                 lambda self, eventActionSrc, *args, **kwargs: self._eventActionAddEquipWashAnima(eventActionSrc, *args,
                                                                                         **kwargs)),
    'AddSkillUltimatePoint': (ActionType.CELL, lambda self, eventActionSrc, *args, **kwargs: self.addUltraSkillPower(int(args[0]))),

    'temporaryskill' : (ActionType.BASE,
                lambda self, eventActionSrc, *args, **kwargs: self._eventActionTemporarySkill(eventActionSrc, *args,
                                                                                              **kwargs))
}
