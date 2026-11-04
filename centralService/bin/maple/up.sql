
CREATE TABLE IF NOT EXISTS `maple` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `server_id` int(11) NOT NULL,
    `server_name` varchar(255) NOT NULL,
    `zone_id` int(11) NOT NULL,
    `game_server` varchar(255) NOT NULL,
    `queue_server` varchar(255) NOT NULL,
    `central_login` varchar(255) NOT NULL,
    `server_group` int(11) NOT NULL,
    `server_sub_group` int(11) NOT NULL DEFAULT 1,
    `server_state` int(11) NOT NULL,
    `server_flag_state` int(11) NOT NULL,
    `alias` varchar(255) NOT NULL,
    `start_time` int(11) NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `server_id` (`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `maple_zone` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `zone_id` int(11) NOT NULL,
    `zone_name` varchar(255) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `zone_id` (`zone_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `maple_kv` (
    `key` VARCHAR(255) NOT NULL,
    `value` TEXT NOT NULL,
    PRIMARY KEY (`key`)
);


-- 和服映射: from_server_id 是被合入的服, to_server_id 是合入目标
-- 每服最多一条出边, 由 PRIMARY KEY (from_server_id) 保证
CREATE TABLE IF NOT EXISTS `maple_merge_server` (
    `from_server_id` INT NOT NULL,
    `to_server_id`   INT NOT NULL,
    PRIMARY KEY (`from_server_id`),
    INDEX `idx_to` (`to_server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET @db_name = DATABASE();
SET @table_name = 'maple';

SET @column_name = 'server_sub_group';
SET @column_def = 'int(11) NOT NULL DEFAULT 1';

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
