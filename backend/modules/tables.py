# TODO setup actual tables here
TABLES = {
    "players": (
        "CREATE TABLE `players` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `discord_id` varchar(64) NOT NULL,"
        "  PRIMARY KEY (`discord_id`),"
        "  UNIQUE KEY (`id`, `discord_id`)"
        ") ENGINE=InnoDB"
    ),
    "servers": (
        "CREATE TABLE `servers` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(255) NOT NULL,"
        "  `discord_id` varchar(255) NOT NULL,"
        "  PRIMARY KEY (`id`),"
        "  UNIQUE KEY (`id`, `discord_id`)"
        ") ENGINE=InnoDB"
    ),
    "channels": (
        "CREATE TABLE `channels` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(255) NOT NULL,"
        "  `discord_id` varchar(255) NOT NULL,"
        "  `server_id` int NOT NULL,"
        "  PRIMARY KEY (`id`),"
        "  UNIQUE KEY (`id`, `discord_id`),"
        "  FOREIGN KEY (`server_id`) REFERENCES servers(`id`)"
        ") ENGINE=InnoDB"
    ),
    "parties": (
        "CREATE TABLE `parties` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `title` varchar(255) NOT NULL,"
        "  `game` varchar(64),"
        "  `max_players` int NOT NULL,"
        "  `description` varchar(2000),"
        "  `notify_channel` int,"
        "  PRIMARY KEY (`id`),"
        "  UNIQUE KEY (`id`),"
        "  FOREIGN KEY (`notify_channel`) REFERENCES channels(`id`)"
        ") ENGINE=InnoDB"
    ),
    "rolesInParties": (
        "CREATE TABLE `rolesInParties` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `party_id` int NOT NULL,"
        "  `name` varchar(64) NOT NULL,"
        "  `max_players` int,"
        "  PRIMARY KEY (`id`),"
        "  UNIQUE KEY (`id`),"
        "  FOREIGN KEY (`party_id`) REFERENCES parties(`id`)"
        ") ENGINE=InnoDB"
    ),
    "playersInParties": (
        "CREATE TABLE `playersInParties` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `party_id` int NOT NULL,"
        "  `player_id` int NOT NULL,"
        "  `role_id` int,"
        "  PRIMARY KEY (`id`),"
        "  UNIQUE KEY (`id`),"
        "  FOREIGN KEY (`party_id`) REFERENCES parties(`id`),"
        "  FOREIGN KEY (`player_id`) REFERENCES players(`id`),"
        "  FOREIGN KEY (`role_id`) REFERENCES rolesInParties(`id`)"
        ") ENGINE=InnoDB"
    )

}
