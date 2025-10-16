# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import utils
import gameconst
import time


class DateType():
    DAY = 1
    WEEK = 2
    MONTH = 3   # 暂未实现

class IDateData(object):
    """
    提供按日、按周、按月过期的通用数据支持
    1.使用
        直接使用 self.getDailyData(key, default) 等方法即可
        推荐使用 self.addDailyData(key, val) 方法增加数据
        谨慎使用 self.setDailyData(key, val) 方法设置数据。 如要使用，确保先 getDailyData(key) 再设置

        搭配 gameconst.AvatarDailyProps 里面的属性字段作为key使用，防止key冲突。
        注：AvatarDailyProps 仅为 avatar 的专属。如果用在其他stub上，需自定义新的类作为key的集合

        对过期数据处理时，提供 onExpireDailyData(key, val) 和 onExpireWeeklyData(key, val) 的回调处理。

    2.注意
        最好只存int类型数据, 复杂数据不适用


    3.示例
        可查看 iRedBag.py 中的使用示例
    
    
    """
    # def __init__(self):
        # 初始化
        # if len(self.dateTimeDataDict) == 0:
        #     self._calcNextUpdateTime()

        
    def _calcNextUpdateTime(self):
        tNow = time.time()
        self.dateTimeDataDict[DateType.DAY] = self._calcDailyUpdateTime(tNow)

        self.dateTimeDataDict[DateType.WEEK] = self._calcWeeklyUpdateTime(tNow)

    def _calcDailyUpdateTime(self, tNow):
        tUpdate = utils.getCurrentDayTS(offsetSec=gameconst.COMMON_CYCLE_TIME)
        if tUpdate <= tNow:
            tUpdate += gameconst.ONE_DAY_SECONDS

        return tUpdate

    def _calcWeeklyUpdateTime(self, tNow):
        tUpdate = utils.getCurrentWeekTS(offsetSec=gameconst.COMMON_CYCLE_TIME)
        if tUpdate <= tNow:
            tUpdate += gameconst.WEEK_SENCONDS

        return tUpdate
   
    def checkDataExpire(self):
        tNow = time.time()
        updateTime = self.dateTimeDataDict.get(DateType.DAY, 0)
        if updateTime < tNow:
            self.onDayChanged(updateTime, tNow)

        updateTime = self.dateTimeDataDict.get(DateType.WEEK, 0)
        if updateTime < tNow:
            self.onWeekChanged(updateTime, tNow)


    def onDayChanged(self, lastUpdateTime, now):
        INFO_MSG("IDateData::onDayChanged: %i => %i" % (lastUpdateTime, now))
        try:
            for key, val in self.dateDailyDataDict.items():
                self.onExpireDailyData(key, val)
        except Exception as e:
            ERROR_MSG("IDateData::onDayChanged error: %s" % e)

        self.dateTimeDataDict[DateType.DAY] = self._calcDailyUpdateTime(now)
        self.dateDailyDataDict.clear()
    
    def onExpireDailyData(self, key, val):
        INFO_MSG('dateData daily expire')
        

    def onWeekChanged(self, lastUpdateTime, now):
        INFO_MSG("IDateData::onWeekChanged: %i => %i" % (lastUpdateTime, now))
        try:
            for key, val in self.dateWeeklyDataDict.items():
                self.onExpireWeeklyData(key, val)
        except Exception as e:
            ERROR_MSG("IDateData::onWeekChanged error: %s" % e)

        self.dateTimeDataDict[DateType.WEEK] = self._calcWeeklyUpdateTime(now)
        self.dateWeeklyDataDict.clear()
    
    def onExpireWeeklyData(self, key, val):
        INFO_MSG('dateData weekly expire')

    def checkKeyValid(self, key):
        if key not in gameconst.AvatarDailyProps.__dict__.values():
            raise ValueError("IDateData::checkKeyValid: invalid daily key ", key)

    def getDailyData(self, key, default=0):
        self.checkDataExpire()
        return self.dateDailyDataDict.get(key, default)
    

    def setDailyData(self, key, val):
        self.dateDailyDataDict[key] = val

    def addDailyData(self, key, val=1):
        oldVal = self.getDailyData(key, 0)
        newVal = oldVal + val
        self.dateDailyDataDict[key] = newVal


    def getWeeklyData(self, key, default=0):
        self.checkDataExpire()       
        return self.dateWeeklyDataDict.get(key, default)
    
    def setWeeklyData(self, key, val):
        self.dateWeeklyDataDict[key] = val

    def addWeeklyData(self, key, val=1):
        oldVal = self.getWeeklyData(key, 0)
        newVal = oldVal + val
        self.dateWeeklyDataDict[key] = newVal

    def gmGetDateData(self):
        INFO_MSG('dateTimeDataDict: ', self.dateTimeDataDict)
        INFO_MSG('dayUpdateTimeStamp: ', utils.getTimeStr(self.dateTimeDataDict[DateType.DAY]), utils.getTimeStr(self.dateTimeDataDict[DateType.WEEK]))
        INFO_MSG('dateDailyDataDict: ', self.dateDailyDataDict)
        INFO_MSG('dateWeeklyDataDict: ', self.dateWeeklyDataDict)
