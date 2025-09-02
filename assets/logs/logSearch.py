# -*- coding: utf-8 -*-

import argparse
import glob
import os
import time
import re
import sys
import io
#import locale

if not sys.stdout.isatty():
    sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)

blockSize = 100*1024

component2FileName = {
    'loggerbaseapp': 'logger_baseapp.log',
    'baseapp': 'baseapp_',
    'loggercellapp': 'logger_cellapp.log',
    'cellapp': 'cellapp_',
    'dbmgr': 'logger_dbmgr.log'
}

levelKeywords = {
    'debug': ['DEBUG', 'S_DBG', 'INFO', 'S_INFO', 'WARNING', 'S_WARN', 'ERROR', 'S_ERR'],
    'info': ['INFO', 'S_INFO', 'WARNING', 'S_WARN', 'ERROR', 'S_ERR'],
    'warn': ['WARNING', 'S_WARN', 'ERROR', 'S_ERR'],
    'error': ['ERROR', 'S_ERR']
}
levelList = ['DEBUG', 'S_DBG', 'INFO', 'S_INFO', 'WARNING', 'S_WARN', 'ERROR', 'S_ERR']

args = None

def str2Time(arg):
    if not re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', arg):
        raise argparse.ArgumentTypeError('Unsupported value, correct format: %Y-%m-%d %H:%M:%S, input='+arg)

    return arg

def str2Component(arg):

    components = arg.split(',')
    for component in components:
        if component not in component2FileName.keys():
            raise argparse.ArgumentTypeError("Unsupported value, please select in %s" % str(component2FileName.keys()))

    return components

def logInputDir(arg):
    if not os.path.exists(arg):
        raise argparse.ArgumentTypeError("Unsupported value, dir not exist")

    if not os.path.isdir(arg):
        raise argparse.ArgumentTypeError("Unsupported value, please use correct dir")

    os.chdir(arg)
    return arg

def str2DisplayNum(arg):
    if not arg.isdigit():
        raise argparse.ArgumentTypeError("Unsupported value, not digit")

    arg = int(arg)
    if arg < 1 or arg > 10000:
        raise argparse.ArgumentTypeError("Unsupported value, valid value in [1,10000]")

    return arg

def parseArgs():
    parser = argparse.ArgumentParser(description='use for search kbengine log file')
    parser.add_argument('-c', '--component',default='baseapp,cellapp,dbmgr,loggerbaseapp,loggercellapp',
                        help="component name, choice in ['baseapp', 'cellapp', 'dbmgr', 'loggerbaseapp', 'loggercellapp']. default search all component, use ',' to search multi component, for example: loggerbaseapp,loggercellapp",
                        type=str2Component)
    parser.add_argument('-s', '--starttime', help='log start time', type=str2Time, required=True)
    parser.add_argument('-e', '--endtime', help='log end time', type=str2Time)
    parser.add_argument('-l', '--level', help='log level', choices=['debug', 'info', 'warn', 'error'])
    parser.add_argument('-m', '--maximum', type=int, help='maximum number of log rows searched')
    parser.add_argument('-i', '--input', help='the path where the log file is located', type=logInputDir)
    parser.add_argument('-n', '--number', help='number of log rows display', type=str2DisplayNum)
    global args
    args = parser.parse_args()


def fileSuffix(filename):
    suffix = re.search(r'\.(\d+)$', filename)
    return int(suffix.group(1)) if suffix else 0

def fileSuffixDate(filename):
    suffix = re.search(r'\.(\d{4}-\d{2}-\d{2}.*)$', filename)
    suffixDate = suffix.group(1) if suffix else 0
    if suffixDate :
        if len(suffixDate.split('-')) == 3:
            datetimeVal = time.strptime(suffixDate, '%Y-%m-%d')
        elif len(suffixDate.split('-')) == 4:
            datetimeVal = time.strptime(suffixDate, '%Y-%m-%d-%H')
        return int(time.mktime(datetimeVal))
    else :
        return sys.maxsize

def getTargetFiles():
    # dirs = os.listdir(os.getcwd())
    targetFiles = {}
    for element in args.component:
        targetFiles[element] = []

    dirs = glob.iglob(os.path.join(os.getcwd(), '*'))
    for file in dirs:
        # print('####file',file)
        if os.path.isfile(file):
            for element in args.component:
                # print('####element', element,component2FileName[element])
                if component2FileName[element] in file:
                    targetFiles[element].append(file)
                    break
    # print('##targetFiles',targetFiles)
    for files in targetFiles.values():
        files.sort(key=fileSuffixDate, reverse=False)

    filterFileByTime(targetFiles)

    return targetFiles

def filterFileByTime(targetFiles):
    for component, files in targetFiles.items():
        if component in ('loggerbaseapp','loggercellapp','dbmgr') :
            left, right = searchRange(files)

            if left != -1 and right != -1:
                targetFiles[component] = files[left:right+1]
            else:
                targetFiles[component] = []
        else :
            targetFiles[component] = searchRangeSingle(files)

def searchRange(files):
    if not files:
        return -1, -1

    low = 0
    high = len(files)-1

    while low < high:

        mid = (low + high) // 2
        if getMaxLogTime(files[mid]) >= args.starttime:
            high = mid
        else:
            low = mid + 1
    if getMaxLogTime(files[low]) >= args.starttime:
        left = low
    else:
        left = -1

    right = len(files)-1
    if args.endtime:
        low = 0
        high = len(files)-1
        while low < high:
            mid = (low + high) // 2
            if getMinLogTime(files[mid]) > args.endtime:
                high = mid - 1
            else:
                if low == mid:
                    if getMinLogTime(files[high]) <= args.endtime:
                        low = high
                    break
                else:
                    low = mid
        if getMinLogTime(files[low]) <= args.endtime:
            right = low
        else:
            right = -1

    return left, right

def searchRangeSingle(files):
    fileList = []
    for file in files :
        if getMinLogTime(file) > args.endtime or getMaxLogTime(file) < args.starttime :
            continue
        fileList.append(file)
    return fileList

def isLogFileInTime(filepath):
    minTime = getMinLogTime(filepath)
    if args.endtime and minTime > args.endtime:
        return False

    maxTime = getMaxLogTime(filepath)
    if maxTime < args.starttime:
        return False

    return True

def getMaxLogTime(filepath):
    fsize = os.path.getsize(filepath)
    fseek = (fsize - blockSize if fsize > blockSize else 0)

    with open(filepath, 'rb') as f:
        while fseek >= 0:
            f.seek(fseek, 0)
            logs = f.readlines(blockSize)

            if logs:
                for i in range(len(logs) - 1, -1, -1):
                    try:
                        date, millsec = getLogTime(logs[i].decode())
                    except:
                        continue
                    else:
                        if date:
                            return date
            if not fseek:
                break
            fseek = (fseek - blockSize if fseek > blockSize else 0)

    return '9999-99-99 99:99:99'

def getMinLogTime(filepath):
    with open(filepath, 'rb') as f:
        log = f.readline()
        if log:
            try:
                date, millsec = getLogTime(log.decode())
            except:
                return

            if date:
                return date

    return '0000-00-00 00:00:00'

def getOffsetByStartTime(filepath, startTime):
    offset = 0
    fstart = 0
    # print("####", startTime)
    fend = os.path.getsize(filepath)

    with open(filepath, 'rb') as f:
        datas = f.readlines(blockSize)
        startdate=""
        for i in range( 0, len(datas) - 1, 1):
            try:
                sdate, startmillsec = getLogTime(datas[i].decode())
            except:
                continue
            else:
                if sdate:
                    startdate = sdate
                    break

        enddate=""
        for i in range(len(datas) - 1, -1, -1):
            try:
                edate, endmillsec = getLogTime(datas[i].decode())
            except:
                continue
            else:
                if edate:
                    enddate = edate
                    break
        # print("####", startdate,enddate,startTime)
        if startdate > startTime or enddate == "" or startdate == "":
            offset = 0
        else:
            while fstart < fend:
                # print("start###",(offset, fstart, fend))
                fseek = (fstart + fend) // 2
                f.seek(fseek, 0)
                offdatas = f.readlines(blockSize)
                startdate = ""

                for i in range(0, len(offdatas) - 1, 1):
                    try:
                        sdate, startmillsec = getLogTime(offdatas[i].decode())
                    except:
                        continue
                    if sdate:
                        startdate = sdate
                        break

                enddate = ""
                for i in range(len(offdatas) - 1, -1, -1):
                    try:
                        edate, endmillsec = getLogTime(offdatas[i].decode())
                    except:
                        continue
                    else:
                        if edate:
                            enddate = edate
                            break

                if startdate == "" and enddate == "" :
                    startdate,enddate = noTimeCalStart(filepath,fseek)
                    
                # print("======",startdate,enddate)
                if startdate <= startTime and enddate >= startTime:
                    # print("======",startdate,enddate)
                    offset = innerCalStart(filepath,fseek,startTime)
                    # offset = fseek
                    break
                elif startdate > startTime:
                    fend=fseek-1
                elif enddate < startTime :
                    fstart = fseek +blockSize+1
    return offset

def noTimeCalStart(filepath,fseek):
    MAX_DOUBLESIZE = 5
    with open(filepath, 'rb') as f:
        for i in range(MAX_DOUBLESIZE):
            f.seek(fseek, 0)
            multi = 2**(i+1)
            datas = f.readlines(blockSize*multi)
            startdate = ""
            for i in range(0, len(datas) - 1, 1):
                try:
                    sdate, startmillsec = getLogTime(datas[i].decode())
                except:
                    continue
                else:
                    if sdate:
                        startdate = sdate
                        break

            enddate = ""
            for i in range(len(datas) - 1, -1, -1):
                try:
                    edate, endmillsec = getLogTime(datas[i].decode())
                except:
                    continue
                else:
                    if edate:
                        enddate = edate
                        break

            if startdate != "" and enddate != "":
                break

    return startdate,enddate

def innerCalStart(filepath,fstart,startTime):
    offset = 0
    with open(filepath, 'rb') as f:
        f.seek(fstart, 0)
        datas = f.readlines(blockSize)

        for i in range( 1, len(datas) - 1, 1):
            try:
                sdate, startmillsec = getLogTime(datas[i].decode())
            except:
                offset += len(datas[i - 1])
                continue
            else:
                if sdate >= startTime:
                    break
                else:
                    offset+=len(datas[i-1])
    return fstart+offset

class logReader(object):
    def __init__(self, component, filepath, isHead, isTail):
        self.component = component
        self.fileHandler = open(filepath, 'rb')
        self.date = ''
        self.millsec = 0
        self.cacheLogs = []
        self.index = 0
        self.isTail = isTail
        self.curLevel = None
        # print(">>>isHead",isHead)
        # if isHead:
        offset = getOffsetByStartTime(filepath, args.starttime)
        # print('####offset',offset)
        self.fileHandler.seek(offset, 0)

    def __del__(self):
        self.fileHandler.close()

    def __cmp__(self, other):
        if self.__eq__(other):
            return 0
        elif self.__lt__(other):
            return -1
        elif self.__gt__(other):
            return 1

    def __eq__(self, other):
        if not isinstance(other, logReader):
            raise TypeError("can't cmp other type to logReader")

        if self.date == other.date and self.millsec == other.millsec:
            return True
        else:
            return False

    def __lt__(self, other):
        if not isinstance(other, logReader):
            raise TypeError("can't cmp other type to logReader")

        if self.date < other.date:
            return True
        elif self.date == other.date and self.millsec < other.millsec:
            return True
        else:
            return False

    def __gt__(self, other):
        if not isinstance(other, logReader):
            raise TypeError("can't cmp other type to logReader")

        if self.date > other.date:
            return True
        elif self.date == other.date and self.millsec > other.millsec:
            return True
        else:
            return False

    def readNextLog(self):
        while True:
            self.index += 1
            if self.index >= len(self.cacheLogs):
                lines = self.fileHandler.readlines(blockSize)
                cacheLines = []
                for line in lines:
                    try:
                        cacheLines.append(line.decode('utf-8'))
                    except Exception as e:
                        #print('line decode error:', e, line)
                        cacheLines.append(repr(line)[1:].strip('b\''))
                self.cacheLogs = cacheLines
                if not self.cacheLogs:
                    break
                self.index = 0

            if self.cacheLogs[self.index] == '\n':
                continue

            if args.level:
                level = re.search(r'(\s+)(\w+)(\s+)', self.cacheLogs[self.index])
                if not level:
                    if self.curLevel and self.curLevel in levelKeywords[args.level]:
                        print('          {}'.format(self.cacheLogs[self.index]), end='')
                    continue

                if level.group(2) not in levelList:
                    if self.curLevel and self.curLevel in levelKeywords[args.level]:
                        print('          {}'.format(self.cacheLogs[self.index]), end='')
                    continue

                self.curLevel = level.group(2)
                if level.group(2) not in levelKeywords[args.level]:
                    continue
            # print('######index', self.index, self.cacheLogs[self.index])
            self.date, self.millsec = getLogTime(self.cacheLogs[self.index])
            # print('######date',self.date,self.isTail,args.endtime)
            if self.date:
                if self.isTail and args.endtime and self.date > args.endtime:
                    return False
                else:
                    return True

            print('          {}'.format(self.cacheLogs[self.index]), end='')

        return False

    def getCurLog(self):
        return self.cacheLogs[self.index]

def searchMultiComponetLogs(targetFiles):
    logReaders = []
    logCnt = 0

    for component in args.component:
        head = True
        while targetFiles[component]:
            filepath = targetFiles[component].pop(0)
            reader = logReader(component, filepath, head, True)
            if reader.readNextLog():
                logReaders.append(reader)

            head = False
    # print(logReaders)
    pauseNum = 0
    while logReaders:
        if args.maximum:
            if args.maximum == logCnt:
                break

        if args.number == pauseNum:
            yield True, logCnt
            pauseNum = 0

        reader = min(logReaders)
        logCnt += 1
        pauseNum += 1
        print('{0}'.format(reader.getCurLog()), end='')

        while not reader.readNextLog():
            if targetFiles[reader.component]:
                filepath = targetFiles[reader.component].pop(0)
                newReader = logReader(reader.component, filepath, False, False if targetFiles[reader.component] else True)
                logReaders[logReaders.index(reader)] = newReader
                reader = newReader
            else:
                logReaders.remove(reader)
                break

    yield False, logCnt

##暂时不用
def searchSingleComponetLogs(targetFiles):
    logReaders = []
    component = args.component[0]
    logCnt = 0

    if targetFiles[component]:
        filepath = targetFiles[component].pop(0)
        reader = logReader(component, filepath, True, False if targetFiles[component] else True)
    else:
        yield False, logCnt


    pauseNum = 0
    while True:
        if not reader.readNextLog():
            if targetFiles[component]:
                filepath = targetFiles[component].pop(0)
                reader = logReader(component, filepath, False, False if targetFiles[component] else True)
                continue
            else:
                break

        if args.maximum:
            if args.maximum == logCnt:
                break

        if args.number == pauseNum:
            yield True, logCnt
            pauseNum = 0

        logCnt += 1
        pauseNum += 1
        print('{0}'.format(reader.getCurLog()), end='')

    yield False, logCnt

def getLogTime(log):
    # print('####getLogTime',log)
    timeStr = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})[\s|,](\d{3})]', log)
    # print('####timeStr',timeStr)
    if timeStr:
        # print('##',timeStr.group(1),int(timeStr.group(2)))
        return timeStr.group(1), int(timeStr.group(2))
    else:
        return '', 0

if __name__ == "__main__":
    # print('系统编码:',locale.getdefaultlocale())
    # print('代码编码:',sys.getdefaultencoding())
    # print('终端输入编码:', sys.stdout.encoding)
    # print('终端输出编码:',sys.stdout.encoding)
    parseArgs()
    targetFiles = getTargetFiles()

    # print(targetFiles)

    # if len(args.component) == 1:
    #     logGen = searchSingleComponetLogs(targetFiles)
    # else:
    logGen = searchMultiComponetLogs(targetFiles)

    while True:
        moreLogs, logCnt = next(logGen, False)
        if moreLogs:
            if args.number:
                while True:
                    inputStr = input('search continue? y/n:  ').lower()
                    if inputStr == 'y':
                        break
                    elif inputStr == 'n':
                        sys.exit()
                    else:
                        print('illegal input, try again')
        else:
            print('\nEnd search, find {0} logs'.format(logCnt))
            sys.exit()
