-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 06-03-2025 a las 16:58:15
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `psicologia`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Cita`
--

CREATE TABLE `Cita` (
  `id_cita` int(250) NOT NULL,
  `id_estudiante` int(10) NOT NULL,
  `id_diagnostico` int(250) NOT NULL,
  `fecha` varchar(1000) NOT NULL,
  `motivo` varchar(10000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Diagnostico`
--

CREATE TABLE `Diagnostico` (
  `id_diagnostico` int(250) NOT NULL,
  `diagnostico` varchar(10000) NOT NULL,
  `nivel` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Estudiantes`
--

CREATE TABLE `Estudiantes` (
  `id_estudiante` int(10) NOT NULL,
  `documento` int(10) NOT NULL,
  `nombre` varchar(500) NOT NULL,
  `apellido` varchar(500) NOT NULL,
  `edad` int(2) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `nombreAcudiente` varchar(500) NOT NULL,
  `email` varchar(500) NOT NULL,
  `grado` varchar(10) NOT NULL,
  `id_diagnostico` int(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `HistoriaClinica`
--

CREATE TABLE `HistoriaClinica` (
  `id_historia` int(250) NOT NULL,
  `id_estudiante` int(250) NOT NULL,
  `id_diagnostico` int(250) NOT NULL,
  `observaciones` varchar(1000) NOT NULL,
  `piar` varchar(1000) NOT NULL,
  `detalles_piar` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Intervencion`
--

CREATE TABLE `Intervencion` (
  `id_intervencion` int(250) NOT NULL,
  `id_historia` int(250) NOT NULL,
  `tipo_intervencion` varchar(1000) NOT NULL,
  `fecha` varchar(10000) NOT NULL,
  `detalles` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Cita`
--
ALTER TABLE `Cita`
  ADD PRIMARY KEY (`id_cita`),
  ADD KEY `fk_estudiante_cita` (`id_estudiante`),
  ADD KEY `fk_diagnostico_cita` (`id_diagnostico`);

--
-- Indices de la tabla `Diagnostico`
--
ALTER TABLE `Diagnostico`
  ADD PRIMARY KEY (`id_diagnostico`);

--
-- Indices de la tabla `Estudiantes`
--
ALTER TABLE `Estudiantes`
  ADD PRIMARY KEY (`id_estudiante`),
  ADD KEY `fk_diagnostico` (`id_diagnostico`);

--
-- Indices de la tabla `HistoriaClinica`
--
ALTER TABLE `HistoriaClinica`
  ADD PRIMARY KEY (`id_historia`),
  ADD KEY `fk_estudiante` (`id_estudiante`),
  ADD KEY `fk_diagnostico_historia` (`id_diagnostico`);

--
-- Indices de la tabla `Intervencion`
--
ALTER TABLE `Intervencion`
  ADD PRIMARY KEY (`id_intervencion`),
  ADD KEY `fk_historia` (`id_historia`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `Cita`
--
ALTER TABLE `Cita`
  ADD CONSTRAINT `fk_diagnostico_cita` FOREIGN KEY (`id_diagnostico`) REFERENCES `Diagnostico` (`id_diagnostico`),
  ADD CONSTRAINT `fk_estudiante_cita` FOREIGN KEY (`id_estudiante`) REFERENCES `Estudiantes` (`id_estudiante`);

--
-- Filtros para la tabla `Estudiantes`
--
ALTER TABLE `Estudiantes`
  ADD CONSTRAINT `fk_diagnostico` FOREIGN KEY (`id_diagnostico`) REFERENCES `Diagnostico` (`id_diagnostico`);

--
-- Filtros para la tabla `HistoriaClinica`
--
ALTER TABLE `HistoriaClinica`
  ADD CONSTRAINT `fk_diagnostico_historia` FOREIGN KEY (`id_diagnostico`) REFERENCES `Diagnostico` (`id_diagnostico`),
  ADD CONSTRAINT `fk_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `Estudiantes` (`id_estudiante`);

--
-- Filtros para la tabla `Intervencion`
--
ALTER TABLE `Intervencion`
  ADD CONSTRAINT `fk_historia` FOREIGN KEY (`id_historia`) REFERENCES `HistoriaClinica` (`id_historia`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
