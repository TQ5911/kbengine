CREATE TABLE IF NOT EXISTS `game_entity_dbid`
(
`entityType` varbinary(60) NOT NULL,
`entityDBID` bigint(15) NOT NULL,
PRIMARY KEY  `entityType` (`entityType`)
);

CREATE TABLE IF NOT EXISTS `game_config`
(
`name` varchar(64) NOT NULL,
`value` varchar(128) NOT NULL,
PRIMARY KEY  `name` (`name`)
);

CREATE TABLE IF NOT EXISTS `game_state_info`
        (
        `name` varchar(64) NOT NULL,
        `value` bigint(15) NOT NULL,
        PRIMARY KEY  `name` (`name`)
        );
		
CREATE TABLE IF NOT EXISTS `game_take_over`
        (
        `accountName` varchar(128) NOT NULL,
        `entityDBID` bigint(15) NOT NULL,
        PRIMARY KEY  `accountName` (`accountName`)
        );
		
CREATE TABLE IF NOT EXISTS `game_leader_board_stub_info`
        (
        `lbType` int(10) NOT NULL,
        `value` bigint(15) NOT NULL,
        PRIMARY KEY  `lbType` (`lbType`)
        );

CREATE TABLE IF NOT EXISTS `game_last_global_mail_info`
        (
        `gbId` bigint(20) NOT NULL,
        `lastGlobalMailGBID` bigint(20) NOT NULL,
        `lastGlobalMailTime` int(10) NOT NULL,
         PRIMARY KEY  `gbId` (`gbId`)
        );

CREATE TABLE IF NOT EXISTS `game_player_mails`
        (
         id int auto_increment primary key,
        `toGBID` bigint(20) NOT NULL,
        `mailId` int(10) NOT NULL,
        `mailGBID` bigint(20) NOT NULL,
        `globalMailGBID` bigint(20) NOT NULL,
        `readStat` tinyint(2) NOT NULL,
        `createTime` int(10) NOT NULL,
        `expiredTime` int(10) NOT NULL,
        `fromGBID` bigint(20) NOT NULL,
        `attach` blob,
        `attachStat` tinyint(2) NOT NULL,
        `despArgs` blob,
        `title` varchar(128) NOT NULL,
        `cont`   varchar(1024) NOT NULL,
        `opUUID` bigint(20) NOT NULL,
        `srcType` int(20) NOT NULL,
        `srcSubType` int(20) NOT NULL,
        `desp` varchar(128) NOT NULL,
        `idipSource` int(10) NOT NULL,
        `dueTime` int(10) NOT NULL,
         index `index_1` (`toGBID`, `createTime`),
         index `index_2` (`toGBID`, `mailGBID`)
        );
		

CREATE TABLE IF NOT EXISTS `game_switch_server`
        (
        `account` varchar(64) NOT NULL,
        `dbid` bigint(15) NOT NULL,
        PRIMARY KEY  `account` (`account`)
        );
		
		
CREATE TABLE IF NOT EXISTS `game_guild_avatar`
        (
		`gbId` bigint(15) NOT NULL,
		`guildUUID` bigint(15) NOT NULL,
        PRIMARY KEY  `gbId` (`gbId`),
		index `guildUUID` (`guildUUID`)
        );
		
		
CREATE TABLE IF NOT EXISTS `game_friends`
        (
        id int auto_increment primary key,
		`sGbId` bigint(15) NOT NULL,
		`bGbId` bigint(15) NOT NULL,
		INDEX (`sGbId`),
        INDEX (`bGbId`),
        unique index `index_var` (`sGbId`, `bGbId`)
        );
		

CREATE TABLE IF NOT EXISTS `game_account_mails`
        (
        id int auto_increment primary key,
        `accountName` varchar(128) NOT NULL,
        `accountType` int(2) NOT NULL,
        `mailId` int(10) NOT NULL,
        `sendTime` int(10) NOT NULL,
        `attachStr` varchar(256) NOT NULL,
        `despStr`  varchar(256) NOT NULL,
        `title` varchar(128) NOT NULL,
        `cont`  varchar(1024) NOT NULL,
        `opUUID` bigint(20) NOT NULL,
        `srcType` int(20) NOT NULL,
        `srcSubType` int(20) NOT NULL,
        `desp` varchar(128) NOT NULL,
        `idipSource` int(10) NOT NULL,
         index `accountIndex` (`accountName`, `accountType`)
        );

CREATE TABLE IF NOT EXISTS `game_login_white_list`
        (
        `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `accountName` varchar(128) NOT NULL UNIQUE,
        `accountGmMode` int(10) NOT NULL DEFAULT 0
        );

CREATE TABLE IF NOT EXISTS `game_avatar_offline_callbacks`
        (
        `id` int auto_increment primary key,
        `gbId` bigint(20) NOT NULL,
        `callbackName`  varchar(128) NOT NULL,
        `args`  BLOB NOT NULL,
         index `gbId` (`gbId`)
        );


CREATE TABLE IF NOT EXISTS `game_admin_cmds`
        (
        `id` int auto_increment primary key,
        `cmdSerial` varchar(64) NOT NULL,
        `result` int NOT NULL,
        `retErrMsg` varchar(255) NOT NULL,
        `retStr` varchar(1024) NOT NULL,
        `tWhen` int(10) NOT NULL,
        index `cmdSerial` (`cmdSerial`)
        );
		
CREATE TABLE IF NOT EXISTS `game_account_characters`
(
	`id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`parentID` bigint(20) UNSIGNED NOT NULL,
	`gbId` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
	`authDbId` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
	`dbId` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
	`name` varchar(255) NOT NULL DEFAULT '',
	`school` smallint(5) UNSIGNED NOT NULL DEFAULT '0',
	`sex` tinyint(3) UNSIGNED NOT NULL DEFAULT '0',
	`level` int(10) UNSIGNED NOT NULL DEFAULT '0',
	`tLastOnline` int(10) UNSIGNED NOT NULL DEFAULT '0',
	`authExpire` int(10) UNSIGNED NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`),
	KEY `idx_parentID` (`parentID`),
	KEY `idx_gbId` (`gbId`),
	KEY `idx_authGbId` (`authDbId`)
);

-- 用来migrate 添加 authExpire字段
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_add_expireTime_if_not_exists`$$
CREATE PROCEDURE `sp_add_expireTime_if_not_exists`()
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME   = 'game_account_characters'
          AND COLUMN_NAME  = 'authExpire'
    ) THEN
        ALTER TABLE `game_account_characters`
        ADD COLUMN `authExpire` int(10) UNSIGNED NOT NULL DEFAULT '0'
        AFTER `tLastOnline`;
    END IF;
END$$

DELIMITER ;

-- 执行迁移
CALL `sp_add_expireTime_if_not_exists`;

-- 清理（可选）
DROP PROCEDURE `sp_add_expireTime_if_not_exists`;


CREATE TABLE IF NOT EXISTS `game_account_offline_callbacks`
        (
        `id` int auto_increment primary key,
        `accountName` varchar(128) NOT NULL,
        `callbackName`  varchar(128) NOT NULL,
        `args`  BLOB NOT NULL,
         index `accountName` (`accountName`)
        );

DROP PROCEDURE IF EXISTS gamesp_record_avatar_offline_callbacks;
DELIMITER ;;
CREATE PROCEDURE gamesp_record_avatar_offline_callbacks(
        IN p_gbId BIGINT(20),
        IN callbackName varchar(128),
        IN args BLOB
        )
        BEGIN
            INSERT INTO `game_avatar_offline_callbacks` (`gbId`, `callbackName`, `args`) VALUES (p_gbId, callbackName, args);
            SELECT count(`id`) FROM `game_avatar_offline_callbacks` where gbId=p_gbId;
        END;;
DELIMITER ;

DROP PROCEDURE IF EXISTS gamesp_load_avatar_offline_callbacks;
DELIMITER ;;
CREATE PROCEDURE gamesp_load_avatar_offline_callbacks(
        IN p_gbId BIGINT(20))
        BEGIN
            SELECT `callbackName`, hex(`args`) FROM `game_avatar_offline_callbacks` where gbId=p_gbId order by id limit 2000;
            DELETE FROM `game_avatar_offline_callbacks` WHERE gbId=p_gbId;
        END;;
DELIMITER ;

DROP PROCEDURE IF EXISTS gamesp_load_last_global_mail_info;
DELIMITER ;;
CREATE PROCEDURE gamesp_load_last_global_mail_info(
    IN p_gbId BIGINT(20),
    IN p_svrTime BIGINT(20))
BEGIN
    DECLARE db_gbId BIGINT(20) DEFAULT 0;
    DECLARE db_lastGlobalMailGBID BIGINT(20) DEFAULT 0;
    DECLARE db_lastGlobalMailTime INT DEFAULT p_svrTime;

    SELECT gbId, lastGlobalMailGBID, lastGlobalMailTime
    INTO db_gbId, db_lastGlobalMailGBID, db_lastGlobalMailTime
    FROM game_last_global_mail_info WHERE gbId=p_gbId;

    IF db_gbId=0 THEN
        INSERT INTO game_last_global_mail_info (gbId, lastGlobalMailGBID, lastGlobalMailTime) VALUES (p_gbId, 0, p_svrTime);
    END IF;
    SELECT db_gbId, db_lastGlobalMailGBID, db_lastGlobalMailTime;
END;;
DELIMITER ;

DROP PROCEDURE IF EXISTS gamesp_send_mail;
DELIMITER ;;
CREATE PROCEDURE gamesp_send_mail(
    IN p_toGBID BIGINT(20),
    IN p_mailId INT,
    IN p_mailGBID BIGINT(20),
    IN p_globalMailGBID BIGINT(20),
    IN p_readState TINYINT(2),
    IN p_dueTime INT,
    IN p_createTime INT,
    IN p_expiredTime INT,
    IN p_fromGBID BIGINT(20),
    IN p_attach BLOB,
    IN p_attachState TINYINT(2),
    IN p_despArgs BLOB,
    IN p_title VARCHAR(128),
    IN p_cont VARCHAR(1024),
    IN p_opUUID BIGINT(20),
    IN p_srcType INT,
    IN p_srcSubType INT,
    IN p_desc VARCHAR(128),
    IN p_source INT)
BEGIN
    DECLARE r_globalMailGBID BIGINT(20) DEFAULT p_globalMailGBID;
    DECLARE r_createTime INT UNSIGNED DEFAULT p_createTime;
    DECLARE r_delMailGBID BIGINT(20) DEFAULT 0;
    DECLARE db_lastGlobalMailTime INT DEFAULT 0;

    IF p_globalMailGBID>0 THEN
        SELECT lastGlobalMailTime INTO db_lastGlobalMailTime
        FROM game_last_global_mail_info WHERE gbId=p_toGBID;
        IF p_createTime>db_lastGlobalMailTime THEN
            UPDATE game_last_global_mail_info
            SET lastGlobalMailGBID=p_globalMailGBID,lastGlobalMailTime=p_createTime
            WHERE gbId=p_toGBID;
        END IF;
    END IF;

    INSERT INTO game_player_mails (toGBID, mailId, mailGBID, globalMailGBID, readStat, dueTime, createTime,
                                   expiredTime, fromGBID, attach, attachStat, despArgs, title, cont, opUUID,
                                   srcType, srcSubType, desp, idipSource)
    VALUES (p_toGBID, p_mailId, p_mailGBID, p_globalMailGBID, p_readState, p_dueTime,
            p_createTime,  p_expiredTime, p_fromGBID, p_attach, p_attachState, p_despArgs,
            p_title, p_cont, p_opUUID, p_srcType, p_srcSubType, p_desc, p_source);
    SELECT r_globalMailGBID, r_createTime, r_delMailGBID;
END;;
DELIMITER ;

DROP PROCEDURE IF EXISTS gamesp_load_account_mails;
DELIMITER ;;
CREATE PROCEDURE gamesp_load_account_mails(
    IN p_accountName varchar(128),
    IN p_accountType int(2),
    IN p_gbId BIGINT(20))
BEGIN
    SELECT accountName,mailId,sendTime,attachStr,despStr,title,cont,opUUID,srcType,srcSubType,desp,idipSource
    FROM game_account_mails
    WHERE accountName=p_accountName and accountType=p_accountType;

    DELETE FROM game_account_mails
    WHERE accountName=p_accountName and accountType=p_accountType;
END;;
DELIMITER ;

SET @db_name = DATABASE();
SET @table_name = 'game_player_mails';
SET @column_name = 'dueTime';
SET @column_def = 'int(10) NOT NULL';

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

CREATE TABLE IF NOT EXISTS `game_safe_box`
        (
        `id` int auto_increment primary key,
        `gbId` bigint(20) NOT NULL,
        `itemId` int(10) NOT NULL,
        `itemCount` int(10) NOT NULL,
        `itemPrice` decimal(10, 2) NOT NULL,
        `claimed` int(10) NOT NULL,
        `claimTime` int(10) NOT NULL,
        `orderId` varchar(64) NOT NULL,
        `orderTime` int(10) NOT NULL,
        unique index (`orderId`),
        INDEX `idx_unclaimed` (`gbId`, `claimed`, `orderTime` DESC, `id` DESC),
        INDEX `idx_claimed` (`gbId`, `claimed`, `claimTime` DESC, `id` DESC)
        );

CREATE TABLE IF NOT EXISTS `game_safe_box_idempotent`
        (
        `id` int auto_increment primary key,
        `orderId` varchar(64) NOT NULL,
        unique index (`orderId`)
        );

CREATE TABLE IF NOT EXISTS `game_modify_currency`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `sm_gbId` bigint UNSIGNED NOT NULL DEFAULT 0,
  `sm_money` bigint NOT NULL DEFAULT 0,
  `sm_bindMoney` bigint NOT NULL DEFAULT 0,
  `sm_coin` bigint NOT NULL DEFAULT 0,
  `sm_darkIron` bigint NOT NULL DEFAULT 0,
  `sm_guildContrib` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_gbId`(`sm_gbId`)
);

DROP PROCEDURE IF EXISTS gamesp_record_modify_currency;
DELIMITER ;;
CREATE PROCEDURE gamesp_record_modify_currency(
        IN gbId BIGINT(20),
        IN fieldStr VARCHAR(255),
        IN updateNum INT
    )
    BEGIN
        DECLARE cur_value BIGINT DEFAULT 0;
        DECLARE update_old_value BIGINT DEFAULT 0;
        DECLARE update_new_value BIGINT DEFAULT 0;
        
        DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            ROLLBACK;
            RESIGNAL;
        END;

        SET @p_gbId = gbId;
        SET @p_updateNum = updateNum;
        
        START TRANSACTION;
        
        SET @sql_cur = CONCAT('SELECT `', fieldStr, '` INTO @cur_val FROM `tbl_Avatar` WHERE `sm_gbID` = ? LIMIT 1');
        PREPARE stmt FROM @sql_cur;
        EXECUTE stmt USING @p_gbId;
        DEALLOCATE PREPARE stmt;
        SET cur_value = @cur_val;
        
        SET @old_val = NULL;
        SET @sql_old = CONCAT('SELECT `', fieldStr, '` INTO @old_val FROM `game_modify_currency` WHERE `sm_gbID` = ? LIMIT 1');
        PREPARE stmt FROM @sql_old;
        EXECUTE stmt USING @p_gbId;
        DEALLOCATE PREPARE stmt;
        SET update_old_value = IFNULL(@old_val, 0);
        
        SET @sql_update = CONCAT(
            'INSERT INTO `game_modify_currency` (`sm_gbID`, `', fieldStr, '`) VALUES (?, ?) ',
            'ON DUPLICATE KEY UPDATE `', fieldStr, '` = `', fieldStr, '` + ?'
        );
        PREPARE stmt FROM @sql_update;
        EXECUTE stmt USING @p_gbId, @p_updateNum, @p_updateNum;
        DEALLOCATE PREPARE stmt;
        
        SET @sql_new = CONCAT('SELECT `', fieldStr, '` INTO @new_val FROM `game_modify_currency` WHERE `sm_gbID` = ? LIMIT 1');
        PREPARE stmt FROM @sql_new;
        EXECUTE stmt USING @p_gbId;
        DEALLOCATE PREPARE stmt;
        SET update_new_value = @new_val;
        
        SELECT 
            gbId AS `gbId`,
            fieldStr AS `fieldName`,
            cur_value AS `curValue`,
            updateNum AS `updateNum`,
            update_old_value AS `updateOldNum`,
            update_new_value AS `updateNewNum`;
        
        COMMIT;
    END;;
DELIMITER ;

DROP PROCEDURE IF EXISTS gamesp_record_mul_modify_currency;
DELIMITER ;;
CREATE PROCEDURE gamesp_record_mul_modify_currency(
        IN gbId BIGINT(20),
        IN fieldListStr VARCHAR(1000),
        IN updateNumListStr VARCHAR(1000)
    )
    BEGIN
        DECLARE done INT DEFAULT FALSE;
        DECLARE field_name VARCHAR(255);
        DECLARE update_val BIGINT;
        DECLARE cur_value BIGINT DEFAULT 0;
        DECLARE update_old_value BIGINT DEFAULT 0;
        DECLARE update_new_value BIGINT DEFAULT 0;
        
        DECLARE field_cursor CURSOR FOR 
        SELECT 
            TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(fieldListStr, ',', n.n), ',', -1)) AS field_name,
            CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(updateNumListStr, ',', n.n), ',', -1)) AS SIGNED) AS update_val
        FROM 
            (SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 
            UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) n
        WHERE 
            n.n <= (LENGTH(fieldListStr) - LENGTH(REPLACE(fieldListStr, ',', '')) + 1)
        ORDER BY n.n;
        
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
        
        DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            DROP TEMPORARY TABLE IF EXISTS temp_result;
            ROLLBACK;
            RESIGNAL;
        END;
        
        DROP TEMPORARY TABLE IF EXISTS temp_result;
        CREATE TEMPORARY TABLE temp_result (
            fieldName VARCHAR(255),
            curValue BIGINT,
            updateNum BIGINT,
            updateOldNum BIGINT,
            updateNewNum BIGINT
        );
        
        SET @p_gbId = gbId;
        
        START TRANSACTION;
        
        OPEN field_cursor;
        
        read_loop: LOOP
            FETCH field_cursor INTO field_name, update_val;
            IF done THEN
                LEAVE read_loop;
            END IF;
            
            SET @p_update_val = update_val;
            SET @sql_cur = CONCAT('SELECT `', field_name, '` INTO @cur_val FROM `tbl_Avatar` WHERE `sm_gbID` = ? LIMIT 1');
            PREPARE stmt FROM @sql_cur;
            EXECUTE stmt USING @p_gbId;
            DEALLOCATE PREPARE stmt;
            SET cur_value = IFNULL(@cur_val, 0);
            
            SET @old_val = NULL;
            SET @sql_old = CONCAT('SELECT `', field_name, '` INTO @old_val FROM `game_modify_currency` WHERE `sm_gbID` = ? LIMIT 1');
            PREPARE stmt FROM @sql_old;
            EXECUTE stmt USING @p_gbId;
            DEALLOCATE PREPARE stmt;
            SET update_old_value = IFNULL(@old_val, 0);
            
            SET @sql_update = CONCAT(
                'INSERT INTO `game_modify_currency` (`sm_gbID`, `', field_name, '`) VALUES (?, ?) ',
                'ON DUPLICATE KEY UPDATE `', field_name, '` = `', field_name, '` + ?'
            );
            PREPARE stmt FROM @sql_update;
            EXECUTE stmt USING @p_gbId, @p_update_val, @p_update_val;
            DEALLOCATE PREPARE stmt;
            
            SET @sql_new = CONCAT('SELECT `', field_name, '` INTO @new_val FROM `game_modify_currency` WHERE `sm_gbID` = ? LIMIT 1');
            PREPARE stmt FROM @sql_new;
            EXECUTE stmt USING @p_gbId;
            DEALLOCATE PREPARE stmt;
            SET update_new_value = IFNULL(@new_val, 0);
            
            INSERT INTO temp_result VALUES (field_name, cur_value, update_val, update_old_value, update_new_value);
            
            SET done = FALSE;
        END LOOP;
        
        CLOSE field_cursor;
        
        SELECT 
            gbId AS `gbId`,
            fieldName,
            curValue,
            updateNum,
            updateOldNum,
            updateNewNum
        FROM temp_result;
        
        DROP TEMPORARY TABLE IF EXISTS temp_result;
        
        COMMIT;
    END;;
DELIMITER ;

DROP PROCEDURE IF EXISTS gamesp_load_modify_currency;
DELIMITER ;;
CREATE PROCEDURE gamesp_load_modify_currency(
        IN gbId BIGINT(20)
    )
    BEGIN
        SELECT `sm_money`, `sm_bindMoney`, `sm_coin`, `sm_darkIron`, `sm_guildContrib` FROM `game_modify_currency` where sm_gbID=gbId limit 1;
        DELETE FROM `game_modify_currency` WHERE sm_gbID=gbId;
    END;;
DELIMITER ;