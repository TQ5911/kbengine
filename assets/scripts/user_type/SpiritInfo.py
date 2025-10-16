# -*- coding: utf-8 -*-
from KBEDebug import *
import userType
import gameconst
import AffixInfo

class SpiritInfo(userType.UserSoleType):
    def __init__(self):
        self.spiritAffixes = []

    def _lateReload(self):
        super(SpiritInfo, self)._lateReload()
        for v in self.spiritAffixes:
            v.reloadScript()

    def toDBData(self):
        data = []
        for spiritAffix in self.spiritAffixes:
            data.append(spiritAffix.toAffixValList())
        return data

    def fromDBData(self, datas):
        for data in datas:
            affixData = AffixInfo.Affix()
            affixData.fromAffixValList(data)
            self.spiritAffixes.append(affixData)
        
    def toClientData(self):
        return {
            'spiritAffixes' : [spiritAffix.toAfxClientDic() for spiritAffix in self.spiritAffixes]
        }
    
    def UpdateSpiritAffixes(self, affixes):
        self.spiritAffixes = affixes

    def GetSpiritAffixes(self):
        return self.spiritAffixes