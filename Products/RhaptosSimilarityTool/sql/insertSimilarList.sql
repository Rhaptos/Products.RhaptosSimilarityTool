<dtml-comment>
arguments: similar
</dtml-comment>


<dtml-in similar prefix="s">
   INSERT INTO similarities (objectId, version, sims) VALUES 
   (
     <dtml-sqlvar expr="s_item[0]" type="string">,
     <dtml-sqlvar expr="s_item[1]" type="string">,
     ARRAY [ ARRAY <dtml-var expr="str([str(x) for x in s_item[2]])"> ] 
   )
;
</dtml-in>
