-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2020-01-23 05:50:36
-- 服务器版本： 5.7.26-log
-- PHP 版本： 7.0.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `bot`
--

-- --------------------------------------------------------

--
-- 表的结构 `house_data`
--

CREATE TABLE `house_data` (
  `id` bigint(20) NOT NULL,
  `group_id` bigint(20) NOT NULL,
  `no1` bigint(20) NOT NULL DEFAULT '0',
  `no2` bigint(20) NOT NULL DEFAULT '0',
  `no3` bigint(20) NOT NULL DEFAULT '0',
  `no4` bigint(20) NOT NULL DEFAULT '0',
  `no5` bigint(20) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `qq_group`
--

CREATE TABLE `qq_group` (
  `id` bigint(20) NOT NULL,
  `group_id` bigint(20) NOT NULL,
  `group_name` varchar(200) NOT NULL,
  `approve_time` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `race_data`
--

CREATE TABLE `race_data` (
  `id` bigint(20) NOT NULL,
  `total_money` bigint(20) DEFAULT NULL,
  `race_date` bigint(20) NOT NULL,
  `group_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `id` bigint(20) NOT NULL,
  `qq` bigint(20) NOT NULL,
  `qq_group_id` bigint(20) NOT NULL,
  `money` decimal(38,2) NOT NULL DEFAULT '0.00',
  `fish_power` bigint(20) NOT NULL DEFAULT '0',
  `help_count` smallint(6) NOT NULL DEFAULT '10'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转储表的索引
--

--
-- 表的索引 `house_data`
--
ALTER TABLE `house_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `house_data_qq_group_group_id_fk` (`group_id`);

--
-- 表的索引 `qq_group`
--
ALTER TABLE `qq_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qq_group_group_id_uindex` (`group_id`);

--
-- 表的索引 `race_data`
--
ALTER TABLE `race_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `race_data_qq_group_group_id_fk` (`group_id`);

--
-- 表的索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_qq_group_group_id_fk` (`qq_group_id`),
  ADD KEY `user_qq_index` (`qq`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `house_data`
--
ALTER TABLE `house_data`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `qq_group`
--
ALTER TABLE `qq_group`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `race_data`
--
ALTER TABLE `race_data`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
