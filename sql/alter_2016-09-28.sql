ALTER TABLE dbmp_mysql_business_detail
    ADD UNIQUE INDEX udx$mysql_business_database_id(mysql_business_id, mysql_database_id),
    DROP INDEX idx$mysql_business_id,
    DROP INDEX idx$mysql_database_id;
