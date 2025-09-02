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
        `accountName` varchar(128) NOT NULL,
        `accountGmMode` int(10) NOT NULL DEFAULT 0,
         index `accountName` (`accountName`)
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

    INSERT INTO game_player_mails (toGBID, mailId, mailGBID, globalMailGBID, readStat, createTime,
                                   expiredTime, fromGBID, attach, attachStat, despArgs, title, cont, opUUID,
                                   srcType, srcSubType, desp, idipSource)
    VALUES (p_toGBID, p_mailId, p_mailGBID, p_globalMailGBID, p_readState,
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
