ALTER TABLE dbmp_mysql_instance 
    MODIFY `username` varchar(50) NOT NULL DEFAULT '' COMMENT '管理MySQL用户名'; 

ALTER TABLE dbmp_mysql_instance_info
    ADD start_cmd VARCHAR(200) NOT NULL DEFAULT '' COMMENT '启动MySQL命令' AFTER my_cnf_path,
    ADD base_dir VARCHAR(200) NOT NULL DEFAULT '' COMMENT 'MySQL软件目录'  AFTER my_cnf_path;
    
UPDATE dbmp_mysql_instance_info
SET start_cmd = '/bin/bash /usr/local/mysql/bin/mysqld_safe --defaults-file=/etc/my_3306.cnf > /dev/null 2>&1 &',
    base_dir = '/usr/local/mysql';

ALTER TABLE dbmp_mysql_instance_info
    ADD UNIQUE KEY udx$mysql_instance_id(mysql_instance_id); 
