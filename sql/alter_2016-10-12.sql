ALTER TABLE dbmp_inception_database
    MODIFY `inception_record_id` int(10) unsigned NOT NULL COMMENT '审核记录ID',
    MODIFY `mysql_database_id` int(10) unsigned NOT NULL COMMENT '数据库ID';

CREATE TABLE dbmp_inception_business(
    inception_business_id INT unsigned NOT NULL AUTO_INCREMENT COMMENT 'SQL审核业务组ID',
    inception_record_id int(10) unsigned NOT NULL COMMENT '审核记录ID',
    mysql_business_id int(10) unsigned NOT NULL COMMENT '业务组ID',
    execute_status tinyint(4) NOT NULL DEFAULT '1' COMMENT '执行状态: 1未执行 2执行成功 3执行失败 4部分执行失败',
    create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY(inception_business_id),
    UNIQUE INDEX udx$record_business_id(inception_record_id, mysql_business_id),
    INDEX idx$mysql_business_id(mysql_business_id)
)COMMENT = 'SQL审核业务组';

CREATE TABLE dbmp_inception_business_detail(
    inception_business_id INT unsigned NOT NULL AUTO_INCREMENT COMMENT 'SQL审核业务组ID',
    inception_record_id int(10) unsigned NOT NULL COMMENT '审核记录ID',
    mysql_business_id int(10) unsigned NOT NULL COMMENT '业务组ID',
    mysql_database_id int(10) unsigned NOT NULL COMMENT '数据库ID',
    execute_status tinyint(4) NOT NULL DEFAULT '1' COMMENT '执行状态: 1未执行 2执行成功 3执行失败 4部分执行失败',
    create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY(inception_business_id),
    UNIQUE INDEX udx$record_business_id(inception_record_id, mysql_database_id),
    INDEX idx$mysql_business_id(mysql_business_id),
    INDEX idx$mysql_database_id(mysql_database_id)
)COMMENT = 'SQL审核业务组明细';
