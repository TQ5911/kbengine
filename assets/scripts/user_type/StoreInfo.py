# -*- coding: utf-8 -*-

import Store


class StoreItemInfo(object):

    def createObjFromDict(self, dataDict):
        storeItem = Store.StoreItem()
        storeItem.fromStoreItemSavedDict(dataDict)
        return storeItem

    def getDictFromObj(self, obj):
        return obj.toStoreItemSavedDict()

    def isSameType(self, obj):
        return type(obj) is Store.StoreItem


storeItemInstance = StoreItemInfo()


class StoreInfo(object):
    def createObjFromDict(self, dataDict):
        store = Store.StoreData()
        store.fromStoreDataSavedDict(dataDict)
        return store

    def getDictFromObj(self, obj):
        return obj.toStoreDataSavedDict()

    def isSameType(self, obj):
        return type(obj) is Store.StoreData


storeInstance = StoreInfo()
