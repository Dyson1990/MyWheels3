IF NOT EXISTS(SELECT 1 
              FROM  information_schema.COLUMNS
              WHERE TABLE_SCHEMA='数据库' 
                    AND table_name='表' 
                    AND COLUMN_NAME='列')
THEN
    ALTER TABLE 表 ADD 列 VARCHAR(255) NOT NULL
END IF;