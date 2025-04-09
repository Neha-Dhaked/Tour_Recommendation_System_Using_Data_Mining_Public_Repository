-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2025 at 10:00 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `newtrs2`
--

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `feedback_text` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `user_id`, `feedback_text`) VALUES
(1, 5, 'It is a good website for searching tours.');

-- --------------------------------------------------------

--
-- Table structure for table `search_history`
--

CREATE TABLE `search_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `search_string` text DEFAULT NULL,
  `tours_viewed` text DEFAULT NULL,
  `search_date` TIMESTAMP DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `search_history`
--


INSERT INTO `search_history` (`id`, `user_id`, `search_string`, `tours_viewed`, `search_date`) VALUES
(1, 1, 'beach', NULL, '2025-03-06 00:36:22'),
(2, 1, 'beach', NULL, '2025-03-06 00:50:13'),
(3, 1, 'fun', NULL, '2025-03-06 01:40:55'),
(4, 1, 'fun', NULL, '2025-03-06 01:46:11'),
(5, 1, 'tigers', NULL, '2025-03-06 02:04:16'),
(6, 1, 'fun', NULL, '2025-03-06 02:04:56'),
(7, 1, 'mountain', NULL, '2025-03-06 02:08:01'),
(9, 5, 'waterfall', NULL, '2025-03-10 23:04:35'),
(10, 5, 'mountain', NULL, '2025-03-10 23:09:32'),
(11, 5, 'mountain', NULL, '2025-03-10 23:23:03'),
(12, 5, 'valley', NULL, '2025-03-11 00:14:04'),
(13, 5, 'fun', NULL, '2025-03-11 03:50:44'),
(14, 5, 'beach', NULL, '2025-03-11 14:17:35'),
(15, 5, 'manali', NULL, '2025-03-30 18:49:00'),
(16, 5, 'mountain', NULL, '2025-03-31 22:06:16'),
(17, 5, 'mountain', NULL, '2025-03-31 22:06:43');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `profile` text DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT 0,
  `verification_token` varchar(255) DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `profile`, `is_verified`, `verification_token`, `profile_pic`) VALUES
(1, 'user1', 'user1@gmail.com', 'user1@123', 'fun, adventure\r\n', 0, NULL, NULL),
(2, 'user2', 'user2@gmail.com', 'User2@123', 'Skiing, Hiking', 0, NULL, NULL),
(4, 'user4', 'omshivphotocopier@gmail.com', 'User4@123', 'Family fun, vacational tours', 0, NULL, NULL),
(5, 'user5', 'garimaphotostat@gmail.com', 'User5@123', 'Historical, Cultural tours', 1, NULL, NULL),
(6, 'user6', 'mansinigam2003@gmail.com', 'User6@123', 'Climbing, Hiking', 0, '6ccf9f248e3d6cbf7769cef24e2445c8', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_search`
--

CREATE TABLE `user_search` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `search_query` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_search`
--

INSERT INTO `user_search` (`id`, `user_id`, `search_query`) VALUES
(1, 1, 'beach'),
(2, 1, 'beach'),
(3, 1, 'fun'),
(4, 1, 'fun'),
(5, 5, 'waterfall'),
(6, 5, 'mountain'),
(7, 5, 'mountain'),
(8, 5, 'valley'),
(9, 5, 'fun'),
(10, 5, 'beach'),
(11, 5, 'manali'),
(12, 5, 'mountain'),
(13, 5, 'mountain');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `search_history`
--
ALTER TABLE `search_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_search`
--
ALTER TABLE `user_search`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `search_history`
--
ALTER TABLE `search_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user_search`
--
ALTER TABLE `user_search`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `search_history`
--
ALTER TABLE `search_history`
  ADD CONSTRAINT `search_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `user_search`
--
ALTER TABLE `user_search`
  ADD CONSTRAINT `user_search_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
