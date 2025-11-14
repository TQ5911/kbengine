# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: NPC/teleporter
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    17100002: _tools.RODict({
        "ID": 17100002,
        "name": "测试场景",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17100101: _tools.RODict({
        "ID": 17100101,
        "name": "同心谷",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17100102: _tools.RODict({
        "ID": 17100102,
        "name": "新元城郊",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17100201: _tools.RODict({
        "ID": 17100201,
        "name": "新元城",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17100202: _tools.RODict({
        "ID": 17100202,
        "name": "月光海港",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17100203: _tools.RODict({
        "ID": 17100203,
        "name": "精灵村外",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17100401: _tools.RODict({
        "ID": 17100401,
        "name": "新元城郊",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17100402: _tools.RODict({
        "ID": 17100402,
        "name": "石窟走廊",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17100501: _tools.RODict({
        "ID": 17100501,
        "name": "同心谷",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17100502: _tools.RODict({
        "ID": 17100502,
        "name": "精灵宝殿",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17100601: _tools.RODict({
        "ID": 17100601,
        "name": "精灵村外",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17101001: _tools.RODict({
        "ID": 17101001,
        "name": "飞沙要塞",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17101002: _tools.RODict({
        "ID": 17101002,
        "name": "五毒石窟",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17101101: _tools.RODict({
        "ID": 17101101,
        "name": "新元城",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17101102: _tools.RODict({
        "ID": 17101102,
        "name": "祖珂地堡",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17101103: _tools.RODict({
        "ID": 17101103,
        "name": "飞沙要塞",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102001: _tools.RODict({
        "ID": 17102001,
        "name": "新元城郊",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102002: _tools.RODict({
        "ID": 17102002,
        "name": "祖珂地堡二层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102101: _tools.RODict({
        "ID": 17102101,
        "name": "祖珂地堡一层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102102: _tools.RODict({
        "ID": 17102102,
        "name": "祖珂地堡五层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102201: _tools.RODict({
        "ID": 17102201,
        "name": "祖珂地堡二层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102202: _tools.RODict({
        "ID": 17102202,
        "name": "祖珂地堡四层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102301: _tools.RODict({
        "ID": 17102301,
        "name": "祖珂地堡三层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102302: _tools.RODict({
        "ID": 17102302,
        "name": "祖珂地堡五层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102401: _tools.RODict({
        "ID": 17102401,
        "name": "祖珂地堡二层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102402: _tools.RODict({
        "ID": 17102402,
        "name": "祖珂地堡七层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102501: _tools.RODict({
        "ID": 17102501,
        "name": "祖珂地堡五层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102502: _tools.RODict({
        "ID": 17102502,
        "name": "祖珂地堡七层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17102601: _tools.RODict({
        "ID": 17102601,
        "name": "祖珂地堡五层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17103001: _tools.RODict({
        "ID": 17103001,
        "name": "同心谷",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17103002: _tools.RODict({
        "ID": 17103002,
        "name": "月光海港二层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17103101: _tools.RODict({
        "ID": 17103101,
        "name": "月光海港一层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17103102: _tools.RODict({
        "ID": 17103102,
        "name": "月光海港四层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17103501: _tools.RODict({
        "ID": 17103501,
        "name": "月光海港二层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17103502: _tools.RODict({
        "ID": 17103502,
        "name": "月光五层北入口",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17103503: _tools.RODict({
        "ID": 17103503,
        "name": "月光五层东入口",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17103601: _tools.RODict({
        "ID": 17103601,
        "name": "月光海港四层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17103602: _tools.RODict({
        "ID": 17103602,
        "name": "月光海港四层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17112001: _tools.RODict({
        "ID": 17112001,
        "name": "石窟走廊",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17112002: _tools.RODict({
        "ID": 17112002,
        "name": "五毒石窟二层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17112101: _tools.RODict({
        "ID": 17112101,
        "name": "五毒石窟一层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17112102: _tools.RODict({
        "ID": 17112102,
        "name": "五毒石窟三层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17112201: _tools.RODict({
        "ID": 17112201,
        "name": "五毒石窟二层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17112202: _tools.RODict({
        "ID": 17112202,
        "name": "五毒石窟四层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17112301: _tools.RODict({
        "ID": 17112301,
        "name": "五毒石窟三层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17112302: _tools.RODict({
        "ID": 17112302,
        "name": "五毒石窟五层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17300001: _tools.RODict({
        "ID": 17300001,
        "name": "回廊一层",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17310101: _tools.RODict({
        "ID": 17310101,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17310201: _tools.RODict({
        "ID": 17310201,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17310301: _tools.RODict({
        "ID": 17310301,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17310401: _tools.RODict({
        "ID": 17310401,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17310501: _tools.RODict({
        "ID": 17310501,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17310601: _tools.RODict({
        "ID": 17310601,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17310701: _tools.RODict({
        "ID": 17310701,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17310801: _tools.RODict({
        "ID": 17310801,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17310901: _tools.RODict({
        "ID": 17310901,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17311001: _tools.RODict({
        "ID": 17311001,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17311101: _tools.RODict({
        "ID": 17311101,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17311201: _tools.RODict({
        "ID": 17311201,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17311301: _tools.RODict({
        "ID": 17311301,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17311401: _tools.RODict({
        "ID": 17311401,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17311501: _tools.RODict({
        "ID": 17311501,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17311601: _tools.RODict({
        "ID": 17311601,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17311701: _tools.RODict({
        "ID": 17311701,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17311801: _tools.RODict({
        "ID": 17311801,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17311901: _tools.RODict({
        "ID": 17311901,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17312001: _tools.RODict({
        "ID": 17312001,
        "name": "混沌之境",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17312101: _tools.RODict({
        "ID": 17312101,
        "name": "",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17600001: _tools.RODict({
        "ID": 17600001,
        "name": "城战（临时）",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17600002: _tools.RODict({
        "ID": 17600002,
        "name": "随机传送点",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17600003: _tools.RODict({
        "ID": 17600003,
        "name": "随机传送点",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    }),
    17600004: _tools.RODict({
        "ID": 17600004,
        "name": "进入战场",
        "isOpen": 1,
        "teleportOffset": 6,
        "Area": 2,
        "wayPointID": 2,
        "activateType": 1,
        "activateParam": 1,
        "showMsg": 0
    })
})
minKey = 17100002
maxKey = 17600004

taskId2teleporterId = _tools.RODict({ 
})


unlockTeleporterId = _tools.RODict({ 
        1:[17100002, 17100101, 17100102, 17100201, 17100202, 17100203, 17100401, 17100402, 17100501, 17100502, 17100601, 17101001, 17101002, 17101101, 17101102, 17101103, 17102001, 17102002, 17102101, 17102102, 17102201, 17102202, 17102301, 17102302, 17102401, 17102402, 17102501, 17102502, 17102601, 17103001, 17103002, 17103101, 17103102, 17103501, 17103502, 17103503, 17103601, 17103602, 17112001, 17112002, 17112101, 17112102, 17112201, 17112202, 17112301, 17112302, 17300001, 17310101, 17310201, 17310301, 17310401, 17310501, 17310601, 17310701, 17310801, 17310901, 17311001, 17311101, 17311201, 17311301, 17311401, 17311501, 17311601, 17311701, 17311801, 17311901, 17312001, 17312101, 17600001, 17600002, 17600003, 17600004, ],
})
