# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: auction/auctionConst
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "auctionMinListingPrice": _tools.RODict({
        "key": "auctionMinListingPrice",
        "value": 10,
    }),
    "auctionMaxListingPrice": _tools.RODict({
        "key": "auctionMaxListingPrice",
        "value": 999999,
    }),
    "auctionPriceMinNumMsg": _tools.RODict({
        "key": "auctionPriceMinNumMsg",
        "value": 54000135,
    }),
    "auctionTaxRate": _tools.RODict({
        "key": "auctionTaxRate",
        "value": 10,
    }),
    "auctionServiceFee": _tools.RODict({
        "key": "auctionServiceFee",
        "value": 100,
    }),
    "auctionAutoUnlist": _tools.RODict({
        "key": "auctionAutoUnlist",
        "value": 24,
    }),
    "auctionInitShelfNum": _tools.RODict({
        "key": "auctionInitShelfNum",
        "value": 10,
    }),
    "auctionCollectionListNum": _tools.RODict({
        "key": "auctionCollectionListNum",
        "value": 20,
    }),
    "auctionRefreshCD": _tools.RODict({
        "key": "auctionRefreshCD",
        "value": 1,
    }),
    "auctionCollectionListFullMsg": _tools.RODict({
        "key": "auctionCollectionListFullMsg",
        "value": 54000229,
    }),
    "auctionCollectedMsg": _tools.RODict({
        "key": "auctionCollectedMsg",
        "value": 54000232,
    }),
    "auctionUncollectedMsg": _tools.RODict({
        "key": "auctionUncollectedMsg",
        "value": 54000233,
    }),
    "tradeCoolingDownMsg": _tools.RODict({
        "key": "tradeCoolingDownMsg",
        "value": 54000234,
    }),
    "auctionNoItemsInCategoryMsg": _tools.RODict({
        "key": "auctionNoItemsInCategoryMsg",
        "value": 54000236,
    }),
    "auctionItemNotExistMsg": _tools.RODict({
        "key": "auctionItemNotExistMsg",
        "value": 54000237,
    }),
    "auctionShelfFullMsg": _tools.RODict({
        "key": "auctionShelfFullMsg",
        "value": 54000238,
    }),
    "tradeRecordRetentionCount": _tools.RODict({
        "key": "tradeRecordRetentionCount",
        "value": 20,
    }),
    "auctionSoldMsg": _tools.RODict({
        "key": "auctionSoldMsg",
        "value": 54000239,
    }),
    "auctionTimeUpMsg": _tools.RODict({
        "key": "auctionTimeUpMsg",
        "value": 54000240,
    }),
    "auctionBuyItemSuccessMsg": _tools.RODict({
        "key": "auctionBuyItemSuccessMsg",
        "value": 54000241,
    }),
    "auctionSeverErrorMsg": _tools.RODict({
        "key": "auctionSeverErrorMsg",
        "value": 54000137,
    }),
    "auctionSeverErrorTime": _tools.RODict({
        "key": "auctionSeverErrorTime",
        "value": 5,
    }),
    "auctionItemsPerPage": _tools.RODict({
        "key": "auctionItemsPerPage",
        "value": 10,
    }),
    "auctionPutawayConfirm": _tools.RODict({
        "key": "auctionPutawayConfirm",
        "value": 54000242,
    }),
    "auction_removeConfirm": _tools.RODict({
        "key": "auction_removeConfirm",
        "value": 54000249,
    }),
    "auction_TabText2": _tools.RODict({
        "key": "auction_TabText2",
        "value": "公示商品",
    }),
    "auctionHelpInfo": _tools.RODict({
        "key": "auctionHelpInfo",
        "value": 38,
    }),
    "auctionPublicityCountdownText": _tools.RODict({
        "key": "auctionPublicityCountdownText",
        "value": "{0}后公式结束",
    }),
    "auctionPublicityTime": _tools.RODict({
        "key": "auctionPublicityTime",
        "value": 4,
    }),
    "auctionOnSale": _tools.RODict({
        "key": "auctionOnSale",
        "value": "出售中",
    }),
    "auctionOnShow": _tools.RODict({
        "key": "auctionOnShow",
        "value": "公示中",
    }),
    "auctionPublicityConfirm": _tools.RODict({
        "key": "auctionPublicityConfirm",
        "value": 54000250,
    }),
    "auctionCountdownTips": _tools.RODict({
        "key": "auctionCountdownTips",
        "value": "该商品处于公示期，将于{0}后方可购买",
    }),
    "auctionPublicityPeriod": _tools.RODict({
        "key": "auctionPublicityPeriod",
        "value": 54000251,
    })
})