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
        "value": 9999999,
    }),
    "auctionPriceMinNumMsg": _tools.RODict({
        "key": "auctionPriceMinNumMsg",
        "value": 54000135,
    }),
    "auctionPriceMaxNumMsg": _tools.RODict({
        "key": "auctionPriceMaxNumMsg",
        "value": 54000261,
    }),
    "auctionUnitPriceMinMsg": _tools.RODict({
        "key": "auctionUnitPriceMinMsg",
        "value": 54000262,
    }),
    "auctionUnitPriceMaxMsg": _tools.RODict({
        "key": "auctionUnitPriceMaxMsg",
        "value": 54000263,
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
    "auctionPurchaseConfirm": _tools.RODict({
        "key": "auctionPurchaseConfirm",
        "value": 54000235,
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
        "value": "<color=#dea050>{0}后上架</color>",
    }),
    "auctionPublicityTime": _tools.RODict({
        "key": "auctionPublicityTime",
        "value": ((2, 10), (3, 30), (4, 60)),
    }),
    "auctionOnSale": _tools.RODict({
        "key": "auctionOnSale",
        "value": "出售",
    }),
    "auctionOnShow": _tools.RODict({
        "key": "auctionOnShow",
        "value": "公示",
    }),
    "auctionPublicityConfirm": _tools.RODict({
        "key": "auctionPublicityConfirm",
        "value": 54000250,
    }),
    "auctionCountdownTips": _tools.RODict({
        "key": "auctionCountdownTips",
        "value": "公示期结束后才可购买此商品",
    }),
    "auctionPublicityPeriod": _tools.RODict({
        "key": "auctionPublicityPeriod",
        "value": 54000251,
    }),
    "auctionNoItemsInPublicityMsg": _tools.RODict({
        "key": "auctionNoItemsInPublicityMsg",
        "value": 54000252,
    }),
    "auctionOnSaleRefer": _tools.RODict({
        "key": "auctionOnSaleRefer",
        "value": "出售参考",
    }),
    "auctionOnShowRefer": _tools.RODict({
        "key": "auctionOnShowRefer",
        "value": "公示参考",
    }),
    "auctionPaymentDelayTime": _tools.RODict({
        "key": "auctionPaymentDelayTime",
        "value": 20,
    }),
    "auctionPaymentDelayText": _tools.RODict({
        "key": "auctionPaymentDelayText",
        "value": "<color=#c60c0c>入账中</color>",
    }),
    "auctionPaymentClaimText": _tools.RODict({
        "key": "auctionPaymentClaimText",
        "value": "<color=#038304>已到账</color>",
    }),
    "auctionPaymentWithdrawText": _tools.RODict({
        "key": "auctionPaymentWithdrawText",
        "value": "（当前可提取{0}，剩余{1}入账中）",
    }),
    "auctionSellNeedMonthCard": _tools.RODict({
        "key": "auctionSellNeedMonthCard",
        "value": 54000260,
    }),
    "auctionChannel_jumpToBuy": _tools.RODict({
        "key": "auctionChannel_jumpToBuy",
        "value": 58000035,
    }),
    "auctionLuckyBuyTime": _tools.RODict({
        "key": "auctionLuckyBuyTime",
        "value": 10,
    }),
    "auctionLuckyBuyCheck": _tools.RODict({
        "key": "auctionLuckyBuyCheck",
        "value": 54000310,
    }),
    "auctionLuckyBuyFail": _tools.RODict({
        "key": "auctionLuckyBuyFail",
        "value": 54000311,
    }),
    "auctionLuckyBuyMail": _tools.RODict({
        "key": "auctionLuckyBuyMail",
        "value": 37000024,
    }),
    "auctionLuckyBuyTag": _tools.RODict({
        "key": "auctionLuckyBuyTag",
        "value": "<color=#038304>抢购中</color>",
    }),
    "auctionPublicityTag": _tools.RODict({
        "key": "auctionPublicityTag",
        "value": "<color=#b35b00>公示中</color>",
    }),
    "auctionSoulSale": _tools.RODict({
        "key": "auctionSoulSale",
        "value": 1,
    }),
    "auctionSoulScoreRule": _tools.RODict({
        "key": "auctionSoulScoreRule",
        "value": ((1, 1), (2, 3), (3, 5), (4, 8)),
    }),
    "auctionSoulPubScore": _tools.RODict({
        "key": "auctionSoulPubScore",
        "value": 8,
    }),
    "auctionSoulPubAddTime": _tools.RODict({
        "key": "auctionSoulPubAddTime",
        "value": ((8, 14, 10), (15, 19, 20), (20, 99, 30)),
    }),
    "rentalProp01": _tools.RODict({
        "key": "rentalProp01",
        "value": (0.1, 0.2, 0.7),
    }),
    "rentalProp02": _tools.RODict({
        "key": "rentalProp02",
        "value": (0.3, 0.7, 0),
    }),
    "rentalTime": _tools.RODict({
        "key": "rentalTime",
        "value": (3, 10),
    }),
    "rentalCost": _tools.RODict({
        "key": "rentalCost",
        "value": 1000,
    }),
    "rentalTimelimit": _tools.RODict({
        "key": "rentalTimelimit",
        "value": 1,
    }),
    "rentalAutoUnlist": _tools.RODict({
        "key": "rentalAutoUnlist",
        "value": 24,
    }),
    "rentalInitShelfNum": _tools.RODict({
        "key": "rentalInitShelfNum",
        "value": 10,
    }),
    "redeemA": _tools.RODict({
        "key": "redeemA",
        "value": 54482017,
    }),
    "redeemB": _tools.RODict({
        "key": "redeemB",
        "value": 54482005,
    }),
    "redeemC": _tools.RODict({
        "key": "redeemC",
        "value": 54482018,
    })
})