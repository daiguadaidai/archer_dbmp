ALTER TABLE dbmp_inception_record
    ADD inception_target TINYINT NOT NULL DEFAULT 1
        COMMENT 'SQL审核对象:1仅数据库 2仅业务组 3混合'
        AFTER is_remote_backup,
    ADD charset VARCHAR(20) NOT NULL DEFAULT '' COMMENT '字符集',
    MODIFY is_remote_backup tinyint(4) NOT NULL DEFAULT '1'
        COMMENT '执行前是否进行备份:0否 1是';

CREATE TABLE dbmp_inception_database(
    inception_database_id INT unsigned NOT NULL AUTO_INCREMENT COMMENT '需要执行审核的SQL ID',
    inception_record_id int(10) unsigned NOT NULL COMMENT 'MySQL数据库ID',
    mysql_database_id int(10) unsigned NOT NULL COMMENT 'MySQL实例ID',
    execute_status TINYINT NOT NULL DEFAULT 1 COMMENT '执行状态: 1未执行 2执行成功 3执行失败',
    create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY(inception_database_id),
    UNIQUE INDEX udx$record_database(inception_record_id, mysql_database_id)
) COMMENT ='需要执行审核的SQL';
