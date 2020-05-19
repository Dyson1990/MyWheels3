SELECT 
  DISTINCT(ENTID)
  --, ALTAF0
  , LAST_VALUE(ALTAF) over(PARTITION BY ENTID ORDER BY length(ALTAF) ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) ALTAF
FROM
(
  SELECT 
      ENTID
      ,ALTAF0
      ,sys_connect_by_path(ALTAF,'|') ALTAF
  FROM
  (
         SELECT 
             ENTID
             ,ALTAF
             ,ALTAF0
             ,ENTID||rn rchild
             ,ENTID||(rn-1) rfather
         FROM
         (
             SELECT 
                 cdb_nov.f_qy_bg.ENTID ENTID
                 ,to_char(cdb_nov.f_qy_bg.ALTAF) ALTAF0
                 ,name_extract(to_char(cdb_nov.f_qy_bg.ALTAF)) ALTAF
                 ,row_number() over (PARTITION BY cdb_nov.f_qy_bg.ENTID ORDER BY to_char(cdb_nov.f_qy_bg.ALTAF)) rn 
             FROM cdb_nov.f_qy_bg
             WHERE ALTITEM = '03' AND ALTDATE < to_date('2001-01-01 00:00:00','yyyy-mm-dd hh24:mi:ss') --AND ENTID = '02c477d8ec2daf2727555ebcd1de0a54'   
         )
     )
  CONNECT BY PRIOR rchild=rfather START WITH rfather LIKE '%0'
)
--GROUP BY ENTID; 
