DROP TABLE IF EXISTS `drop_info`;
CREATE TABLE `drop_info` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `serverId` INT UNSIGNED NOT NULL,
  `uniqueId` BIGINT UNSIGNED NOT NULL,
  `dropGbId` BIGINT UNSIGNED NOT NULL,
  `takerGbId` BIGINT UNSIGNED NOT NULL,
  `dropType` INT UNSIGNED NOT NULL,
  `endTime` INT UNSIGNED NOT NULL,
  `giveUpTime` INT UNSIGNED NOT NULL,
  `dropTime` INT UNSIGNED NOT NULL,
  `collExpireTime` INT UNSIGNED NOT NULL,
  `price` INT UNSIGNED NOT NULL,
  `equipInfo` BLOB NOT NULL,
  `extraInfo` BLOB NOT NULL,
  `collectionId` INT UNSIGNED NOT NULL,
  KEY (`id`),
  KEY (`dropGbId`),
  KEY (`takerGbId`),
  PRIMARY KEY (`uniqueId`)
);

DROP TABLE IF EXISTS `drop_notify`;
CREATE TABLE `drop_notify` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `uniqueId` BIGINT UNSIGNED NOT NULL,
  `notifyType` INT UNSIGNED NOT NULL,
  `gbId` BIGINT UNSIGNED NOT NULL,
  `notifyTime` INT UNSIGNED NOT NULL,
  `equipInfo` BLOB NOT NULL,
  KEY (`gbId`),
  KEY (`id`),
  PRIMARY KEY (`uniqueId`)
);

ALTER TABLE `drop_info` DEFAULT character set utf8mb4;
ALTER TABLE `drop_notify` DEFAULT character set utf8mb4;
