# -*- encoding:utf-8 -*-

import GlyphData


class GlyphDataInfo(object):
    def createObjFromDict(self, dataDict):
        glyphData = GlyphData.GlyphData()
        glyphData.initObjFromSavedDict(dataDict)
        return glyphData

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is GlyphData.GlyphData

glyphInfoInstance = GlyphDataInfo()