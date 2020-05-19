create or replace function name_extract(s0 in VARCHAR2) return varchar2 as
  s varchar2(3000);
  m varchar2(3000);
begin
    /*  0069c673efce12c584ab31c66fba8592
      |���ű��ɱ�Ϊ�ų��ӵ��Ρ�|���ų��ӱ�ΪΤ̫��*/
    --s = dbms_lob.fileisopen(s, SIMPLIFIED CHINESE_CHINA.UTF8);
    --s := convert(s0, 'SIMPLIFIED CHINESE_CHINA.UTF8'); --, 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
    s := REGEXP_REPLACE(s0, '(��|;|��|:)', ' ');
    m := REGEXP_SUBSTR(s, '(��\s*?��\s*?\S+\s*?)+');
    IF m IS NOT NULL THEN
      s := m;
    END IF;
    --s := REGEXP_SUBSTR(s, '��\s*?��\s*?��\s*?\S+\s*?|.+'); --������
    m := REGEXP_SUBSTR(s, '(��\s*?��\s*?��\s*?\S+\s*?)+');
    IF m IS NOT NULL THEN
      s := m;
    END IF;
    --s := REGEXP_SUBSTR(s, '����������\s*?\S+?\s*?|.+');--����������
    m := REGEXP_SUBSTR(s, '(����������\s*?\S+\s*?)+');
    IF m IS NOT NULL THEN
      s := m;
    END IF;
    
    
    s := REGEXP_REPLACE(s, '((����)|(������)|(����������)|����������ݡ�|\s|\d)+', '');
    RETURN s;
  return(s);
end name_extract;
/
