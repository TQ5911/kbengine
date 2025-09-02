# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst

import userType
import auction


class AuctionItemInfo(userType.UserSTDSoleInfo):

    @property
    def cls(self):
        return auction.AuctionItem


class AuctionInfo(userType.UserSTDSoleInfo):

    @property
    def cls(self):
        return auction.Auction


class AuctionPlayerCacheInfo(userType.UserSTDSoleInfo):

    @property
    def cls(self):
        return auction.AuctionPlayerCache

