# 参考资料 https://www.cnblogs.com/gongchenglion/articles/11629236.html

# 创建两张表，一张为内存表，一张为正式表,内存表主要放存储过程生成的随机数据，正式表再用查询插入从内存表中获取数据。
DROP TABLE IF EXISTS `vote_record`;
CREATE TABLE `vote_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(20) NOT NULL,
  `vote_id` int NOT NULL,
  `group_id` int NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_user_id` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS `vote_record_memory`;
CREATE TABLE `vote_record_memory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(20) NOT NULL,
  `vote_id` int NOT NULL,
  `group_id` int NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_user_id` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

DROP FUNCTION IF EXISTS `rand_string`;
DELIMITER $$
CREATE DEFINER=`Dyson`@`%` FUNCTION `rand_string`(n INT) RETURNS varchar(255) CHARSET utf8mb4
    DETERMINISTIC
BEGIN
    DECLARE chars_str varchar(100) DEFAULT 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    DECLARE return_str varchar(255) DEFAULT '' ;
    DECLARE i INT DEFAULT 0;
    WHILE i < n DO
        SET return_str = concat(return_str, substring(chars_str, FLOOR(1 + RAND() * 62), 1));
        SET i = i + 1;
    END WHILE;
    RETURN return_str;
END
DELIMITER ;

DROP PROCEDURE IF EXISTS `add_vote_memory`;
DELIMITER $$
CREATE DEFINER=`Dyson`@`%` PROCEDURE `add_vote_memory`(IN n int)
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE (i <= n) DO
        INSERT INTO vote_record_memory (user_id, vote_id, group_id, create_time) VALUES (rand_string(20), FLOOR(RAND() * 1000), FLOOR(RAND() * 100), NOW());
        SET i = i + 1;
    END WHILE;
END
DELIMITER ;

CALL add_vote_memory(1000000);
