DROP TABLE dbmp_mysql_business_group;
CREATE TABLE dbmp_mysql_business(
    `mysql_business_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '业务组ID',
    `name` varchar(50) NOT NULL DEFAULT '' COMMENT '业务名称',
    `remark` varchar(200) NOT NULL DEFAULT '' COMMENT '备注',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`mysql_business_id`),
    UNIQUE KEY udx$name(name)
)COMMENT='MySQL业务库，主要记录表结构相同的数据库';

CREATE TABLE dbmp_mysql_business_detail(
    mysql_business_detail_id INT unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
    mysql_business_id int(10) unsigned NOT NULL COMMENT '业务组ID',
    mysql_database_id int(10) unsigned NOT NULL COMMENT 'MySQL数据库ID',
    create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`mysql_business_detail_id`),
    KEY idx$mysql_business_id(mysql_business_id),
    KEY idx$mysql_database_id(mysql_database_id)
)COMMENT='记录着业务相关表结构相同的数据库';
