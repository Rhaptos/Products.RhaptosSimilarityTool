<dtml-comment>
arguments: similar
</dtml-comment>


<dtml-in similar prefix="s">
   UPDATE similarities SET sims = ARRAY [ <dtml-var expr="'ARRAY ' + ',ARRAY '.join([str([str(x) for x in s]) for s in s_item[2]])"> ]
   WHERE 
     <dtml-sqltest expr="s_item[0]" column="objectId" type="string"> AND
     <dtml-sqltest expr="s_item[1]" column="version" type="string">
;
</dtml-in>
