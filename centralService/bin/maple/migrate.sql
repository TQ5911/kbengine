-- Add start_time column to maple table
ALTER TABLE `maple`
    ADD COLUMN `start_time` INT(11) NOT NULL DEFAULT 0 AFTER `alias`;
