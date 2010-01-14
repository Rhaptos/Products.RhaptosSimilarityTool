<dtml-comment>
arguments: objectId version
max_rows: 0
</dtml-comment>

select moduleid as "objectId", version, revised, sum(weight) as weight from (
select mk.module_ident, count(*) as weight
from modulefti mf, keywords k, modulekeywords mk, modules m
where
<dtml-sqltest objectId column="m.moduleid" type="string"> and
<dtml-sqltest version column="m.version" type="string"> and
mf.module_ident = m.module_ident and
mk.keywordid=k.keywordid and
module_idx @@ plainto_tsquery(word)
group by mk.module_ident
having count(*) > 1

UNION ALL
select mk.module_ident, count(*)*20 as weight from  
modulekeywords mk, modulekeywords mk2 , modules m
where 
<dtml-sqltest objectId column="m.moduleid" type="string"> and
<dtml-sqltest version column="m.version" type="string"> and
mk2.module_ident = m.module_ident and
mk.keywordid = mk2.keywordid 
group by mk.module_ident

UNION ALL
select mk.module_ident, count(*)*100 as weight from 
keywords k, modules m, modulekeywords mk
where 
k.keywordid = mk.keywordid and 
m.name ~* ('\\y'||re_quote(word)||'\\y') and 
<dtml-sqltest objectId column="m.moduleid" type="string"> and
<dtml-sqltest version column="m.version" type="string">
group by mk.module_ident 

UNION ALL
select mf.module_ident, count(*) as weight
from modulefti mf, keywords k, modulekeywords mk, modules m
where
<dtml-sqltest objectId column="m.moduleid" type="string"> and
<dtml-sqltest version column="m.version" type="string"> and
mk.module_ident = m.module_ident and
mk.keywordid=k.keywordid and
module_idx @@ plainto_tsquery(word)
group by mf.module_ident
having count(*) > 1

UNION ALL
select m2.module_ident, count(*)*100 as weight from 
keywords k, modules m, modulekeywords mk, modules m2
where 
<dtml-sqltest objectId column="m.moduleid" type="string"> and
<dtml-sqltest version column="m.version" type="string"> and
mk.module_ident = m.module_ident and
k.keywordid = mk.keywordid and 
m2.name ~* ('\\y'||re_quote(word)||'\\y') 
group by m2.module_ident 

) matched natural join modules
where <dtml-sqltest objectId op="<>" column="moduleid" type="string"> 
group by moduleid,version,revised;
