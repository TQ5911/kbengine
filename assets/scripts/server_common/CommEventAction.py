# -*- coding: utf-8 -*-

class CommEvEnum(object):
    BASE = 0
    CELL = 1

CommEventActionDic = {
    'Gettask': (CommEvEnum.CELL,
                lambda self, src, *args, **kwargs: self._eventActionGettask(src, *args, **kwargs)),

    'GettaskPopup': (CommEvEnum.CELL,
                    lambda self, src, *args, **kwargs: self._eventActionGettask(src, *args, **kwargs)),
    
    'Fnstalk': (CommEvEnum.BASE,
                lambda self, src, *args, **kwargs: self._eventActionFnstalk(src, *args, **kwargs)),
    
    'Fnstask': (CommEvEnum.BASE,
                lambda self, src, *args, **kwargs: self._eventActionFnstask(src, *args, **kwargs)),

    'Failtask': (CommEvEnum.BASE, 
                 lambda self, src, *args, **kwargs: self._eventActionFailtask(src, *args, **kwargs)),

    'enterSence': (CommEvEnum.CELL, lambda self, src, *args, **kwargs: self.enterLineByNpc(*args, **kwargs)),

    'taskRepeat': (CommEvEnum.BASE,
                   lambda self, src, *args, **kwargs: self._eventActionTaskRepeat(src, *args,
                                                                                             **kwargs)),
    'setVariableNoCharProp': (CommEvEnum.BASE,
                              lambda self, src, *args, **kwargs: self._eventActionSetVariableNoCharProp(
                                  src, *args, **kwargs)),
    'addEquipWashAnima': (CommEvEnum.BASE, 
                          lambda self, src, *args, **kwargs: self._eventActionAddEquipWashAnima(src, *args, 
                                                                                                           **kwargs)),
    'AddSkillUltimatePoint': (CommEvEnum.CELL, 
                              lambda self, src, *args, **kwargs: self._eventActionAddUltraSkillPower(src, *args, 
                                                                                                                **kwargs)),

    'temporaryskill' : (CommEvEnum.BASE, 
                        lambda self, src, *args, **kwargs: self._eventActionTemporarySkill(src, *args, 
                                                                                                      **kwargs)),

    'arenaKing' : (CommEvEnum.CELL, 
                        lambda self, src, *args, **kwargs: self._eventActionInteractArenaKing(*args, **kwargs))

}

