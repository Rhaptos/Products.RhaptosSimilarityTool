<dtml-comment>
arguments: objectId version
max_rows: 0
class_file: RhaptosSimilarityTool.SimData.py
class_name: SimData
cache_time: 60
max_cache:  100
</dtml-comment>

SELECT objectId AS "objectId", version, sims FROM similarities WHERE
   <dtml-sqltest objectId type="string"> AND
   <dtml-sqltest version type="string">
;
