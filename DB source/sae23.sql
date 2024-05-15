-- phpMyAdmin SQL Dump
-- version 4.5.4.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 05, 2024 at 09:33 PM
-- Server version: 5.7.11
-- PHP Version: 5.6.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sae23`
--

-- --------------------------------------------------------

--
-- Table structure for table `army`
--

CREATE TABLE `army` (
  `Id` int(11) NOT NULL,
  `Owner` int(11) DEFAULT NULL,
  `Name` varchar(50) NOT NULL,
  `Points` int(11) DEFAULT NULL,
  `Models` int(11) DEFAULT NULL,
  `Price` float DEFAULT NULL,
  `Tags` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `army`
--

INSERT INTO `army` (`Id`, `Owner`, `Name`, `Points`, `Models`, `Price`, `Tags`) VALUES
(7, 2, '  testArmy', 815, 17, 279.99, '  {}'),
(11, 2, '  Imperial Guard Regiment', 530, 38, 322.5, '  {}');

-- --------------------------------------------------------

--
-- Table structure for table `armylink`
--

CREATE TABLE `armylink` (
  `Id` int(11) NOT NULL,
  `ArmyId` int(11) NOT NULL,
  `UnitId` int(11) NOT NULL,
  `Quantity` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `armylink`
--

INSERT INTO `armylink` (`Id`, `ArmyId`, `UnitId`, `Quantity`) VALUES
(1, 7, 2, 1),
(2, 7, 3, 2),
(4, 7, 5, 1),
(7, 11, 8, 3),
(8, 11, 9, 2),
(9, 11, 10, 1),
(10, 11, 11, 1),
(11, 11, 12, 1);

-- --------------------------------------------------------

--
-- Table structure for table `game`
--

CREATE TABLE `game` (
  `Id` int(11) NOT NULL,
  `Date` date NOT NULL,
  `Rules` varchar(50) NOT NULL,
  `Length` int(11) NOT NULL,
  `Winner` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `gameplayer`
--

CREATE TABLE `gameplayer` (
  `Id` int(11) NOT NULL,
  `GameId` int(11) NOT NULL,
  `PlayerId` int(11) NOT NULL,
  `ArmyId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `player`
--

CREATE TABLE `player` (
  `Id` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `FirstName` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `player`
--

INSERT INTO `player` (`Id`, `Name`, `FirstName`) VALUES
(1, '  Petiaud', '  Tanguy'),
(2, '  Cavill', '  Henry'),
(3, '  Calgar', '  Marneus'),
(4, '  the Betrayer', '  Kharn');

-- --------------------------------------------------------

--
-- Table structure for table `unit`
--

CREATE TABLE `unit` (
  `Id` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Points` int(11) NOT NULL,
  `Models` int(11) NOT NULL,
  `Stats` text NOT NULL,
  `Price` float NOT NULL,
  `Tags` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `unit`
--

INSERT INTO `unit` (`Id`, `Name`, `Points`, `Models`, `Stats`, `Price`, `Tags`) VALUES
(2, '  Battle Sisters Squad', 100, 10, '  {"movement": 6, "toughness": 3, "armour save": 3, "wounds": 1, "leadership": 7, "objective control": 2, "invulnerable save": 6}', 39.99, '  {"faction": "Adepta Sororitas", "keywords": ["Infantry", "Battleline", "Grenades", "Imperium"]}'),
(3, '  Eightbound', 145, 3, '  {"movement": 9, "toughness": 6, "armour save": 3, "wounds": 3, "leadership": 6, "objective control": 1, "invulnerable save": 5}', 50, '  {"faction": "World Eaters", "keywords": ["Chaos", "Space Marines", "Khorne", "Infantry", "Daemon"]}'),
(5, '  Knight Paladin', 425, 1, '  {"movement": 10, "toughness": 12, "armour save": 3, "wounds": 22, "leadership": 6, "objective control": 10, "invulnerable save": 5}', 140, '  {"faction": "Imperial Knights", "keywords": ["Vehicle", "Walker", "Titanic", "Towering", "Questoris", "Character", "Imperium"]}'),
(8, '  Cadian Shock Troops', 60, 10, '  {"movement": 6, "toughness": 3, "armour save": 5, "wounds": 1, "leadership": 7, "objective control": 2, "invulnerable save": -1}', 40, '  {"faction": "Astra Militarum", "keywords": ["Infantry", "Battleline", "Imperium", "Grenades", "Regiment", "Platoon", "Cadian"]}'),
(9, '  Chimera', 70, 1, '  {"movement": 10, "toughness": 9, "armour save": 3, "wounds": 11, "leadership": 7, "objective control": 2, "invulnerable save": -1}', 45, '  {"faction": "Astra Militarum", "keywords": ["Vehicle", "Imperium", "Squadron", "Transport", "Dedicated Transport", "Smoke"]}'),
(10, '  Commissar', 30, 1, '  {"movement": 6, "toughness": 3, "armour save": 5, "wounds": 3, "leadership": 6, "objective control": 1, "invulnerable save": 5}', 30, '  {"faction": "Astra Militarum", "keywords": ["Infantry", "Character", "Imperium", "Officer"]}'),
(11, '  Field Ordnance Battery', 120, 2, '  {"movement": 4, "toughness": 5, "armour save": 4, "wounds": 6, "leadership": 7, "objective control": 2, "invulnerable save": -1}', 42.5, '  {"faction": "Astra Militarum", "keywords": ["Infantry", "Artillery", "Imperium", "Grenades", "Regiment"]}'),
(12, '  Heavy Weapons Squad', 60, 3, '  {"movement": 6, "toughness": 3, "armour save": 5, "wounds": 2, "leadership": 7, "objective control": 2, "invulnerable save": -1}', 40, '  {"faction": "Astra Militarum", "keywords": ["Infantry", "Imperium", "Grenades", "Regiment"]}');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `army`
--
ALTER TABLE `army`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `Owner` (`Owner`);

--
-- Indexes for table `armylink`
--
ALTER TABLE `armylink`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `ArmyName` (`ArmyId`),
  ADD KEY `UnitId` (`UnitId`);

--
-- Indexes for table `game`
--
ALTER TABLE `game`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `gameplayer`
--
ALTER TABLE `gameplayer`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `GameId` (`GameId`,`PlayerId`,`ArmyId`),
  ADD KEY `PlayerId` (`PlayerId`),
  ADD KEY `ArmyId` (`ArmyId`);

--
-- Indexes for table `player`
--
ALTER TABLE `player`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `unit`
--
ALTER TABLE `unit`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `army`
--
ALTER TABLE `army`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `armylink`
--
ALTER TABLE `armylink`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `game`
--
ALTER TABLE `game`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `gameplayer`
--
ALTER TABLE `gameplayer`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `player`
--
ALTER TABLE `player`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `unit`
--
ALTER TABLE `unit`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `army`
--
ALTER TABLE `army`
  ADD CONSTRAINT `army_ibfk_1` FOREIGN KEY (`Owner`) REFERENCES `player` (`Id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `armylink`
--
ALTER TABLE `armylink`
  ADD CONSTRAINT `armylink_ibfk_1` FOREIGN KEY (`ArmyId`) REFERENCES `army` (`Id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `armylink_ibfk_2` FOREIGN KEY (`UnitId`) REFERENCES `unit` (`Id`) ON UPDATE CASCADE;

--
-- Constraints for table `gameplayer`
--
ALTER TABLE `gameplayer`
  ADD CONSTRAINT `gameplayer_ibfk_1` FOREIGN KEY (`GameId`) REFERENCES `game` (`Id`),
  ADD CONSTRAINT `gameplayer_ibfk_2` FOREIGN KEY (`PlayerId`) REFERENCES `player` (`Id`),
  ADD CONSTRAINT `gameplayer_ibfk_3` FOREIGN KEY (`ArmyId`) REFERENCES `army` (`Id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
