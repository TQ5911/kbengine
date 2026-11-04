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
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "defLevelWeight": (828103, 100000, 40000, 20000, 10000, 800, 444, 286, 200, 168),
        "propertyNumQuality": 1,
        "baseProp": (1005, 1005, 1005, 1005),
        "rareProp": (2001, 2001, 2001, 2001),
        "rareProp2": (3001, 3001, 3001, 3001)
    }),
    30770102: _tools.RODict({
        "ID": 30770102,
        "equipmentID": 1,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "defLevelWeight": (828103, 100000, 40000, 20000, 10000, 800, 444, 286, 200, 168),
        "propertyNumQuality": 1,
        "baseProp": (1001, 1001, 1001, 1001),
        "rareProp": (2002, 2002, 2002, 2002),
        "rareProp2": (3002, 3002, 3002, 3002)
    }),
    30770103: _tools.RODict({
        "ID": 30770103,
        "equipmentID": 8,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "defLevelWeight": (828103, 100000, 40000, 20000, 10000, 800, 444, 286, 200, 168),
        "propertyNumQuality": 1,
        "baseProp": (1006, 1006, 1006, 1006),
        "rareProp": (2003, 2003, 2003, 2003),
        "rareProp2": (3003, 3003, 3003, 3003)
    }),
    30770104: _tools.RODict({
        "ID": 30770104,
        "equipmentID": 3,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "defLevelWeight": (828103, 100000, 40000, 20000, 10000, 800, 444, 286, 200, 168),
        "propertyNumQuality": 1,
        "baseProp": (1008, 1008, 1008, 1008),
        "rareProp": (2004, 2004, 2004, 2004),
        "rareProp2": (3004, 3004, 3004, 3004)
    }),
    30770105: _tools.RODict({
        "ID": 30770105,
        "equipmentID": 4,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "defLevelWeight": (828103, 100000, 40000, 20000, 10000, 800, 444, 286, 200, 168),
        "propertyNumQuality": 1,
        "baseProp": (1007, 1007, 1007, 1007),
        "rareProp": (2005, 2005, 2005, 2005),
        "rareProp2": (3005, 3005, 3005, 3005)
    }),
    30770106: _tools.RODict({
        "ID": 30770106,
        "equipmentID": 7,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "defLevelWeight": (828103, 100000, 40000, 20000, 10000, 800, 444, 286, 200, 168),
        "propertyNumQuality": 1,
        "baseProp": (1003, 1003, 1003, 1003),
        "rareProp": (2006, 2006, 2006, 2006),
        "rareProp2": (3006, 3006, 3006, 3006)
    }),
    30770107: _tools.RODict({
        "ID": 30770107,
        "equipmentID": 5,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "defLevelWeight": (828103, 100000, 40000, 20000, 10000, 800, 444, 286, 200, 168),
        "propertyNumQuality": 1,
        "baseProp": (1002, 1002, 1002, 1002),
        "rareProp": (2007, 2007, 2007, 2007),
        "rareProp2": (3007, 3007, 3007, 3007)
    }),
    30770108: _tools.RODict({
        "ID": 30770108,
        "equipmentID": 6,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "defLevelWeight": (828103, 100000, 40000, 20000, 10000, 800, 444, 286, 200, 168),
        "propertyNumQuality": 1,
        "baseProp": (1004, 1004, 1004, 1004),
        "rareProp": (2008, 2008, 2008, 2008),
        "rareProp2": (3008, 3008, 3008, 3008)
    }),
    30770201: _tools.RODict({
        "ID": 30770201,
        "equipmentID": 2,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
        "defLevelWeight": (733620, 200000, 100000, 40000, 20000, 2000, 1334, 1000, 800, 444, 200, 134, 100, 80, 66),
        "propertyNumQuality": 2,
        "baseProp": (1005, 1005, 1005, 1005),
        "rareProp": (2001, 2001, 2001, 2001),
        "rareProp2": (3001, 3001, 3001, 3001)
    }),
    30770202: _tools.RODict({
        "ID": 30770202,
        "equipmentID": 1,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
        "defLevelWeight": (733620, 200000, 100000, 40000, 20000, 2000, 1334, 1000, 800, 444, 200, 134, 100, 80, 66),
        "propertyNumQuality": 2,
        "baseProp": (1001, 1001, 1001, 1001),
        "rareProp": (2002, 2002, 2002, 2002),
        "rareProp2": (3002, 3002, 3002, 3002)
    }),
    30770203: _tools.RODict({
        "ID": 30770203,
        "equipmentID": 8,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
        "defLevelWeight": (733620, 200000, 100000, 40000, 20000, 2000, 1334, 1000, 800, 444, 200, 134, 100, 80, 66),
        "propertyNumQuality": 2,
        "baseProp": (1006, 1006, 1006, 1006),
        "rareProp": (2003, 2003, 2003, 2003),
        "rareProp2": (3003, 3003, 3003, 3003)
    }),
    30770204: _tools.RODict({
        "ID": 30770204,
        "equipmentID": 3,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
        "defLevelWeight": (733620, 200000, 100000, 40000, 20000, 2000, 1334, 1000, 800, 444, 200, 134, 100, 80, 66),
        "propertyNumQuality": 2,
        "baseProp": (1008, 1008, 1008, 1008),
        "rareProp": (2004, 2004, 2004, 2004),
        "rareProp2": (3004, 3004, 3004, 3004)
    }),
    30770205: _tools.RODict({
        "ID": 30770205,
        "equipmentID": 4,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
        "defLevelWeight": (733620, 200000, 100000, 40000, 20000, 2000, 1334, 1000, 800, 444, 200, 134, 100, 80, 66),
        "propertyNumQuality": 2,
        "baseProp": (1007, 1007, 1007, 1007),
        "rareProp": (2005, 2005, 2005, 2005),
        "rareProp2": (3005, 3005, 3005, 3005)
    }),
    30770206: _tools.RODict({
        "ID": 30770206,
        "equipmentID": 7,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
        "defLevelWeight": (733620, 200000, 100000, 40000, 20000, 2000, 1334, 1000, 800, 444, 200, 134, 100, 80, 66),
        "propertyNumQuality": 2,
        "baseProp": (1003, 1003, 1003, 1003),
        "rareProp": (2006, 2006, 2006, 2006),
        "rareProp2": (3006, 3006, 3006, 3006)
    }),
    30770207: _tools.RODict({
        "ID": 30770207,
        "equipmentID": 5,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
        "defLevelWeight": (733620, 200000, 100000, 40000, 20000, 2000, 1334, 1000, 800, 444, 200, 134, 100, 80, 66),
        "propertyNumQuality": 2,
        "baseProp": (1002, 1002, 1002, 1002),
        "rareProp": (2007, 2007, 2007, 2007),
        "rareProp2": (3007, 3007, 3007, 3007)
    }),
    30770208: _tools.RODict({
        "ID": 30770208,
        "equipmentID": 6,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
        "defLevelWeight": (733620, 200000, 100000, 40000, 20000, 2000, 1334, 1000, 800, 444, 200, 134, 100, 80, 66),
        "propertyNumQuality": 2,
        "baseProp": (1004, 1004, 1004, 1004),
        "rareProp": (2008, 2008, 2008, 2008),
        "rareProp2": (3008, 3008, 3008, 3008)
    }),
    30770301: _tools.RODict({
        "ID": 30770301,
        "equipmentID": 2,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24),
        "defLevelWeight": (26821, 400000, 266666, 160000, 124000, 9999, 4444, 3334, 2666, 2223, 666, 444, 333, 267, 222, 63, 56, 50, 42, 36),
        "propertyNumQuality": 3,
        "baseProp": (1005, 1005, 1005, 1005),
        "rareProp": (2001, 2001, 2001, 2001),
        "rareProp2": (3001, 3001, 3001, 3001)
    }),
    30770302: _tools.RODict({
        "ID": 30770302,
        "equipmentID": 1,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24),
        "defLevelWeight": (26821, 400000, 266666, 160000, 124000, 9999, 4444, 3334, 2666, 2223, 666, 444, 333, 267, 222, 63, 56, 50, 42, 36),
        "propertyNumQuality": 3,
        "baseProp": (1001, 1001, 1001, 1001),
        "rareProp": (2002, 2002, 2002, 2002),
        "rareProp2": (3002, 3002, 3002, 3002)
    }),
    30770303: _tools.RODict({
        "ID": 30770303,
        "equipmentID": 8,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24),
        "defLevelWeight": (26821, 400000, 266666, 160000, 124000, 9999, 4444, 3334, 2666, 2223, 666, 444, 333, 267, 222, 63, 56, 50, 42, 36),
        "propertyNumQuality": 3,
        "baseProp": (1006, 1006, 1006, 1006),
        "rareProp": (2003, 2003, 2003, 2003),
        "rareProp2": (3003, 3003, 3003, 3003)
    }),
    30770304: _tools.RODict({
        "ID": 30770304,
        "equipmentID": 3,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24),
        "defLevelWeight": (26821, 400000, 266666, 160000, 124000, 9999, 4444, 3334, 2666, 2223, 666, 444, 333, 267, 222, 63, 56, 50, 42, 36),
        "propertyNumQuality": 3,
        "baseProp": (1008, 1008, 1008, 1008),
        "rareProp": (2004, 2004, 2004, 2004),
        "rareProp2": (3004, 3004, 3004, 3004)
    }),
    30770305: _tools.RODict({
        "ID": 30770305,
        "equipmentID": 4,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24),
        "defLevelWeight": (26821, 400000, 266666, 160000, 124000, 9999, 4444, 3334, 2666, 2223, 666, 444, 333, 267, 222, 63, 56, 50, 42, 36),
        "propertyNumQuality": 3,
        "baseProp": (1007, 1007, 1007, 1007),
        "rareProp": (2005, 2005, 2005, 2005),
        "rareProp2": (3005, 3005, 3005, 3005)
    }),
    30770306: _tools.RODict({
        "ID": 30770306,
        "equipmentID": 7,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24),
        "defLevelWeight": (26821, 400000, 266666, 160000, 124000, 9999, 4444, 3334, 2666, 2223, 666, 444, 333, 267, 222, 63, 56, 50, 42, 36),
        "propertyNumQuality": 3,
        "baseProp": (1003, 1003, 1003, 1003),
        "rareProp": (2006, 2006, 2006, 2006),
        "rareProp2": (3006, 3006, 3006, 3006)
    }),
    30770307: _tools.RODict({
        "ID": 30770307,
        "equipmentID": 5,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24),
        "defLevelWeight": (26821, 400000, 266666, 160000, 124000, 9999, 4444, 3334, 2666, 2223, 666, 444, 333, 267, 222, 63, 56, 50, 42, 36),
        "propertyNumQuality": 3,
        "baseProp": (1002, 1002, 1002, 1002),
        "rareProp": (2007, 2007, 2007, 2007),
        "rareProp2": (3007, 3007, 3007, 3007)
    }),
    30770308: _tools.RODict({
        "ID": 30770308,
        "equipmentID": 6,
        "defLevel": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24),
        "defLevelWeight": (26821, 400000, 266666, 160000, 124000, 9999, 4444, 3334, 2666, 2223, 666, 444, 333, 267, 222, 63, 56, 50, 42, 36),
        "propertyNumQuality": 3,
        "baseProp": (1004, 1004, 1004, 1004),
        "rareProp": (2008, 2008, 2008, 2008),
        "rareProp2": (3008, 3008, 3008, 3008)
    }),
    30770400: _tools.RODict({
        "ID": 30770400,
        "equipmentID": 4,
        "defLevel": (2,),
        "defLevelWeight": (1000,),
        "propertyNumQuality": 4,
        "baseProp": (1010, 1010, 1010, 1010),
        "rareProp": (2005, 2005, 2005, 2005),
        "rareProp2": (3005, 3005, 3005, 3005)
    }),
    30770407: _tools.RODict({
        "ID": 30770407,
        "equipmentID": 7,
        "defLevel": (6,),
        "defLevelWeight": (1000,),
        "propertyNumQuality": 1,
        "baseProp": (1003, 1003, 1003, 1003),
        "rareProp": (2006, 2006, 2006, 2006),
        "rareProp2": (3006, 3006, 3006, 3006)
    }),
    30770408: _tools.RODict({
        "ID": 30770408,
        "equipmentID": 5,
        "defLevel": (6,),
        "defLevelWeight": (1000,),
        "propertyNumQuality": 1,
        "baseProp": (1002, 1002, 1002, 1002),
        "rareProp": (2007, 2007, 2007, 2007),
        "rareProp2": (3007, 3007, 3007, 3007)
    }),
    30770409: _tools.RODict({
        "ID": 30770409,
        "equipmentID": 6,
        "defLevel": (6,),
        "defLevelWeight": (1000,),
        "propertyNumQuality": 1,
        "baseProp": (1004, 1004, 1004, 1004),
        "rareProp": (2008, 2008, 2008, 2008),
        "rareProp2": (3008, 3008, 3008, 3008)
    })
})
minKey = 30770101
maxKey = 30770409