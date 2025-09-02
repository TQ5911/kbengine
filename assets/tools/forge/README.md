# FORGE

## 输入命令

```
bash forge.sh user_type GuildMember
```

将会生成一个文件

```
# coding: utf-8

import userType


class GuildMemberVal(userType.UserSoleType):
    def __init__(self):
        pass

    def toGuildMemberSavedDict(self):
        return {
        }


class GuildMemberInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildMemberVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildMemberSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildMemberVal


GuildMemberInstance = GuildMemberInfo()

```

并在types.xml中生成

```

    <GUILD_MEMBER_DATA_INFO> FIXED_DICT
        <implementedBy>     GuildMemberInfo.GuildMemberInstance    </implementedBy>
        <Properties>
            <gbId>
                <Type>  PLAYER_GBID     </Type>
            </gbId>
        </Properties>
    </GUILD_MEMBER_DATA_INFO>

```

