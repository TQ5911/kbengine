import KBEngine
from KBEDebug import *
from CollectionBase import CollectionBase

class Collection(CollectionBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("Collection::__init__")
