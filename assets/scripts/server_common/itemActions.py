import gameconst

ITEM_ACTION_MAP = {}


def itemSubTypeAction(subType):
    def fwrap(f):
        ITEM_ACTION_MAP[subType] = f
        return f

    return fwrap


def getItemAction(item):
    return ITEM_ACTION_MAP.get(item.itemSubType)
