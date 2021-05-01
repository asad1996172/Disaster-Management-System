-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 30, 2021 at 11:15 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dams`
--

-- --------------------------------------------------------

--
-- Table structure for table `Events`
--

CREATE TABLE `Events` (
  `id` int(11) NOT NULL,
  `event_name` varchar(255) NOT NULL,
  `disaster_type` varchar(255) NOT NULL,
  `severity` enum('mild','medium','extreme') DEFAULT NULL,
  `location` varchar(255) NOT NULL,
  `event_date` datetime NOT NULL,
  `zipcode` varchar(255) DEFAULT NULL,
  `items` varchar(255) DEFAULT NULL,
  `expired` tinyint(1) DEFAULT 0,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Events`
--

INSERT INTO `Events` (`id`, `event_name`, `disaster_type`, `severity`, `location`, `event_date`, `zipcode`, `items`, `expired`, `createdAt`, `updatedAt`) VALUES
(1, 'Katrina', 'Hurricane', 'medium', 'United States ', '2021-04-04 00:00:00', '54000', 'Blankets', 0, '2021-04-30 20:53:06', '2021-04-30 20:53:06'),
(2, 'Katalina', 'Earth Quake', 'extreme', 'United States ', '2021-04-11 00:00:00', '52242', 'Cloths, Cash', 0, '2021-04-30 20:53:32', '2021-04-30 20:53:32');

-- --------------------------------------------------------

--
-- Table structure for table `Pledges`
--

CREATE TABLE `Pledges` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `item_quantities` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Pledges`
--

INSERT INTO `Pledges` (`id`, `email`, `item_quantities`, `createdAt`, `updatedAt`) VALUES
(1, 'donor@donor.com', 'Blankets:20|Cash:3000|Cloths:50', '2021-04-30 20:55:01', '2021-04-30 20:55:01'),
(2, 'donor@donor.com', 'Blankets:20|Carpet:100', '2021-04-30 21:12:48', '2021-04-30 21:12:48');

-- --------------------------------------------------------

--
-- Table structure for table `Requests`
--

CREATE TABLE `Requests` (
  `id` int(11) NOT NULL,
  `event_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `item_quantities` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Requests`
--

INSERT INTO `Requests` (`id`, `event_name`, `email`, `item_quantities`, `createdAt`, `updatedAt`) VALUES
(1, 'Katrina', 'recipient@recipient.com', 'Blankets:100', '2021-04-30 20:53:54', '2021-04-30 20:53:54'),
(2, 'Katalina', 'recipient@recipient.com', 'Cloths:50|Cash:2000', '2021-04-30 20:54:00', '2021-04-30 20:54:00');

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `id` int(11) NOT NULL,
  `fullName` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','donor','recipient') NOT NULL,
  `zipcode` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`id`, `fullName`, `email`, `password`, `role`, `zipcode`, `createdAt`, `updatedAt`) VALUES
(1, 'Admin', 'admin@admin.com', 'admin', 'admin', '52246', '2021-04-30 20:50:00', '2021-04-30 20:50:00'),
(2, 'Donor', 'donor@donor.com', 'donor', 'donor', '52242', '2021-04-30 20:52:02', '2021-04-30 20:52:02'),
(3, 'Recipient', 'recipient@recipient.com', 'recipient', 'recipient', '52242', '2021-04-30 20:52:15', '2021-04-30 20:52:15');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Events`
--
ALTER TABLE `Events`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Pledges`
--
ALTER TABLE `Pledges`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Requests`
--
ALTER TABLE `Requests`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Events`
--
ALTER TABLE `Events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `Pledges`
--
ALTER TABLE `Pledges`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `Requests`
--
ALTER TABLE `Requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
