
# coding: utf-8

import userType


class BigBitVal(userType.UserSoleType):
    '''BIG_BIT_DATA_INFO'''
    def __init__(self, stateList=()):
        if stateList is None:
            self.stateList = []
        else:
            self.stateList = list(stateList)

    def isHasState(self, state):
        """
        判断指定的位是否为True。

        Args:
            state: 位的位置（从0开始计数）。

        Returns:
            bool: 如果位存在且为True则返回True，否则返回False。
        """
        # 计算该位所在的字节索引
        byte_index = state // 8
        # 检查索引是否超出stateList的长度
        if byte_index >= len(self.stateList):
            return False
        # 获取对应的字节值
        byte_value = self.stateList[byte_index]
        # 计算字节内的位偏移
        bit_offset = state % 8
        # 检查该位是否为1
        return (byte_value & (1 << bit_offset)) != 0

    def initBit(self, total_bits=0):
        """
        初始化指定总位数的位存储。

        Args:
            total_bits: 要初始化的总位数（默认0）。
        """
        # 计算需要多少个字节来存储这些位
        num_bytes = (total_bits + 7) // 8
        # 初始化stateList为全0
        self.stateList = [0] * num_bytes

    def setBit(self, state, value=True):
        """
        设置指定位的值。

        Args:
            state: 位的位置（从0开始计数）。
            value: 要设置的值，True表示1，False表示0（默认True）。
        """
        # 计算该位所在的字节索引
        byte_index = state // 8
        # 确保stateList有足够的长度
        if byte_index >= len(self.stateList):
            # 扩展stateList到足够的长度，新增的字节初始化为0
            self.stateList.extend([0] * (byte_index - len(self.stateList) + 1))

        # 获取对应的字节值
        byte_value = self.stateList[byte_index]
        # 计算字节内的位偏移
        bit_offset = state % 8

        if value:
            # 设置位为1
            self.stateList[byte_index] = byte_value | (1 << bit_offset)
        else:
            # 设置位为0
            self.stateList[byte_index] = byte_value & ~(1 << bit_offset)

    def unsetBit(self, state):
        """
        清除指定位的值（设置为False）。

        Args:
            state: 位的位置（从0开始计数）。
        """
        self.setBit(state, False)

    def toBigBitSavedDict(self):
        return {
            'stateList': self.stateList
        }


class BigBitInfo(object):
    def createObjFromDict(self, dataDict):
        obj = BigBitVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toBigBitSavedDict()

    def isSameType(self, obj):
        return type(obj) is BigBitVal


BigBitInstance = BigBitInfo()

