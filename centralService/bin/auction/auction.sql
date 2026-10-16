CREATE TABLE IF NOT EXISTS `auction_blackList`
(
    id bigint(20) unsigned AUTO_INCREMENT,
    `playerGBID` bigint unsigned not null DEFAULT 0,
    UNIQUE INDEX (`playerGBID`),
    PRIMARY KEY idKey (id)
    );

CREATE TABLE IF NOT EXISTS `auction_auctionItemData`
(
    id bigint(20) unsigned AUTO_INCREMENT,
    `serverId` int unsigned not null DEFAULT 0,
    `auctionType` tinyint unsigned not null DEFAULT 0,
    `auctionItemUUID` bigint unsigned not null DEFAULT 0,
    `addTime` int unsigned not null DEFAULT 0,
    `itemData_itemId` int unsigned not null DEFAULT 0,
    `itemData_itemNum` int unsigned not null DEFAULT 0,
    `itemData_createTime` int unsigned not null DEFAULT 0,
    `itemData_expireTime` int unsigned not null DEFAULT 0,
    `itemData_uniqueId` bigint unsigned not null DEFAULT 0,
    `itemData_bindType` tinyint unsigned not null DEFAULT 0,
    `itemData_attrJson` varchar(5120) not null DEFAULT '',
    `price` bigint unsigned not null DEFAULT 0,
    `number` int unsigned not null DEFAULT 0,
    `bagType` tinyint unsigned not null DEFAULT 0,
    `source` tinyint unsigned not null DEFAULT 0,
    `status` tinyint unsigned not null DEFAULT 0,
    `locked` int unsigned not null DEFAULT 0,
    `extraInfo` varchar(1024) not null DEFAULT '',
    `tCreate` int unsigned not null DEFAULT 0,
	`fromPlayerGBID` bigint unsigned not null DEFAULT 0,
    `addPublicityTime` int unsigned not null DEFAULT 0,
    UNIQUE INDEX (`auctionItemUUID`),
    PRIMARY KEY idKey (id)
    );

CREATE TABLE IF NOT EXISTS `auction_priceRecord_lastPrices`
(
    id bigint(20) unsigned AUTO_INCREMENT,
    `serverId` int unsigned not null DEFAULT 0,
    `itemId` int unsigned not null DEFAULT 0,
    `price` bigint unsigned not null DEFAULT 0,
    INDEX (`itemId`, `serverId`),
    PRIMARY KEY idKey (id)
    );

CREATE TABLE IF NOT EXISTS `auction_priceRecord_avgPrices`
(
    id bigint(20) unsigned AUTO_INCREMENT,
    `serverId` int unsigned not null DEFAULT 0,
    `itemId` int unsigned not null DEFAULT 0,
    `totalPrice` bigint unsigned not null DEFAULT 0,
    `number` bigint unsigned not null DEFAULT 0,
	`avgPrice` float not null DEFAULT 0.0,
    `recentPrices` LONGTEXT NULL,
    `tLastUpdateTime` bigint unsigned not null DEFAULT 0,
    INDEX (`itemId`, `serverId`),
    PRIMARY KEY idKey (id)
    );