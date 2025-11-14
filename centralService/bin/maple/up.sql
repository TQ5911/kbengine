
CREATE TABLE IF NOT EXISTS `maple` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `server_id` int(11) NOT NULL,
    `server_name` varchar(255) NOT NULL,
    `zone_id` int(11) NOT NULL,
    `game_server` varchar(255) NOT NULL,
    `queue_server` varchar(255) NOT NULL,
    `server_group` int(11) NOT NULL,
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

