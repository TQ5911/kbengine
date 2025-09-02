import sys
import time
import os

modName, _botNamePrefix, _numAll, _numPerSec, _fromIdx,_avatarName,_school = sys.argv[1:8]

if modName.endswith('.py'):
    modName = os.path.splitext(modName)[0]

mod = __import__(modName)
import BotClient

if not hasattr(mod, 'DELEGATE_CLS'):
    print('%s has no attribute DELEGATE_CLS' % modName)
    exit(-1)


def startBot(delegateCls, botPrefix, numAll, numPerSec, fromIdx,avatarName,school):
    ts = []
    print('start bot from', fromIdx)
    for i in range(numAll):
        idx = fromIdx + i
        client = BotClient.BotClient('%s%d' % (botPrefix, idx),'%s%d' % (avatarName, idx),school)
        robot = client.login()
        robot.setPlayerDelegate(delegateCls(robot, client))

        ts.append(client.tickThread)

        if (i + 1) % numPerSec == 0:
            time.sleep(1)

    for t in ts:
        t.join()


if __name__ == '__main__':
    time.sleep(10)
    startBot(getattr(mod, 'DELEGATE_CLS'), _botNamePrefix, int(_numAll), int(_numPerSec), int(_fromIdx),str(_avatarName),int(_school))
