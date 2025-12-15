CREATE DATABASE  IF NOT EXISTS `veluya_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `veluya_db`;
-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: veluya_db
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `anime`
--

DROP TABLE IF EXISTS `anime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anime` (
  `Title` varchar(100) NOT NULL,
  `ReleaseYear` int DEFAULT NULL,
  `Rating` decimal(3,1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anime`
--

LOCK TABLES `anime` WRITE;
/*!40000 ALTER TABLE `anime` DISABLE KEYS */;
INSERT INTO `anime` VALUES ('Attack on Titan',2013,9.1),('Demon Slayer',2019,8.7),('One Piece',1999,9.0),('Jujutsu Kaisen',2020,8.8),('My Hero Academia',2016,8.4),('Fullmetal Alchemist: Brotherhood',2009,9.2),('Naruto',2002,8.3),('Death Note',2006,8.9),('Haikyuu!!',2014,8.7),('Spy x Family',2022,8.5),('Chainsaw Man',2022,8.2),('Sword Art Online',2012,7.7),('Tokyo Ghoul',2014,7.8),('Your Lie in April',2014,8.6),('Blue Lock',2022,8.3),('Solo Leveling',2024,8.9),('Black Clover',2017,8.1),('Violet Evergarden',2018,8.5),('Re:Zero',2016,8.3),('Bleach: Thousand-Year Blood War',2022,9.0),('Attack on Titan',2013,9.1),('Demon Slayer',2019,8.7),('One Piece',1999,9.0),('Jujutsu Kaisen',2020,8.8),('My Hero Academia',2016,8.4),('Fullmetal Alchemist: Brotherhood',2009,9.2),('Naruto',2002,8.3),('Death Note',2006,8.9),('Haikyuu!!',2014,8.7),('Spy x Family',2022,8.5),('Chainsaw Man',2022,8.2),('Sword Art Online',2012,7.7),('Tokyo Ghoul',2014,7.8),('Your Lie in April',2014,8.6),('Blue Lock',2022,8.3),('Solo Leveling',2024,8.9),('Black Clover',2017,8.1),('Violet Evergarden',2018,8.5),('Re:Zero',2016,8.3),('Bleach: Thousand-Year Blood War',2022,9.0);
/*!40000 ALTER TABLE `anime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cartoons`
--

DROP TABLE IF EXISTS `cartoons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cartoons` (
  `cartoon_id` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(100) NOT NULL,
  `Episode` int DEFAULT NULL,
  PRIMARY KEY (`cartoon_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cartoons`
--

LOCK TABLES `cartoons` WRITE;
/*!40000 ALTER TABLE `cartoons` DISABLE KEYS */;
INSERT INTO `cartoons` VALUES (1,'SpongeBob SquarePants',295),(2,'Tom and Jerry',162),(3,'Adventure Time',283),(4,'Ben 10',52),(5,'The Amazing World of Gumball',240),(6,'Regular Show',261),(7,'Teen Titans Go!',390),(8,'Avatar: The Last Airbender',61),(9,'Phineas and Ferb',222),(10,'Gravity Falls',40),(11,'The Loud House',300),(12,'Rick and Morty',61),(13,'Steven Universe',160),(14,'Miraculous Ladybug',104),(15,'Family Guy',420),(16,'The Simpsons',750),(17,'South Park',330),(18,'Dragon Ball Z',291),(19,'Naruto',220),(20,'Pokemon',1200),(21,'SpongeBob SquarePants',295),(22,'Tom and Jerry',162),(23,'Adventure Time',283),(24,'Ben 10',52),(25,'The Amazing World of Gumball',240),(26,'Regular Show',261),(27,'Teen Titans Go!',390),(28,'Avatar: The Last Airbender',61),(29,'Phineas and Ferb',222),(30,'Gravity Falls',40),(31,'The Loud House',300),(32,'Rick and Morty',61),(33,'Steven Universe',160),(34,'Miraculous Ladybug',104),(35,'Family Guy',420),(36,'The Simpsons',750),(37,'South Park',330),(38,'Dragon Ball Z',291),(39,'Naruto',220),(40,'Pokemon',1200);
/*!40000 ALTER TABLE `cartoons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movies`
--

DROP TABLE IF EXISTS `movies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movies` (
  `Mies_id` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(100) NOT NULL,
  `ReleaseYear` int DEFAULT NULL,
  PRIMARY KEY (`Mies_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movies`
--

LOCK TABLES `movies` WRITE;
/*!40000 ALTER TABLE `movies` DISABLE KEYS */;
INSERT INTO `movies` VALUES (1,'The Shawshank Redemption',1994),(2,'The Godfather',1972),(3,'The Dark Knight',2008),(4,'Pulp Fiction',1994),(5,'Forrest Gump',1994),(6,'Inception',2010),(7,'Interstellar',2014),(8,'The Matrix',1999),(9,'Parasite',2019),(10,'Avengers: Endgame',2019),(11,'Titanic',1997),(12,'Jurassic Park',1993),(13,'Gladiator',2000),(14,'Toy Story',1995),(15,'Spider-Man: No Way Home',2021),(16,'Oppenheimer',2023),(17,'Joker',2019),(18,'Avatar',2009),(19,'Frozen',2013),(20,'The Lion King',1994),(21,'The Shawshank Redemption',1994),(22,'The Godfather',1972),(23,'The Dark Knight',2008),(24,'Pulp Fiction',1994),(25,'Forrest Gump',1994),(26,'Inception',2010),(27,'Interstellar',2014),(28,'The Matrix',1999),(29,'Parasite',2019),(30,'Avengers: Endgame',2019),(31,'Titanic',1997),(32,'Jurassic Park',1993),(33,'Gladiator',2000),(34,'Toy Story',1995),(35,'Spider-Man: No Way Home',2021),(36,'Oppenheimer',2023),(37,'Joker',2019),(38,'Avatar',2009),(39,'Frozen',2013),(40,'The Lion King',1994);
/*!40000 ALTER TABLE `movies` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-23 14:27:54
