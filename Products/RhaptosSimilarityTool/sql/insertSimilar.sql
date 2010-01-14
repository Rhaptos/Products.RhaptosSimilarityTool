<dtml-comment>
arguments: objectId version similar
</dtml-comment>


INSERT INTO similarities (objectId, version, sims) VALUES 
(
   <dtml-sqlvar objectId type="string">,
   <dtml-sqlvar version type="string">,
   ARRAY [ <dtml-var expr="'ARRAY ' + ',ARRAY '.join([str(list([str(x) for x in s])) for s in similar])"> ]
)
