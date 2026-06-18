#-*- coding: utf-8 -*-

import sys
import random
import Math
import math

try:
    import cSMath
except ImportError:
    cSMath = {}

################################################
def __scriptInRange3D(r, point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    dz = point2[2] - point1[2]
    return dx * dx + dy * dy + dz * dz < r * r

try:
    inRange3D = cSMath.inRange3D
except AttributeError:
    inRange3D = __scriptInRange3D

################################################
def __scriptInRange2D(r, point1, point2):
    dx = point2[0] - point1[0]
    dz = point2[2] - point1[2]
    return dx * dx + dz * dz < r * r

try:
    inRange2D = cSMath.inRange2D
except AttributeError:
    inRange2D = __scriptInRange2D

################################################
def __scriptDistance(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    dz = point2[2] - point1[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)

def distance3D(point1, point2):
    try:
        return cSMath.distance(tuple(point1), tuple(point2))
    except AttributeError:
        return __scriptDistance(point1, point2)

try:
    distance = cSMath.distance
except AttributeError:
    distance = __scriptDistance

def distance3DToCompare(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    dz = point2[2] - point1[2]
    return dx * dx + dy * dy + dz * dz

################################################
def __scriptDistance2D(point1, point2):
    dx = point1[0] - point2[0]
    dz = point1[2] - point2[2]
    return math.sqrt(dx * dx + dz * dz)

try:
    distance2D = cSMath.distance2D
except AttributeError:
    distance2D = __scriptDistance2D

def distance2DToCompareFrom3DPosition(point1, point2):
    dx = point1[0] - point2[0]
    dz = point1[2] - point2[2]
    return dx * dx + dz * dz

def distance2DToCompareFrom2DPosition(point1, point2):
    dx = point1[0] - point2[0]
    dz = point1[1] - point2[1]
    return dx * dx + dz * dz

def inRectRange2D(r, point1, point2):
    dx = point1[0] - point2[0]
    dz = point1[2] - point2[2]
    return abs(dx) <= r and abs(dz) <= r

################################################

def __scriptLimit(value, minV, maxV):

    if value > maxV:
        value = maxV
    elif value < minV:
        value = minV

    return value

# 这里不能用C的limit, 因为有些逻辑超出了2**31

limit = __scriptLimit

def __scriptLimitf(value, minV, maxV):

    if value > maxV:
        value = maxV
    elif value < minV:
        value = minV

    return float(value)


limitf = __scriptLimitf

################################################

GLOBAL_VECTORS=(
    (0,1),(0.866,0.5), (0.866,-0.5), (0.0,-1), (-0.866,-0.5), (-0.866,0.5),
)

#(self.position[0], self.position[2]), self.bornRadii, self.patrolRadii
#--R->出生点半径, r->巡逻半径

def scatter(pos, R, r):
    _vPos = Math.Vector2(pos[0], pos[1])

    if R == 0 or r == 0:
        return [_vPos, ]

    if 2*r > R:
        return [_vPos, ]

    if 2*r < R and 3*r >= R:
        return _roundCircleFlat(_vPos,r)

    points=[]
    points.append(_vPos)

    n=1
    while r*(n*2+1)<=R:
        points += _roundCircleHexagen(n,r,_vPos)
        n+=1

    _quadrants = [[], [], [], [], ]
    for vp in points:
        _v = vp - _vPos
        if _v.x>0 and _v.y>0:
            _quadrants[0].append(vp)
        elif _v.x<0 and _v.y>0:
            _quadrants[1].append(vp)
        elif _v.x>0 and _v.y<0:
            _quadrants[2].append(vp)
        elif _v.x<0 and _v.y<0:
            _quadrants[3].append(vp)

    random.shuffle(_quadrants)

    sortPoints = []
    i = 0
    while True:
        if len(_quadrants[i]) > 1:
            p = random.choice(_quadrants[i])
            sortPoints.append(p)
            _quadrants[i].remove(p)
            if i >= (len(_quadrants)-1):
                i = 0
            else:
                i += 1
        elif len(_quadrants[i]) == 1:
            p = random.choice(_quadrants[i])
            sortPoints.append(p)
            _quadrants.pop(i)
            if len(_quadrants) == 0:
                break
            elif i >= (len(_quadrants)-1):
                i = 0
            else:
                i += 1
        else:
            _quadrants.pop(i)
            if len(_quadrants) == 0:
                break
            elif i >= (len(_quadrants)-1):
                i = 0
            else:
                i += 1

    sortPoints.append(_vPos)

    return sortPoints

def _roundCircleHexagen(layer,r,pos):
    ret=[]
    _vectors = rotate2D(GLOBAL_VECTORS)
    dist=layer*2*r
    for _v in _vectors:
        dpos=pos+Math.Vector2(_v[0]*dist,_v[1]*dist)
        ret.append(dpos)

    _hexagen=[]
    for _n in range(len(ret)):
        _a=ret[_n]
        nn=_n+1
        if nn>=len(ret):
            nn=0
        b=ret[nn]
        line=b-_a
        _lineLen=line.length
        interN=int(round((_lineLen-2*r)/(2*r)))
        line.normalise()
        for _i in range(interN):
            dpos=_a+Math.Vector2(line[0]*(_i+1)*2*r,line[1]*(_i+1)*2*r)
            _hexagen.append(dpos)

    return ret+_hexagen

def _roundCircleFlat(pos,r):
    _ret=[]
    _vectors = rotate2D(GLOBAL_VECTORS)
    _v=_vectors[0]
    dpos=pos+Math.Vector2(_v[0]*r,_v[1]*r)
    _ret.append(dpos)
    _v=_vectors[3]
    dpos=pos+Math.Vector2(_v[0]*r,_v[1]*r)
    _ret.append(dpos)
    return _ret

pi = 3.1415926535897931

def rotate2D(vector2Ds):    #传进一组2D vector,返回将这组2Dvector旋转一个角度的vector list
    global pi
    _rt = []
    yaw = (random.random()*2-1)*pi
    for _vector2D in vector2Ds:
        a = Math.Matrix()
        a.setRotateY(yaw)
        lastP = a.applyPoint((_vector2D[0],0,_vector2D[1]))
        _rt.append((lastP[0],lastP[2]))
    return _rt


def internalPoint(srcPos, dstPos):
    _x, _y, _z = srcPos
    _x2, _y2, _z2 = dstPos

    return ((_x+_x2)/2, (_y+_y2)/2, (_z+_z2)/2)


# 输入一个中心点和起始点位置，获得绕中心点一圈均匀分布的3D点位置（包括起始点位置在内）
# centerPos  : 中心点位置 Vector3
# startPos   : 起始点位置 Vector3
# pointCount : 获得均匀分布点的个数
# 返回值 : pointCount个Vector3的tuple
def getCirclePoints(centerPos,startPos,pointCount):
    if pointCount<=1:
        return (startPos,)
    _mat = Math.Matrix()
    _mat.setRotateY( 3.1415926535*2/pointCount )
    _result = []
    point = startPos-centerPos
    for i in range(pointCount):
        _result.append(point+centerPos)
        point = _mat.applyPoint(point)

    return tuple(_result)

#
#dValue 是一个字典，以需要随机的关键字作为key,权重作为值
#
def getSection(dValue):
    _totalValue = 0

    vkDict = {}

    sections = []
    for k,v in dValue.items():
        _totalValue += v
        sections.append(_totalValue)
        vkDict[_totalValue] = k

    _r = random.randint(0, _totalValue-1)

    for _,_s in enumerate(sections):
        if _r < _s:
            return vkDict[_s]
    else:
        return vkDict[_s]

def clamp(v, minval, maxval):
    if minval > maxval:
        maxval, minval = minval, maxval
    return max(minval, min(v, maxval))

def circleIntersectRectange2D(cx, cz, r, minx, minz, maxx, maxz):
    _closestX = clamp(cx, minx, maxx)
    _closestZ = clamp(cz, minz, maxz)
    _dx = _closestX - cx;
    _dz = _closestZ - cz;

    return ( _dx * _dx + _dz * _dz ) <= r * r;

def circleIntersectLineSegment2D(cx, cz, r, x, z):
    """
    refer to http://yehar.com/blog/?p=2926

    end points of line segment are (0,0) and (x,y)
    r is the radius of circle, while center of circle is (cx, cz)
    """
    _r2 = r * r
    # end point in circle
    if cx * cx + cz * cz <= _r2 or \
        (cx - x) * (cx - x) + (cz - z) * (cz - z) <= _r2:
        return True

    # segment cross circle
    _a = cx * x + cz * z
    _b = cz * x - cx * z
    _b2 = _b * _b
    _d2 = x * x + z * z

    return _a >= 0 and _a <= _d2 and _b2 <= _r2 * _d2

def position3DTo2D(p):
    return (p[0],p[2])

def position2DTo3D(p):
    return (p[0], 0, p[1])

def vector3WithoutY(p):
    return Math.Vector3(p[0], 0, p[2])

def postion3DTo2DCell(point):
    return (math.floor(point[0]), math.floor(point[2]))

def position3DCellWithoutY(point):
    return (math.floor(point[0]), 0, math.floor(point[2]))

def getYawFromPoints(point1, point2):
    _direction = Math.Vector3(point1)-Math.Vector3(point2)
    return getYawFromDirection(_direction)

def getYawFromDirection(direction):
    direction[1] = 0
    direction.normalise()
    _yaw = math.asin(direction[0])
    if direction[2] < 0:
        if _yaw > 0:
            _yaw = math.pi - _yaw
        else:
            _yaw = 0 - math.pi - _yaw

    return _yaw

def getForwardPos(fromPosition, toDirYaw, distance):
    return Math.Vector3(fromPosition)+Math.Vector3(math.sin(toDirYaw), 0, math.cos(toDirYaw))*distance

def getDirFromYaw(yaw):
    return Math.Vector3(math.sin(yaw), 0, math.cos(yaw))

#z周朝下，x轴朝右，知道矩形左下角坐标和长宽，判断点是否在矩形内
def inRectangle(leftBottom, w, h, point):
    return 0<=point[0]-leftBottom[0]<=w and 0<=point[2]-leftBottom[2]<=h

# c：AABB的中心
# h：AABB的半长度
# p：圆盘的圆心
# r：圆盘的半径
def isAabbDiskIntersect(c, h, p, r = 0.5):
    _v = Math.Vector2(abs(p.x - c.x), abs(p.y - c.y))
    _u = Math.Vector2(max(_v.x - h.x, 0), max(_v.y - h.y, 0))
    return (_u.x * _u.x + _u.y * _u.y) <= r * r

def getNearestPoint(fromPosition, targetPosList):
    _targetPos = None
    dist = 0
    for pos in targetPosList:
        if not _targetPos:
            _targetPos = pos
            dist = distance2DToCompareFrom3DPosition(fromPosition, _targetPos)
            continue

        curDist = distance2DToCompareFrom3DPosition(fromPosition, pos)
        if curDist<dist:
            _targetPos = pos
            dist = distance2DToCompareFrom3DPosition(fromPosition, _targetPos)

    return _targetPos

def getNearest2DPoint(fromPosition, targetPosList):
    _targetPos = None
    dist = 0
    for pos in targetPosList:
        if not _targetPos:
            _targetPos = pos
            dist = distance2DToCompareFrom2DPosition(fromPosition, _targetPos)
            continue

        curDist = distance2DToCompareFrom2DPosition(fromPosition, pos)
        if curDist<dist:
            _targetPos = pos
            dist = distance2DToCompareFrom2DPosition(fromPosition, _targetPos)

    return _targetPos

def getNearestEntity(fromPosition, entityList):
    _targetEntity = None
    dist = sys.maxsize
    for e in entityList:
        curDist = distance2DToCompareFrom3DPosition(fromPosition, e.position)
        if curDist < dist:
            _targetEntity = e
            dist = curDist

    return _targetEntity

def posByOffsetEx(fromPosition, offset):
    return (int(fromPosition[0]+offset[0]), int(fromPosition[1]+offset[1]), int(fromPosition[2]+offset[2]))

def posByOffset(fromPosition, offset):
    return (fromPosition[0]+offset[0], fromPosition[1]+offset[1], fromPosition[2]+offset[2])

def posBy2DOffset(fromPosition, offset):
    return (fromPosition[0]+offset[0], fromPosition[2]+offset[2])

def offset2DSum(point1, point2):
    return abs(point1[0]-point2[0])+abs(point1[2]-point2[2])


def gcd(a, b):
    if a < b:
        a, b = b, a
    while b != 0:
        _temp = round(a % b, 2)
        a = b
        b = _temp
    return a


def mgcd(*nums):
    _maxIdx = len(nums) - 1
    _idx = 2
    r = gcd(nums[0], nums[1])
    while True:
        if _idx > _maxIdx:
            break
        r = gcd(r, nums[_idx])
        _idx += 1
    return r

def getRotatePos(position2D, direction):
    if direction[0]:
        _angle = math.atan(direction[1] / direction[0])
    else:
        _angle = pi/2

    posX = position2D[0] * math.cos(_angle) + position2D[1] * math.sin(_angle)
    posY = position2D[1] * math.cos(_angle) - position2D[0] * math.sin(_angle)
    return (posX, posY)

def getRotatePosByYaw(position2D, yaw):
    _posX = position2D[0] * math.cos(yaw) + position2D[1] * math.sin(yaw)
    _posY = position2D[1] * math.cos(yaw) - position2D[0] * math.sin(yaw)
    return (_posX, _posY)

def clockwiseRotate(vectorDirection, theta):
    return Math.Vector3(vectorDirection[0]*math.cos(theta)+vectorDirection[2]*math.sin(theta),\
            vectorDirection[1], \
            -vectorDirection[0]*math.sin(theta)+vectorDirection[2]*math.cos(theta))


def isPointInPolygon(position, rangeList, includeVertex=True, includeEdge=True):
    """Ray casting algorithm, see WIKI: https://rosettacode.org/wiki/Ray-casting_algorithm"""
    _lngList = []
    _latList = []
    if rangeList[0] != rangeList[-1]:
        # do Fix ploygon as closed polygon
        rangeList = tuple(_i for _i in rangeList) + (rangeList[0], )

    for _i in range(len(rangeList) - 1):
        _lngList.append(rangeList[_i][0])
        _latList.append(rangeList[_i][2])

    _maxLng = max(_lngList)
    _minLng = min(_lngList)
    _maxLat = max(_latList)
    _minLat = min(_latList)
    if position[0] > _maxLng or position[0] < _minLng or position[2] > _maxLat or position[2] < _minLat:
        # out of orthogonal range
        return False

    count = 0
    point1 = rangeList[0]
    for _i in range(1, len(rangeList)):

        point2 = rangeList[_i]
        if (position[0] == point1[0] and position[2] == point1[2]) or (position[0] == point2[0] and position[2] == point2[2]):
            # in polygon vertex
            return includeVertex

        if (point1[2] < position[2] <= point2[2]) or (point1[2] >= position[2] > point2[2]):
            _point12lng = point2[0] - (point2[2] - position[2]) * (point2[0] - point1[0]) / (point2[2] - point1[2])

            if _point12lng == position[0]:
                # in polygon edge
                return includeEdge

            if _point12lng < position[0]:
                count += 1

        point1 = point2

    if count % 2 == 0:
        return False

    return True


def manhattanDist(p1, p2):
    _dx = p1[0] - p2[0]
    _dz = p1[2] - p2[2]
    return abs(_dx) + abs(_dz)


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
    _x = radii * math.cos(direction) + point[0]
    _y = radii * math.sin(direction) + point[2]
    return _x, point[1], _y

def roundDown(x):
    return int(math.floor(x))


def roundUp(x):
    return int(math.ceil(x))


def chunks(l, n):
    for _i in range(0, len(l), n):
        yield l[_i:_i+n]

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
