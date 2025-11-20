import random
import math
import Math


def getRandomPos(pos, radius):
    """获取指定范围内的随机位置"""
    angle = random.uniform(0, 2 * 3.1415926)
    r = random.uniform(0, radius)
    new_x = pos[0] + r * math.cos(angle)
    new_y = pos[1] + r * math.sin(angle)
    return (new_x, new_y, pos[2])
    
def getRandomPosVec3(pos, radius):
    """获取指定范围内的随机位置，返回Vector3格式"""
    angle = random.uniform(0, 2 * 3.1415926)
    r = random.uniform(0, radius)
    new_x = pos.x + r * math.cos(angle)
    new_z = pos.z + r * math.sin(angle)
    return Math.Vector3(new_x, pos.y, new_z)

def distance2D(pos1, pos2):
    """计算二维平面上的距离"""
    return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.z - pos2.z) ** 2)