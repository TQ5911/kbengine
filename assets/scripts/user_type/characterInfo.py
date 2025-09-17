# -*- coding: utf-8 -*-
import utils
import character


class CharacterValInfo(object):

    def createObjFromDict(self, dict):
        return character.CharacterVal.fromSavedData(dict)

    def getDictFromObj(self, obj):
        return obj.toSavedData()

    def isSameType(self, obj):
        return type(obj) is character.CharacterVal


class CharactersInfo(object):

    def createObjFromDict(self, dict):
        chars = character.Characters()
        chars.isArchiving = dict.get('isArchiving', False)
        chars.needArchiveAgain = dict.get('needArchiveAgain', False)

        for charInfo in dict['characters']:
            chars[charInfo.gbId] = charInfo

        return chars

    def getDictFromObj(self, obj):
        avals = {'characters': []}
        avals['isArchiving'] = obj.isArchiving
        avals['needArchiveAgain'] = obj.needArchiveAgain
        for gbId, cVal in obj.items():
            avals['characters'].append(cVal)

        return avals

    def isSameType(self, obj):
        return type(obj) is character.Characters


instance = CharactersInfo()
characterValInstance = CharacterValInfo()
