import sys
import time
import os
from simpleBotBase import FACE_DATA

# 添加loginserver参数：modName, botPrefix, numAll, numPerSec, fromIdx, avatarName, school, loginHost, loginPort
modName, _botNamePrefix, _numAll, _numPerSec, _fromIdx, _avatarName, _school, _loginHost, _loginPort = sys.argv[1:10]

if modName.endswith('.py'):
    modName = os.path.splitext(modName)[0]

mod = __import__(modName)
import BotClient

if not hasattr(mod, 'DELEGATE_CLS'):
    print('%s has no attribute DELEGATE_CLS' % modName)
    exit(-1)


def startBot(delegateCls, botPrefix, numAll, numPerSec, fromIdx, avatarName, school, loginHost, loginPort):
    ts = []
    print('start bot from', fromIdx)
    print(f'target login server: {loginHost}:{loginPort}')
    import random
    faceData = FACE_DATA()
    for i in range(numAll):
        idx = fromIdx + i
        random_school = school
        if random_school == 0:
            random_school = random.choice([1001,1002,1003])
            print(f"{'%s%d' % (avatarName, idx)}机器人随机选择职业{random_school}")
        faceData.random_set_face_data_by_id(random_school)
        client = BotClient.BotClient('%s%d' % (botPrefix, idx), '%s%d' % (avatarName, idx), random_school,faceData.toSavedDict())
        # 如果提供了登录服务器地址和端口，则使用指定服务器登录
        if loginHost and loginPort and loginHost.strip() and loginPort.strip():
            print(f'bot {idx} logging to server: {loginHost}:{loginPort}')
            robot = client.login(accountType=0, loginAddr=loginHost.strip(), loginPort=int(loginPort))
        else:
            print(f'bot {idx} logging to default server')
            robot = client.login()
            
        robot.setPlayerDelegate(delegateCls(robot, client))
        ts.append(client.tickThread)

        if (i + 1) % numPerSec == 0:
            time.sleep(1)

    print(f"总共创建了 {len(ts)} 个机器人，目标服务器: {loginHost}:{loginPort}")
    for t in ts:
        t.join()


if __name__ == '__main__':
    time.sleep(10)
    startBot(getattr(mod, 'DELEGATE_CLS'), _botNamePrefix, int(_numAll), int(_numPerSec), 
             int(_fromIdx), str(_avatarName), int(_school), str(_loginHost), str(_loginPort))
