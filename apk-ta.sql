-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 28, 2026 at 02:56 PM
-- Server version: 8.4.3
-- PHP Version: 8.3.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `apk-ta`
--

-- --------------------------------------------------------

--
-- Table structure for table `tabel_kasus`
--

CREATE TABLE `tabel_kasus` (
  `id_kasus` int NOT NULL,
  `jenis_perangkat` varchar(100) DEFAULT NULL,
  `kategori_problem` varchar(100) DEFAULT NULL,
  `dampak_gangguan` varchar(100) DEFAULT NULL,
  `akses_remote` varchar(100) DEFAULT NULL,
  `status_fisik` varchar(100) DEFAULT NULL,
  `kondisi_kabel` varchar(100) DEFAULT NULL,
  `diagnosis` text,
  `solusi` text,
  `status_kasus` varchar(20) DEFAULT 'Terverifikasi'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tabel_kasus`
--

INSERT INTO `tabel_kasus` (`id_kasus`, `jenis_perangkat`, `kategori_problem`, `dampak_gangguan`, `akses_remote`, `status_fisik`, `kondisi_kabel`, `diagnosis`, `solusi`, `status_kasus`) VALUES
(1, 'Multiple Perangkat (Area/POP Down)', 'ICMP RTO/Loss', 'Banyak Perangkat di beberapa Area (Problem Pusat)', 'Tidak bisa di remote', 'Listrik lokasi Mati', 'Perkabelan Aman', 'Terdapat Masalah Kelistrikan di salah satu Data center pusat yang menyebabkan beberapa router core mati/restart', 'Mengecek Panel listrik utama di lokasi | Mengecek UPS | Mengecek Terminal listrik yg terhubung kepada perangkat jika menggunakan power AC | Mengecek Rectifier jika perangkat menggunakan power DC | Mengecek kabel power yg terhubung pada perangkat', 'Terverifikasi'),
(2, 'Router', 'Interface link down', 'Banyak Perangkat di beberapa Area (Problem Pusat)', 'Bisa diakses dan Normal', 'Listrik & Perangkat Aman (Menyala Normal)', 'SFP Rusak', 'Terdapat Masalah SFP di pada salah satu port Router Core yg terletak di Data Center Pusat', 'Mengganti SFP', 'Terverifikasi'),
(3, 'Switch', 'Interface link down', 'Banyak Perangkat di beberapa Area (Problem Pusat)', 'Bisa diakses dan Normal', 'Listrik & Perangkat Aman (Menyala Normal)', 'Redaman Optik Jelek', 'Terdapat Masalah antara pada Kabel, SFP atau Port Perangkat', 'Mengganti Kabel Patchcore | Mengganti SFP | Mencoba pindah ke Port lain', 'Terverifikasi'),
(4, 'Router', 'Temperature Alert', 'Banyak Perangkat di beberapa Area (Problem Pusat)', 'Bisa diakses tapi lag/timeout', 'Listrik aman perangkat Mati/Hang', 'Perkabelan Aman', 'Terdapat Masalah pada AC di Data Center Pusat,  atau pada Fan Perangkat Router Core ', 'Mengecek Kondisi AC pada Ruangan Data Center | Mengganti Fan Module yg rusak pada Router Core | Jika Fan pada Router Core bukan versi modular maka Router core harus diganti', 'Terverifikasi'),
(5, 'Multiple Perangkat (Area/POP Down)', 'ICMP RTO/Loss', 'Banyak Perangkat dalam 1 Area', 'Tidak bisa di remote', 'Listrik & Perangkat Aman (Menyala Normal)', 'Perkabelan Aman', 'Terdapat Gangguan pada kabel Core menuju PoP', 'Di eskalasi kan ke Tim FO Lapangan terkait untuk melakukan pengecekan ke jalur', 'Terverifikasi'),
(6, 'Multiple Perangkat (Area/POP Down)', 'ICMP RTO/Loss', 'Banyak Perangkat dalam 1 Area', 'Tidak bisa di remote', 'Listrik lokasi Mati', 'Perkabelan Aman', 'Terdapat Masalah Kelistrikan pada PoP', 'Mengecek KwH Meter PoP | Mengecek perangkat kelistrikan di lokasi seperti UPS, Rectifier, Inverter, dan Terminal Listrik', 'Terverifikasi'),
(7, 'Switch', 'ICMP RTO/Loss', 'Banyak Perangkat dalam 1 Area', 'Tidak bisa di remote', 'Listrik aman perangkat Mati/Hang', 'Perkabelan Aman', 'Terdapat Masalah pada perangkat Switch Core di PoP', 'Mengecek Patchcore, SFP, Dan Port Backbone jika terdapat masalah antara 3 hal tersebut ganti | Mengecek PSU Switch Core dan ganti jika bermasalah | Replace perangkat Switch Core jika Hang/Mati', 'Terverifikasi'),
(8, 'Router', 'ICMP RTO/Loss', 'Banyak Perangkat dalam 1 Area', 'Tidak bisa di remote', 'Listrik & Perangkat Aman (Menyala Normal)', 'Perkabelan Aman', 'Terdapat Masalah pada perangkat Router Core di PoP', 'Mengecek Patchcore, SFP, Dan Port kearah Switch Core jika terdapat masalah antara 3 hal tersebut ganti', 'Terverifikasi'),
(9, 'Router', 'High CPU/Memory', 'Banyak Perangkat dalam 1 Area', 'Bisa diakses dan Normal', 'Listrik & Perangkat Aman (Menyala Normal)', 'Perkabelan Aman', 'Traffik pada router overload ( Jumlah Client melebihi batas spesifikasi router ), Terlalu banyak konfigurasi pada Router, Adanya serangan jaringan seperti DDOS', 'Mengganti Router Existing dengan Router yang memiliki spesifikasi lebih tinggi | Menambah Router baru untuk membagi beban jaringan | Mengecek Log dan memastikan tidak ada log yg mencurigakan, jika ada maka tutup atau disable port/IP yg mencurigakan', 'Terverifikasi'),
(10, 'CPE/ONT Client', 'ICMP RTO/Loss', '1 Perangkat dalam 1 Site', 'Tidak bisa di remote', 'Listrik aman perangkat Mati/Hang', 'Perkabelan Aman', 'Terdapat masalah pada perangkat CPE/ONT di sisi Client', 'Melakukan Hard Reset pada ONT| Mengganti perangkat CPE/ONT', 'Terverifikasi'),
(11, 'CPE/ONT Client', 'ICMP RTO/Loss', '1 Perangkat dalam 1 Site', 'Tidak bisa di remote', 'Perangkat nyala normal indikator port mati', 'Redaman Optik Jelek', 'Terdapat masalah di jalur kabel FO dri FAT kearah client', 'Melakukan pengecekan di sisi FAT dan dibersihkan jika kondisi kotor atau banyak serangga | Mengganti konektor di sisi FAT | Mengganti Port di sisi FAT', 'Terverifikasi'),
(12, 'Router', 'BGP Peer Down', '1 Perangkat dalam 1 Site', 'Tidak bisa di remote', 'Listrik & Perangkat Aman (Menyala Normal)', 'Redaman Optik Jelek', 'Terdapat masalah di jalur kabel core kearah Client ( Kemungkinan FO Cut )', 'Di eskalasi kan ke Tim FO Lapangan terkait untuk melakukan pengecekan ke jalur', 'Terverifikasi'),
(13, 'OLT', 'ICMP RTO/Loss', 'Banyak Perangkat dalam 1 Area', 'Bisa diakses tapi lag/timeout', 'Listrik aman perangkat Mati/Hang', 'Perkabelan Aman', 'Terdapat masalah pada fisik perangkat OLT', 'Mengganti card module yg bermasalah pada OLT | Mengganti perangkat OLT', 'Terverifikasi'),
(14, 'Multiple Perangkat (Area/POP Down)', 'ICMP RTO/Loss', 'Banyak Perangkat di beberapa Area (Problem Pusat)', 'Tidak bisa di remote', 'Listrik lokasi Mati', 'Perkabelan Aman', 'Terdapat Masalah Kelistrikan di salah satu Data center pusat yang menyebabkan beberapa router core mati/restart', 'Mengecek Panel listrik utama di lokasi | Mengecek UPS | Mengecek Terminal listrik yg terhubung kepada perangkat jika menggunakan power AC | Mengecek Rectifier jika perangkat menggunakan power DC | Mengecek kabel power yg terhubung pada perangkat', 'Terverifikasi'),
(15, 'CPE/ONT Client', '[ ONT ] Dying Gasp', '1 Perangkat dalam 1 Site', 'Tidak bisa di remote', 'Listrik aman perangkat Mati/Hang', 'Perkabelan Aman', 'Terdapat masalah pada power adaptor perangkat CPE/ONT di sisi Client', 'Mengganti power adaptor ONT client', 'Terverifikasi'),
(16, 'CPE/ONT Client', '[ ONT ] Dying Gasp', '1 Perangkat dalam 1 Site', 'Tidak bisa di remote', 'Listrik aman perangkat Mati/Hang', 'Perkabelan Aman', 'Terdapat masalah pada perangkat CPE/ONT di sisi Client', 'Hard reset ONT existing | Mengganti ONT dengan yang baru', 'Terverifikasi'),
(17, 'CPE/ONT Client', '[ ONT ] LOS/LOBi', '1 Perangkat dalam 1 Site', 'Tidak bisa di remote', 'Listrik & Perangkat Aman (Menyala Normal)', 'Perkabelan Aman', 'Terdapat masalah pada jalur FO kearah CPE/ONT di sisi Client', 'Mengecek Kabel FO dari FAT kearah ONT Client dan test redamannya | Kalau redaman Tinggi/Loss ganti Barrel Konektor kabel atau perbaiki bagian kabel yg bending', 'Terverifikasi'),
(18, 'CPE/ONT Client', '[ ONT ] LOS/LOBi', '1 Perangkat dalam 1 Site', 'Tidak bisa di remote', 'Listrik & Perangkat Aman (Menyala Normal)', 'Perkabelan Aman', 'Terdapat masalah pada jalur FO kearah CPE/ONT di sisi Client', 'Mengecek Kabel FO dari FAT kearah ONT Client dan test redamannya | Kalau redaman aman regist ulang ONT pada OLT atau ganti ONT dengan yang baru', 'Terverifikasi'),
(19, 'OLT', 'ICMP RTO/Loss', 'Banyak Perangkat dalam 1 Area', 'Bisa diakses tapi lag/timeout', 'Listrik & Perangkat Aman (Menyala Normal)', 'Perkabelan Aman', 'Terdapat Masalah Pada OLT tersebut', 'Cek terlebih dahulu apakah kelistrikan, Jalur Core, atau perangkat menyala dengan normal | Kalau 3 hal diatas normal maka coba console OLT tersebut | Kalau tidak bisa di console ganti card OLT nya | Kalau masih bisa di console coba restart dlu module card nya dan jika masih bermasalah coba restart OLT nya | Kalau Langkah\" diatas sudah dilakukan dan masih bermasalah maka ganti perangkat OLT nya', 'Terverifikasi');

-- --------------------------------------------------------

--
-- Table structure for table `tabel_parameter`
--

CREATE TABLE `tabel_parameter` (
  `id_param` int NOT NULL,
  `kategori` varchar(50) DEFAULT NULL,
  `nilai` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tabel_parameter`
--

INSERT INTO `tabel_parameter` (`id_param`, `kategori`, `nilai`) VALUES
(2, 'kategori_problem', '[ ONT ] Dying Gasp'),
(3, 'kategori_problem', '[ ONT ] LOS/LOBi');

-- --------------------------------------------------------

--
-- Table structure for table `tabel_user`
--

CREATE TABLE `tabel_user` (
  `id_user` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tabel_user`
--

INSERT INTO `tabel_user` (`id_user`, `username`, `password`, `role`) VALUES
(1, 'admin', 'admin', 'admin'),
(10, 'osa', 'osa', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tabel_kasus`
--
ALTER TABLE `tabel_kasus`
  ADD PRIMARY KEY (`id_kasus`);

--
-- Indexes for table `tabel_parameter`
--
ALTER TABLE `tabel_parameter`
  ADD PRIMARY KEY (`id_param`);

--
-- Indexes for table `tabel_user`
--
ALTER TABLE `tabel_user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tabel_kasus`
--
ALTER TABLE `tabel_kasus`
  MODIFY `id_kasus` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `tabel_parameter`
--
ALTER TABLE `tabel_parameter`
  MODIFY `id_param` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tabel_user`
--
ALTER TABLE `tabel_user`
  MODIFY `id_user` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
