-- MySQL dump 10.13  Distrib 5.6.31-77.0, for Linux (x86_64)
--
-- Host: 192.168.1.233    Database: my_free
-- ------------------------------------------------------
-- Server version	5.6.31-77.0-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cmdb_os`
--

DROP TABLE IF EXISTS `cmdb_os`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_os` (
  `os_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '操作系统ID',
  `hostname` varchar(50) NOT NULL DEFAULT '' COMMENT '操作系统的hostname信息',
  `alias` varchar(40) NOT NULL DEFAULT '' COMMENT '别名',
  `ip` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '操作系统IP',
  `username` varchar(30) NOT NULL DEFAULT '' COMMENT '用于登陆操作系统执行一些命令的用户',
  `password` varchar(200) NOT NULL DEFAULT '' COMMENT '登陆用户密码，是个可逆的加密串',
  `remark` varchar(50) NOT NULL DEFAULT '' COMMENT '备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`os_id`)
) ENGINE=InnoDB AUTO_INCREMENT=257 DEFAULT CHARSET=utf8 COMMENT='操作系统信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_inception_business`
--

DROP TABLE IF EXISTS `dbmp_inception_business`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_inception_business` (
  `inception_business_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'SQL审核业务组ID',
  `inception_record_id` int(10) unsigned NOT NULL COMMENT '审核记录ID',
  `mysql_business_id` int(10) unsigned NOT NULL COMMENT '业务组ID',
  `execute_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '执行状态: 1未执行 2执行成功 3执行失败 4部分执行失败',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`inception_business_id`),
  UNIQUE KEY `udx$record_business_id` (`inception_record_id`,`mysql_business_id`),
  KEY `idx$mysql_business_id` (`mysql_business_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='SQL审核业务组';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_inception_business_detail`
--

DROP TABLE IF EXISTS `dbmp_inception_business_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_inception_business_detail` (
  `inception_business_detail_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'SQL审核业务组ID',
  `inception_business_id` int(10) unsigned NOT NULL COMMENT 'SQL审核业务组ID',
  `inception_record_id` int(10) unsigned NOT NULL COMMENT '审核记录ID',
  `mysql_business_id` int(10) unsigned NOT NULL COMMENT '业务组ID',
  `mysql_database_id` int(10) unsigned NOT NULL COMMENT '数据库ID',
  `execute_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '执行状态: 1未执行 2执行成功 3执行失败 4部分执行失败',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`inception_business_detail_id`),
  UNIQUE KEY `udx$record_business_id` (`inception_record_id`,`mysql_database_id`),
  KEY `idx$inception_business_id` (`inception_business_id`),
  KEY `idx$mysql_business_id` (`mysql_business_id`),
  KEY `idx$mysql_database_id` (`mysql_database_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='SQL审核业务组明细';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_inception_database`
--

DROP TABLE IF EXISTS `dbmp_inception_database`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_inception_database` (
  `inception_database_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '需要执行审核的SQL ID',
  `inception_record_id` int(10) unsigned NOT NULL COMMENT '审核记录ID',
  `mysql_database_id` int(10) unsigned NOT NULL COMMENT '数据库ID',
  `execute_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '执行状态: 1未执行 2执行成功 3执行失败',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`inception_database_id`),
  UNIQUE KEY `udx$record_database` (`inception_record_id`,`mysql_database_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='需要执行审核的SQL';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_inception_instance`
--

DROP TABLE IF EXISTS `dbmp_inception_instance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_inception_instance` (
  `inception_instance_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `host` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '链接Inception HOST',
  `port` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '链接Inception PORT',
  `alias` varchar(50) NOT NULL DEFAULT '' COMMENT '别名',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`inception_instance_id`),
  UNIQUE KEY `udx$host_port` (`host`,`port`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='Inception实例';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_inception_record`
--

DROP TABLE IF EXISTS `dbmp_inception_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_inception_record` (
  `inception_record_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inception_instance_id` int(10) unsigned NOT NULL COMMENT 'Inception 实例ID',
  `is_remote_backup` tinyint(4) NOT NULL DEFAULT '1' COMMENT '执行前是否进行备份:0否 1是',
  `inception_target` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'SQL审核对象:1仅数据库 2仅业务组 3混合',
  `tag` varchar(20) NOT NULL DEFAULT '' COMMENT '用于标记该审核语句的特点',
  `remark` varchar(200) NOT NULL DEFAULT '' COMMENT '该语句的备注说明',
  `sql_text` text COMMENT '审核是SQL语句',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `charset` varchar(20) NOT NULL DEFAULT '' COMMENT '字符集',
  `execute_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '执行状态: 1未执行 2执行成功 3执行失败 4部分失败',
  PRIMARY KEY (`inception_record_id`),
  KEY `idx$inception_instance_id` (`inception_instance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='需要审核的记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_mysql_backup_info`
--

DROP TABLE IF EXISTS `dbmp_mysql_backup_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_mysql_backup_info` (
  `mysql_backup_info_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '备份过程信息ID',
  `mysql_instance_id` int(10) unsigned NOT NULL COMMENT 'MySQL实例ID',
  `backup_status` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '备份状态：1、未备份，2、正在备份，3、备份完成，4、备份失败，5、备份完成但和指定的有差异',
  `backup_data_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '备份数据状态：1、未备份，2、备份失败，3、备份完成',
  `check_status` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '校验备份集状态：1、未校验，2、正在校验，3、校验完成，4、校验失败',
  `binlog_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'binlog备份状态:1、未备份，2、备份失败，3、完成备份',
  `trans_data_status` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '备份数据远程传输状态：1、未传输，2、传输失败，3、传输完成',
  `trans_binlog_status` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '备份binlog远程传输状态：1、未传输，2、传输失败，3、传输完成',
  `compress_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'binlog备份状态:1、未压缩，2、压缩失败，3、压缩完成',
  `thread_id` int(11) NOT NULL DEFAULT '-1' COMMENT '备份操作系统进程ID',
  `backup_dir` varchar(250) NOT NULL DEFAULT '' COMMENT '本地备份文件夹名称',
  `remote_backup_dir` varchar(250) NOT NULL DEFAULT '' COMMENT '远程备份文件夹名称',
  `backup_size` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '备份集大小',
  `backup_start_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '备份开始时间',
  `backup_end_time` datetime DEFAULT NULL COMMENT '备份结束时间',
  `check_start_time` datetime DEFAULT NULL COMMENT '校验开始时间',
  `check_end_time` datetime DEFAULT NULL COMMENT '校验结束时间',
  `trans_start_time` datetime DEFAULT NULL COMMENT '传输至远程开始时间',
  `trans_end_time` datetime DEFAULT NULL COMMENT '传输至远程结束时间',
  `message` varchar(50) NOT NULL DEFAULT '' COMMENT '备份信息',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`mysql_backup_info_id`),
  KEY `idx$mysql_instance_id` (`mysql_instance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='描述整个备份过程的信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_mysql_backup_instance`
--

DROP TABLE IF EXISTS `dbmp_mysql_backup_instance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_mysql_backup_instance` (
  `mysql_backup_instance_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '备份实例ID',
  `mysql_instance_id` int(10) unsigned NOT NULL COMMENT 'MySQL实例ID',
  `backup_tool` tinyint(3) unsigned NOT NULL DEFAULT '4' COMMENT '使用备份工具：1、mysqldump，2、mysqlpump、3、mydumper、4、xtrabackup',
  `backup_type` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '备份类型: 1、强制指定实例备份，2、强制寻找备份，3、最优型备份',
  `is_all_instance` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '是否备份整个实例：0、否，1、是',
  `is_binlog` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '是否备份binlog：0、否，1、是',
  `is_compress` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '备份集是否压缩：0、否，1、是',
  `is_to_remote` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '将备份传输至远程：0、否，1、是',
  `backup_dir` varchar(200) NOT NULL DEFAULT '' COMMENT '本地备份目录',
  `backup_tool_file` varchar(200) NOT NULL DEFAULT '' COMMENT '备份工具路径及名称',
  `backup_tool_param` varchar(200) NOT NULL DEFAULT '' COMMENT '备份额外参数',
  `backup_name` varchar(100) NOT NULL DEFAULT '' COMMENT '备份名称',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`mysql_backup_instance_id`),
  UNIQUE KEY `udx$mysql_instance_id` (`mysql_instance_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='MySQL需要备份的实例信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_mysql_backup_remote`
--

DROP TABLE IF EXISTS `dbmp_mysql_backup_remote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_mysql_backup_remote` (
  `mysql_backup_remote_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '备份传输到远程系统ID',
  `mysql_backup_instance_id` int(10) unsigned NOT NULL COMMENT '备份实例ID',
  `os_id` int(10) unsigned NOT NULL COMMENT '操作系统ID',
  `mysql_instance_id` int(10) unsigned NOT NULL COMMENT 'MySQL实例ID',
  `remote_dir` varchar(200) NOT NULL DEFAULT '' COMMENT '远程备份目录',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`mysql_backup_remote_id`),
  UNIQUE KEY `udx$mysql_instance_id` (`mysql_instance_id`),
  UNIQUE KEY `udx$mysql_backup_instance_id` (`mysql_backup_instance_id`),
  KEY `idx$os_id` (`os_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='备份传输到远程机器';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_mysql_business`
--

DROP TABLE IF EXISTS `dbmp_mysql_business`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_mysql_business` (
  `mysql_business_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '业务组ID',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '业务名称',
  `remark` varchar(200) NOT NULL DEFAULT '' COMMENT '备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`mysql_business_id`),
  UNIQUE KEY `udx$name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='MySQL业务库，主要记录表结构相同的数据库';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_mysql_business_detail`
--

DROP TABLE IF EXISTS `dbmp_mysql_business_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_mysql_business_detail` (
  `mysql_business_detail_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `mysql_business_id` int(10) unsigned NOT NULL COMMENT '业务组ID',
  `mysql_database_id` int(10) unsigned NOT NULL COMMENT 'MySQL数据库ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`mysql_business_detail_id`),
  UNIQUE KEY `udx$mysql_business_database_id` (`mysql_business_id`,`mysql_database_id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8 COMMENT='记录着业务相关表结构相同的数据库';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_mysql_database`
--

DROP TABLE IF EXISTS `dbmp_mysql_database`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_mysql_database` (
  `mysql_database_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'MySQL数据库ID',
  `mysql_instance_id` int(10) unsigned NOT NULL COMMENT 'MySQL实例ID',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT 'MySQL数据库名称',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`mysql_database_id`),
  UNIQUE KEY `udx$mysql_instance_id_name` (`mysql_instance_id`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8 COMMENT='MySQL实例数据库';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_mysql_ha_group`
--

DROP TABLE IF EXISTS `dbmp_mysql_ha_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_mysql_ha_group` (
  `mysql_ha_group_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '高可用组ID',
  `alias` varchar(40) NOT NULL DEFAULT '' COMMENT '组别名',
  `remark` varchar(50) NOT NULL DEFAULT '' COMMENT '备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`mysql_ha_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='MySQL高可用组, 主要用于MySQL备份使用';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_mysql_ha_group_detail`
--

DROP TABLE IF EXISTS `dbmp_mysql_ha_group_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_mysql_ha_group_detail` (
  `mysql_ha_group_detail_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'HA GROUP MySQL 管理表',
  `mysql_instance_id` int(10) unsigned NOT NULL COMMENT 'MySQL实例ID',
  `mysql_ha_group_id` int(10) unsigned NOT NULL COMMENT '高可用组ID',
  `backup_priority` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '备份优先级，值越大优先级越高',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`mysql_ha_group_detail_id`),
  UNIQUE KEY `udx$mysql_instance_id` (`mysql_instance_id`),
  KEY `idx$mysql_ha_group_id` (`mysql_ha_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='MySQL HA 组和MySQL实例关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_mysql_instance`
--

DROP TABLE IF EXISTS `dbmp_mysql_instance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_mysql_instance` (
  `mysql_instance_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'MySQL实例ID',
  `os_id` int(10) unsigned NOT NULL COMMENT '操作系统ID',
  `host` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '链接MySQL HOST',
  `port` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '链接MySQL PORT',
  `username` varchar(50) NOT NULL DEFAULT '' COMMENT '管理MySQL用户名',
  `password` varchar(200) NOT NULL DEFAULT '' COMMENT '管理MySQL用户名密码，是个可逆的加密串',
  `run_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'MySQL运行状态:1、停止，2、运行中，3、未知，4、正在关闭，5、正在启动',
  `possible_pid` varchar(100) NOT NULL DEFAULT '' COMMENT 'MySQL可能运行的PID',
  `remark` varchar(50) NOT NULL DEFAULT '' COMMENT '备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`mysql_instance_id`),
  UNIQUE KEY `udx$os_id_port` (`os_id`,`port`),
  KEY `idx$os_id` (`os_id`)
) ENGINE=InnoDB AUTO_INCREMENT=298 DEFAULT CHARSET=utf8 COMMENT='MySQL实例信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbmp_mysql_instance_info`
--

DROP TABLE IF EXISTS `dbmp_mysql_instance_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbmp_mysql_instance_info` (
  `mysql_instance_info_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'MySQL实例ID',
  `mysql_instance_id` int(10) unsigned NOT NULL COMMENT 'MySQL实例ID',
  `my_cnf_path` varchar(200) NOT NULL DEFAULT '' COMMENT 'my.cnf 文件路径',
  `base_dir` varchar(200) NOT NULL DEFAULT '' COMMENT 'MySQL软件目录',
  `start_cmd` varchar(200) NOT NULL DEFAULT '' COMMENT '启动MySQL命令',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`mysql_instance_info_id`),
  UNIQUE KEY `udx$mysql_instance_id` (`mysql_instance_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='MySQL实例信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-12 14:51:22
