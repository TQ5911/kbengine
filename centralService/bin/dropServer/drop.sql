DROP TABLE IF EXISTS `drop_info`;
CREATE TABLE `drop_info` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `serverId` INT UNSIGNED NOT NULL,
  `uniqueId` BIGINT UNSIGNED NOT NULL,
  `dropGbId` BIGINT UNSIGNED NOT NULL,
  `takerGbId` BIGINT UNSIGNED NOT NULL,
  `takerServerId` INT UNSIGNED NOT NULL,
  `dropType` INT UNSIGNED NOT NULL,
  `endTime` INT UNSIGNED NOT NULL,
  `giveUpTime` INT UNSIGNED NOT NULL,
  `dropTime` INT UNSIGNED NOT NULL,
  `collExpireTime` INT UNSIGNED NOT NULL,
  `price` INT UNSIGNED NOT NULL,
  `maxPrice` INT UNSIGNED NOT NULL,
  `equipInfo` BLOB NOT NULL,
  `extraInfo` BLOB NOT NULL,
  `collectionId` INT UNSIGNED NOT NULL,
  `redeemWaitTime` INT UNSIGNED NOT NULL,
  `hasRedeemPrice` INT UNSIGNED NOT NULL,
  `hasPayment` INT UNSIGNED NOT NULL,
  `returnTime` BIGINT UNSIGNED NOT NULL,
  `ownerGbId` BIGINT UNSIGNED NOT NULL,
  `ownerServerId` INT UNSIGNED NOT NULL,
  `returnTimeBack` INT UNSIGNED NOT NULL,
  KEY (`id`),
  KEY (`dropGbId`),
  KEY (`takerGbId`),
  KEY (`ownerServerId`, `dropType`, `returnTime`),
  KEY `idx_dropType_endTime` (`dropType`, `endTime`),
  KEY `idx_dropType_redeemWaitTime` (`dropType`, `redeemWaitTime`),
  PRIMARY KEY (`uniqueId`)
);

DROP TABLE IF EXISTS `reward_info`;
CREATE TABLE `reward_info` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `uniqueId` BIGINT UNSIGNED NOT NULL,
  `gbId` BIGINT UNSIGNED NOT NULL,
  `bindMoney` INT UNSIGNED NOT NULL,
  `money` INT UNSIGNED NOT NULL,
  `serverId` INT UNSIGNED NOT NULL,
  `equipInfo` BLOB NOT NULL,
  KEY (`id`),
  KEY (`gbId`),
  PRIMARY KEY (`uniqueId`)
);

DROP TABLE IF EXISTS `custody_info`;
CREATE TABLE `custody_info` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `uniqueId` BIGINT UNSIGNED NOT NULL,
  `dropType` INT UNSIGNED NOT NULL,
  `equipInfo` BLOB NOT NULL,
  `holderGbId` BIGINT UNSIGNED NOT NULL,
  `holderServerId` INT UNSIGNED NOT NULL,
  `returnTime` INT UNSIGNED NOT NULL,
  `ownerGbId` BIGINT UNSIGNED NOT NULL,
  `ownerServerId` INT UNSIGNED NOT NULL,
  KEY (`id`),
  KEY (`holderGbId`),
  KEY (`ownerGbId`),
  KEY (`ownerServerId`, `dropType`, `returnTime`),
  PRIMARY KEY (`uniqueId`)
);

ALTER TABLE `drop_info` DEFAULT character set utf8mb4;
ALTER TABLE `custody_info` DEFAULT character set utf8mb4;
ALTER TABLE `reward_info` DEFAULT character set utf8mb4;

SET @db_name = DATABASE();
SET @table_name = 'drop_info';

SET @column_name = 'redeemWaitTime';
SET @column_def = 'INT UNSIGNED NOT NULL';

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

SET @table_name = 'drop_info';
SET @column_name = 'hasRedeemPrice';
SET @column_def = 'INT UNSIGNED NOT NULL';

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

SET @table_name = 'drop_info';
SET @column_name = 'maxPrice';
SET @column_def = 'INT UNSIGNED NOT NULL';

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

SET @table_name = 'drop_info';
SET @column_name = 'takerServerId';
SET @column_def = 'INT UNSIGNED NOT NULL';

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

SET @table_name = 'drop_info';
SET @column_name = 'returnTimeBack';
SET @column_def = 'INT UNSIGNED NOT NULL';

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

SET @table_name = 'reward_info';
SET @column_name = 'bindMoney';
SET @column_def = 'INT UNSIGNED NOT NULL';

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


SET @table_name = 'reward_info';
SET @column_name = 'money';
SET @column_def = 'INT UNSIGNED NOT NULL';

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

ALTER TABLE `reward_info` DROP COLUMN IF EXISTS price;

SET @db_name = DATABASE();
SET @table_name = 'drop_info';

SET @table_name = 'drop_info';
SET @index_name = 'idx_dropType_endTime';
SET @index_def = '(`dropType`, `endTime`)';

SET @sql = IF(
    (SELECT COUNT(*) FROM information_schema.STATISTICS
     WHERE TABLE_SCHEMA = @db_name
       AND TABLE_NAME = @table_name
       AND INDEX_NAME = @index_name) = 0,
    CONCAT('ALTER TABLE ', @table_name, ' ADD INDEX ', @index_name, ' ', @index_def),
    'SELECT concat(concat(concat("Table: ", @table_name), concat(", Index: ", @index_name)), " already exists, skipped") AS ''execute result message:'''
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @table_name = 'drop_info';
SET @index_name = 'idx_dropType_redeemWaitTime';
SET @index_def = '(`dropType`, `redeemWaitTime`)';

SET @sql = IF(
    (SELECT COUNT(*) FROM information_schema.STATISTICS
     WHERE TABLE_SCHEMA = @db_name
       AND TABLE_NAME = @table_name
       AND INDEX_NAME = @index_name) = 0,
    CONCAT('ALTER TABLE ', @table_name, ' ADD INDEX ', @index_name, ' ', @index_def),
    'SELECT concat(concat(concat("Table: ", @table_name), concat(", Index: ", @index_name)), " already exists, skipped") AS ''execute result message:'''
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;