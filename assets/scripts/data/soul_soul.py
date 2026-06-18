# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: soul/soul
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    30770101: _tools.RODict({
        "ID": 30770101,
        "equipmentID": 2,
        "propertyNum": ((0, 9867), (1, 100), (2, 33)),
        "baseProp": ((78004001, 15), (78004002, 20), (78004003, 15), (78004004, 20)),
        "rareProp": ((78004005, 15), (78004006, 15)),
        "qualityWeight": ((1, 8000), (2, 1700), (3, 300)),
        "LuckyWeight": None
    }),
    30770102: _tools.RODict({
        "ID": 30770102,
        "equipmentID": 1,
        "propertyNum": ((0, 9867), (1, 100), (2, 33)),
        "baseProp": ((78004007, 30), (78004008, 40), (78004009, 30), (78004010, 40)),
        "rareProp": ((78004011, 15), (78004012, 15)),
        "qualityWeight": ((1, 8000), (2, 1700), (3, 300)),
        "LuckyWeight": None
    }),
    30770103: _tools.RODict({
        "ID": 30770103,
        "equipmentID": 8,
        "propertyNum": ((0, 9867), (1, 100), (2, 33)),
        "baseProp": ((78004013, 15), (78004014, 20), (78004015, 15), (78004016, 20)),
        "rareProp": ((78004017, 30),),
        "qualityWeight": ((1, 8000), (2, 1700), (3, 300)),
        "LuckyWeight": None
    }),
    30770104: _tools.RODict({
        "ID": 30770104,
        "equipmentID": 3,
        "propertyNum": ((0, 9867), (1, 100), (2, 33)),
        "baseProp": ((78004018, 15), (78004019, 20), (78004020, 15), (78004021, 20)),
        "rareProp": ((78004022, 30),),
        "qualityWeight": ((1, 8000), (2, 1700), (3, 300)),
        "LuckyWeight": None
    }),
    30770105: _tools.RODict({
        "ID": 30770105,
        "equipmentID": 4,
        "propertyNum": ((0, 9867), (1, 100), (2, 33)),
        "baseProp": ((78004023, 15), (78004024, 20), (78004025, 15), (78004026, 20)),
        "rareProp": ((78004027, 30),),
        "qualityWeight": ((1, 8000), (2, 1700), (3, 300)),
        "LuckyWeight": None
    }),
    30770106: _tools.RODict({
        "ID": 30770106,
        "equipmentID": 7,
        "propertyNum": ((0, 9867), (1, 100), (2, 33)),
        "baseProp": ((78004028, 30), (78004029, 40), (78004030, 30), (78004031, 40)),
        "rareProp": ((78004032, 30),),
        "qualityWeight": ((1, 8000), (2, 1700), (3, 300)),
        "LuckyWeight": None
    }),
    30770107: _tools.RODict({
        "ID": 30770107,
        "equipmentID": 5,
        "propertyNum": ((0, 9867), (1, 100), (2, 33)),
        "baseProp": ((78004033, 30), (78004034, 40), (78004035, 30), (78004036, 40)),
        "rareProp": ((78004037, 15), (78004038, 15)),
        "qualityWeight": ((1, 8000), (2, 1700), (3, 300)),
        "LuckyWeight": None
    }),
    30770108: _tools.RODict({
        "ID": 30770108,
        "equipmentID": 6,
        "propertyNum": ((0, 9867), (1, 100), (2, 33)),
        "baseProp": ((78004039, 30), (78004040, 40), (78004041, 30), (78004042, 40)),
        "rareProp": ((78004043, 30),),
        "qualityWeight": ((1, 8000), (2, 1700), (3, 300)),
        "LuckyWeight": None
    }),
    30770201: _tools.RODict({
        "ID": 30770201,
        "equipmentID": 2,
        "propertyNum": ((0, 9617), (1, 200), (2, 100), (3, 50), (4, 33)),
        "baseProp": ((78004001, 15), (78004002, 20), (78004003, 15), (78004004, 20)),
        "rareProp": ((78004005, 15), (78004006, 15)),
        "qualityWeight": ((1, 7000), (2, 2000), (3, 700), (4, 300)),
        "LuckyWeight": None
    }),
    30770202: _tools.RODict({
        "ID": 30770202,
        "equipmentID": 1,
        "propertyNum": ((0, 9617), (1, 200), (2, 100), (3, 50), (4, 33)),
        "baseProp": ((78004007, 30), (78004008, 40), (78004009, 30), (78004010, 40)),
        "rareProp": ((78004011, 15), (78004012, 15)),
        "qualityWeight": ((1, 7000), (2, 2000), (3, 700), (4, 300)),
        "LuckyWeight": None
    }),
    30770203: _tools.RODict({
        "ID": 30770203,
        "equipmentID": 8,
        "propertyNum": ((0, 9617), (1, 200), (2, 100), (3, 50), (4, 33)),
        "baseProp": ((78004013, 15), (78004014, 20), (78004015, 15), (78004016, 20)),
        "rareProp": ((78004017, 30),),
        "qualityWeight": ((1, 7000), (2, 2000), (3, 700), (4, 300)),
        "LuckyWeight": None
    }),
    30770204: _tools.RODict({
        "ID": 30770204,
        "equipmentID": 3,
        "propertyNum": ((0, 9617), (1, 200), (2, 100), (3, 50), (4, 33)),
        "baseProp": ((78004018, 15), (78004019, 20), (78004020, 15), (78004021, 20)),
        "rareProp": ((78004022, 30),),
        "qualityWeight": ((1, 7000), (2, 2000), (3, 700), (4, 300)),
        "LuckyWeight": None
    }),
    30770205: _tools.RODict({
        "ID": 30770205,
        "equipmentID": 4,
        "propertyNum": ((0, 9617), (1, 200), (2, 100), (3, 50), (4, 33)),
        "baseProp": ((78004023, 15), (78004024, 20), (78004025, 15), (78004026, 20)),
        "rareProp": ((78004027, 30),),
        "qualityWeight": ((1, 7000), (2, 2000), (3, 700), (4, 300)),
        "LuckyWeight": None
    }),
    30770206: _tools.RODict({
        "ID": 30770206,
        "equipmentID": 7,
        "propertyNum": ((0, 9617), (1, 200), (2, 100), (3, 50), (4, 33)),
        "baseProp": ((78004028, 30), (78004029, 40), (78004030, 30), (78004031, 40)),
        "rareProp": ((78004032, 30),),
        "qualityWeight": ((1, 7000), (2, 2000), (3, 700), (4, 300)),
        "LuckyWeight": None
    }),
    30770207: _tools.RODict({
        "ID": 30770207,
        "equipmentID": 5,
        "propertyNum": ((0, 9617), (1, 200), (2, 100), (3, 50), (4, 33)),
        "baseProp": ((78004033, 30), (78004034, 40), (78004035, 30), (78004036, 40)),
        "rareProp": ((78004037, 15), (78004038, 15)),
        "qualityWeight": ((1, 7000), (2, 2000), (3, 700), (4, 300)),
        "LuckyWeight": ((1, 0), (2, 0), (3, 1000), (4, 0))
    }),
    30770208: _tools.RODict({
        "ID": 30770208,
        "equipmentID": 6,
        "propertyNum": ((0, 9617), (1, 200), (2, 100), (3, 50), (4, 33)),
        "baseProp": ((78004039, 30), (78004040, 40), (78004041, 30), (78004042, 40)),
        "rareProp": ((78004043, 30),),
        "qualityWeight": ((1, 7000), (2, 2000), (3, 700), (4, 300)),
        "LuckyWeight": None
    }),
    30770301: _tools.RODict({
        "ID": 30770301,
        "equipmentID": 2,
        "propertyNum": ((0, 8300), (1, 1000), (2, 400), (3, 200), (4, 100)),
        "baseProp": ((78004001, 15), (78004002, 20), (78004003, 15), (78004004, 20)),
        "rareProp": ((78004005, 15), (78004006, 15)),
        "qualityWeight": ((1, 4900), (2, 3000), (3, 1500), (4, 600)),
        "LuckyWeight": None
    }),
    30770302: _tools.RODict({
        "ID": 30770302,
        "equipmentID": 1,
        "propertyNum": ((0, 8300), (1, 1000), (2, 400), (3, 200), (4, 100)),
        "baseProp": ((78004007, 30), (78004008, 40), (78004009, 30), (78004010, 40)),
        "rareProp": ((78004011, 15), (78004012, 15)),
        "qualityWeight": ((1, 4900), (2, 3000), (3, 1500), (4, 600)),
        "LuckyWeight": None
    }),
    30770303: _tools.RODict({
        "ID": 30770303,
        "equipmentID": 8,
        "propertyNum": ((0, 8300), (1, 1000), (2, 400), (3, 200), (4, 100)),
        "baseProp": ((78004013, 15), (78004014, 20), (78004015, 15), (78004016, 20)),
        "rareProp": ((78004017, 30),),
        "qualityWeight": ((1, 4900), (2, 3000), (3, 1500), (4, 600)),
        "LuckyWeight": None
    }),
    30770304: _tools.RODict({
        "ID": 30770304,
        "equipmentID": 3,
        "propertyNum": ((0, 8300), (1, 1000), (2, 400), (3, 200), (4, 100)),
        "baseProp": ((78004018, 15), (78004019, 20), (78004020, 15), (78004021, 20)),
        "rareProp": ((78004022, 30),),
        "qualityWeight": ((1, 4900), (2, 3000), (3, 1500), (4, 600)),
        "LuckyWeight": None
    }),
    30770305: _tools.RODict({
        "ID": 30770305,
        "equipmentID": 4,
        "propertyNum": ((0, 8300), (1, 1000), (2, 400), (3, 200), (4, 100)),
        "baseProp": ((78004023, 15), (78004024, 20), (78004025, 15), (78004026, 20)),
        "rareProp": ((78004027, 30),),
        "qualityWeight": ((1, 4900), (2, 3000), (3, 1500), (4, 600)),
        "LuckyWeight": None
    }),
    30770306: _tools.RODict({
        "ID": 30770306,
        "equipmentID": 7,
        "propertyNum": ((0, 8300), (1, 1000), (2, 400), (3, 200), (4, 100)),
        "baseProp": ((78004028, 30), (78004029, 40), (78004030, 30), (78004031, 40)),
        "rareProp": ((78004032, 30),),
        "qualityWeight": ((1, 4900), (2, 3000), (3, 1500), (4, 600)),
        "LuckyWeight": None
    }),
    30770307: _tools.RODict({
        "ID": 30770307,
        "equipmentID": 5,
        "propertyNum": ((0, 8300), (1, 1000), (2, 400), (3, 200), (4, 100)),
        "baseProp": ((78004033, 30), (78004034, 40), (78004035, 30), (78004036, 40)),
        "rareProp": ((78004037, 15), (78004038, 15)),
        "qualityWeight": ((1, 4900), (2, 3000), (3, 1500), (4, 600)),
        "LuckyWeight": ((1, 0), (2, 0), (3, 8400), (4, 1600))
    }),
    30770308: _tools.RODict({
        "ID": 30770308,
        "equipmentID": 6,
        "propertyNum": ((0, 8300), (1, 1000), (2, 400), (3, 200), (4, 100)),
        "baseProp": ((78004039, 30), (78004040, 40), (78004041, 30), (78004042, 40)),
        "rareProp": ((78004043, 30),),
        "qualityWeight": ((1, 4900), (2, 3000), (3, 1500), (4, 600)),
        "LuckyWeight": None
    }),
    30770400: _tools.RODict({
        "ID": 30770400,
        "equipmentID": 2,
        "propertyNum": ((0, 0), (1, 100), (2, 0)),
        "baseProp": ((78004001, 200),),
        "rareProp": None,
        "qualityWeight": ((1, 8000), (2, 0), (3, 0)),
        "LuckyWeight": None
    })
})
minKey = 30770101
maxKey = 30770400