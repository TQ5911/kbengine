# -*- encoding:utf-8 -*-
import KBEngine
from KBEDebug import *

from CreationBase import CreationBase

# TODO: use Creation global dic
import global_data as GD


class Creation(CreationBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("Creation::__init__:%s." % (self.__dict__))

    ########## Monster.def##########
