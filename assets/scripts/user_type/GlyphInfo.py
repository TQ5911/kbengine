# -*- coding: utf-8 -*-
from KBEDebug import *
import userType
import gameconst
import AffixInfo

class GlyphInfo(userType.UserSoleType):
    def __init__(self, state = gameconst.GlyphState.LOCKED):
        self.glyphState = state
        self.glyphAffixes = []

    def _lateReload(self):
        super(GlyphInfo, self)._lateReload()
        for v in self.glyphAffixes:
            v.reloadScript()

    def toDBData(self):
        data = []
        data.append(self.glyphState)
        for glyphAffix in self.glyphAffixes:
            data.append(glyphAffix.toAffixValList())
        return data

    def fromDBData(self, datas):
        self.glyphState = datas[0]
        datas = datas[1:]
        for data in datas:
            affixData = AffixInfo.GlyphAffix()
            affixData.fromAffixValList(data)
            self.glyphAffixes.append(affixData)
        
    def toClientData(self):
        return {
            'glyphState' : self.glyphState,
            'glyphAffixes' : [glyphAffix.toAfxClientDic() for glyphAffix in self.glyphAffixes]
        }
    
    def CheckGlyphState(self, state):
        return state == self.glyphState
    
    def UpdateGlyphAffixes(self, affixes):
        self.glyphAffixes = affixes
        self.glyphState = gameconst.GlyphState.MADE

    def GetGlyphAffixes(self):
        return self.glyphAffixes