# coding: utf-8
from KBEDebug import *

import struct

_MAX_UINT16 = 2 ** 16 - 1


class ByteMatric(object):
    """
             |<--- col=10 ---->|
       ----- [[0 1 2 3 4 5 6 7 8 9],
         |    [1..., ],
       row=5  [2..., ],
         |    [3..., ],
       -----  [4..., ]]
    """

    def __init__(self, data):
        self.row = 0
        self.col = 0
        self._data = bytearray()
        self._build(data)

    @staticmethod
    def pack_matric_to_bytearray(data):
        mr_row = len(data)
        mr_col = len(data[0])
        mr_new_data = bytearray()
        for _row in data:
            for _cell in _row:
                if _cell == float('inf'):
                    _cell = _MAX_UINT16
                mr_new_data.extend(struct.pack('>H', _cell))
        return mr_row, mr_col, mr_new_data

    def _build(self, data):
        _row, _col, _data = self.pack_matric_to_bytearray(data)
        self.row = _row
        self.col = _col
        self._data.clear()
        self._data.extend(_data)

    def get_node(self, x, y):
        _m_spnt = (y * self.col + x) * 2
        _m_epnt = _m_spnt + 2
        rm_data = int.from_bytes(self._data[_m_spnt:_m_epnt],
                                 byteorder='big', signed=False)
        if rm_data == _MAX_UINT16:
            return float('inf')
        return rm_data

    def export_data_tofile(self, path):
        m_export_data = bytearray()
        m_export_data.extend(struct.pack('>H', self.row))
        m_export_data.extend(struct.pack('>H', self.col))
        m_export_data.extend(self._data)
        with open(path, 'bw') as fp:
            fp.write(m_export_data)

    @classmethod
    def build_data_fromfile(cls, path):
        with open(path, 'rb') as fp:
            data = fp.read()
        mr_obj = cls([[]])
        mr_obj.row = int.from_bytes(data[0:2], byteorder='big', signed=False)
        mr_obj.col = int.from_bytes(data[2:4], byteorder='big', signed=False)
        mr_obj._data = bytearray(data[4:])
        return mr_obj
