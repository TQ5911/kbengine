CREATE TABLE IF NOT EXISTS `auction`
(
    id bigint(20) unsigned AUTO_INCREMENT,
    `tLastUpdateTime` bigint unsigned not null DEFAULT 0,
    PRIMARY KEY idKey (id)
    );

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
    `itemId` int unsigned not null DEFAULT 0,
    `price` bigint unsigned not null DEFAULT 0,
    INDEX (`itemId`),
    PRIMARY KEY idKey (id)
    );

CREATE TABLE IF NOT EXISTS `auction_priceRecord_avgPrices`
(
    id bigint(20) unsigned AUTO_INCREMENT,
    `itemId` int unsigned not null DEFAULT 0,
    `totalPrice` bigint unsigned not null DEFAULT 0,
    `number` bigint unsigned not null DEFAULT 0,
	`avgPrice` float not null DEFAULT 0.0,
    `recentPrices` LONGTEXT NULL,
    INDEX (`itemId`),
    PRIMARY KEY idKey (id)
    );

SET @db_name = DATABASE();
SET @table_name = 'auction_auctionItemData';
SET @column_name = 'addPublicityTime';
SET @column_def = 'int(10) unsigned NOT NULL DEFAULT 0';

SET @sql = IF(
    (SELECT COUNT(*) FROM information_schema.COLUMNS
     WHERE TABLE_SCHEMA = @db_name
       AND TABLE_NAME = @table_name
       AND COLUMN_NAME = @column_name) = 0,
    CONCAT('ALTER TABLE ', @table_name, ' ADD COLUMN ', @column_name, ' ', @column_def),
    'SELECT concat(concat(concat("Table: ", @table_name), concat(", Column: ", @column_name)), " already exists, skipped") AS ''execute result message:'''
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;