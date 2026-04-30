#-*- coding: utf-8 -*-

import random
import sys
import math
import Math

try:
    import cSMath
except ImportError:
    cSMath = {}

################################################
def __script_inRange3D(r, p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    if dx * dx + dy * dy + dz * dz < r * r:
        return True
    return False

try:
    inRange3D = cSMath.inRange3D
except AttributeError:
    inRange3D = __script_inRange3D

################################################
def __script_inRange2D(r, p1, p2):
    dx = p1[0] - p2[0]
    dz = p1[2] - p2[2]
    if dx * dx + dz * dz < r * r:
        return True
    return False

try:
    inRange2D = cSMath.inRange2D
except AttributeError:
    inRange2D = __script_inRange2D

################################################
def __script_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)

def distance3D(p1, p2):
    try:
        return cSMath.distance(tuple(p1), tuple(p2))
    except AttributeError:
        return __script_distance(p1, p2)

try:
    distance = cSMath.distance
except AttributeError:
    distance = __script_distance

def distance3DToCompare(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return dx * dx + dy * dy + dz * dz

################################################
def __script_distance2D(p1, p2):
    dx = p1[0] - p2[0]
    dz = p1[2] - p2[2]
    return math.sqrt(dx * dx + dz * dz)

try:
    distance2D = cSMath.distance2D
except AttributeError:
    distance2D = __script_distance2D

def distance2DToCompareFrom3DPosition(p1, p2):
    dx = p1[0] - p2[0]
    dz = p1[2] - p2[2]
    return dx * dx + dz * dz

def distance2DToCompareFrom2DPosition(p1, p2):
    dx = p1[0] - p2[0]
    dz = p1[1] - p2[1]
    return dx * dx + dz * dz

def inRectRange2D(r, p1, p2):
    dx = p1[0] - p2[0]
    dz = p1[2] - p2[2]
    return abs(dx) <= r and abs(dz) <= r

################################################

def __script_limit(value, minV, maxV):

    if value > maxV:
        value = maxV
    elif value < minV:
        value = minV

    return value

# 这里不能用C的limit, 因为有些逻辑超出了2**31
#try:
#    limit = cSMath.limit
#except AttributeError:
#    limit = __script_limit

limit = __script_limit

def __script_limitf(value, minV, maxV):

    if value > maxV:
        value = maxV
    elif value < minV:
        value = minV

    return float(value)

#try:
#        limitf = cSMath.limitf
#except AttributeError:
#        limitf = __script_limitf

limitf = __script_limitf

################################################

G_VECTORS=(
    (0,1),(0.866,0.5), (0.866,-0.5), (0,-1), (-0.866,-0.5), (-0.866,0.5),
)

#(self.position[0], self.position[2]), self.bornRadii, self.patrolRadii
#R->出生点半径, r->巡逻半径

def scatter(pos, R, r):
    vPos = Math.Vector2(pos[0], pos[1])

    if R == 0 or r == 0:
        return [vPos, ]

    if 2*r > R:
        return [vPos, ]

    if 2*r < R and 3*r >= R:
        return _roundCircleFlat(vPos,r)

    points=[]
    points.append(vPos)

    n=1
    while r*(n*2+1)<=R:
        points += _roundCircleHexagen(n,r,vPos)
        n+=1

    quadrants = [[], [], [], [], ]
    for vp in points:
        v = vp - vPos
        if v.x>0 and v.y>0:
            quadrants[0].append(vp)
        elif v.x<0 and v.y>0:
            quadrants[1].append(vp)
        elif v.x>0 and v.y<0:
            quadrants[2].append(vp)
        elif v.x<0 and v.y<0:
            quadrants[3].append(vp)

    random.shuffle(quadrants)

    sortPoints = []
    i = 0
    while True:
        if len(quadrants[i]) > 1:
            p = random.choice(quadrants[i])
            sortPoints.append(p)
            quadrants[i].remove(p)
            if i >= (len(quadrants)-1):
                i = 0
            else:
                i += 1
        elif len(quadrants[i]) == 1:
            p = random.choice(quadrants[i])
            sortPoints.append(p)
            quadrants.pop(i)
            if len(quadrants) == 0:
                break
            elif i >= (len(quadrants)-1):
                i = 0
            else:
                i += 1
        else:
            quadrants.pop(i)
            if len(quadrants) == 0:
                break
            elif i >= (len(quadrants)-1):
                i = 0
            else:
                i += 1

    sortPoints.append(vPos)

    return sortPoints

def _roundCircleHexagen(layer,r,pos):
    ret=[]
    vectors = rotate2D(G_VECTORS)
    dist=layer*2*r
    for v in vectors:
        dpos=pos+Math.Vector2(v[0]*dist,v[1]*dist)
        ret.append(dpos)

    hexagen=[]
    for n in range(len(ret)):
        a=ret[n]
        nn=n+1
        if nn>=len(ret):
            nn=0
        b=ret[nn]
        line=b-a
        lineLen=line.length
        interN=int(round((lineLen-2*r)/(2*r)))
        line.normalise()
        for i in range(interN):
            dpos=a+Math.Vector2(line[0]*(i+1)*2*r,line[1]*(i+1)*2*r)
            hexagen.append(dpos)

    return ret+hexagen

def _roundCircleFlat(pos,r):
    ret=[]
    vectors = rotate2D(G_VECTORS)
    v=vectors[0]
    dpos=pos+Math.Vector2(v[0]*r,v[1]*r)
    ret.append(dpos)
    v=vectors[3]
    dpos=pos+Math.Vector2(v[0]*r,v[1]*r)
    ret.append(dpos)
    return ret

pi = 3.1415926535897931

def rotate2D(vector2Ds):    #传进一组2D vector,返回将这组2Dvector旋转一个角度的vector list
    global pi
    rt = []
    yaw = (random.random()*2-1)*pi
    for vector2D in vector2Ds:
        a = Math.Matrix()
        a.setRotateY(yaw)
        lastP = a.applyPoint((vector2D[0],0,vector2D[1]))
        rt.append((lastP[0],lastP[2]))
    return rt

def twin(originD, fixP, fixD, relP, relD):
    a = Math.Matrix()
    b = Math.Matrix()
    c = Math.Matrix()

    a.setRotateY(-originD[2])
    b.setRotateY(fixD[2])
    c.setTranslate(fixP)

    a.postMultiply(b)
    a.postMultiply(c)

    lastP = a.applyPoint(relP)
    lastD = (fixD[0]+relD[0], fixD[1]+relD[1], fixD[2]+relD[2])

    return Math.Vector3(lastP), Math.Vector3(lastD)

def internalPoint(srcPos, dstPos):
    x, y, z = srcPos
    x2, y2, z2 = dstPos

    return ((x+x2)/2, (y+y2)/2, (z+z2)/2)


# 输入一个中心点和起始点位置，获得绕中心点一圈均匀分布的3D点位置（包括起始点位置在内）
# centerPos  : 中心点位置 Vector3
# startPos   : 起始点位置 Vector3
# pointCount : 获得均匀分布点的个数
# 返回值 : pointCount个Vector3的tuple
def getCirclePoints(centerPos,startPos,pointCount):
    if pointCount<=1:
        return (startPos,)
    mat = Math.Matrix()
    mat.setRotateY( 3.1415926535*2/pointCount )
    result = []
    point = startPos-centerPos
    for i in range(pointCount):
        result.append(point+centerPos)
        point = mat.applyPoint(point)

    return tuple(result)

#
#dValue 是一个字典，以需要随机的关键字作为key,权重作为值
#
def getSection(dValue):
    totalValue = 0

    vkDict = {}

    sections = []
    for k,v in dValue.items():
        totalValue += v
        sections.append(totalValue)
        vkDict[totalValue] = k

    r = random.randint(0, totalValue-1)

    for i,s in enumerate(sections):
        if r < s:
            return vkDict[s]
    else:
        return vkDict[s]

def clamp(v, minv, maxv):
    if minv > maxv:
        maxv, minv = minv, maxv
    return max(minv, min(v, maxv))

def circleIntersectRectange2D(cx, cz, r, minx, minz, maxx, maxz):
    closestX = clamp(cx, minx, maxx)
    closestZ = clamp(cz, minz, maxz)
    dx = closestX - cx;
    dz = closestZ - cz;

    return ( dx * dx + dz * dz ) <= r * r;

def circleIntersectLineSegment2D(cx, cz, r, x, z):
    """
    refer to http://yehar.com/blog/?p=2926

    end points of line segment are (0,0) and (x,y)
    r is the radius of circle, while center of circle is (cx, cz)
    """
    r2 = r * r
    # end point in circle
    if cx * cx + cz * cz <= r2 or \
        (cx - x) * (cx - x) + (cz - z) * (cz - z) <= r2:
        return True

    # segment cross circle
    a = cx * x + cz * z
    b = cz * x - cx * z
    b2 = b * b
    d2 = x * x + z * z

    return a >= 0 and a <= d2 and b2 <= r2 * d2

def position2DTo3D(p):
    return (p[0], 0, p[1])

def position3DTo2D(p):
    return (p[0],p[2])

def postion3DTo2DCell(p):
    return (math.floor(p[0]), math.floor(p[2]))

def vector3WithoutY(p):
    return Math.Vector3(p[0], 0, p[2])

def position3DCellWithoutY(p):
    return (math.floor(p[0]), 0, math.floor(p[2]))

def getYawFromPoints(p1, p2):
    direction = Math.Vector3(p1)-Math.Vector3(p2)
    return getYawFromDirection(direction)

def getYawFromDirection(direction):
    direction[1] = 0
    direction.normalise()
    yaw = math.asin(direction[0])
    if direction[2] < 0:
        if yaw > 0:
            yaw = math.pi - yaw
        else:
            yaw = 0 - math.pi - yaw

    return yaw

def getDirFromYaw(yaw):
    return Math.Vector3(math.sin(yaw), 0, math.cos(yaw))

def getForwardPos(fromPos, toDirYaw, distance):
    return Math.Vector3(fromPos)+Math.Vector3(math.sin(toDirYaw), 0, math.cos(toDirYaw))*distance

#z周朝下，x轴朝右，知道矩形左下角坐标和长宽，判断点是否在矩形内
def inRectangle(leftBottom, w, h, p):
    return 0<=p[0]-leftBottom[0]<=w and 0<=p[2]-leftBottom[2]<=h

# c：AABB的中心
# h：AABB的半长度
# p：圆盘的圆心
# r：圆盘的半径
def isAabbDiskIntersect(c, h, p, r = 0.5):
    v = Math.Vector2(abs(p.x - c.x), abs(p.y - c.y))
    u = Math.Vector2(max(v.x - h.x, 0), max(v.y - h.y, 0))
    return (u.x * u.x + u.y * u.y) <= r * r

def getNearestPoint(fromPos, targetPosList):
    targetPos = None
    dist = 0
    for pos in targetPosList:
        if not targetPos:
            targetPos = pos
            dist = distance2DToCompareFrom3DPosition(fromPos, targetPos)
            continue

        curDist = distance2DToCompareFrom3DPosition(fromPos, pos)
        if curDist<dist:
            targetPos = pos
            dist = distance2DToCompareFrom3DPosition(fromPos, targetPos)

    return targetPos

def getNearest2DPoint(fromPos, targetPosList):
    targetPos = None
    dist = 0
    for pos in targetPosList:
        if not targetPos:
            targetPos = pos
            dist = distance2DToCompareFrom2DPosition(fromPos, targetPos)
            continue

        curDist = distance2DToCompareFrom2DPosition(fromPos, pos)
        if curDist<dist:
            targetPos = pos
            dist = distance2DToCompareFrom2DPosition(fromPos, targetPos)

    return targetPos

def getNearestEntity(fromPos, entityList):
    targetEntity = None
    dist = sys.maxsize
    for e in entityList:
        curDist = distance2DToCompareFrom3DPosition(fromPos, e.position)
        if curDist < dist:
            targetEntity = e
            dist = curDist

    return targetEntity

def posByOffset(fromPos, offset):
    return (fromPos[0]+offset[0], fromPos[1]+offset[1], fromPos[2]+offset[2])

def posByOffsetEx(fromPos, offset):
    return (int(fromPos[0]+offset[0]), int(fromPos[1]+offset[1]), int(fromPos[2]+offset[2]))

def posBy2DOffset(fromPos, offset):
    return (fromPos[0]+offset[0], fromPos[2]+offset[2])

def offset2DSum(p1, p2):
    return abs(p1[0]-p2[0])+abs(p1[2]-p2[2])


def gcd(a, b):
    if a < b:
        a, b = b, a
    while b != 0:
        temp = round(a % b, 2)
        a = b
        b = temp
    return a


def mgcd(*nums):
    max_idx = len(nums) - 1
    idx = 2
    r = gcd(nums[0], nums[1])
    while True:
        if idx > max_idx:
            break
        r = gcd(r, nums[idx])
        idx += 1
    return r

def getRotatePos(pos2D, direction):
    if direction[0]:
        angle = math.atan(direction[1] / direction[0])
    else:
        angle = pi/2

    posX = pos2D[0] * math.cos(angle) + pos2D[1] * math.sin(angle)
    posY = pos2D[1] * math.cos(angle) - pos2D[0] * math.sin(angle)
    return (posX, posY)

def getRotatePosByYaw(pos2D, yaw):
    posX = pos2D[0] * math.cos(yaw) + pos2D[1] * math.sin(yaw)
    posY = pos2D[1] * math.cos(yaw) - pos2D[0] * math.sin(yaw)
    return (posX, posY)

def clockwiseRotate(vectorDir, theta):
    return Math.Vector3(vectorDir[0]*math.cos(theta)+vectorDir[2]*math.sin(theta),\
            vectorDir[1], \
            -vectorDir[0]*math.sin(theta)+vectorDir[2]*math.cos(theta))


def isPointInPolygon(point, rangeList, includeVertex=True, includeEdge=True):
    """Ray casting algorithm, see WIKI: https://rosettacode.org/wiki/Ray-casting_algorithm"""
    lngList = []
    latList = []
    if rangeList[0] != rangeList[-1]:
        # Fix ploygon as closed polygon
        rangeList = tuple(i for i in rangeList) + (rangeList[0], )

    for i in range(len(rangeList) - 1):
        lngList.append(rangeList[i][0])
        latList.append(rangeList[i][2])

    maxLng = max(lngList)
    minLng = min(lngList)
    maxLat = max(latList)
    minLat = min(latList)
    if point[0] > maxLng or point[0] < minLng or point[2] > maxLat or point[2] < minLat:
        # out of orthogonal range
        return False

    count = 0
    point1 = rangeList[0]
    for i in range(1, len(rangeList)):

        point2 = rangeList[i]
        if (point[0] == point1[0] and point[2] == point1[2]) or (point[0] == point2[0] and point[2] == point2[2]):
            # in polygon vertex
            return includeVertex

        if (point1[2] < point[2] <= point2[2]) or (point1[2] >= point[2] > point2[2]):
            point12lng = point2[0] - (point2[2] - point[2]) * (point2[0] - point1[0]) / (point2[2] - point1[2])

            if point12lng == point[0]:
                # in polygon edge
                return includeEdge

            if point12lng < point[0]:
                count += 1

        point1 = point2

    if count % 2 == 0:
        return False

    return True


def choiceInWeights(weightPairs):
    """ choice random val in given weight

    :param weightPairs: pairs
    :type weightPairs: list[(val, weight)]
    :return: choice val
    """
    sumWeight = sum([_[1] for _ in weightPairs])
    randNum = random.uniform(0, sumWeight)

    flagVal = 0
    for val, weight in weightPairs:
        flagVal += weight
        if randNum < flagVal:
            return val
    return None


def getPointInRadii(point, direction, radii):
    x = radii * math.cos(direction) + point[0]
    y = radii * math.sin(direction) + point[2]
    return x, point[1], y

def roundUp(x):
    return int(math.ceil(x))

def roundDown(x):
    return int(math.floor(x))


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def distancePointToLine(point, lineStart, lineEnd):
    """
	计算点到线段的最短距离
	@param point: 点坐标 (Math.Vector2)
	@param lineStart: 线段起点 (Math.Vector2)
	@param lineEnd: 线段终点 (Math.Vector2)
	@return: 点到线段的最短距离
	"""

    lineDir = lineEnd - lineStart
    lineLengthSq = lineDir.x ** 2 + lineDir.y ** 2

    if lineLengthSq == 0:
        return (point - lineStart).length

    t = max(0, min(1, (point - lineStart).dot(lineDir) / lineLengthSq))

    projection = lineStart + lineDir * t

    return (point - projection).length


def projectPointOnLine(point, lineStart, lineEnd):
    """
	计算点在线上的投影点
	@param point: 点坐标 (Math.Vector2)
	@param lineStart: 线段起点 (Math.Vector2)
	@param lineEnd: 线段终点 (Math.Vector2)
	@return: 投影点坐标 (Math.Vector2)
	"""

    lineDir = lineEnd - lineStart
    lineLengthSq = lineDir.x ** 2 + lineDir.y ** 2

    if lineLengthSq == 0:
        return Math.Vector2(lineStart.x, lineStart.y)

    t = (point - lineStart).dot(lineDir) / lineLengthSq

    projection = lineStart + lineDir * t

    return projection
