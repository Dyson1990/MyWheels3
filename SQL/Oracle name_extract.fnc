create or replace function name_extract(s0 in VARCHAR2) return varchar2 as
  s varchar2(3000);
  m varchar2(3000);
begin
    /*  0069c673efce12c584ab31c66fba8592
      |有张保成变为张长河担任。|由张长河变为韦太岳*/
    --s = dbms_lob.fileisopen(s, SIMPLIFIED CHINESE_CHINA.UTF8);
    --s := convert(s0, 'SIMPLIFIED CHINESE_CHINA.UTF8'); --, 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
    s := REGEXP_REPLACE(s0, '(；|;|：|:)', ' ');
    m := REGEXP_SUBSTR(s, '(姓\s*?名\s*?\S+\s*?)+');
    IF m IS NOT NULL THEN
      s := m;
    END IF;
    --s := REGEXP_SUBSTR(s, '负\s*?责\s*?人\s*?\S+\s*?|.+'); --负责人
    m := REGEXP_SUBSTR(s, '(负\s*?责\s*?人\s*?\S+\s*?)+');
    IF m IS NOT NULL THEN
      s := m;
    END IF;
    --s := REGEXP_SUBSTR(s, '法定代表人\s*?\S+?\s*?|.+');--法定代表人
    m := REGEXP_SUBSTR(s, '(法定代表人\s*?\S+\s*?)+');
    IF m IS NOT NULL THEN
      s := m;
    END IF;
    
    
    s := REGEXP_REPLACE(s, '((姓名)|(负责人)|(法定代表人)|【变更后内容】|\s|\d)+', '');
    RETURN s;
  return(s);
end name_extract;
/
