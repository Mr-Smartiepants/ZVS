-- MariaDB dump 10.19  Distrib 10.4.28-MariaDB, for osx10.10 (x86_64)
--
-- Host: localhost    Database: zeitschriften_db
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
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aktionen`
--

LOCK TABLES `aktionen` WRITE;
/*!40000 ALTER TABLE `aktionen` DISABLE KEYS */;
INSERT INTO `aktionen` VALUES (1,2,'Zeitschrift \'ct-Magazin für Computer und Technik Ausgabe 22\' zurückgegeben','2025-06-11 08:21:59'),(2,2,'Zeitschrift \'ct-Magazin für Computer und Technik Ausgabe 22\' ausgeliehen','2025-06-11 08:22:24'),(3,2,'Zeitschrift \'ct-Magazin für Computer und Technik Ausgabe 22\' zurückgegeben','2025-06-11 08:24:35'),(4,2,'Zeitschrift \'ct-Magazin für Computer und Technik Ausgabe 22\' ausgeliehen','2025-06-11 08:31:29'),(5,2,'Zeitschrift \'ct-Magazin für Computer und Technik Ausgabe 22\' zurückgegeben','2025-06-11 08:46:51'),(6,3,'Zeitschrift \'ct-Magazin für Computer und Technik Ausgabe 22\' ausgeliehen','2025-06-11 08:48:29'),(7,3,'Zeitschrift \'ct-Magazin für Computer und Technik Ausgabe 22\' zurückgegeben','2025-06-11 08:50:58'),(8,9,'hat sich angemeldet','2025-06-11 09:00:33'),(9,9,'hat sich angemeldet','2025-06-11 09:02:43'),(10,2,'Zeitschrift \'ct-Magazin für Computer und Technik Ausgabe 22\' ausgeliehen','2025-06-12 06:50:59'),(11,9,'hat sich angemeldet','2025-06-12 06:54:38'),(12,9,'hat sich angemeldet','2025-06-12 06:55:19'),(13,9,'hat sich angemeldet','2025-06-12 06:59:17'),(14,9,'hat sich angemeldet','2025-06-12 07:00:16'),(15,9,'hat sich angemeldet','2025-06-12 07:09:50'),(16,9,'hat sich angemeldet','2025-06-12 07:12:30'),(17,9,'hat sich angemeldet','2025-06-12 07:16:48'),(18,9,'hat sich angemeldet','2025-06-12 07:32:53'),(19,9,'hat sich angemeldet','2025-06-12 07:40:15'),(20,2,'Zeitschrift \'ct-Magazin für Computer und Technik Ausgabe 22\' zurückgegeben','2025-06-12 07:41:34'),(21,9,'hat sich angemeldet','2025-06-12 07:46:00'),(22,9,'hat Zeitschrift \'ct-Magazin für Computer und Technik Ausgabe 22\' gelöscht','2025-06-12 07:55:26'),(23,9,'hat sich angemeldet','2025-06-17 05:52:05'),(24,9,'hat sich angemeldet','2025-06-17 05:59:15'),(25,9,'hat sich angemeldet','2025-06-17 06:04:46'),(26,9,'hat Zeitschrift \'Test1\' gelöscht','2025-06-17 06:06:11'),(27,9,'hat sich angemeldet','2025-06-17 06:12:32'),(28,9,'hat sich angemeldet','2025-06-17 06:14:00'),(29,9,'hat sich angemeldet','2025-06-17 06:20:05'),(30,9,'hat sich angemeldet','2025-06-17 06:25:27'),(31,9,'hat sich angemeldet','2025-06-17 06:32:38'),(32,9,'hat sich angemeldet','2025-06-17 06:38:02'),(33,9,'hat sich angemeldet','2025-06-17 06:46:44'),(34,9,'hat sich angemeldet','2025-06-17 07:28:50'),(35,9,'hat sich angemeldet','2025-06-17 07:38:27'),(36,9,'hat sich angemeldet','2025-06-17 08:14:56'),(37,3,'Zeitschrift \'Ct\' ausgeliehen','2025-06-17 08:21:42'),(38,9,'hat sich angemeldet','2025-06-17 08:21:57'),(39,9,'hat sich angemeldet','2025-06-17 11:02:12'),(40,9,'hat sich angemeldet','2025-06-17 11:03:24'),(41,9,'hat sich angemeldet','2025-06-17 11:06:55'),(42,9,'hat sich angemeldet','2025-06-24 06:35:25'),(43,9,'hat sich angemeldet','2025-06-24 06:45:33'),(44,9,'hat Benutzerliste aufgerufen','2025-06-24 06:45:37'),(45,9,'hat Benutzerliste aufgerufen','2025-06-24 06:45:48'),(46,9,'hat Benutzerliste aufgerufen','2025-06-24 06:46:05'),(47,9,'hat Benutzerliste aufgerufen','2025-06-24 06:46:50'),(48,9,'hat Benutzer Max Mustermann entfernt','2025-06-24 06:46:54'),(49,9,'hat Benutzerliste aufgerufen','2025-06-24 06:46:54'),(50,9,'hat Zeitschrift \'Test3\' gelöscht','2025-06-24 06:47:03'),(51,9,'hat Zeitschrift \'Test3\' gelöscht','2025-06-24 06:47:03'),(52,9,'hat Benutzerliste aufgerufen','2025-06-24 06:49:58'),(53,9,'hat sich angemeldet','2025-06-24 06:53:09'),(54,9,'hat Benutzerliste aufgerufen','2025-06-24 06:53:43'),(55,9,'hat Zeitschriftenliste aufgerufen','2025-06-24 06:57:34'),(56,9,'hat sich angemeldet','2025-06-24 06:59:02'),(57,2,'hat Zeitschrift \'Ct\' ausgeliehen','2025-06-24 07:05:14'),(58,2,'hat Zeitschrift \'Ct\' zurückgegeben','2025-06-24 07:05:33'),(59,9,'hat sich angemeldet','2025-06-24 07:06:04'),(60,9,'hat Benutzerliste aufgerufen','2025-06-24 07:06:18'),(61,9,'hat Zeitschriftenliste aufgerufen','2025-06-24 07:06:19'),(62,9,'hat sich angemeldet','2025-06-24 08:06:24'),(63,9,'hat sich angemeldet','2025-06-24 08:06:48'),(64,9,'hat Benutzerliste aufgerufen','2025-06-24 08:07:35'),(65,2,'hat Zeitschrift \'Ct\' ausgeliehen','2025-06-24 08:09:11'),(66,9,'hat sich angemeldet','2025-06-24 08:09:31'),(67,9,'hat sich angemeldet','2025-06-30 05:43:11'),(68,9,'hat Benutzerliste aufgerufen','2025-06-30 05:43:46'),(69,9,'hat Benutzerliste aufgerufen','2025-06-30 05:44:27'),(70,9,'hat Zeitschriftenliste aufgerufen','2025-06-30 05:44:49'),(71,9,'hat Zeitschriftenliste aufgerufen','2025-06-30 05:44:57'),(72,9,'hat Zeitschriftenliste aufgerufen','2025-06-30 05:45:24'),(73,9,'fehlgeschlagener Loginversuch','2025-12-01 08:10:33'),(74,9,'hat sich angemeldet','2025-12-01 08:10:51');
/*!40000 ALTER TABLE `aktionen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ausleihen`
--

DROP TABLE IF EXISTS `ausleihen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ausleihen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `zeitschrift_id` int(11) DEFAULT NULL,
  `benutzer_id` int(11) DEFAULT NULL,
  `ausleihdatum` datetime DEFAULT current_timestamp(),
  `rueckgabedatum` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `zeitschrift_id` (`zeitschrift_id`),
  KEY `benutzer_id` (`benutzer_id`),
  CONSTRAINT `ausleihen_ibfk_1` FOREIGN KEY (`zeitschrift_id`) REFERENCES `zeitschriften` (`id`),
  CONSTRAINT `ausleihen_ibfk_2` FOREIGN KEY (`benutzer_id`) REFERENCES `benutzer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ausleihen`
--

LOCK TABLES `ausleihen` WRITE;
/*!40000 ALTER TABLE `ausleihen` DISABLE KEYS */;
INSERT INTO `ausleihen` VALUES (6,6,3,'2025-06-17 10:21:42','2025-06-24 08:58:46'),(7,6,2,'2025-06-24 09:05:14','2025-06-24 09:05:33'),(8,6,2,'2025-06-24 10:09:11',NULL);
/*!40000 ALTER TABLE `ausleihen` ENABLE KEYS */;
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
  `name` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `benutzer`
--

LOCK TABLES `benutzer` WRITE;
/*!40000 ALTER TABLE `benutzer` DISABLE KEYS */;
INSERT INTO `benutzer` VALUES (2,'dallk','$2b$12$kMwim6kba850bP0Qio/OTuifKhH/QZLLD4vnUvaA7kCHvI4tf4Lgu','user','Dall','Karl'),(3,'mahonit','$2b$12$zNdC1JLxEJgNrXr9OdnrfOcdg6KOAXFCQL5O7CLxwJZNO5NsgFWra','user','Mahoni','Toni'),(9,'weissgerberst','$2b$12$pVIpFd1XLqACUzY4A9.g5.rr1Uv/iNWJJC9ZFCm08gYV/4rX5ncm6','admin','Weißgerber','Stefan'),(11,'hoffsteddeb','$2b$12$CPFAd40pOLxEDQP45/WwxeEkEO9QkyxIoZZtCm7iboi/zfgLKiN5y','admin','Hoffstedde','Bernd'),(13,'strunkh','$2b$12$EXAjHKy4QRn2wQNKKQGx5ufE.fozaWbHa9UtY1u3uf3q79T16Yz/.','admin','Strunk','Holger'),(14,'kolumnak',NULL,'user','Kolumna','Karla'),(15,'lewandowskir',NULL,'user','Lewandowski','Robert'),(16,'weissgerberj',NULL,'user','Weißgerber','Julia'),(18,'panzerp',NULL,'user','Panzer','Paul');
/*!40000 ALTER TABLE `benutzer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zeitschriften`
--

DROP TABLE IF EXISTS `zeitschriften`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zeitschriften` (
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
  CONSTRAINT `zeitschriften_ibfk_1` FOREIGN KEY (`benutzer_id`) REFERENCES `benutzer` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zeitschriften`
--

LOCK TABLES `zeitschriften` WRITE;
/*!40000 ALTER TABLE `zeitschriften` DISABLE KEYS */;
INSERT INTO `zeitschriften` VALUES (2,'Test2',NULL,NULL,'5678',NULL,1),(5,'Gartenpraxis 3',NULL,NULL,'4190290312955',NULL,1),(6,'Ct','22','2025-06-17','4199148406204',2,1);
/*!40000 ALTER TABLE `zeitschriften` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-01  9:36:40
