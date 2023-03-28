# ************************************************************
# Sequel Ace SQL dump
# Version 20035
#
# https://sequel-ace.com/
# https://github.com/Sequel-Ace/Sequel-Ace
#
# Host: 127.0.0.1 (MySQL 8.0.32)
# Database: tasker
# Generation Time: 2023-03-28 07:26:33 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE='NO_AUTO_VALUE_ON_ZERO', SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table tasks
# ------------------------------------------------------------

DROP TABLE IF EXISTS `tasks`;

CREATE TABLE `tasks` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `group_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `started_at` datetime DEFAULT NULL,
  `finished_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;

INSERT INTO `tasks` (`id`, `name`, `group_id`, `user_id`, `started_at`, `finished_at`)
VALUES
	(71,'aaaaaaaa',NULL,2,'2023-03-28 10:09:57',NULL),
	(74,'Uztaisit UI spēlitei',NULL,4,'2023-03-28 10:12:13','2023-03-28 10:12:31'),
	(68,'Uztaisīt prezentāciju dabaszinībās līdz nākamai nedēļai.',NULL,3,NULL,NULL),
	(40,'read book',NULL,2,NULL,NULL),
	(77,'Hack todo list',NULL,5,NULL,NULL),
	(75,'ツツツtest',NULL,4,NULL,NULL),
	(73,'wdwdwdw',NULL,2,NULL,NULL),
	(72,'bbbbbbb',NULL,2,NULL,NULL),
	(65,'play',NULL,1,'2023-03-27 23:43:10','2023-03-27 23:43:14'),
	(64,'make',NULL,1,'2023-03-27 23:48:58','2023-03-27 23:49:03'),
	(63,'task',NULL,1,'2023-03-27 23:49:05','2023-03-27 23:49:06'),
	(79,'do homework',NULL,1,NULL,NULL),
	(80,'aaaaa',NULL,1,NULL,NULL),
	(81,'wdwdsds',NULL,1,'2023-03-28 10:13:55','2023-03-28 10:13:58'),
	(82,'sdsdsdd',NULL,1,'2023-03-28 10:13:58','2023-03-28 10:14:43');

/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`id`, `name`, `password`)
VALUES
	(1,'Deniss','12345'),
	(2,'Alex','12345'),
	(3,'Tomass','12345'),
	(4,'Edijs','456');

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
