ALTER TABLE dbmp_inception_database
    MODIFY `execute_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '执行状态: 1未执行 2执行成功 3执行失败';
    
ALTER TABLE dbmp_inception_business
    MODIFY `execute_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '执行状态: 1未执行 2执行成功 3执行失败 4部分失败';
    
ALTER TABLE dbmp_inception_business_detail
    MODIFY `execute_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '执行状态: 1未执行 2执行成功 3执行失败';
