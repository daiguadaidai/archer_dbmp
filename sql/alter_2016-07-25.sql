ALTER TABLE dbmp_mysql_instance 
    ADD run_status TINYINT NOT NULL DEFAULT 1
    COMMENT 'MySQL运行状态:1、停止，2、运行中，3、未知' AFTER password;
