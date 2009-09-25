<dtml-comment>
arguments: objects
class_file: RhaptosSimilarityTool.SimData.py
class_name: SimData
max_rows: 0
</dtml-comment>

SELECT objectId AS "objectId", version, sims from similarities WHERE
<dtml-in expr="objects.items()" prefix="o">
   <dtml-in expr="o_item.items()" prefix="v"> 
    <dtml-unless expr="o_start and v_start">OR</dtml-unless> 
   (
    <dtml-sqltest o_key column="objectId" type="string" > AND
    <dtml-sqltest v_key column="version" type="string" >
   ) 
   </dtml-in>
</dtml-in>
;
