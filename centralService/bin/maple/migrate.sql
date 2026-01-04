-- Add start_time column to maple table
ALTER TABLE `maple`
    ADD COLUMN `start_time` INT(11) NOT NULL DEFAULT 0 AFTER `alias`;

-- Add central_login column to maple table
ALTER TABLE `maple`
    ADD COLUMN `central_login` VARCHAR(255) NOT NULL DEFAULT '' AFTER `queue_server`;

-- Create maple_kv table
CREATE TABLE IF NOT EXISTS `maple_kv` (
    `key` VARCHAR(255) NOT NULL,
    `value` TEXT NOT NULL,
    PRIMARY KEY (`key`)
);
