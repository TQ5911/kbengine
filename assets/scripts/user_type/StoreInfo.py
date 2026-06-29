# -*- coding: utf-8 -*-

import Store


class StoreItemInfo(object):

    def createObjFromDict(self, dataDict):
        storeItem = Store.StoreItem()
        storeItem.fromStoreItemSavedDict(dataDict)
        return storeItem

    def isSameType(self, obj):
        return type(obj) is Store.StoreItem

    def getDictFromObj(self, obj):
        return obj.toStoreItemSavedDict()


storeItemInstance = StoreItemInfo()


class StoreInfo(object):
    def createObjFromDict(self, dataDict):
        store = Store.StoreData()
        store.fromStoreDataSavedDict(dataDict)
        return store

    def isSameType(self, obj):
        return type(obj) is Store.StoreData

    def getDictFromObj(self, obj):
        return obj.toStoreDataSavedDict()


storeInstance = StoreInfo()
