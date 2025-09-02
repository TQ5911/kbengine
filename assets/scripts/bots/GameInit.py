import os
import sys
import threading
import subprocess

class RepeatTimer(threading.Thread):
    def __init__(self, delay, interval, onTimerCall, stopEvent):
        threading.Thread.__init__(self)
        self.delay = delay
        self.interval = interval
        self.onTimerCall = onTimerCall
        self.stopEvent = stopEvent

    def run(self):
        if not self.stopEvent.wait(self.delay):
            self.onTimerCall()

        while not self.stopEvent.wait(self.interval):
            self.onTimerCall()

def getCmdOut(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    except:
        print('exec cmd error:', cmd)
        output = ''

    return output

def init():
    curFileDir = getCmdOut('pwd')
    root = os.path.sep.join(curFileDir.split(os.path.sep)[:-2])
    os.environ['KBE_ROOT'] = root
    os.environ['KBE_RES_PATH'] = root + '/res;'+ root + '/kbe_res;'+ root + ';' + root + '/scripts/'

    myPathList = []
    myPathList.append(root + '/scripts/common')
    myPathList.append(root + '/scripts/data')
    myPathList.append(root + '/scripts/user_type')
    myPathList.append(root + '/scripts/bots')
    myPathList.append(root + '/scripts/bots/interfaces')
    myPathList.append(root + '/scripts/bots/components')
    myPathList.append(root + '/scripts/common/Lib')
    myPathList.append(root + '/scripts/server_common')
    myPathList.append(root + '/kbe_res/scripts')
    myPathList.append(root + '/kbe_res/scripts/common')
    myPathList.append(root + '/kbe_res/scripts/common/lib-dynload')
    myPathList.append(root + '/kbe_res/scripts/common/DLLs')
    myPathList.append(root + '/kbe_res/scripts/common/Lib')
    myPathList.append(root + '/kbe_res/scripts/common/Lib/site-packages')
    myPathList.append(root + '/kbe_res/scripts/common/Lib/dist-packages')
    for p in myPathList:
        sys.path.append(p)

    import XZJ
    XZJ.init()
    import KBEngine

    t = RepeatTimer(0.1, 0.1, KBEngine.gameMainTick, threading.Event())
    t.setDaemon(True)
    t.start()
