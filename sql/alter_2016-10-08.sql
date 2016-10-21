CREATE TABLE dbmp_inception_instance(
    inception_instance_id INT unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
    host int(10) unsigned NOT NULL DEFAULT '0' COMMENT '链接Inception HOST',
    port int(10) unsigned NOT NULL DEFAULT '0' COMMENT '链接Inception PORT',
    alias VARCHAR(50) NOT NULL DEFAULT '' COMMENT '别名',
    create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (inception_instance_id),
    UNIQUE INDEX udx$host_port(host, port)
)COMMENT='Inception实例';
    
CREATE TABLE dbmp_inception_record(
    inception_record_id INT unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
    inception_instance_id INT unsigned NOT NULL COMMENT 'Inception 实例ID',
    is_remote_backup TINYINT NOT NULL DEFAULT 0 COMMENT '执行前是否进行备份:0否 1是',
    tag VARCHAR(20) NOT NULL DEFAULT '' COMMENT '用于标记该审核语句的特点',
    remark VARCHAR(200) NOT NULL DEFAULT '' COMMENT '该语句的备注说明',
    sql_text TEXT DEFAULT NULL COMMENT '审核是SQL语句',
    create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY(inception_record_id),
    INDEX idx$inception_instance_id(inception_instance_id)
)COMMENT='需要审核的记录';

INSERT INTO dbmp_inception_instance VALUES(NULL, INET_ATON('127.0.0.1'), 6669, '测试Inception', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());
