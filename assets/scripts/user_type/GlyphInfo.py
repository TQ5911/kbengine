# -*- coding: utf-8 -*-
from KBEDebug import *
import userType
import gameconst
import AffixInfo

class GlyphInfo(userType.UserSingleType):
    def __init__(self, glyphPos = 0):
        self.glyphPos = glyphPos
        self.glyphAffixes = []

    def _lateReload(self):
        super(GlyphInfo, self)._lateReload()
        for v in self.glyphAffixes:
            v.reloadScript()

    def toDBData(self):
        data = []
        data.append(self.glyphPos)
        for glyphAffix in self.glyphAffixes:
            data.append(glyphAffix.toAffixValList())
        return data

    def fromDBData(self, datas):
        self.glyphPos = datas[0]
        if len(datas) == 1:
            return
        datas = datas[1:]
        if not datas:
            return
        for data in datas:
            affixData = AffixInfo.GlyphAffix()
            affixData.fromAffixValList(data)
            self.glyphAffixes.append(affixData)
        
    def toClientData(self):
        return {
            'glyphPos' : self.glyphPos,
            'glyphAffixes' : [glyphAffix.toAfxClientDic() for glyphAffix in self.glyphAffixes]
        }
    
    def updateGlyphAffixes(self, affixes):
        self.glyphAffixes = affixes

    def getGlyphAffixes(self):
        return self.glyphAffixes
    
    def getGlyphPos(self):
        return self.glyphPos