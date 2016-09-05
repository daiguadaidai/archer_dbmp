ALTER TABLE dbmp_mysql_backup_remote
    ADD mysql_backup_instance_id INT unsigned NOT NULL COMMENT '备份实例ID' AFTER mysql_backup_remote_id,
    ADD UNIQUE INDEX udx$mysql_backup_instance_id(mysql_backup_instance_id);
