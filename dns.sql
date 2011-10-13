#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#       If you have any questions or inquiries please feel free to email at
#       eugene@jinocloud.com


CREATE DATABASE IF NOT EXISTS `dns` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `dns` ;

CREATE  TABLE IF NOT EXISTS `zones` (
  `zoneid` INT AUTO_INCREMENT,
  `domain` VARCHAR(90) NOT NULL UNIQUE ,
  `date` TIMESTAMP DEFAULT NOW() ,
  `soa` VARCHAR(90) NOT NULL DEFAULT 'ns0.jinocloud.com',
  `admin` VARCHAR(90) NOT NULL DEFAULT 'dnsadmin.jinocloud.com',
  `ttl` MEDIUMINT UNSIGNED NOT NULL DEFAULT '86400',
  `refresh` MEDIUMINT UNSIGNED NOT NULL DEFAULT '14400',
  `retry` MEDIUMINT UNSIGNED NOT NULL DEFAULT '7200',
  `expiry` MEDIUMINT UNSIGNED NOT NULL DEFAULT '1209600',
  `min` MEDIUMINT NOT NULL DEFAULT '86400',
  PRIMARY KEY (`zoneid`) ,
  KEY (`domain`)
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE  TABLE IF NOT EXISTS `records` (
  `id` INT AUTO_INCREMENT ,
  `zoneid` INT NOT NULL ,
  `subdomain` VARCHAR(64) ,
  `type` VARCHAR(4) NOT NULL DEFAULT 'A' ,
  `ttl` MEDIUMINT UNSIGNED NOT NULL DEFAULT '86400' ,
  `target` VARCHAR(128) NOT NULL ,
  PRIMARY KEY (`id`) ,
  FOREIGN KEY (`zoneid`) REFERENCES zones(`zoneid`) ON DELETE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE  TABLE IF NOT EXISTS `srv` (
  `id` INT AUTO_INCREMENT ,
  `zoneid` INT NOT NULL ,
  `service` VARCHAR(64) ,
  `proto` VARCHAR(4) NOT NULL ,
  `ttl` MEDIUMINT UNSIGNED NOT NULL DEFAULT '86400' ,
  `priority` SMALLINT UNSIGNED ,
  `weight` SMALLINT UNSIGNED ,
  `port` SMALLINT UNSIGNED ,
  `target` VARCHAR(128) NOT NULL ,
  PRIMARY KEY (`id`) ,
  FOREIGN KEY (`zoneid`) REFERENCES zones(`zoneid`) ON DELETE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE  TABLE IF NOT EXISTS `spf` (
  `id` INT AUTO_INCREMENT ,
  `zoneid` INT NOT NULL UNIQUE,
  `ttl` MEDIUMINT UNSIGNED NOT NULL DEFAULT '86400' ,
  `record` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`id`) ,
  FOREIGN KEY (`zoneid`) REFERENCES zones(`zoneid`) ON DELETE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

