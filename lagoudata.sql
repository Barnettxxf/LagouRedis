-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: lagoudata
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.17.10.1

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
-- Table structure for table `lagoucategory`
--

DROP TABLE IF EXISTS `lagoucategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lagoucategory` (
  `category` varchar(45) DEFAULT NULL,
  `positionid` int(12) NOT NULL,
  `positionname` varchar(45) DEFAULT NULL,
  `company` varchar(45) DEFAULT NULL,
  `companyid` int(12) NOT NULL,
  `salary` varchar(45) DEFAULT NULL,
  `publish_time` varchar(45) DEFAULT NULL,
  `labels` varchar(300) DEFAULT NULL,
  `acquire_year` varchar(45) DEFAULT NULL,
  `acquire_edu_bg` varchar(45) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`positionid`,`companyid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lagoucategory`
--

LOCK TABLES `lagoucategory` WRITE;
/*!40000 ALTER TABLE `lagoucategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `lagoucategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lagoujobs`
--

DROP TABLE IF EXISTS `lagoujobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lagoujobs` (
  `jobid` int(12) NOT NULL,
  `jobname` varchar(45) DEFAULT NULL,
  `jobcompanyname` varchar(45) DEFAULT NULL,
  `jobadvantage` varchar(200) DEFAULT NULL,
  `jobreposibilit` text,
  `jobacquire` text,
  `jobsite` varchar(45) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`jobid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lagoujobs`
--

LOCK TABLES `lagoujobs` WRITE;
/*!40000 ALTER TABLE `lagoujobs` DISABLE KEYS */;
/*!40000 ALTER TABLE `lagoujobs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-22 12:53:13
