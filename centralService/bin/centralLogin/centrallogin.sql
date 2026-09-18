DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `accountType` SMALLINT NOT NULL,
  `accountName` VARCHAR(100) NOT NULL,
  `accountCDKey` VARCHAR(20) NOT NULL DEFAULT '',
  `banAccountTime` BIGINT NOT NULL DEFAULT 0,
  `banPostTime` BIGINT NOT NULL DEFAULT 0,
  `banAccountReason` VARCHAR(1024) NOT NULL DEFAULT '',
  `banPostReason` VARCHAR(1024) NOT NULL DEFAULT '',
  `deleteTime` INT UNSIGNED NOT NULL DEFAULT 0,
  KEY (`id`),
  PRIMARY KEY (`accountType`, `accountName`)
);

DROP TABLE IF EXISTS `account_characters`;
CREATE TABLE `account_characters` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `parentID` BIGINT UNSIGNED NOT NULL,
  `hostId` INT NOT NULL,
  `gbId` BIGINT UNSIGNED NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  `level` SMALLINT NOT NULL,
  `school` SMALLINT NOT NULL,
  `gens` SMALLINT NOT NULL,
  `sex` SMALLINT NOT NULL,
  `tLastLogin` INT NOT NULL,
  KEY (`id`),
  PRIMARY KEY (`gbId`)
);

ALTER TABLE `account_characters` DEFAULT character set utf8mb4;
ALTER TABLE `account_characters` modify `name` varchar(20) character set utf8mb4;
