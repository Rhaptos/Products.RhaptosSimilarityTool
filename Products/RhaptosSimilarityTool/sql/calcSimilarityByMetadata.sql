<dtml-comment>
arguments: keywords title
max_rows: 0
</dtml-comment>

select moduleid as "objectId", version, revised, sum(weight) as weight from (

<dtml-if keywords>
select mf.module_ident, count(*) as weight
from (
<dtml-in keywords>
<dtml-unless sequence-start>union all </dtml-unless>
select mf.module_ident
from
modulefti mf
where
module_idx @@ plainto_tsquery(<dtml-sqlvar sequence-item type="string">)
</dtml-in>
) mf
group by mf.module_ident
having count(*) > 1

UNION ALL
select mk.module_ident, count(*)*20 as weight from  
(
<dtml-in keywords>
<dtml-unless sequence-start>union all </dtml-unless>
select mk.module_ident from  
modulekeywords mk, keywords k, modules m
where 
mk.module_ident = m.module_ident and
mk.keywordid = k.keywordid  and
k.word = <dtml-sqlvar sequence-item type="string">
</dtml-in>
) mk
group by mk.module_ident

UNION ALL
select mk.module_ident, count(*)*100 as weight from 
( 
<dtml-in keywords>
<dtml-unless sequence-start>union all </dtml-unless>
select module_ident from
modules m
where 
m.name ~* ('\\y'||re_quote(<dtml-sqlvar sequence-item type="string">)||'\\y')
</dtml-in>
) mk
group by mk.module_ident 

UNION ALL
</dtml-if>

select mk.module_ident, count(*)*100 as weight from 
keywords k, modulekeywords mk
where 
k.keywordid = mk.keywordid and <dtml-sqlvar title type=string> ~* ('\\y'||re_quote(k.word)||'\\y')
group by mk.module_ident 

) matched natural join modules
group by moduleid,version,revised;
