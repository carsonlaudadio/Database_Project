
DROP DATABASE IF EXISTS `Plantly`;
CREATE DATABASE `Plantly`;
USE `Plantly`;


CREATE TABLE `plantcatalog` (
  `PlantDesignationID` int(11) NOT NULL AUTO_INCREMENT,
  `PlantName` varchar(50) NOT NULL,
  `GroupID` int(11) NOT NULL,
  `IdealSoil_pH` decimal(4,2) NOT NULL,
  `IdealSunlight` int(11) NOT NULL,
  `IdealTemperature` int(120) NOT NULL,
  `Environment` varchar(24) NOT NULL,

  PRIMARY KEY (`PlantDesignationID`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `plantcatalog` VALUES (1,'Indian Paintbrush',2,1.21,10,77,'chaparral');
INSERT INTO `plantcatalog` VALUES (2,'White Spruce Tree',12,4.65,10,55,'taiga');
INSERT INTO `plantcatalog` VALUES (3,'Mangrove',11,3.35,10,58,'marine');
INSERT INTO `plantcatalog` VALUES (4,'Fern',90,4.53,10,77, 'deciduous');
INSERT INTO `plantcatalog` VALUES (5,'Pine Tree',94,1.63,10,70, 'taiga');
INSERT INTO `plantcatalog` VALUES (6,'Petit Baguette',14,2.39,10,38,'tundra');
INSERT INTO `plantcatalog` VALUES (7,'Orchid',98,3.29,10,62,'rainforest');
INSERT INTO `plantcatalog` VALUES (8,'Island Oasis - Raspberry',26,0.74,10,90,'deciduous');
INSERT INTO `plantcatalog` VALUES (9,'Foxtail Agave',67,2.26,10,79,'desert');
INSERT INTO `plantcatalog` VALUES (10,'Lemon Grass',6,1.09,10,80,'savannah');
INSERT INTO `plantcatalog` VALUES (11,'Tomatoes',6,1.09,10,80,'rainforest');
INSERT INTO `plantcatalog` VALUES (12,'Lillies',26,0.74,10,85,'deciduous');
INSERT INTO `plantcatalog` VALUES (13,'Monkey Grass',67,2.26,10,79,'Savannah');
INSERT INTO `plantcatalog` VALUES (14,'Japanese Maple',6,1.09,10,58,'deciduous');



CREATE TABLE `Plant_Status` (
  `PlantID` int(11) NOT NULL,
  `last_watering` varchar(50) NOT NULL,
  `SoilMoisture` varchar(50) NOT NULL,
  `Soil_pH` varchar(50) NOT NULL,
  `Sunlight` int(11) NOT NULL,
  `Temperature` int(11) DEFAULT NULL,
  `PlantDesignationID` int(11) NOT NULL,
  PRIMARY KEY (`PlantID`),
  KEY `fk_Plant_Status_offices_idx` (`PlantDesignationID`),
  KEY `fk_Plant_Status_Plant_Status_idx` (`Temperature`),
  CONSTRAINT `fk_Plant_Status_managers` FOREIGN KEY (`Temperature`) REFERENCES `Plant_Status` (`PlantID`),
  CONSTRAINT `fk_Plant_Status_PlantCatalog` FOREIGN KEY (`PlantDesignationID`) REFERENCES `PlantCatalog` (`PlantDesignationID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `Plant_Status` VALUES (37270,'Yovonnda','Magrannell','Executive Secretary',63996,NULL,10);
INSERT INTO `Plant_Status` VALUES (33391,'D\'arcy','Nortunen','Account Executive',62871,37270,1);
INSERT INTO `Plant_Status` VALUES (37851,'Sayer','Matterson','Statistician III',98926,37270,1);
INSERT INTO `Plant_Status` VALUES (40448,'Mindy','Crissil','Staff Scientist',94860,37270,1);
INSERT INTO `Plant_Status` VALUES (56274,'Keriann','Alloisi','VP Marketing',110150,37270,1);
INSERT INTO `Plant_Status` VALUES (63196,'Alaster','Scutchin','Assistant Professor',32179,37270,2);
INSERT INTO `Plant_Status` VALUES (67009,'North','de Clerc','VP Product Management',114257,37270,2);
INSERT INTO `Plant_Status` VALUES (67370,'Elladine','Rising','Social Worker',96767,37270,2);
INSERT INTO `Plant_Status` VALUES (68249,'Nisse','Voysey','Financial Advisor',52832,37270,2);







CREATE TABLE `users` (
  `UserID` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `users` VALUES (1,'carlton','ladidio','AL','cldidiy','p455w0rd');
INSERT INTO `users` VALUES (2,'Ollie','Tabooger','NY','olive','juice104');
INSERT INTO `users` VALUES (3,'Tess T.','smith','VA','dewy11','cheedom');
INSERT INTO `users` VALUES (4,'Carl','Smithers','OH','al','coholic');
INSERT INTO `users` VALUES (5,'Jonathan','Milslea','MN','seymor','butz1221');
INSERT INTO `users` VALUES (6,'Yuri','Nator','CO','m1k3','R0tc4');
INSERT INTO `users` VALUES (7,'Sara','Bilensworth','ID','Hugh','4$$123');
INSERT INTO `users` VALUES (8,'Isabelle','Ringing','NY','Ivana','t1n7L3');
INSERT INTO `users` VALUES (9,'Avery','Jones','TN','Anita122','B4th112');
INSERT INTO `users` VALUES (10,'Joe','Wunzboogerz','GA','Eura223','5n0t34ll');
DELETE FROM `users` WHERE first_name = 'Mohan';

CREATE TABLE `groups` (
  `Group_ID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `CareLvl` varchar(50) NOT NULL,
  `Environment` varchar(50) NOT NULL,

  PRIMARY KEY (`Group_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `groups` VALUES (1,'carlton','ladidio','AL');
INSERT INTO `groups` VALUES (2,'Ollie','Tabooger','NY');
INSERT INTO `groups` VALUES (3,'Tess T.','smith','VA');
INSERT INTO `groups` VALUES (4,'Carl','Smithers','OH');
INSERT INTO `groups` VALUES (5,'Jonathan','Milslea','MN');
INSERT INTO `groups` VALUES (6,'Yuri','Nator','CO');
INSERT INTO `groups` VALUES (7,'Sara','Bilensworth','ID');
INSERT INTO `groups` VALUES (8,'Isabelle','Ringing','NY');
INSERT INTO `groups` VALUES (9,'Avery','Jones','TN');
INSERT INTO `groups` VALUES (10,'Joe','Wunzboogerz','GA');

CREATE TABLE `registered_plants` (
  `PlantID` int(11) NOT NULL,
  `Date_Added` varchar(50) NOT NULL,
  `PlantName` varchar(50) NOT NULL,
  `room_loc_name` varchar(50) NOT NULL,
  `Group_ID` int(11) DEFAULT NULL,
  `UserID` int(11) NOT NULL,
  PRIMARY KEY (`PlantID`),
  KEY `fk_registered_plants_users_idx` (`Group_ID`),
  KEY `fk_registered_plants_registered_plants_idx` (`PlantID`),
  CONSTRAINT `fk_registered_plants_PlantStatus` FOREIGN KEY (`PlantID`) REFERENCES `Plant_Status` (`PlantID`),
  CONSTRAINT `fk_registered_plants_users` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON UPDATE CASCADE,
  CONSTRAINT `fk_registered_plants_groups` FOREIGN KEY (`UserID`) REFERENCES `groups` (`Group_ID`) ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `registered_plants` VALUES (37270,'Yovonnda','Fern','office',NULL,10);
INSERT INTO `registered_plants` VALUES (33391,'D\'arcy','Fern','kitchen',37270,1);
INSERT INTO `registered_plants` VALUES (37851,'Sayer','Lillies','front-yard',37270,1);
INSERT INTO `registered_plants` VALUES (40448,'Mindy','Tomatoes','back-yard',37270,1);
INSERT INTO `registered_plants` VALUES (56274,'Keriann','Monkey Grass','front-yard',37270,1);
INSERT INTO `registered_plants` VALUES (63196,'Alaster','Japanese Maple','side-yard',37270,2);








