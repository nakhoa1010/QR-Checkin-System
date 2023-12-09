-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th10 17, 2023 lúc 10:08 AM
-- Phiên bản máy phục vụ: 10.4.28-MariaDB
-- Phiên bản PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `qrevent`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `yourtablename`
--

CREATE TABLE `yourtablename` (
  `ID` int(11) NOT NULL,
  `QRID` varchar(255) DEFAULT NULL,
  `Ten` varchar(255) DEFAULT NULL,
  `GioiTinh` varchar(10) DEFAULT NULL,
  `FacePath` varchar(255) DEFAULT NULL,
  `Flag` int(11) DEFAULT 0,
  `TimeIn` timestamp NULL DEFAULT NULL,
  `TimeOut` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `yourtablename`
--

INSERT INTO `yourtablename` (`ID`, `QRID`, `Ten`, `GioiTinh`, `FacePath`, `Flag`, `TimeIn`, `TimeOut`) VALUES
(1, 'EventA-abc123xyz', 'Nguyen Van A', 'Nam', 'K:\\FacePath\\ID001.jpg', 1, '2023-10-03 05:24:45', NULL),
(2, 'EventA-abc124xyz', 'Nguyen Thi B', 'Nu', NULL, 0, NULL, NULL);

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `yourtablename`
--
ALTER TABLE `yourtablename`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `yourtablename`
--
ALTER TABLE `yourtablename`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
