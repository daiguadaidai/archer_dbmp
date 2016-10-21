CREATE TABLE dbmp_mysql_database(
    mysql_database_id INT unsigned NOT NULL AUTO_INCREMENT COMMENT 'MySQL数据库ID',
    mysql_instance_id int(10) unsigned NOT NULL COMMENT 'MySQL实例ID',
    name varchar(50) NOT NULL DEFAULT '' COMMENT 'MySQL数据库名称',
    create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (mysql_database_id),
    INDEX idx$mysql_instance_id(mysql_instance_id)
)COMMENT='MySQL数据库实例';
