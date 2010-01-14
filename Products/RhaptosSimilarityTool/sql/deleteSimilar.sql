<dtml-comment>
arguments: objectId version 
</dtml-comment>

UPDATE similarities SET sims = 
sims[1:array_position(sims[1:array_upper(sims,1)][1:1],
ARRAY[<dtml-sqlvar objectId type="string">]::text[])-1] ||
sims[array_position(sims[1:array_upper(sims,1)][1:1],
ARRAY[<dtml-sqlvar objectId type="string">]::text[])+1:array_upper(sims,1)] 
<dtml-if version>
where array_position(sims[1:array_upper(sims,1)][1:2],
ARRAY[<dtml-sqlvar objectId type="string">,<dtml-sqlvar version type="string">]::text[]) is not null
<dtml-else>
where <dtml-sqlvar objectId type="string"> = any (sims[1:array_upper(sims,1)][1:1])
</dtml-if>
;
DELETE from similarities where
<dtml-sqlgroup>
<dtml-sqltest objectId column="objectid" type="string">
<dtml-and>
<dtml-sqltest version column="version" type="string" optional>
</dtml-sqlgroup>
;
DELETE from similarities where sims is null;
