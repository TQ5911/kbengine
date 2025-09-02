# -*- coding: utf-8 -*-
import utils
import character


class CharacterValInfo(object):

    def createObjFromDict(self, dict):
        cVal = character.CharacterVal(dict['gbId'], dict['dbId'], dict['school'], dict['name'],
                                      dict['sex'], dict['level'],
                                      dict.get('birthInDB', 0), dict.get('tLastOnline', 0),
                                      dict.get('charAppearance', None),
                                      )
        return cVal

    def getDictFromObj(self, obj):
        return {'gbId': obj.gbId, 'dbId': obj.dbId, 'name': obj.name, 'school': obj.school,
                'sex': obj.sex, 'level': obj.level, 'birthInDB': obj.birthInDB, 'tLastOnline': obj.tLastOnline,
                'charAppearance': obj.charAppearance}

    def isSameType(self, obj):
        return type(obj) is character.CharacterVal


class CharactersInfo(object):

    def createObjFromDict(self, dict):
        chars = character.Characters()

        for charInfo in dict['characters']:
            chars[charInfo.gbId] = charInfo

        return chars

    def getDictFromObj(self, obj):
        avals = {'characters': []}
        for gbId, cVal in obj.items():
            avals['characters'].append(cVal)

        return avals

    def isSameType(self, obj):
        return type(obj) is character.Characters


instance = CharactersInfo()
characterValInstance = CharacterValInfo()
