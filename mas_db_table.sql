CREATE DATABASE  IF NOT EXISTS `mas_db` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `mas_db`;
-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: mas_db
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `LogFileControl`
--

DROP TABLE IF EXISTS `LogFileControl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LogFileControl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` text,
  `downloaded` tinyint(1) DEFAULT NULL,
  `processed` tinyint(1) DEFAULT NULL,
  `correct` tinyint(1) DEFAULT NULL,
  `coments` text,
  `imported` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4166 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `server_statistics`
--

DROP TABLE IF EXISTS `server_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time_min_date` datetime DEFAULT NULL,
  `time_max_date` datetime DEFAULT NULL,
  `r_avg` float DEFAULT NULL,
  `r_max` int(11) DEFAULT NULL,
  `r_p90` float DEFAULT NULL,
  `us_avg` float DEFAULT NULL,
  `us_max` float DEFAULT NULL,
  `us_p90` float DEFAULT NULL,
  `sy_avg` float DEFAULT NULL,
  `sy_max` float DEFAULT NULL,
  `sy_p90` float DEFAULT NULL,
  `id_avg` float DEFAULT NULL,
  `id_max` float DEFAULT NULL,
  `id_p90` float DEFAULT NULL,
  `server` text,
  `agregation` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=205153 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-05 17:19:09
