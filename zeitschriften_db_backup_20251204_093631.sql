-- MySQL dump 10.13  Distrib 9.5.0, for macos26.0 (arm64)
--
-- Host: 127.0.0.1    Database: zeitschriften_db
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aktionen`
--

DROP TABLE IF EXISTS `aktionen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aktionen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `benutzer_id` int(11) NOT NULL,
  `aktion` varchar(255) NOT NULL,
  `zeitpunkt` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `benutzer_id` (`benutzer_id`),
  CONSTRAINT `aktionen_ibfk_1` FOREIGN KEY (`benutzer_id`) REFERENCES `benutzer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=406 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aktionen`
--

LOCK TABLES `aktionen` WRITE;
/*!40000 ALTER TABLE `aktionen` DISABLE KEYS */;
INSERT INTO `aktionen` VALUES (185,26,'fehlgeschlagener Loginversuch','2025-12-02 10:01:47'),(186,26,'hat sich angemeldet','2025-12-02 10:03:00'),(187,26,'hat sich angemeldet','2025-12-02 10:03:43'),(188,26,'hat sich angemeldet','2025-12-02 10:06:25'),(189,26,'hat Benutzerliste aufgerufen','2025-12-02 10:06:29'),(190,26,'hat Benutzer admin#1 entfernt','2025-12-02 10:06:35'),(191,26,'hat Benutzerliste aufgerufen','2025-12-02 10:06:35'),(192,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:09:36'),(193,26,'hat Benutzerliste aufgerufen','2025-12-02 10:09:36'),(194,26,'hat sich angemeldet','2025-12-02 10:12:26'),(195,26,'hat Benutzerliste aufgerufen','2025-12-02 10:12:29'),(196,26,'hat Benutzerliste aufgerufen','2025-12-02 10:12:51'),(197,26,'hat Benutzerliste aufgerufen','2025-12-02 10:14:24'),(198,26,'hat Benutzerliste aufgerufen','2025-12-02 10:14:39'),(199,26,'hat Benutzer admin#3 hinzugefügt','2025-12-02 10:15:08'),(200,26,'hat Benutzerliste aufgerufen','2025-12-02 10:15:08'),(201,26,'hat Benutzerliste aufgerufen','2025-12-02 10:15:28'),(202,26,'hat Benutzerliste aufgerufen','2025-12-02 10:16:25'),(203,26,'hat Benutzer admin#4 hinzugefügt','2025-12-02 10:16:57'),(204,26,'hat Benutzerliste aufgerufen','2025-12-02 10:16:57'),(205,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:17:40'),(206,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:20:09'),(207,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:20:17'),(208,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:21:49'),(209,26,'hat sich angemeldet','2025-12-02 10:22:18'),(210,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:22:20'),(211,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:22:26'),(212,26,'hat Benutzerliste aufgerufen','2025-12-02 10:23:12'),(213,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:23:14'),(214,26,'hat Zeitschrift \'Pups\' hinzugefügt','2025-12-02 10:23:26'),(215,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:23:26'),(216,26,'hat sich angemeldet','2025-12-02 10:25:08'),(217,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:25:13'),(218,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:25:16'),(219,26,'hat sich angemeldet','2025-12-02 10:55:50'),(220,26,'hat sich angemeldet','2025-12-02 10:57:47'),(221,26,'hat sich angemeldet','2025-12-02 11:45:45'),(222,26,'hat sich angemeldet','2025-12-02 11:46:52'),(223,26,'hat Benutzerliste aufgerufen','2025-12-02 11:46:55'),(224,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 11:47:00'),(225,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 11:48:53'),(226,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 11:49:20'),(227,26,'hat Bestand um 5 für Zeitschrift 1 erhöht','2025-12-02 11:49:31'),(228,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 11:49:31'),(229,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 11:50:44'),(230,26,'hat Benutzerliste aufgerufen','2025-12-02 11:50:51'),(231,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 11:52:16'),(232,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 11:52:20'),(233,26,'hat Benutzerliste aufgerufen','2025-12-02 11:52:21'),(234,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 11:53:47'),(235,26,'hat sich angemeldet','2025-12-02 12:00:05'),(236,26,'hat Benutzerliste aufgerufen','2025-12-02 12:00:06'),(237,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 12:00:07'),(238,26,'hat sich angemeldet','2025-12-02 12:10:34'),(239,26,'hat Benutzerliste aufgerufen','2025-12-02 12:10:38'),(240,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 12:10:41'),(241,26,'hat sich angemeldet','2025-12-02 12:15:15'),(242,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 12:15:17'),(243,26,'hat Benutzerliste aufgerufen','2025-12-02 12:16:21'),(244,26,'hat Benutzer user#2 hinzugefügt','2025-12-02 12:17:05'),(245,26,'hat Benutzerliste aufgerufen','2025-12-02 12:17:05'),(246,26,'hat Benutzer user#3 hinzugefügt','2025-12-02 12:17:26'),(247,26,'hat Benutzerliste aufgerufen','2025-12-02 12:17:26'),(248,26,'hat Benutzer user#4 hinzugefügt','2025-12-02 12:17:45'),(249,26,'hat Benutzerliste aufgerufen','2025-12-02 12:17:45'),(250,26,'hat Benutzer user#5 hinzugefügt','2025-12-02 12:18:21'),(251,26,'hat Benutzerliste aufgerufen','2025-12-02 12:18:21'),(252,26,'hat Benutzer user#6 hinzugefügt','2025-12-02 12:18:36'),(253,26,'hat Benutzerliste aufgerufen','2025-12-02 12:18:36'),(254,26,'hat Benutzer user#7 hinzugefügt','2025-12-02 12:19:01'),(255,26,'hat Benutzerliste aufgerufen','2025-12-02 12:19:01'),(256,26,'hat Benutzer user#8 hinzugefügt','2025-12-02 12:19:26'),(257,26,'hat Benutzerliste aufgerufen','2025-12-02 12:19:26'),(258,26,'hat Benutzerliste aufgerufen','2025-12-02 12:19:43'),(259,26,'hat Benutzer user#9 hinzugefügt','2025-12-02 12:19:59'),(260,26,'hat Benutzerliste aufgerufen','2025-12-02 12:19:59'),(261,26,'hat Benutzerliste aufgerufen','2025-12-02 12:20:14'),(262,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 12:20:19'),(263,26,'hat Benutzerliste aufgerufen','2025-12-02 12:20:38'),(264,26,'hat sich angemeldet','2025-12-02 12:28:10'),(265,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 12:28:12'),(266,26,'hat Zeitschrift \'c‘t Magazin für Computertechnik\' hinzugefügt','2025-12-02 12:30:07'),(267,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 12:30:07'),(268,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 12:30:37'),(269,26,'hat Zeitschrift \'c‘t Magazin für Computertechnik\' gelöscht','2025-12-02 12:30:40'),(270,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 12:30:40'),(271,26,'hat Zeitschrift \'c‘t Magazin für Computertechnik\' gelöscht','2025-12-02 12:30:44'),(272,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 12:30:44'),(273,26,'hat Benutzerliste aufgerufen','2025-12-02 12:30:46'),(274,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 12:30:47'),(275,26,'hat sich angemeldet','2025-12-02 13:03:03'),(276,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:03:05'),(277,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:03:31'),(278,26,'hat Bestand um 5 für Zeitschrift 6 erhöht','2025-12-02 13:05:07'),(279,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:05:07'),(280,29,'hat \'c‘t Magazin für Computertechnik\' ausgeliehen','2025-12-02 13:06:58'),(281,26,'hat sich angemeldet','2025-12-02 13:07:11'),(282,26,'hat Benutzerliste aufgerufen','2025-12-02 13:08:45'),(283,26,'hat Benutzerliste aufgerufen','2025-12-02 13:09:07'),(284,26,'hat Benutzerliste aufgerufen','2025-12-02 13:09:10'),(285,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:09:11'),(286,26,'hat Benutzerliste aufgerufen','2025-12-02 13:09:12'),(287,26,'hat Benutzerliste aufgerufen','2025-12-02 13:09:15'),(288,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:09:16'),(289,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:11:41'),(290,26,'hat Benutzerliste aufgerufen','2025-12-02 13:11:43'),(291,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:11:44'),(292,26,'hat Benutzerliste aufgerufen','2025-12-02 13:11:54'),(293,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:11:55'),(294,26,'hat Benutzerliste aufgerufen','2025-12-02 13:12:00'),(295,26,'hat Benutzerliste aufgerufen','2025-12-02 13:12:02'),(296,26,'hat Benutzerliste aufgerufen','2025-12-02 13:12:05'),(297,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:12:08'),(298,26,'hat sich angemeldet','2025-12-02 13:13:08'),(299,26,'hat Benutzerliste aufgerufen','2025-12-02 13:13:10'),(300,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:13:11'),(301,26,'hat Benutzerliste aufgerufen','2025-12-02 13:13:22'),(302,26,'hat Benutzerliste aufgerufen','2025-12-02 13:13:30'),(303,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:13:31'),(304,26,'hat Benutzerliste aufgerufen','2025-12-02 13:14:13'),(305,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:14:14'),(306,26,'hat Benutzerliste aufgerufen','2025-12-02 13:14:42'),(307,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:14:43'),(308,26,'hat Benutzerliste aufgerufen','2025-12-02 13:15:50'),(309,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:15:52'),(310,26,'hat Benutzerliste aufgerufen','2025-12-02 13:15:57'),(311,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:15:58'),(312,26,'hat Benutzerliste aufgerufen','2025-12-02 13:16:09'),(313,26,'hat sich angemeldet','2025-12-02 13:18:50'),(314,26,'hat Benutzerliste aufgerufen','2025-12-02 13:20:15'),(315,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:20:23'),(316,26,'hat Benutzerliste aufgerufen','2025-12-02 13:21:40'),(317,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:22:01'),(318,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:22:28'),(319,26,'hat Zeitschrift 6 bearbeitet','2025-12-02 13:23:17'),(320,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:23:17'),(321,26,'hat Benutzerliste aufgerufen','2025-12-02 13:24:56'),(322,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:24:57'),(323,26,'hat Bestand um 1 für Zeitschrift 6 reduziert','2025-12-02 13:25:12'),(324,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:25:12'),(325,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:27:07'),(326,26,'hat Benutzerliste aufgerufen','2025-12-02 13:29:37'),(327,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:29:38'),(328,26,'hat Bestand um 1 erhöht für Zeitschrift \'c‘t Magazin für Computertechnik\' 22','2025-12-02 13:29:52'),(329,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:29:52'),(330,26,'hat Benutzerliste aufgerufen','2025-12-02 13:30:09'),(331,26,'hat Benutzerliste aufgerufen','2025-12-02 13:30:13'),(332,26,'hat Benutzerliste aufgerufen','2025-12-02 13:30:16'),(333,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:31:08'),(334,26,'hat Zeitschrift \'Test\' hinzugefügt','2025-12-02 13:31:17'),(335,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:31:17'),(336,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:31:25'),(337,26,'hat Zeitschrift \'Test\' gelöscht','2025-12-02 13:31:34'),(338,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:31:34'),(339,26,'hat Zeitschrift \'Test2\' gelöscht','2025-12-02 13:31:38'),(340,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:31:38'),(341,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:31:45'),(342,26,'hat Zeitschrift \'Test2\' gelöscht','2025-12-02 13:31:53'),(343,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:31:54'),(344,26,'hat Benutzerliste aufgerufen','2025-12-02 13:33:25'),(345,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:33:26'),(346,26,'hat Zeitschrift \'Pups\' gelöscht','2025-12-02 13:33:32'),(347,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:33:32'),(348,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:33:39'),(349,26,'hat Zeitschrift \'Ct\' gelöscht','2025-12-02 13:33:47'),(350,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:33:47'),(351,26,'hat Ausleihe 4 storniert','2025-12-02 13:34:14'),(352,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:34:25'),(353,26,'hat Zeitschrift \'Gartenpraxis 3\' gelöscht','2025-12-02 13:34:31'),(354,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:34:31'),(355,26,'hat sich angemeldet','2025-12-02 13:41:52'),(356,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:42:02'),(357,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:43:50'),(358,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:46:36'),(359,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:46:46'),(360,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:48:15'),(361,26,'hat Zeitschrift \'Ct Magazin für Computertechnik \' hinzugefügt','2025-12-02 13:48:49'),(362,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:48:49'),(363,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:49:25'),(364,26,'hat Bestand um 5 reduziert für Zeitschrift \'Ct Magazin für Computertechnik \' 22/2024','2025-12-02 13:49:35'),(365,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:49:35'),(366,26,'hat Benutzerliste aufgerufen','2025-12-02 13:49:50'),(367,29,'hat \'Ct Magazin für Computertechnik \' ausgeliehen','2025-12-02 13:50:21'),(368,26,'hat sich angemeldet','2025-12-02 13:50:35'),(369,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 13:54:23'),(370,29,'hat \'Ct Magazin für Computertechnik \' zurückgegeben','2025-12-02 13:54:47'),(371,26,'hat sich angemeldet','2025-12-02 14:01:43'),(372,26,'hat Benutzerliste aufgerufen','2025-12-02 14:02:01'),(373,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 14:02:09'),(374,26,'hat Bestand um 5 erhöht für Zeitschrift \'Ct Magazin für Computertechnik \' 22/2024','2025-12-02 14:02:24'),(375,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 14:02:25'),(376,26,'hat Zeitschrift \'Didacta\' hinzugefügt','2025-12-02 14:03:34'),(377,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 14:03:34'),(378,26,'hat Benutzerliste aufgerufen','2025-12-02 14:04:22'),(379,26,'hat Benutzerliste aufgerufen','2025-12-02 14:06:39'),(380,26,'hat sich angemeldet','2025-12-03 06:31:09'),(381,26,'hat Benutzerliste aufgerufen','2025-12-03 06:31:44'),(382,26,'hat Zeitschriftenliste aufgerufen','2025-12-03 06:32:07'),(383,25,'hat \'Ct Magazin für Computertechnik \' ausgeliehen','2025-12-03 06:36:37'),(384,26,'hat sich angemeldet','2025-12-03 06:36:51'),(385,25,'hat \'Ct Magazin für Computertechnik \' 22/2024 ausgeliehen','2025-12-03 08:09:28'),(386,28,'hat sich angemeldet','2025-12-03 08:09:49'),(387,28,'hat Benutzerliste aufgerufen','2025-12-03 08:10:13'),(388,28,'hat Benutzerliste aufgerufen','2025-12-03 08:11:14'),(389,28,'hat Benutzerliste aufgerufen','2025-12-03 08:12:04'),(390,28,'hat Zeitschriftenliste aufgerufen','2025-12-03 08:12:46'),(391,28,'hat Zeitschriftenliste aufgerufen','2025-12-03 08:13:05'),(392,28,'hat Zeitschriftenliste aufgerufen','2025-12-03 08:13:26'),(393,28,'hat Benutzerliste aufgerufen','2025-12-03 08:13:27'),(394,28,'hat Benutzerliste aufgerufen','2025-12-03 08:14:04'),(395,26,'hat sich angemeldet','2025-12-03 08:15:10'),(396,26,'hat Zeitschriftenliste aufgerufen','2025-12-03 08:15:12'),(397,26,'hat Zeitschriftenliste aufgerufen','2025-12-03 08:19:06'),(398,26,'hat Benutzerliste aufgerufen','2025-12-03 08:23:13'),(399,26,'hat Zeitschriftenliste aufgerufen','2025-12-03 08:23:45'),(400,25,'hat \'Ct Magazin für Computertechnik \' 22/2024 ausgeliehen','2025-12-04 08:20:21'),(401,26,'hat sich angemeldet','2025-12-04 08:20:36'),(402,26,'hat Benutzerliste aufgerufen','2025-12-04 08:21:07'),(403,26,'hat Benutzerliste aufgerufen','2025-12-04 08:21:36'),(404,26,'hat Zeitschriftenliste aufgerufen','2025-12-04 08:23:56'),(405,26,'hat Zeitschriftenliste aufgerufen','2025-12-04 08:24:18');
/*!40000 ALTER TABLE `aktionen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ausleihen`
--

DROP TABLE IF EXISTS `ausleihen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ausleihen` (
  `AusleiheID` int(11) NOT NULL AUTO_INCREMENT,
  `Ausleihdatum` datetime DEFAULT current_timestamp(),
  `Rueckgabedatum` datetime DEFAULT NULL,
  `ExemplarID` int(11) NOT NULL,
  `BenutzerID` int(11) NOT NULL,
  PRIMARY KEY (`AusleiheID`),
  KEY `ExemplarID` (`ExemplarID`),
  KEY `BenutzerID` (`BenutzerID`),
  CONSTRAINT `ausleihen_ibfk_1` FOREIGN KEY (`ExemplarID`) REFERENCES `exemplare` (`ExemplarID`),
  CONSTRAINT `ausleihen_ibfk_2` FOREIGN KEY (`BenutzerID`) REFERENCES `benutzer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ausleihen`
--

LOCK TABLES `ausleihen` WRITE;
/*!40000 ALTER TABLE `ausleihen` DISABLE KEYS */;
INSERT INTO `ausleihen` VALUES (4,'2025-12-02 14:06:58','2025-12-02 14:34:14',4,29),(5,'2025-12-02 14:50:21','2025-12-02 14:54:47',4,29),(6,'2025-12-03 07:36:37',NULL,4,25),(7,'2025-12-03 09:09:28',NULL,4,25),(8,'2025-12-04 09:20:21',NULL,4,25);
/*!40000 ALTER TABLE `ausleihen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ausleihen_alt`
--

DROP TABLE IF EXISTS `ausleihen_alt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ausleihen_alt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `zeitschrift_id` int(11) DEFAULT NULL,
  `benutzer_id` int(11) DEFAULT NULL,
  `ausleihdatum` datetime DEFAULT current_timestamp(),
  `rueckgabedatum` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `zeitschrift_id` (`zeitschrift_id`),
  KEY `benutzer_id` (`benutzer_id`),
  CONSTRAINT `ausleihen_alt_ibfk_1` FOREIGN KEY (`zeitschrift_id`) REFERENCES `zeitschriften_alt` (`id`),
  CONSTRAINT `ausleihen_alt_ibfk_2` FOREIGN KEY (`benutzer_id`) REFERENCES `benutzer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ausleihen_alt`
--

LOCK TABLES `ausleihen_alt` WRITE;
/*!40000 ALTER TABLE `ausleihen_alt` DISABLE KEYS */;
/*!40000 ALTER TABLE `ausleihen_alt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ausleihen_backup_20251202`
--

DROP TABLE IF EXISTS `ausleihen_backup_20251202`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ausleihen_backup_20251202` (
  `AusleiheID` int(11) NOT NULL DEFAULT 0,
  `Ausleihdatum` datetime DEFAULT current_timestamp(),
  `Rueckgabedatum` datetime DEFAULT NULL,
  `ExemplarID` int(11) NOT NULL,
  `BenutzerID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ausleihen_backup_20251202`
--

LOCK TABLES `ausleihen_backup_20251202` WRITE;
/*!40000 ALTER TABLE `ausleihen_backup_20251202` DISABLE KEYS */;
/*!40000 ALTER TABLE `ausleihen_backup_20251202` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `benutzer`
--

DROP TABLE IF EXISTS `benutzer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `benutzer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('admin','user') NOT NULL DEFAULT 'user',
  `display_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `idx_benutzer_display_name` (`display_name`(100))
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `benutzer`
--

LOCK TABLES `benutzer` WRITE;
/*!40000 ALTER TABLE `benutzer` DISABLE KEYS */;
INSERT INTO `benutzer` VALUES (25,'user#1',NULL,'user',NULL),(26,'admin#2','$2b$12$l2zMJAsV.Gdr8j00WMXgG.Z9ZTnHinMIoP7mJWxr3GpPvAGx/zYLa','admin',NULL),(27,'admin#3','$2b$12$i6EWLAhs/VuXatGmJ3UH8en59Zzcc7mit.w45y6PBWygMUK3ZXjbS','admin',NULL),(28,'admin#4','$2b$12$5XFsT9oUB/s/xIImUenpDOlZF09i50EMi3W8POy333cASw2RKnPY6','admin',NULL),(29,'user#2',NULL,'user',NULL),(30,'user#3',NULL,'user',NULL),(31,'user#4',NULL,'user',NULL),(32,'user#5',NULL,'user',NULL),(33,'user#6',NULL,'user',NULL),(34,'user#7',NULL,'user',NULL),(35,'user#8',NULL,'user',NULL),(36,'user#9',NULL,'user',NULL);
/*!40000 ALTER TABLE `benutzer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exemplare`
--

DROP TABLE IF EXISTS `exemplare`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exemplare` (
  `ExemplarID` int(11) NOT NULL AUTO_INCREMENT,
  `ZeitschriftID` int(11) NOT NULL,
  `Bestand` int(11) NOT NULL DEFAULT 0,
  `Verfuegbar` int(11) NOT NULL DEFAULT 0,
  `Aktiv` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`ExemplarID`),
  UNIQUE KEY `uniq_zeitschrift` (`ZeitschriftID`),
  CONSTRAINT `exemplare_ibfk_1` FOREIGN KEY (`ZeitschriftID`) REFERENCES `zeitschriften` (`ZeitschriftID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exemplare`
--

LOCK TABLES `exemplare` WRITE;
/*!40000 ALTER TABLE `exemplare` DISABLE KEYS */;
INSERT INTO `exemplare` VALUES (1,1,6,0,0),(2,2,1,0,0),(3,3,1,0,0),(4,6,10,7,1),(10,7,0,0,0),(12,8,1,1,1);
/*!40000 ALTER TABLE `exemplare` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exemplare_backup_20251202`
--

DROP TABLE IF EXISTS `exemplare_backup_20251202`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exemplare_backup_20251202` (
  `ExemplarID` int(11) NOT NULL DEFAULT 0,
  `Barcode` varchar(100) NOT NULL,
  `Erscheinungsdatum` date DEFAULT NULL,
  `AusgabeHeftnummer` varchar(50) DEFAULT NULL,
  `Aktiv` tinyint(1) DEFAULT 1,
  `ZeitschriftID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exemplare_backup_20251202`
--

LOCK TABLES `exemplare_backup_20251202` WRITE;
/*!40000 ALTER TABLE `exemplare_backup_20251202` DISABLE KEYS */;
INSERT INTO `exemplare_backup_20251202` VALUES (1,'5678',NULL,NULL,1,1),(2,'4190290312955',NULL,NULL,1,2),(3,'4199148406204','2025-06-17','22',1,3);
/*!40000 ALTER TABLE `exemplare_backup_20251202` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zeitschriften`
--

DROP TABLE IF EXISTS `zeitschriften`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zeitschriften` (
  `ZeitschriftID` int(11) NOT NULL AUTO_INCREMENT,
  `Titel` varchar(255) NOT NULL,
  `barcode` varchar(255) DEFAULT NULL,
  `ausgabe_heftnummer` varchar(255) DEFAULT NULL,
  `erscheinungsdatum` date DEFAULT NULL,
  `aktiv` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`ZeitschriftID`),
  UNIQUE KEY `barcode` (`barcode`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zeitschriften`
--

LOCK TABLES `zeitschriften` WRITE;
/*!40000 ALTER TABLE `zeitschriften` DISABLE KEYS */;
INSERT INTO `zeitschriften` VALUES (1,'Test2',NULL,NULL,NULL,0),(2,'Gartenpraxis 3',NULL,NULL,NULL,0),(3,'Ct',NULL,NULL,NULL,0),(5,'Pups',NULL,NULL,NULL,0),(6,'Ct Magazin für Computertechnik ','4199148406204','22/2024','2024-10-04',1),(7,'Test',NULL,'',NULL,0),(8,'Didacta','4197694804901','4/25','2025-12-02',1);
/*!40000 ALTER TABLE `zeitschriften` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zeitschriften_alt`
--

DROP TABLE IF EXISTS `zeitschriften_alt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zeitschriften_alt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titel` varchar(255) NOT NULL,
  `ausgabe` varchar(255) DEFAULT NULL,
  `erscheinungsdatum` date DEFAULT NULL,
  `barcode` varchar(255) NOT NULL,
  `benutzer_id` int(11) DEFAULT NULL,
  `aktiv` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `barcode` (`barcode`),
  KEY `benutzer_id` (`benutzer_id`),
  CONSTRAINT `zeitschriften_alt_ibfk_1` FOREIGN KEY (`benutzer_id`) REFERENCES `benutzer` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zeitschriften_alt`
--

LOCK TABLES `zeitschriften_alt` WRITE;
/*!40000 ALTER TABLE `zeitschriften_alt` DISABLE KEYS */;
INSERT INTO `zeitschriften_alt` VALUES (2,'Test2',NULL,NULL,'5678',NULL,1),(5,'Gartenpraxis 3',NULL,NULL,'4190290312955',NULL,1),(6,'Ct','22','2025-06-17','4199148406204',NULL,1);
/*!40000 ALTER TABLE `zeitschriften_alt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zeitschriften_backup_20251202`
--

DROP TABLE IF EXISTS `zeitschriften_backup_20251202`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zeitschriften_backup_20251202` (
  `ZeitschriftID` int(11) NOT NULL DEFAULT 0,
  `Titel` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zeitschriften_backup_20251202`
--

LOCK TABLES `zeitschriften_backup_20251202` WRITE;
/*!40000 ALTER TABLE `zeitschriften_backup_20251202` DISABLE KEYS */;
INSERT INTO `zeitschriften_backup_20251202` VALUES (3,'Ct'),(2,'Gartenpraxis 3'),(5,'Pups'),(1,'Test2');
/*!40000 ALTER TABLE `zeitschriften_backup_20251202` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-04  9:36:31
