# -*- coding: utf-8 -*-
import utils
import character


class CharacterValInfo(object):

    def createObjFromDict(self, dict):
        return character.CharacterVal.fromSavedData(dict)

    def isSameType(self, obj):
        return type(obj) is character.CharacterVal

    def getDictFromObj(self, obj):
        return obj.toSavedData()


class CharactersInfo(object):

    def createObjFromDict(self, dict):
        _chars = character.Characters()
        _chars.isArchiving = dict.get('isArchiving', False)
        _chars.needArchiveAgain = dict.get('needArchiveAgain', False)

        for charInfo in dict['characters']:
            _chars[charInfo.gbId] = charInfo

        return _chars

    def isSameType(self, obj):
        return type(obj) is character.Characters

    def getDictFromObj(self, obj):
        _avals = {'characters': []}
        _avals['isArchiving'] = obj.isArchiving
        _avals['needArchiveAgain'] = obj.needArchiveAgain
        for cVal in obj.values():
            _avals['characters'].append(cVal)

        return _avals


instance = CharactersInfo()
characterValInstance = CharacterValInfo()
