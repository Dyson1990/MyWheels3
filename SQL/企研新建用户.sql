DROP USER IF EXISTS 'usr_lyb'@'%';
CREATE USER'usr_lyb'@'%' IDENTIFIED BY 'qy123456';
-- ALTER USER 'usr_lyb'@'%' IDENTIFIED WITH mysql_native_password BY 'qy1233456';  
-- GRANT SELECT ON usr_lyb.* TO PUBLIC;
-- CREATE ROLE IF NOT EXISTS 'pdb_usr';
-- GRANT ALL ON qy_data.* TO 'pdb_usr';
-- GRANT SELECT ON raw_data.* TO 'pdb_usr';
-- GRANT 'pdb_usr' TO 'usr_lyb'@'%';

GRANT ALL ON qy_data.* TO 'usr_lyb';
GRANT SELECT ON raw_data.* TO 'usr_lyb';

CREATE DATABASE IF NOT EXISTS pdb_usr_lyb;
GRANT ALL ON pdb_usr_lyb.* TO 'usr_lyb'@'%';
-- REVOKE SELECT ON information_schema.* FROM 'usr_lyb'@'%';   --收回角色的权力

DELIMITER $$

DROP PROCEDURE IF EXISTS `qy_data`.`select_to_all` $$
CREATE PROCEDURE `select_to_all`()
BEGIN
	DECLARE usr_name CHAR(32);
	DECLARE schema_name varchar(64);
	DECLARE end_mark INT DEFAULT 0;
	DECLARE usr_cur CURSOR FOR (
		SELECT * FROM
		(SELECT `User` FROM `mysql`.`user` WHERE `Host`='%') t1
		JOIN
		(SELECT `TABLE_SCHEMA` FROM `information_schema`.`SCHEMA_PRIVILEGES` WHERE LEFT(`TABLE_SCHEMA`,7)='pdb_usr') t2
	);
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET end_mark = True;	#声明当游标遍历完后将标志变量置成某个值
-- 	SET @target_database='usr_lyb';
	
	OPEN usr_cur;
	usrLoop:LOOP
		FETCH usr_cur INTO usr_name, schema_name;
-- 		UNTIL end_mark END usr_cur;
		IF end_mark THEN
			LEAVE usrLoop;
		END IF;
		SET @sql_str = CONCAT('GRANT SELECT ON ',schema_name,'.* TO ''',usr_name,'''@''%''');

-- 		SELECT @sql_str;
		PREPARE stmt FROM @sql_str;
			EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
	END LOOP;
	CLOSE usr_cur;
END $$

DELIMITER ;

CALL `qy_data`.`select_to_all`();
DROP PROCEDURE IF EXISTS `qy_data`.`select_to_all`;