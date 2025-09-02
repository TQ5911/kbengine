ALTER TABLE `game_admin_cmds` ADD COLUMN `result` int DEFAULT 0;
ALTER TABLE `game_admin_cmds` ADD COLUMN `retErrMsg` varchar(255) NOT NULL;
ALTER TABLE `game_admin_cmds` ADD COLUMN `retStr` varchar(1024) NOT NULL;