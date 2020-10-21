DELIMITER $$
#########################################################################################################################################
DROP PROCEDURE IF EXISTS clear_usrs $$
CREATE PROCEDURE `clear_usrs`() #删除所有账号中，host为localhost以外的所有账户
BEGIN
	DECLARE usr0 VARCHAR(255);
	DECLARE host0 VARCHAR(255);
	DECLARE done INT DEFAULT false;
	DECLARE usr_cur CURSOR FOR SELECT `User`, `Host` FROM mysql.`user` WHERE `Host` <> 'localhost';
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;

	OPEN usr_cur;
	read_loop:LOOP
		FETCH usr_cur INTO usr0, host0;
		IF done THEN
			LEAVE read_loop;
		END IF;

		SET @sql_str := CONCAT("DROP USER ", usr0, "@'", host0, "'");
		INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('clear_usrs', '@sql_str', @sql_str, NOW());

		PREPARE stmt FROM @sql_str;         -- 预处理动态sql语句
		EXECUTE stmt ;                        -- 执行sql语句
		DEALLOCATE PREPARE stmt;      -- 释放prepare

	END LOOP;
END $$
#########################################################################################################################################
DROP PROCEDURE IF EXISTS create_usr $$
CREATE PROCEDURE `create_usr`(IN `usr_str` varchar(100))  #创建用户，传入的参数为 用户名+IP
BEGIN
	DECLARE res varchar(60);
	IF usr_str <> '' THEN
		SET @usr := SUBSTRING_INDEX(usr_str,'+',1);
		SET @ip := SUBSTRING_INDEX(usr_str,'+',-1);

		#判断用户是否存在，不存在则创建
		SELECT COUNT(`User`) INTO res FROM `mysql`.`user` WHERE `Host` = @ip AND `User` = @usr;
		IF res = 0 THEN
			SET @sql_str := CONCAT("CREATE USER '", @usr, "'@'", @ip, "' IDENTIFIED BY 'qy123456';");
			INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('create_usr', '@sql_str', @sql_str, NOW());

			PREPARE stmt FROM @sql_str;         -- 预处理动态sql语句
			EXECUTE stmt ;                        -- 执行sql语句
			DEALLOCATE PREPARE stmt;      -- 释放prepare
		END IF;
	END IF;
END $$
#########################################################################################################################################
DROP PROCEDURE IF EXISTS create_schema $$
CREATE PROCEDURE `create_schema`(IN `schema_name` varchar(100)) #创建schema
BEGIN
	DECLARE res varchar(60);

	#判断schema是否存在，不存在则创建
	IF schema_name <> '' THEN
		SELECT COUNT(`SCHEMA_NAME`) INTO res FROM `information_schema`.`SCHEMATA` WHERE `SCHEMA_NAME` = schema_name;
		IF res = 0 THEN
			SET @sql_str := CONCAT("CREATE DATABASE ", schema_name, " DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;");
			INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('create_schema', '@sql_str', @sql_str, NOW());

			PREPARE stmt FROM @sql_str;         -- 预处理动态sql语句
			EXECUTE stmt ;                        -- 执行sql语句
			DEALLOCATE PREPARE stmt;      -- 释放prepare
		END IF;
	END IF;
END $$
#########################################################################################################################################
DROP PROCEDURE IF EXISTS init_users $$
CREATE PROCEDURE `init_users`() #调用以上函数初始化所有用户和schema
BEGIN
	DECLARE s0 VARCHAR(255);
	DECLARE done INT DEFAULT false;
	DECLARE gratee_cur CURSOR FOR SELECT DISTINCT `GRATEE` FROM qy_data.auth_tbl LIMIT 1, 999; --由于MySQL导入数据的时候会连标题一起导入，所以跳过第一行
	DECLARE schema_cur CURSOR FOR SELECT DISTINCT `SCHEMA` FROM qy_data.auth_tbl LIMIT 1, 999;
	DECLARE CONTINUE HANDLER FOR NOT found set done = true;

	OPEN gratee_cur;
	read_loop: LOOP
		FETCH gratee_cur INTO s0;
		IF done THEN
			LEAVE read_loop;
		END IF;

		IF s0 <> '*' AND s0 <> '' THEN --此处s0为GRANTEE，为*号或者空值，则跳过
			CALL create_usr(s0);
		END IF;

	END LOOP;

	SET done := false;	 --重置控制参数
	OPEN schema_cur;
	read_loop: LOOP
		FETCH schema_cur INTO s0;
		IF done THEN
			LEAVE read_loop;
		END IF;

		IF s0 <> '*' AND s0 <> '' AND s0 <> 'admin' THEN --此处s0为SCHEMA，为*号、admin或者空值，则跳过
			CALL create_schema(s0);
		END IF;

	END LOOP;

END $$
#########################################################################################################################################
DROP PROCEDURE IF EXISTS grant_user $$
CREATE PROCEDURE `grant_user`(IN `usr_str` varchar(100)
                             , IN `schema0` varchar(2550)
                             , IN `table0` varchar(2550)
                             , IN `priv` varchar(2550)
													 ) #给某用户usr_str授权
BEGIN

	IF NOT (table0 = '*') THEN
		SET table0 := CONCAT('`', table0, '`');
	END IF;

	IF NOT (schema0 = '*') THEN
		SET schema0 := CONCAT('`', schema0, '`');
	END IF;

	IF usr_str <> '' THEN
	  # 从usr_str中取出用户名和IP
		SET @usr := SUBSTRING_INDEX(usr_str,'+',1);
		SET @ip := SUBSTRING_INDEX(usr_str,'+',-1);

		SET @sql_str := CONCAT("GRANT ", priv, " ON ", schema0, '.', table0," TO ", @usr, "@'", @ip, "'");
		INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('grant_user', '@sql_str', @sql_str, NOW()); --写入log表中

		PREPARE stmt FROM @sql_str;         -- 预处理动态sql语句
		EXECUTE stmt ;                        -- 执行sql语句
		DEALLOCATE PREPARE stmt;      -- 释放prepare
	END IF;
END $$
#########################################################################################################################################
DROP PROCEDURE IF EXISTS grant_all_users $$
CREATE PROCEDURE `grant_all_users`(IN `schema0` varchar(2550)
                                   , IN `table0` varchar(2550)
                                   , IN `priv` varchar(2550)
																 ) #给所有用户授权
BEGIN
	DECLARE usr0 VARCHAR(255);
	DECLARE host0 VARCHAR(255);
	DECLARE done INT DEFAULT false;
	DECLARE usr_cur CURSOR FOR SELECT `User`, `Host` FROM mysql.`user` WHERE `Host` <> 'localhost';
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;

	# 为了防止某些表名、schema名与MySQL关键词冲突，需要加反引号
	IF NOT (table0 = '*') THEN
		SET table0 := CONCAT('`', table0, '`');
	END IF;

	IF NOT (schema0 = '*') THEN
		SET schema0 := CONCAT('`', schema0, '`');
	END IF;

	OPEN usr_cur;
	read_loop:LOOP
		FETCH usr_cur INTO usr0, host0;
		IF done THEN
			LEAVE read_loop;
		END IF;

		SET @sql_str := CONCAT("GRANT ", priv, " ON ", schema0, '.', table0," TO ", usr0, "@'", host0, "'");
		INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('grant_all_users', '@sql_str', @sql_str, NOW());

		PREPARE stmt FROM @sql_str;         -- 预处理动态sql语句
		EXECUTE stmt ;                        -- 执行sql语句
		DEALLOCATE PREPARE stmt;      -- 释放prepare

	END LOOP;
END $$
#########################################################################################################################################
DELIMITER ;

################# 此处正式调用函数 ########################################
CALL clear_usrs(); # 清除所有自建账号，若没有需要删掉的用户，可以把此处注销掉

# 新建log表
DROP TABLE IF EXISTS pdb_usr_lyb.`PROC_LOG`;
CREATE TABLE pdb_usr_lyb.`PROC_LOG`  (
  `proc_name` varchar(255),
  `log_type` varchar(255),
  `insert_str` text,
  `insert_time` datetime
) ;

# 新建权限表，表结构需要和csv文件中的结构一致
DROP TABLE IF EXISTS qy_data.auth_tbl;
CREATE TABLE qy_data.auth_tbl  (
	`GRATEE` varchar(100),
	`SCHEMA` varchar(100),
	`TYPE` varchar(100),
	`TABLE` varchar(100),
	`Select_priv` varchar(100),
	`Insert_priv` varchar(100),
	`Update_priv` varchar(100),
	`Delete_priv` varchar(100),
	`Create_priv` varchar(100),
	`Drop_priv` varchar(100),
	`Grant_priv` varchar(100),
	`References_priv` varchar(100),
	`Index_priv` varchar(100),
	`Alter_priv` varchar(100),
	`Create_tmp_table_priv` varchar(100),
	`Lock_tables_priv` varchar(100),
	`Create_view_priv` varchar(100),
	`Show_view_priv` varchar(100),
	`Create_routine_priv` varchar(100),
	`Alter_routine_priv` varchar(100),
	`Execute_priv` varchar(100),
	`Event_priv` varchar(100),
	`Trigger_priv` varchar(100)
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

# 向权限表中导入数据
LOAD DATA INFILE '/var/lib/mysql-files/auth_tbl.csv' INTO TABLE qy_data.auth_tbl
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n';

# csv的权限表的最后一行最后一个字段有格式问题
-- UPDATE qy_data.auth_tbl SET Trigger_priv = '';

CALL init_users(); # 新建所有用户

# 开始授权
DELIMITER $$
DROP PROCEDURE IF EXISTS usr_shuffle $$
CREATE PROCEDURE `usr_shuffle`()
BEGIN
	DECLARE col varchar(2550);
	DECLARE res varchar(2550);
	DECLARE s0 varchar(2550);
	DECLARE done INT DEFAULT false;
	DECLARE done0 INT DEFAULT false;
	DECLARE col_cur CURSOR FOR SELECT COLUMN_NAME FROM information_schema.`COLUMNS` WHERE TABLE_SCHEMA = 'qy_data' AND TABLE_NAME = 'auth_tbl';
	DECLARE json_cur CURSOR FOR SELECT json_str FROM temp;
	DECLARE CONTINUE HANDLER FOR NOT found set done = true;


	SET @sql_str := '';
	OPEN col_cur;
	read_loop:LOOP
		FETCH col_cur INTO col; 读取权限表的每一列

			IF done THEN
				LEAVE read_loop;
			END IF;

			IF @sql_str = '' THEN
				SET @mark := "";
			ELSE
				SET @mark := ","""""","",";
			END IF;

			# 将权限表中的所有字段组成一个json字符串（此处还没加花括号）的sql语句
			SET @sql_str := CONCAT(@sql_str, @mark, """""""", col, """"":"""""",`", col, "`");

-- 		SET done := true;
	END LOOP;
	CLOSE col_cur;

-- 	SELECT @sql_str;
-- 	SET @sql_str := CONCAT("SELECT CONCAT(""{"",", @sql_str, ",""""""}"") INTO @res0 FROM qy_data.auth_tbl LIMIT 1, 999");
-- 	SET res := @res;
-- 	SELECT res;
	DROP TABLE IF EXISTS temp;
	# 将权限表中每一行数据都缩成一个json字符串，写入一个临时表中
	SET @sql_str := CONCAT("CREATE TEMPORARY TABLE temp AS SELECT CONCAT(""{"",", @sql_str, ",""""""}"") json_str FROM qy_data.auth_tbl LIMIT 1, 999");
	INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('usr_shuffle', '@sql_str', @sql_str, NOW());

	PREPARE stmt FROM @sql_str;         -- 预处理动态sql语句
	EXECUTE stmt ;                        -- 执行sql语句
	DEALLOCATE PREPARE stmt;      -- 释放prepare

	SET done := false;

	OPEN json_cur;
	read_loop:LOOP
		FETCH json_cur INTO s0; --从临时表中读数据

			IF done THEN
				LEAVE read_loop;
			END IF;

-- 			SELECT s0;
-- 			SET s0 := REPLACE(s0, CHAR(10), '');
			# 从json字符串中取数据
			SET @usr_str := JSON_UNQUOTE(JSON_EXTRACT(s0, '$.GRATEE'));
			SET @schema0 := JSON_UNQUOTE(JSON_EXTRACT(s0, '$.SCHEMA'));
			SET @table0 := JSON_UNQUOTE(JSON_EXTRACT(s0, '$.TABLE'));

			# table字段为空，则说明
			IF @table0 = '' THEN
				SET @table0 := '*';
			END IF;

			INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('usr_shuffle', '@usr_str  @schema0', CONCAT(@usr_str, '    ', @schema0), NOW());

			# 如果schema处填的是admin，则用户为超级管理员，赋予所有权限
			IF @schema0 = 'admin' THEN
				CALL grant_user(@usr_str, '*', @table0, 'ALL');
			END IF;


			IF @usr_str <> '' AND @schema0 <> '' AND @schema0 <> 'admin' THEN
				SET done0 := false;
				BEGIN
					DECLARE priv VARCHAR(60);
					DECLARE col_cur0 CURSOR FOR SELECT COLUMN_NAME FROM information_schema.`COLUMNS` WHERE TABLE_SCHEMA = 'qy_data' AND TABLE_NAME = 'auth_tbl';
					DECLARE CONTINUE HANDLER FOR NOT found set done0 = true;
					OPEN col_cur0;
					read_loop0:LOOP
						FETCH col_cur0 INTO priv;

							IF done0 THEN
								LEAVE read_loop0;
							END IF;

							# 部分权限的书写格式需要转化一下
							CASE priv
							WHEN "Create_tmp_table_priv" THEN SET priv := "create_temporary_tables_priv";
							WHEN "Grant_priv" THEN SET priv := ""; -- 默认不授予grant权限，因为用户自己授权之后，下次洗盘时又得重新授权
							ELSE SET priv := priv;
							END CASE;

							IF INSTR(priv, '_priv') > 1 THEN --排除不是权限的字段
								SET @v0 := JSON_UNQUOTE(JSON_EXTRACT(s0, CONCAT('$.', priv)));
								INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('usr_shuffle', 'priv', CONCAT(priv), NOW());
								INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('usr_shuffle', 's0', CONCAT(s0), NOW());
								INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('usr_shuffle', 'json_path', CONCAT('$.', priv), NOW());
								INSERT INTO pdb_usr_lyb.PROC_LOG VALUES('usr_shuffle', 'v0', @v0, NOW());

								IF @v0 = 'Y' THEN --只有填写Y的时候，才会授权
								  # 调整priv的格式
								  SET priv := REPLACE(priv, '_priv', '');
									SET priv := REPLACE(priv, '_', ' ');

									IF @usr_str = '*' THEN
										CALL grant_all_users(@schema0, @table0, priv);
									ELSE
										CALL grant_user(@usr_str, @schema0, @table0, priv);
									END IF;

-- 									SET done0 := true;

								END IF;

							END IF;

					END LOOP;
					CLOSE col_cur0;
				END;

-- 				SET done := true;
			END IF;
	END LOOP;
	CLOSE json_cur;
	DROP TABLE IF EXISTS temp; --删除临时表
	FLUSH PRIVILEGES;
END $$
DELIMITER ;

CALL usr_shuffle();

# 删除以上建立的所有存储过程
DROP PROCEDURE create_schema;
DROP PROCEDURE create_usr;
DROP PROCEDURE grant_all_users;
DROP PROCEDURE grant_user;
DROP PROCEDURE init_users;
DROP PROCEDURE usr_shuffle;
