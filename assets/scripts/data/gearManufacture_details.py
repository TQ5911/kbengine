# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearManufacture/details
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    80111001: _tools.RODict({
        "ID": 80111001,
        "isOpen": 1,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80111002: _tools.RODict({
        "ID": 80111002,
        "isOpen": 1,
        "consumeItem": ((80111001, 1), (80111001, 1), (30000287, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80111003: _tools.RODict({
        "ID": 80111003,
        "isOpen": 1,
        "consumeItem": ((80111002, 1), (80111002, 1), (30000287, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80112001: _tools.RODict({
        "ID": 80112001,
        "isOpen": 1,
        "consumeItem": ((80111003, 1), (30990121, 1), (30000290, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80112002: _tools.RODict({
        "ID": 80112002,
        "isOpen": 1,
        "consumeItem": ((80112001, 1), (80112001, 1), (30000290, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80112003: _tools.RODict({
        "ID": 80112003,
        "isOpen": 1,
        "consumeItem": ((80112002, 1), (80112002, 1), (30000290, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80112004: _tools.RODict({
        "ID": 80112004,
        "isOpen": 1,
        "consumeItem": ((80112003, 1), (80112003, 1), (30000290, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80113001: _tools.RODict({
        "ID": 80113001,
        "isOpen": 1,
        "consumeItem": ((80112004, 1), (30990128, 1), (30000293, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80113002: _tools.RODict({
        "ID": 80113002,
        "isOpen": 1,
        "consumeItem": ((80113001, 1), (80113001, 1), (30000293, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80113003: _tools.RODict({
        "ID": 80113003,
        "isOpen": 1,
        "consumeItem": ((80113002, 1), (80113002, 1), (30000293, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80113004: _tools.RODict({
        "ID": 80113004,
        "isOpen": 1,
        "consumeItem": ((80113003, 1), (80113003, 1), (30000293, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80113005: _tools.RODict({
        "ID": 80113005,
        "isOpen": 1,
        "consumeItem": ((80113004, 1), (80113004, 1), (30000293, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80114001: _tools.RODict({
        "ID": 80114001,
        "isOpen": 1,
        "consumeItem": ((80113005, 1), (30990135, 1), (30000296, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80114002: _tools.RODict({
        "ID": 80114002,
        "isOpen": 1,
        "consumeItem": ((80114001, 1), (80114001, 1), (30000296, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80114003: _tools.RODict({
        "ID": 80114003,
        "isOpen": 1,
        "consumeItem": ((80114002, 1), (80114002, 1), (30000296, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80115001: _tools.RODict({
        "ID": 80115001,
        "isOpen": 1,
        "consumeItem": ((80114003, 1), (30990142, 1), (30000296, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80113006: _tools.RODict({
        "ID": 80113006,
        "isOpen": 1,
        "consumeItem": ((80113002, 1), (30000293, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80113007: _tools.RODict({
        "ID": 80113007,
        "isOpen": 1,
        "consumeItem": ((80113006, 1), (80113006, 1), (30000293, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80113008: _tools.RODict({
        "ID": 80113008,
        "isOpen": 1,
        "consumeItem": ((80113007, 1), (80113007, 1), (30000293, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80113009: _tools.RODict({
        "ID": 80113009,
        "isOpen": 1,
        "consumeItem": ((80113008, 1), (80113008, 1), (30000293, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80114005: _tools.RODict({
        "ID": 80114005,
        "isOpen": 1,
        "consumeItem": ((80113009, 1), (30990135, 1), (30000296, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80114006: _tools.RODict({
        "ID": 80114006,
        "isOpen": 1,
        "consumeItem": ((80114005, 1), (80114005, 1), (30000296, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80114007: _tools.RODict({
        "ID": 80114007,
        "isOpen": 1,
        "consumeItem": ((80114006, 1), (80114006, 1), (30000296, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80115002: _tools.RODict({
        "ID": 80115002,
        "isOpen": 1,
        "consumeItem": ((80114007, 1), (30990142, 1), (30000296, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80121001: _tools.RODict({
        "ID": 80121001,
        "isOpen": 1,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80121002: _tools.RODict({
        "ID": 80121002,
        "isOpen": 1,
        "consumeItem": ((80121001, 1), (80121001, 1), (30000287, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80121003: _tools.RODict({
        "ID": 80121003,
        "isOpen": 1,
        "consumeItem": ((80121002, 1), (80121002, 1), (30000287, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80122001: _tools.RODict({
        "ID": 80122001,
        "isOpen": 1,
        "consumeItem": ((80121003, 1), (30990121, 1), (30000290, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80122002: _tools.RODict({
        "ID": 80122002,
        "isOpen": 1,
        "consumeItem": ((80122001, 1), (80122001, 1), (30000290, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80122003: _tools.RODict({
        "ID": 80122003,
        "isOpen": 1,
        "consumeItem": ((80122002, 1), (80122002, 1), (30000290, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80122004: _tools.RODict({
        "ID": 80122004,
        "isOpen": 1,
        "consumeItem": ((80122003, 1), (80122003, 1), (30000290, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80123001: _tools.RODict({
        "ID": 80123001,
        "isOpen": 1,
        "consumeItem": ((80122004, 1), (30990128, 1), (30000293, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80123002: _tools.RODict({
        "ID": 80123002,
        "isOpen": 1,
        "consumeItem": ((80123001, 1), (80123001, 1), (30000293, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80123003: _tools.RODict({
        "ID": 80123003,
        "isOpen": 1,
        "consumeItem": ((80123002, 1), (80123002, 1), (30000293, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80123004: _tools.RODict({
        "ID": 80123004,
        "isOpen": 1,
        "consumeItem": ((80123003, 1), (80123003, 1), (30000293, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80123005: _tools.RODict({
        "ID": 80123005,
        "isOpen": 1,
        "consumeItem": ((80123004, 1), (80123004, 1), (30000293, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80124001: _tools.RODict({
        "ID": 80124001,
        "isOpen": 1,
        "consumeItem": ((80123005, 1), (30990135, 1), (30000296, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80124002: _tools.RODict({
        "ID": 80124002,
        "isOpen": 1,
        "consumeItem": ((80124001, 1), (80124001, 1), (30000296, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80124003: _tools.RODict({
        "ID": 80124003,
        "isOpen": 1,
        "consumeItem": ((80124002, 1), (80124002, 1), (30000296, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80125001: _tools.RODict({
        "ID": 80125001,
        "isOpen": 1,
        "consumeItem": ((80124003, 1), (30990142, 1), (30000296, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80123006: _tools.RODict({
        "ID": 80123006,
        "isOpen": 1,
        "consumeItem": ((80123002, 1), (30000293, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80123007: _tools.RODict({
        "ID": 80123007,
        "isOpen": 1,
        "consumeItem": ((80123006, 1), (80123006, 1), (30000293, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80123008: _tools.RODict({
        "ID": 80123008,
        "isOpen": 1,
        "consumeItem": ((80123007, 1), (80123007, 1), (30000293, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80123009: _tools.RODict({
        "ID": 80123009,
        "isOpen": 1,
        "consumeItem": ((80123008, 1), (80123008, 1), (30000293, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80124005: _tools.RODict({
        "ID": 80124005,
        "isOpen": 1,
        "consumeItem": ((80123009, 1), (30990135, 1), (30000296, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80124006: _tools.RODict({
        "ID": 80124006,
        "isOpen": 1,
        "consumeItem": ((80124005, 1), (80124005, 1), (30000296, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80124007: _tools.RODict({
        "ID": 80124007,
        "isOpen": 1,
        "consumeItem": ((80124006, 1), (80124006, 1), (30000296, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80125002: _tools.RODict({
        "ID": 80125002,
        "isOpen": 1,
        "consumeItem": ((80124007, 1), (30990142, 1), (30000296, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80131001: _tools.RODict({
        "ID": 80131001,
        "isOpen": 1,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80131002: _tools.RODict({
        "ID": 80131002,
        "isOpen": 1,
        "consumeItem": ((80131001, 1), (80131001, 1), (30000287, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80131003: _tools.RODict({
        "ID": 80131003,
        "isOpen": 1,
        "consumeItem": ((80131002, 1), (80131002, 1), (30000287, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80132001: _tools.RODict({
        "ID": 80132001,
        "isOpen": 1,
        "consumeItem": ((80131003, 1), (30990121, 1), (30000290, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80132002: _tools.RODict({
        "ID": 80132002,
        "isOpen": 1,
        "consumeItem": ((80132001, 1), (80132001, 1), (30000290, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80132003: _tools.RODict({
        "ID": 80132003,
        "isOpen": 1,
        "consumeItem": ((80132002, 1), (80132002, 1), (30000290, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80132004: _tools.RODict({
        "ID": 80132004,
        "isOpen": 1,
        "consumeItem": ((80132003, 1), (80132003, 1), (30000290, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80133001: _tools.RODict({
        "ID": 80133001,
        "isOpen": 1,
        "consumeItem": ((80132004, 1), (30990128, 1), (30000293, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80133002: _tools.RODict({
        "ID": 80133002,
        "isOpen": 1,
        "consumeItem": ((80133001, 1), (80133001, 1), (30000293, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80133003: _tools.RODict({
        "ID": 80133003,
        "isOpen": 1,
        "consumeItem": ((80133002, 1), (80133002, 1), (30000293, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80133004: _tools.RODict({
        "ID": 80133004,
        "isOpen": 1,
        "consumeItem": ((80133003, 1), (80133003, 1), (30000293, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80133005: _tools.RODict({
        "ID": 80133005,
        "isOpen": 1,
        "consumeItem": ((80133004, 1), (80133004, 1), (30000293, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80134001: _tools.RODict({
        "ID": 80134001,
        "isOpen": 1,
        "consumeItem": ((80133005, 1), (30990135, 1), (30000296, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80134002: _tools.RODict({
        "ID": 80134002,
        "isOpen": 1,
        "consumeItem": ((80134001, 1), (80134001, 1), (30000296, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80134003: _tools.RODict({
        "ID": 80134003,
        "isOpen": 1,
        "consumeItem": ((80134002, 1), (80134002, 1), (30000296, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80135001: _tools.RODict({
        "ID": 80135001,
        "isOpen": 1,
        "consumeItem": ((80134003, 1), (30990142, 1), (30000296, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80133006: _tools.RODict({
        "ID": 80133006,
        "isOpen": 1,
        "consumeItem": ((80133002, 1), (30000293, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80133007: _tools.RODict({
        "ID": 80133007,
        "isOpen": 1,
        "consumeItem": ((80133006, 1), (80133006, 1), (30000293, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80133008: _tools.RODict({
        "ID": 80133008,
        "isOpen": 1,
        "consumeItem": ((80133007, 1), (80133007, 1), (30000293, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80133009: _tools.RODict({
        "ID": 80133009,
        "isOpen": 1,
        "consumeItem": ((80133008, 1), (80133008, 1), (30000293, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80134005: _tools.RODict({
        "ID": 80134005,
        "isOpen": 1,
        "consumeItem": ((80133009, 1), (30990135, 1), (30000296, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80134006: _tools.RODict({
        "ID": 80134006,
        "isOpen": 1,
        "consumeItem": ((80134005, 1), (80134005, 1), (30000296, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80134007: _tools.RODict({
        "ID": 80134007,
        "isOpen": 1,
        "consumeItem": ((80134006, 1), (80134006, 1), (30000296, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80135002: _tools.RODict({
        "ID": 80135002,
        "isOpen": 1,
        "consumeItem": ((80134007, 1), (30990142, 1), (30000296, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80211001: _tools.RODict({
        "ID": 80211001,
        "isOpen": 0,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80211002: _tools.RODict({
        "ID": 80211002,
        "isOpen": 1,
        "consumeItem": ((80211001, 1), (80211001, 1), (30000288, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80211003: _tools.RODict({
        "ID": 80211003,
        "isOpen": 1,
        "consumeItem": ((80211002, 1), (80211002, 1), (30000288, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80212001: _tools.RODict({
        "ID": 80212001,
        "isOpen": 1,
        "consumeItem": ((80211003, 1), (30990122, 1), (30000291, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80212002: _tools.RODict({
        "ID": 80212002,
        "isOpen": 1,
        "consumeItem": ((80212001, 1), (80212001, 1), (30000291, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80212003: _tools.RODict({
        "ID": 80212003,
        "isOpen": 1,
        "consumeItem": ((80212002, 1), (80212002, 1), (30000291, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80212004: _tools.RODict({
        "ID": 80212004,
        "isOpen": 1,
        "consumeItem": ((80212003, 1), (80212003, 1), (30000291, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80213001: _tools.RODict({
        "ID": 80213001,
        "isOpen": 1,
        "consumeItem": ((80212004, 1), (30990129, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80213002: _tools.RODict({
        "ID": 80213002,
        "isOpen": 1,
        "consumeItem": ((80213001, 1), (80213001, 1), (30000294, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80213003: _tools.RODict({
        "ID": 80213003,
        "isOpen": 1,
        "consumeItem": ((80213002, 1), (80213002, 1), (30000294, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80213004: _tools.RODict({
        "ID": 80213004,
        "isOpen": 1,
        "consumeItem": ((80213003, 1), (80213003, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80213005: _tools.RODict({
        "ID": 80213005,
        "isOpen": 1,
        "consumeItem": ((80213004, 1), (80213004, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80214001: _tools.RODict({
        "ID": 80214001,
        "isOpen": 1,
        "consumeItem": ((80213005, 1), (30990136, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80214002: _tools.RODict({
        "ID": 80214002,
        "isOpen": 1,
        "consumeItem": ((80214001, 1), (80214001, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80214003: _tools.RODict({
        "ID": 80214003,
        "isOpen": 1,
        "consumeItem": ((80214002, 1), (80214002, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80215001: _tools.RODict({
        "ID": 80215001,
        "isOpen": 1,
        "consumeItem": ((80214003, 1), (30990143, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80213006: _tools.RODict({
        "ID": 80213006,
        "isOpen": 1,
        "consumeItem": ((80213003, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80213007: _tools.RODict({
        "ID": 80213007,
        "isOpen": 1,
        "consumeItem": ((80213006, 1), (80213006, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80213008: _tools.RODict({
        "ID": 80213008,
        "isOpen": 1,
        "consumeItem": ((80213007, 1), (80213007, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80214005: _tools.RODict({
        "ID": 80214005,
        "isOpen": 1,
        "consumeItem": ((80213008, 1), (30990136, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80214006: _tools.RODict({
        "ID": 80214006,
        "isOpen": 1,
        "consumeItem": ((80214005, 1), (80214005, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80214007: _tools.RODict({
        "ID": 80214007,
        "isOpen": 1,
        "consumeItem": ((80214006, 1), (80214006, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80215002: _tools.RODict({
        "ID": 80215002,
        "isOpen": 1,
        "consumeItem": ((80214007, 1), (30990143, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80221001: _tools.RODict({
        "ID": 80221001,
        "isOpen": 0,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80221002: _tools.RODict({
        "ID": 80221002,
        "isOpen": 1,
        "consumeItem": ((80221001, 1), (80221001, 1), (30000288, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80221003: _tools.RODict({
        "ID": 80221003,
        "isOpen": 1,
        "consumeItem": ((80221002, 1), (80221002, 1), (30000288, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80222001: _tools.RODict({
        "ID": 80222001,
        "isOpen": 1,
        "consumeItem": ((80221003, 1), (30990122, 1), (30000291, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80222002: _tools.RODict({
        "ID": 80222002,
        "isOpen": 1,
        "consumeItem": ((80222001, 1), (80222001, 1), (30000291, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80222003: _tools.RODict({
        "ID": 80222003,
        "isOpen": 1,
        "consumeItem": ((80222002, 1), (80222002, 1), (30000291, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80222004: _tools.RODict({
        "ID": 80222004,
        "isOpen": 1,
        "consumeItem": ((80222003, 1), (80222003, 1), (30000291, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80223001: _tools.RODict({
        "ID": 80223001,
        "isOpen": 1,
        "consumeItem": ((80222004, 1), (30990129, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80223002: _tools.RODict({
        "ID": 80223002,
        "isOpen": 1,
        "consumeItem": ((80223001, 1), (80223001, 1), (30000294, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80223003: _tools.RODict({
        "ID": 80223003,
        "isOpen": 1,
        "consumeItem": ((80223002, 1), (80223002, 1), (30000294, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80223004: _tools.RODict({
        "ID": 80223004,
        "isOpen": 1,
        "consumeItem": ((80223003, 1), (80223003, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80223005: _tools.RODict({
        "ID": 80223005,
        "isOpen": 1,
        "consumeItem": ((80223004, 1), (80223004, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80224001: _tools.RODict({
        "ID": 80224001,
        "isOpen": 1,
        "consumeItem": ((80223005, 1), (30990136, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80224002: _tools.RODict({
        "ID": 80224002,
        "isOpen": 1,
        "consumeItem": ((80224001, 1), (80224001, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80224003: _tools.RODict({
        "ID": 80224003,
        "isOpen": 1,
        "consumeItem": ((80224002, 1), (80224002, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80225001: _tools.RODict({
        "ID": 80225001,
        "isOpen": 1,
        "consumeItem": ((80224003, 1), (30990143, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80223006: _tools.RODict({
        "ID": 80223006,
        "isOpen": 1,
        "consumeItem": ((80223003, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80223007: _tools.RODict({
        "ID": 80223007,
        "isOpen": 1,
        "consumeItem": ((80223006, 1), (80223006, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80223008: _tools.RODict({
        "ID": 80223008,
        "isOpen": 1,
        "consumeItem": ((80223007, 1), (80223007, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80224005: _tools.RODict({
        "ID": 80224005,
        "isOpen": 1,
        "consumeItem": ((80223008, 1), (30990136, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80224006: _tools.RODict({
        "ID": 80224006,
        "isOpen": 1,
        "consumeItem": ((80224005, 1), (80224005, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80224007: _tools.RODict({
        "ID": 80224007,
        "isOpen": 1,
        "consumeItem": ((80224006, 1), (80224006, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80225002: _tools.RODict({
        "ID": 80225002,
        "isOpen": 1,
        "consumeItem": ((80224007, 1), (30990143, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80231001: _tools.RODict({
        "ID": 80231001,
        "isOpen": 0,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80231002: _tools.RODict({
        "ID": 80231002,
        "isOpen": 1,
        "consumeItem": ((80231001, 1), (80231001, 1), (30000288, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80231003: _tools.RODict({
        "ID": 80231003,
        "isOpen": 1,
        "consumeItem": ((80231002, 1), (80231002, 1), (30000288, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80232001: _tools.RODict({
        "ID": 80232001,
        "isOpen": 1,
        "consumeItem": ((80231003, 1), (30990122, 1), (30000291, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80232002: _tools.RODict({
        "ID": 80232002,
        "isOpen": 1,
        "consumeItem": ((80232001, 1), (80232001, 1), (30000291, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80232003: _tools.RODict({
        "ID": 80232003,
        "isOpen": 1,
        "consumeItem": ((80232002, 1), (80232002, 1), (30000291, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80232004: _tools.RODict({
        "ID": 80232004,
        "isOpen": 1,
        "consumeItem": ((80232003, 1), (80232003, 1), (30000291, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80233001: _tools.RODict({
        "ID": 80233001,
        "isOpen": 1,
        "consumeItem": ((80232004, 1), (30990129, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80233002: _tools.RODict({
        "ID": 80233002,
        "isOpen": 1,
        "consumeItem": ((80233001, 1), (80233001, 1), (30000294, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80233003: _tools.RODict({
        "ID": 80233003,
        "isOpen": 1,
        "consumeItem": ((80233002, 1), (80233002, 1), (30000294, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80233004: _tools.RODict({
        "ID": 80233004,
        "isOpen": 1,
        "consumeItem": ((80233003, 1), (80233003, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80233005: _tools.RODict({
        "ID": 80233005,
        "isOpen": 1,
        "consumeItem": ((80233004, 1), (80233004, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80234001: _tools.RODict({
        "ID": 80234001,
        "isOpen": 1,
        "consumeItem": ((80233005, 1), (30990136, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80234002: _tools.RODict({
        "ID": 80234002,
        "isOpen": 1,
        "consumeItem": ((80234001, 1), (80234001, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80234003: _tools.RODict({
        "ID": 80234003,
        "isOpen": 1,
        "consumeItem": ((80234002, 1), (80234002, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80235001: _tools.RODict({
        "ID": 80235001,
        "isOpen": 1,
        "consumeItem": ((80234003, 1), (30990143, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80233006: _tools.RODict({
        "ID": 80233006,
        "isOpen": 1,
        "consumeItem": ((80233003, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80233007: _tools.RODict({
        "ID": 80233007,
        "isOpen": 1,
        "consumeItem": ((80233006, 1), (80233006, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80233008: _tools.RODict({
        "ID": 80233008,
        "isOpen": 1,
        "consumeItem": ((80233007, 1), (80233007, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80234005: _tools.RODict({
        "ID": 80234005,
        "isOpen": 1,
        "consumeItem": ((80233008, 1), (30990136, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80234006: _tools.RODict({
        "ID": 80234006,
        "isOpen": 1,
        "consumeItem": ((80234005, 1), (80234005, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80234007: _tools.RODict({
        "ID": 80234007,
        "isOpen": 1,
        "consumeItem": ((80234006, 1), (80234006, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80235002: _tools.RODict({
        "ID": 80235002,
        "isOpen": 1,
        "consumeItem": ((80234007, 1), (30990143, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80311001: _tools.RODict({
        "ID": 80311001,
        "isOpen": 0,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80311002: _tools.RODict({
        "ID": 80311002,
        "isOpen": 1,
        "consumeItem": ((80311001, 1), (80311001, 1), (30000288, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80311003: _tools.RODict({
        "ID": 80311003,
        "isOpen": 1,
        "consumeItem": ((80311002, 1), (80311002, 1), (30000288, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80312001: _tools.RODict({
        "ID": 80312001,
        "isOpen": 1,
        "consumeItem": ((80311003, 1), (30990123, 1), (30000291, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80312002: _tools.RODict({
        "ID": 80312002,
        "isOpen": 1,
        "consumeItem": ((80312001, 1), (80312001, 1), (30000291, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80312003: _tools.RODict({
        "ID": 80312003,
        "isOpen": 1,
        "consumeItem": ((80312002, 1), (80312002, 1), (30000291, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80312004: _tools.RODict({
        "ID": 80312004,
        "isOpen": 1,
        "consumeItem": ((80312003, 1), (80312003, 1), (30000291, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80313001: _tools.RODict({
        "ID": 80313001,
        "isOpen": 1,
        "consumeItem": ((80312004, 1), (30990130, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80313002: _tools.RODict({
        "ID": 80313002,
        "isOpen": 1,
        "consumeItem": ((80313001, 1), (80313001, 1), (30000294, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80313003: _tools.RODict({
        "ID": 80313003,
        "isOpen": 1,
        "consumeItem": ((80313002, 1), (80313002, 1), (30000294, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80313004: _tools.RODict({
        "ID": 80313004,
        "isOpen": 1,
        "consumeItem": ((80313003, 1), (80313003, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80313005: _tools.RODict({
        "ID": 80313005,
        "isOpen": 1,
        "consumeItem": ((80313004, 1), (80313004, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80314001: _tools.RODict({
        "ID": 80314001,
        "isOpen": 1,
        "consumeItem": ((80313005, 1), (30990137, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80314002: _tools.RODict({
        "ID": 80314002,
        "isOpen": 1,
        "consumeItem": ((80314001, 1), (80314001, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80314003: _tools.RODict({
        "ID": 80314003,
        "isOpen": 1,
        "consumeItem": ((80314002, 1), (80314002, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80315001: _tools.RODict({
        "ID": 80315001,
        "isOpen": 1,
        "consumeItem": ((80314003, 1), (30990144, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80321001: _tools.RODict({
        "ID": 80321001,
        "isOpen": 0,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80321002: _tools.RODict({
        "ID": 80321002,
        "isOpen": 1,
        "consumeItem": ((80321001, 1), (80321001, 1), (30000288, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80321003: _tools.RODict({
        "ID": 80321003,
        "isOpen": 1,
        "consumeItem": ((80321002, 1), (80321002, 1), (30000288, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80322001: _tools.RODict({
        "ID": 80322001,
        "isOpen": 1,
        "consumeItem": ((80321003, 1), (30990123, 1), (30000291, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80322002: _tools.RODict({
        "ID": 80322002,
        "isOpen": 1,
        "consumeItem": ((80322001, 1), (80322001, 1), (30000291, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80322003: _tools.RODict({
        "ID": 80322003,
        "isOpen": 1,
        "consumeItem": ((80322002, 1), (80322002, 1), (30000291, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80322004: _tools.RODict({
        "ID": 80322004,
        "isOpen": 1,
        "consumeItem": ((80322003, 1), (80322003, 1), (30000291, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80323001: _tools.RODict({
        "ID": 80323001,
        "isOpen": 1,
        "consumeItem": ((80322004, 1), (30990130, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80323002: _tools.RODict({
        "ID": 80323002,
        "isOpen": 1,
        "consumeItem": ((80323001, 1), (80323001, 1), (30000294, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80323003: _tools.RODict({
        "ID": 80323003,
        "isOpen": 1,
        "consumeItem": ((80323002, 1), (80323002, 1), (30000294, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80323004: _tools.RODict({
        "ID": 80323004,
        "isOpen": 1,
        "consumeItem": ((80323003, 1), (80323003, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80323005: _tools.RODict({
        "ID": 80323005,
        "isOpen": 1,
        "consumeItem": ((80323004, 1), (80323004, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80324001: _tools.RODict({
        "ID": 80324001,
        "isOpen": 1,
        "consumeItem": ((80323005, 1), (30990137, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80324002: _tools.RODict({
        "ID": 80324002,
        "isOpen": 1,
        "consumeItem": ((80324001, 1), (80324001, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80324003: _tools.RODict({
        "ID": 80324003,
        "isOpen": 1,
        "consumeItem": ((80324002, 1), (80324002, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80325001: _tools.RODict({
        "ID": 80325001,
        "isOpen": 1,
        "consumeItem": ((80324003, 1), (30990144, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80331001: _tools.RODict({
        "ID": 80331001,
        "isOpen": 0,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80331002: _tools.RODict({
        "ID": 80331002,
        "isOpen": 1,
        "consumeItem": ((80331001, 1), (80331001, 1), (30000288, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80331003: _tools.RODict({
        "ID": 80331003,
        "isOpen": 1,
        "consumeItem": ((80331002, 1), (80331002, 1), (30000288, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80332001: _tools.RODict({
        "ID": 80332001,
        "isOpen": 1,
        "consumeItem": ((80331003, 1), (30990123, 1), (30000291, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80332002: _tools.RODict({
        "ID": 80332002,
        "isOpen": 1,
        "consumeItem": ((80332001, 1), (80332001, 1), (30000291, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80332003: _tools.RODict({
        "ID": 80332003,
        "isOpen": 1,
        "consumeItem": ((80332002, 1), (80332002, 1), (30000291, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80332004: _tools.RODict({
        "ID": 80332004,
        "isOpen": 1,
        "consumeItem": ((80332003, 1), (80332003, 1), (30000291, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80333001: _tools.RODict({
        "ID": 80333001,
        "isOpen": 1,
        "consumeItem": ((80332004, 1), (30990130, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80333002: _tools.RODict({
        "ID": 80333002,
        "isOpen": 1,
        "consumeItem": ((80333001, 1), (80333001, 1), (30000294, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80333003: _tools.RODict({
        "ID": 80333003,
        "isOpen": 1,
        "consumeItem": ((80333002, 1), (80333002, 1), (30000294, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80333004: _tools.RODict({
        "ID": 80333004,
        "isOpen": 1,
        "consumeItem": ((80333003, 1), (80333003, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80333005: _tools.RODict({
        "ID": 80333005,
        "isOpen": 1,
        "consumeItem": ((80333004, 1), (80333004, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80334001: _tools.RODict({
        "ID": 80334001,
        "isOpen": 1,
        "consumeItem": ((80333005, 1), (30990137, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80334002: _tools.RODict({
        "ID": 80334002,
        "isOpen": 1,
        "consumeItem": ((80334001, 1), (80334001, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80334003: _tools.RODict({
        "ID": 80334003,
        "isOpen": 1,
        "consumeItem": ((80334002, 1), (80334002, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80335001: _tools.RODict({
        "ID": 80335001,
        "isOpen": 1,
        "consumeItem": ((80334003, 1), (30990144, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80411001: _tools.RODict({
        "ID": 80411001,
        "isOpen": 0,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80411002: _tools.RODict({
        "ID": 80411002,
        "isOpen": 1,
        "consumeItem": ((80411001, 1), (80411001, 1), (30000288, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80411003: _tools.RODict({
        "ID": 80411003,
        "isOpen": 1,
        "consumeItem": ((80411002, 1), (80411002, 1), (30000288, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80412001: _tools.RODict({
        "ID": 80412001,
        "isOpen": 1,
        "consumeItem": ((80411003, 1), (30990124, 1), (30000291, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80412002: _tools.RODict({
        "ID": 80412002,
        "isOpen": 1,
        "consumeItem": ((80412001, 1), (80412001, 1), (30000291, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80412003: _tools.RODict({
        "ID": 80412003,
        "isOpen": 1,
        "consumeItem": ((80412002, 1), (80412002, 1), (30000291, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80412004: _tools.RODict({
        "ID": 80412004,
        "isOpen": 1,
        "consumeItem": ((80412003, 1), (80412003, 1), (30000291, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80413001: _tools.RODict({
        "ID": 80413001,
        "isOpen": 1,
        "consumeItem": ((80412004, 1), (30990131, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80413002: _tools.RODict({
        "ID": 80413002,
        "isOpen": 1,
        "consumeItem": ((80413001, 1), (80413001, 1), (30000294, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80413003: _tools.RODict({
        "ID": 80413003,
        "isOpen": 1,
        "consumeItem": ((80413002, 1), (80413002, 1), (30000294, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80413004: _tools.RODict({
        "ID": 80413004,
        "isOpen": 1,
        "consumeItem": ((80413003, 1), (80413003, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80413005: _tools.RODict({
        "ID": 80413005,
        "isOpen": 1,
        "consumeItem": ((80413004, 1), (80413004, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80414001: _tools.RODict({
        "ID": 80414001,
        "isOpen": 1,
        "consumeItem": ((80413005, 1), (30990138, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80414002: _tools.RODict({
        "ID": 80414002,
        "isOpen": 1,
        "consumeItem": ((80414001, 1), (80414001, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80414003: _tools.RODict({
        "ID": 80414003,
        "isOpen": 1,
        "consumeItem": ((80414002, 1), (80414002, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80415001: _tools.RODict({
        "ID": 80415001,
        "isOpen": 1,
        "consumeItem": ((80414003, 1), (30990145, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80421001: _tools.RODict({
        "ID": 80421001,
        "isOpen": 0,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80421002: _tools.RODict({
        "ID": 80421002,
        "isOpen": 1,
        "consumeItem": ((80421001, 1), (80421001, 1), (30000288, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80421003: _tools.RODict({
        "ID": 80421003,
        "isOpen": 1,
        "consumeItem": ((80421002, 1), (80421002, 1), (30000288, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80422001: _tools.RODict({
        "ID": 80422001,
        "isOpen": 1,
        "consumeItem": ((80421003, 1), (30990124, 1), (30000291, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80422002: _tools.RODict({
        "ID": 80422002,
        "isOpen": 1,
        "consumeItem": ((80422001, 1), (80422001, 1), (30000291, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80422003: _tools.RODict({
        "ID": 80422003,
        "isOpen": 1,
        "consumeItem": ((80422002, 1), (80422002, 1), (30000291, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80422004: _tools.RODict({
        "ID": 80422004,
        "isOpen": 1,
        "consumeItem": ((80422003, 1), (80422003, 1), (30000291, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80423001: _tools.RODict({
        "ID": 80423001,
        "isOpen": 1,
        "consumeItem": ((80422004, 1), (30990131, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80423002: _tools.RODict({
        "ID": 80423002,
        "isOpen": 1,
        "consumeItem": ((80423001, 1), (80423001, 1), (30000294, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80423003: _tools.RODict({
        "ID": 80423003,
        "isOpen": 1,
        "consumeItem": ((80423002, 1), (80423002, 1), (30000294, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80423004: _tools.RODict({
        "ID": 80423004,
        "isOpen": 1,
        "consumeItem": ((80423003, 1), (80423003, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80423005: _tools.RODict({
        "ID": 80423005,
        "isOpen": 1,
        "consumeItem": ((80423004, 1), (80423004, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80424001: _tools.RODict({
        "ID": 80424001,
        "isOpen": 1,
        "consumeItem": ((80423005, 1), (30990138, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80424002: _tools.RODict({
        "ID": 80424002,
        "isOpen": 1,
        "consumeItem": ((80424001, 1), (80424001, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80424003: _tools.RODict({
        "ID": 80424003,
        "isOpen": 1,
        "consumeItem": ((80424002, 1), (80424002, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80425001: _tools.RODict({
        "ID": 80425001,
        "isOpen": 1,
        "consumeItem": ((80424003, 1), (30990145, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80431001: _tools.RODict({
        "ID": 80431001,
        "isOpen": 0,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80431002: _tools.RODict({
        "ID": 80431002,
        "isOpen": 1,
        "consumeItem": ((80431001, 1), (80431001, 1), (30000288, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80431003: _tools.RODict({
        "ID": 80431003,
        "isOpen": 1,
        "consumeItem": ((80431002, 1), (80431002, 1), (30000288, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80432001: _tools.RODict({
        "ID": 80432001,
        "isOpen": 1,
        "consumeItem": ((80431003, 1), (30990124, 1), (30000291, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80432002: _tools.RODict({
        "ID": 80432002,
        "isOpen": 1,
        "consumeItem": ((80432001, 1), (80432001, 1), (30000291, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80432003: _tools.RODict({
        "ID": 80432003,
        "isOpen": 1,
        "consumeItem": ((80432002, 1), (80432002, 1), (30000291, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80432004: _tools.RODict({
        "ID": 80432004,
        "isOpen": 1,
        "consumeItem": ((80432003, 1), (80432003, 1), (30000291, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80433001: _tools.RODict({
        "ID": 80433001,
        "isOpen": 1,
        "consumeItem": ((80432004, 1), (30990131, 1), (30000294, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80433002: _tools.RODict({
        "ID": 80433002,
        "isOpen": 1,
        "consumeItem": ((80433001, 1), (80433001, 1), (30000294, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80433003: _tools.RODict({
        "ID": 80433003,
        "isOpen": 1,
        "consumeItem": ((80433002, 1), (80433002, 1), (30000294, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80433004: _tools.RODict({
        "ID": 80433004,
        "isOpen": 1,
        "consumeItem": ((80433003, 1), (80433003, 1), (30000294, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80433005: _tools.RODict({
        "ID": 80433005,
        "isOpen": 1,
        "consumeItem": ((80433004, 1), (80433004, 1), (30000294, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80434001: _tools.RODict({
        "ID": 80434001,
        "isOpen": 1,
        "consumeItem": ((80433005, 1), (30990138, 1), (30000297, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80434002: _tools.RODict({
        "ID": 80434002,
        "isOpen": 1,
        "consumeItem": ((80434001, 1), (80434001, 1), (30000297, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80434003: _tools.RODict({
        "ID": 80434003,
        "isOpen": 1,
        "consumeItem": ((80434002, 1), (80434002, 1), (30000297, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80435001: _tools.RODict({
        "ID": 80435001,
        "isOpen": 1,
        "consumeItem": ((80434003, 1), (30990145, 1), (30000297, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80581001: _tools.RODict({
        "ID": 80581001,
        "isOpen": 0,
        "consumeItem": ((30000287, 10),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 500),)
    }),
    80581002: _tools.RODict({
        "ID": 80581002,
        "isOpen": 1,
        "consumeItem": ((80581001, 1), (80581001, 1), (30000289, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1000),)
    }),
    80581003: _tools.RODict({
        "ID": 80581003,
        "isOpen": 1,
        "consumeItem": ((80581002, 1), (80581002, 1), (30000289, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 1500),)
    }),
    80582001: _tools.RODict({
        "ID": 80582001,
        "isOpen": 1,
        "consumeItem": ((80581003, 1), (30990125, 1), (30000292, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80582002: _tools.RODict({
        "ID": 80582002,
        "isOpen": 1,
        "consumeItem": ((80582001, 1), (80582001, 1), (30000292, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80582003: _tools.RODict({
        "ID": 80582003,
        "isOpen": 1,
        "consumeItem": ((80582002, 1), (80582002, 1), (30000292, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80582004: _tools.RODict({
        "ID": 80582004,
        "isOpen": 1,
        "consumeItem": ((80582003, 1), (80582003, 1), (30000292, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80583001: _tools.RODict({
        "ID": 80583001,
        "isOpen": 1,
        "consumeItem": ((80582004, 1), (30990132, 1), (30000295, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80583002: _tools.RODict({
        "ID": 80583002,
        "isOpen": 1,
        "consumeItem": ((80583001, 1), (80583001, 1), (30000295, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80583003: _tools.RODict({
        "ID": 80583003,
        "isOpen": 1,
        "consumeItem": ((80583002, 1), (80583002, 1), (30000295, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80583004: _tools.RODict({
        "ID": 80583004,
        "isOpen": 1,
        "consumeItem": ((80583003, 1), (80583003, 1), (30000295, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80583005: _tools.RODict({
        "ID": 80583005,
        "isOpen": 1,
        "consumeItem": ((80583004, 1), (80583004, 1), (30000295, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80584001: _tools.RODict({
        "ID": 80584001,
        "isOpen": 1,
        "consumeItem": ((80583005, 1), (30990139, 1), (30000298, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80584002: _tools.RODict({
        "ID": 80584002,
        "isOpen": 1,
        "consumeItem": ((80584001, 1), (80584001, 1), (30000298, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80584003: _tools.RODict({
        "ID": 80584003,
        "isOpen": 1,
        "consumeItem": ((80584002, 1), (80584002, 1), (30000298, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80585001: _tools.RODict({
        "ID": 80585001,
        "isOpen": 1,
        "consumeItem": ((80584003, 1), (30990146, 1), (30000298, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80682001: _tools.RODict({
        "ID": 80682001,
        "isOpen": 0,
        "consumeItem": ((30000292, 20),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80682002: _tools.RODict({
        "ID": 80682002,
        "isOpen": 1,
        "consumeItem": ((80682001, 1), (80682001, 1), (30000292, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80682003: _tools.RODict({
        "ID": 80682003,
        "isOpen": 1,
        "consumeItem": ((80682002, 1), (80682002, 1), (30000292, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80682004: _tools.RODict({
        "ID": 80682004,
        "isOpen": 1,
        "consumeItem": ((80682003, 1), (80682003, 1), (30000292, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80683001: _tools.RODict({
        "ID": 80683001,
        "isOpen": 1,
        "consumeItem": ((80682004, 1), (30990133, 1), (30000295, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80683002: _tools.RODict({
        "ID": 80683002,
        "isOpen": 1,
        "consumeItem": ((80683001, 1), (80683001, 1), (30000295, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80683003: _tools.RODict({
        "ID": 80683003,
        "isOpen": 1,
        "consumeItem": ((80683002, 1), (80683002, 1), (30000295, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80683004: _tools.RODict({
        "ID": 80683004,
        "isOpen": 1,
        "consumeItem": ((80683003, 1), (80683003, 1), (30000295, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80683005: _tools.RODict({
        "ID": 80683005,
        "isOpen": 1,
        "consumeItem": ((80683004, 1), (80683004, 1), (30000295, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80684001: _tools.RODict({
        "ID": 80684001,
        "isOpen": 1,
        "consumeItem": ((80683005, 1), (30990140, 1), (30000298, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80684002: _tools.RODict({
        "ID": 80684002,
        "isOpen": 1,
        "consumeItem": ((80684001, 1), (80684001, 1), (30000298, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80684003: _tools.RODict({
        "ID": 80684003,
        "isOpen": 1,
        "consumeItem": ((80684002, 1), (80684002, 1), (30000298, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80685001: _tools.RODict({
        "ID": 80685001,
        "isOpen": 1,
        "consumeItem": ((80684003, 1), (30990147, 1), (30000298, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80692001: _tools.RODict({
        "ID": 80692001,
        "isOpen": 0,
        "consumeItem": ((30000292, 20),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80692002: _tools.RODict({
        "ID": 80692002,
        "isOpen": 1,
        "consumeItem": ((80692001, 1), (80692001, 1), (30000292, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80692003: _tools.RODict({
        "ID": 80692003,
        "isOpen": 1,
        "consumeItem": ((80692002, 1), (80692002, 1), (30000292, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80692004: _tools.RODict({
        "ID": 80692004,
        "isOpen": 1,
        "consumeItem": ((80692003, 1), (80692003, 1), (30000292, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80693001: _tools.RODict({
        "ID": 80693001,
        "isOpen": 1,
        "consumeItem": ((80692004, 1), (30990133, 1), (30000295, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80693002: _tools.RODict({
        "ID": 80693002,
        "isOpen": 1,
        "consumeItem": ((80693001, 1), (80693001, 1), (30000295, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80693003: _tools.RODict({
        "ID": 80693003,
        "isOpen": 1,
        "consumeItem": ((80693002, 1), (80693002, 1), (30000295, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80693004: _tools.RODict({
        "ID": 80693004,
        "isOpen": 1,
        "consumeItem": ((80693003, 1), (80693003, 1), (30000295, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80693005: _tools.RODict({
        "ID": 80693005,
        "isOpen": 1,
        "consumeItem": ((80693004, 1), (80693004, 1), (30000295, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80694001: _tools.RODict({
        "ID": 80694001,
        "isOpen": 1,
        "consumeItem": ((80693005, 1), (30990140, 1), (30000298, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80694002: _tools.RODict({
        "ID": 80694002,
        "isOpen": 1,
        "consumeItem": ((80694001, 1), (80694001, 1), (30000298, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80694003: _tools.RODict({
        "ID": 80694003,
        "isOpen": 1,
        "consumeItem": ((80694002, 1), (80694002, 1), (30000298, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80695001: _tools.RODict({
        "ID": 80695001,
        "isOpen": 1,
        "consumeItem": ((80694003, 1), (30990147, 1), (30000298, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80703001: _tools.RODict({
        "ID": 80703001,
        "isOpen": 1,
        "consumeItem": ((80693001, 1), (30000295, 20)),
        "consumeItem2": ((80693001, 1), (30000295, 20)),
        "consumeMoney": ((30000013, 4000),)
    }),
    80703002: _tools.RODict({
        "ID": 80703002,
        "isOpen": 1,
        "consumeItem": ((80703001, 1), (80703001, 1), (30000295, 40)),
        "consumeItem2": ((80703001, 1), (80703001, 1), (30000295, 40)),
        "consumeMoney": ((30000013, 6000),)
    }),
    80703003: _tools.RODict({
        "ID": 80703003,
        "isOpen": 1,
        "consumeItem": ((80703002, 1), (80703002, 1), (30000295, 60)),
        "consumeItem2": ((80703002, 1), (80703002, 1), (30000295, 60)),
        "consumeMoney": ((30000013, 9000),)
    }),
    80703004: _tools.RODict({
        "ID": 80703004,
        "isOpen": 1,
        "consumeItem": ((80703003, 1), (80703003, 1), (30000295, 80)),
        "consumeItem2": ((80703003, 1), (80703003, 1), (30000295, 80)),
        "consumeMoney": ((30000013, 12000),)
    }),
    80703005: _tools.RODict({
        "ID": 80703005,
        "isOpen": 1,
        "consumeItem": ((80703004, 1), (80703004, 1), (30000295, 100)),
        "consumeItem2": ((80703004, 1), (80703004, 1), (30000295, 100)),
        "consumeMoney": ((30000013, 15000),)
    }),
    80704001: _tools.RODict({
        "ID": 80704001,
        "isOpen": 1,
        "consumeItem": ((80703005, 1), (30990140, 1), (30000298, 20)),
        "consumeItem2": ((80703005, 1), (30990140, 1), (30000298, 20)),
        "consumeMoney": ((30000013, 40000),)
    }),
    80704002: _tools.RODict({
        "ID": 80704002,
        "isOpen": 1,
        "consumeItem": ((80704001, 1), (80704001, 1), (30000298, 40)),
        "consumeItem2": ((80704001, 1), (80704001, 1), (30000298, 40)),
        "consumeMoney": ((30000013, 60000),)
    }),
    80704003: _tools.RODict({
        "ID": 80704003,
        "isOpen": 1,
        "consumeItem": ((80704002, 1), (80704002, 1), (30000298, 60)),
        "consumeItem2": ((80704002, 1), (80704002, 1), (30000298, 60)),
        "consumeMoney": ((30000013, 90000),)
    }),
    80705002: _tools.RODict({
        "ID": 80705002,
        "isOpen": 1,
        "consumeItem": ((80704003, 1), (30990147, 1), (30000298, 200)),
        "consumeItem2": ((80704003, 1), (30990147, 1), (30000298, 200)),
        "consumeMoney": ((30000013, 180000),)
    }),
    80782001: _tools.RODict({
        "ID": 80782001,
        "isOpen": 0,
        "consumeItem": ((30000292, 20),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80782002: _tools.RODict({
        "ID": 80782002,
        "isOpen": 1,
        "consumeItem": ((80782001, 1), (80782001, 1), (30000292, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80782003: _tools.RODict({
        "ID": 80782003,
        "isOpen": 1,
        "consumeItem": ((80782002, 1), (80782002, 1), (30000292, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80782004: _tools.RODict({
        "ID": 80782004,
        "isOpen": 1,
        "consumeItem": ((80782003, 1), (80782003, 1), (30000292, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80783001: _tools.RODict({
        "ID": 80783001,
        "isOpen": 1,
        "consumeItem": ((80782004, 1), (30990134, 1), (30000295, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80783002: _tools.RODict({
        "ID": 80783002,
        "isOpen": 1,
        "consumeItem": ((80783001, 1), (80783001, 1), (30000295, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80783003: _tools.RODict({
        "ID": 80783003,
        "isOpen": 1,
        "consumeItem": ((80783002, 1), (80783002, 1), (30000295, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80783004: _tools.RODict({
        "ID": 80783004,
        "isOpen": 1,
        "consumeItem": ((80783003, 1), (80783003, 1), (30000295, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80783005: _tools.RODict({
        "ID": 80783005,
        "isOpen": 1,
        "consumeItem": ((80783004, 1), (80783004, 1), (30000295, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80784001: _tools.RODict({
        "ID": 80784001,
        "isOpen": 1,
        "consumeItem": ((80783005, 1), (30990141, 1), (30000298, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80784002: _tools.RODict({
        "ID": 80784002,
        "isOpen": 1,
        "consumeItem": ((80784001, 1), (80784001, 1), (30000298, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80784003: _tools.RODict({
        "ID": 80784003,
        "isOpen": 1,
        "consumeItem": ((80784002, 1), (80784002, 1), (30000298, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80785001: _tools.RODict({
        "ID": 80785001,
        "isOpen": 1,
        "consumeItem": ((80784003, 1), (30990148, 1), (30000298, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80792001: _tools.RODict({
        "ID": 80792001,
        "isOpen": 0,
        "consumeItem": ((30000292, 20),),
        "consumeItem2": None,
        "consumeMoney": ((30000002, 2000),)
    }),
    80792002: _tools.RODict({
        "ID": 80792002,
        "isOpen": 1,
        "consumeItem": ((80792001, 1), (80792001, 1), (30000292, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 500),)
    }),
    80792003: _tools.RODict({
        "ID": 80792003,
        "isOpen": 1,
        "consumeItem": ((80792002, 1), (80792002, 1), (30000292, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 1000),)
    }),
    80792004: _tools.RODict({
        "ID": 80792004,
        "isOpen": 1,
        "consumeItem": ((80792003, 1), (80792003, 1), (30000292, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 2000),)
    }),
    80793001: _tools.RODict({
        "ID": 80793001,
        "isOpen": 1,
        "consumeItem": ((80792004, 1), (30990134, 1), (30000295, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 4000),)
    }),
    80793002: _tools.RODict({
        "ID": 80793002,
        "isOpen": 1,
        "consumeItem": ((80793001, 1), (80793001, 1), (30000295, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 6000),)
    }),
    80793003: _tools.RODict({
        "ID": 80793003,
        "isOpen": 1,
        "consumeItem": ((80793002, 1), (80793002, 1), (30000295, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 9000),)
    }),
    80793004: _tools.RODict({
        "ID": 80793004,
        "isOpen": 1,
        "consumeItem": ((80793003, 1), (80793003, 1), (30000295, 80)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 12000),)
    }),
    80793005: _tools.RODict({
        "ID": 80793005,
        "isOpen": 1,
        "consumeItem": ((80793004, 1), (80793004, 1), (30000295, 100)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 15000),)
    }),
    80794001: _tools.RODict({
        "ID": 80794001,
        "isOpen": 1,
        "consumeItem": ((80793005, 1), (30990141, 1), (30000298, 20)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 40000),)
    }),
    80794002: _tools.RODict({
        "ID": 80794002,
        "isOpen": 1,
        "consumeItem": ((80794001, 1), (80794001, 1), (30000298, 40)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 60000),)
    }),
    80794003: _tools.RODict({
        "ID": 80794003,
        "isOpen": 1,
        "consumeItem": ((80794002, 1), (80794002, 1), (30000298, 60)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 90000),)
    }),
    80795001: _tools.RODict({
        "ID": 80795001,
        "isOpen": 1,
        "consumeItem": ((80794003, 1), (30990148, 1), (30000298, 200)),
        "consumeItem2": None,
        "consumeMoney": ((30000013, 180000),)
    }),
    80803001: _tools.RODict({
        "ID": 80803001,
        "isOpen": 1,
        "consumeItem": ((80793001, 1), (30000295, 20)),
        "consumeItem2": ((80793001, 1), (30000295, 20)),
        "consumeMoney": ((30000013, 4000),)
    }),
    80803002: _tools.RODict({
        "ID": 80803002,
        "isOpen": 1,
        "consumeItem": ((80803001, 1), (80803001, 1), (30000295, 40)),
        "consumeItem2": ((80803001, 1), (80803001, 1), (30000295, 40)),
        "consumeMoney": ((30000013, 6000),)
    }),
    80803003: _tools.RODict({
        "ID": 80803003,
        "isOpen": 1,
        "consumeItem": ((80803002, 1), (80803002, 1), (30000295, 60)),
        "consumeItem2": ((80803002, 1), (80803002, 1), (30000295, 60)),
        "consumeMoney": ((30000013, 9000),)
    }),
    80803004: _tools.RODict({
        "ID": 80803004,
        "isOpen": 1,
        "consumeItem": ((80803003, 1), (80803003, 1), (30000295, 80)),
        "consumeItem2": ((80803003, 1), (80803003, 1), (30000295, 80)),
        "consumeMoney": ((30000013, 12000),)
    }),
    80803005: _tools.RODict({
        "ID": 80803005,
        "isOpen": 1,
        "consumeItem": ((80803004, 1), (80803004, 1), (30000295, 100)),
        "consumeItem2": ((80803004, 1), (80803004, 1), (30000295, 100)),
        "consumeMoney": ((30000013, 15000),)
    }),
    80804001: _tools.RODict({
        "ID": 80804001,
        "isOpen": 1,
        "consumeItem": ((80803005, 1), (30990141, 1), (30000298, 20)),
        "consumeItem2": ((80803005, 1), (30990141, 1), (30000298, 20)),
        "consumeMoney": ((30000013, 40000),)
    }),
    80804002: _tools.RODict({
        "ID": 80804002,
        "isOpen": 1,
        "consumeItem": ((80804001, 1), (80804001, 1), (30000298, 40)),
        "consumeItem2": ((80804001, 1), (80804001, 1), (30000298, 40)),
        "consumeMoney": ((30000013, 60000),)
    }),
    80804003: _tools.RODict({
        "ID": 80804003,
        "isOpen": 1,
        "consumeItem": ((80804002, 1), (80804002, 1), (30000298, 60)),
        "consumeItem2": ((80804002, 1), (80804002, 1), (30000298, 60)),
        "consumeMoney": ((30000013, 90000),)
    }),
    80805001: _tools.RODict({
        "ID": 80805001,
        "isOpen": 1,
        "consumeItem": ((80804003, 1), (30990148, 1), (30000298, 200)),
        "consumeItem2": ((80804003, 1), (30990148, 1), (30000298, 200)),
        "consumeMoney": ((30000013, 180000),)
    })
})
minKey = 80111001
maxKey = 80805001