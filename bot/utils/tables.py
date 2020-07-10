TABLES = {
    "webhooks": (
        "CREATE TABLE `webhooks` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `identifier` varchar(64) NOT NULL,"
        "  `name` varchar(64) NOT NULL,"
        "  `type` varchar(16) NOT NULL,"
        "  `channel` varchar(64) NOT NULL,"
        "  `icon_url` varchar(255),"
        "  PRIMARY KEY (`identifier`),"
        "  UNIQUE KEY (`id`, `identifier`)"
        ") ENGINE=InnoDB"
    )
}
