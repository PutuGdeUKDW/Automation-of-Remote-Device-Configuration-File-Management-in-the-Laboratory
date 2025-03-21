-- configuration_version.sql
-- Script to create tables for remote device configuration management
-- Created on: March 21, 2025

-- Table to store configuration versions
CREATE TABLE `configuration_version` (
  `version` int NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`version`)
);

-- Table to store device information
CREATE TABLE `piranti` (
  `nama_piranti` varchar(100) NOT NULL,
  `ip_address` varchar(15) NOT NULL,
  `blok` int DEFAULT NULL,
  `tipe_piranti` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`nama_piranti`,`ip_address`)
);

-- Table to store default configurations with foreign key relationships
CREATE TABLE `default_configuration` (
  `id` int NOT NULL,
  `nama_piranti` varchar(255) NOT NULL,
  `versi` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `default_configuration_ibfk_1` FOREIGN KEY (`versi`) 
    REFERENCES `configuration_version` (`version`) ON DELETE CASCADE,
  CONSTRAINT `fk_piranti_nama` FOREIGN KEY (`nama_piranti`) 
    REFERENCES `piranti` (`nama_piranti`) ON DELETE CASCADE ON UPDATE CASCADE
);