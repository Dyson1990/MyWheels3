CREATE DATABASE IF NOT EXISTS db_ccad;
GRANT ALL ON db_ccad.* TO 'usr_sdy'@'%';

DELIMITER $$

DROP PROCEDURE IF EXISTS `qy_data`.`select_to_all` $$
CREATE PROCEDURE `select_to_all`()
BEGIN
	DECLARE usr_name CHAR(32);
	DECLARE end_mark INT DEFAULT 0;
	DECLARE usr_cur CURSOR FOR (
		SELECT `User` FROM `mysql`.`user` WHERE `Host`='%'
		);
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET end_mark = True;	#声明当游标遍历完后将标志变量置成某个值
-- 	SET @target_database='usr_lyb';
	
	SET @schema_name := 'db_ccad';
	OPEN usr_cur;
	usrLoop:LOOP
		FETCH usr_cur INTO usr_name;
-- 		UNTIL end_mark END usr_cur;
		IF end_mark THEN
			LEAVE usrLoop;
		END IF;
		SET @sql_str = CONCAT('GRANT SELECT ON ',@schema_name,'.* TO ''',usr_name,'''@''%''');

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