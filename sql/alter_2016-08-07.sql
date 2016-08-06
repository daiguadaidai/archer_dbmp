ALTER TABLE dbmp_mysql_instance
    MODIFY `run_status` tinyint(4) NOT NULL DEFAULT '1'
    COMMENT 'MySQL运行状态:1、停止，2、运行中，3、未知，4、正在关闭，5、正在启动';

ALTER TABLE dbmp_mysql_instance
    ADD possible_pid VARCHAR(100) NOT NULL DEFAULT ''
    COMMENT 'MySQL可能运行的PID' AFTER run_status;
