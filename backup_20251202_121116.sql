-- MariaDB dump 10.19  Distrib 10.4.28-MariaDB, for osx10.10 (x86_64)
--
-- Host:     Database: zeitschriften_db
-- ------------------------------------------------------
-- Server version	10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aktionen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `benutzer_id` int(11) NOT NULL,
  `aktion` varchar(255) NOT NULL,
  `zeitpunkt` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `benutzer_id` (`benutzer_id`),
  CONSTRAINT `aktionen_ibfk_1` FOREIGN KEY (`benutzer_id`) REFERENCES `benutzer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=221 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aktionen`
--

LOCK TABLES `aktionen` WRITE;
/*!40000 ALTER TABLE `aktionen` DISABLE KEYS */;
INSERT INTO `aktionen` VALUES (185,26,'fehlgeschlagener Loginversuch','2025-12-02 10:01:47'),(186,26,'hat sich angemeldet','2025-12-02 10:03:00'),(187,26,'hat sich angemeldet','2025-12-02 10:03:43'),(188,26,'hat sich angemeldet','2025-12-02 10:06:25'),(189,26,'hat Benutzerliste aufgerufen','2025-12-02 10:06:29'),(190,26,'hat Benutzer admin#1 entfernt','2025-12-02 10:06:35'),(191,26,'hat Benutzerliste aufgerufen','2025-12-02 10:06:35'),(192,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:09:36'),(193,26,'hat Benutzerliste aufgerufen','2025-12-02 10:09:36'),(194,26,'hat sich angemeldet','2025-12-02 10:12:26'),(195,26,'hat Benutzerliste aufgerufen','2025-12-02 10:12:29'),(196,26,'hat Benutzerliste aufgerufen','2025-12-02 10:12:51'),(197,26,'hat Benutzerliste aufgerufen','2025-12-02 10:14:24'),(198,26,'hat Benutzerliste aufgerufen','2025-12-02 10:14:39'),(199,26,'hat Benutzer admin#3 hinzugefügt','2025-12-02 10:15:08'),(200,26,'hat Benutzerliste aufgerufen','2025-12-02 10:15:08'),(201,26,'hat Benutzerliste aufgerufen','2025-12-02 10:15:28'),(202,26,'hat Benutzerliste aufgerufen','2025-12-02 10:16:25'),(203,26,'hat Benutzer admin#4 hinzugefügt','2025-12-02 10:16:57'),(204,26,'hat Benutzerliste aufgerufen','2025-12-02 10:16:57'),(205,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:17:40'),(206,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:20:09'),(207,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:20:17'),(208,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:21:49'),(209,26,'hat sich angemeldet','2025-12-02 10:22:18'),(210,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:22:20'),(211,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:22:26'),(212,26,'hat Benutzerliste aufgerufen','2025-12-02 10:23:12'),(213,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:23:14'),(214,26,'hat Zeitschrift \'Pups\' hinzugefügt','2025-12-02 10:23:26'),(215,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:23:26'),(216,26,'hat sich angemeldet','2025-12-02 10:25:08'),(217,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:25:13'),(218,26,'hat Zeitschriftenliste aufgerufen','2025-12-02 10:25:16'),(219,26,'hat sich angemeldet','2025-12-02 10:55:50'),(220,26,'hat sich angemeldet','2025-12-02 10:57:47');
/*!40000 ALTER TABLE `aktionen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ausleihen`
--

DROP TABLE IF EXISTS `ausleihen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ausleihen`
--

LOCK TABLES `ausleihen` WRITE;
/*!40000 ALTER TABLE `ausleihen` DISABLE KEYS */;
/*!40000 ALTER TABLE `ausleihen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ausleihen_alt`
--

DROP TABLE IF EXISTS `ausleihen_alt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
-- Table structure for table `benutzer`
--

DROP TABLE IF EXISTS `benutzer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `benutzer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('admin','user') NOT NULL DEFAULT 'user',
  `display_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `idx_benutzer_display_name` (`display_name`(100))
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `benutzer`
--

LOCK TABLES `benutzer` WRITE;
/*!40000 ALTER TABLE `benutzer` DISABLE KEYS */;
INSERT INTO `benutzer` VALUES (25,'user#1',NULL,'user',NULL),(26,'admin#2','$2b$12$l2zMJAsV.Gdr8j00WMXgG.Z9ZTnHinMIoP7mJWxr3GpPvAGx/zYLa','admin',NULL),(27,'admin#3','$2b$12$i6EWLAhs/VuXatGmJ3UH8en59Zzcc7mit.w45y6PBWygMUK3ZXjbS','admin',NULL),(28,'admin#4','$2b$12$5XFsT9oUB/s/xIImUenpDOlZF09i50EMi3W8POy333cASw2RKnPY6','admin',NULL);
/*!40000 ALTER TABLE `benutzer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exemplare`
--

DROP TABLE IF EXISTS `exemplare`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exemplare` (
  `ExemplarID` int(11) NOT NULL AUTO_INCREMENT,
  `Barcode` varchar(100) NOT NULL,
  `Erscheinungsdatum` date DEFAULT NULL,
  `AusgabeHeftnummer` varchar(50) DEFAULT NULL,
  `Aktiv` tinyint(1) DEFAULT 1,
  `ZeitschriftID` int(11) NOT NULL,
  PRIMARY KEY (`ExemplarID`),
  UNIQUE KEY `Barcode` (`Barcode`),
  KEY `ZeitschriftID` (`ZeitschriftID`),
  CONSTRAINT `exemplare_ibfk_1` FOREIGN KEY (`ZeitschriftID`) REFERENCES `zeitschriften` (`ZeitschriftID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exemplare`
--

LOCK TABLES `exemplare` WRITE;
/*!40000 ALTER TABLE `exemplare` DISABLE KEYS */;
INSERT INTO `exemplare` VALUES (1,'5678',NULL,NULL,1,1),(2,'4190290312955',NULL,NULL,1,2),(3,'4199148406204','2025-06-17','22',1,3);
/*!40000 ALTER TABLE `exemplare` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zeitschriften`
--

DROP TABLE IF EXISTS `zeitschriften`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zeitschriften` (
  `ZeitschriftID` int(11) NOT NULL AUTO_INCREMENT,
  `Titel` varchar(255) NOT NULL,
  PRIMARY KEY (`ZeitschriftID`),
  UNIQUE KEY `Titel` (`Titel`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zeitschriften`
--

LOCK TABLES `zeitschriften` WRITE;
/*!40000 ALTER TABLE `zeitschriften` DISABLE KEYS */;
INSERT INTO `zeitschriften` VALUES (3,'Ct'),(2,'Gartenpraxis 3'),(5,'Pups'),(1,'Test2');
/*!40000 ALTER TABLE `zeitschriften` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zeitschriften_alt`
--

DROP TABLE IF EXISTS `zeitschriften_alt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-02 12:11:17
