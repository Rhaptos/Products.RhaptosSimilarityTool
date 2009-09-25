from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
import string

def upgrade(self):
    """Upgrade the installed tool"""
    out = StringIO()

    # get the tool
    sim = getToolByName(self, 'portal_similarity')
    db=getattr(self,sim.db)
    db.manage_test(query="""CREATE OR REPLACE FUNCTION array_position (ANYARRAY, ANYELEMENT)
RETURNS INTEGER
IMMUTABLE STRICT
LANGUAGE PLPGSQL
AS '
BEGIN
  for i in array_lower($1,1) .. array_upper($1,1)
  LOOP
    IF ($1[i] = $2)
    THEN
      RETURN i;
    END IF;
  END LOOP;
  RETURN NULL;
END;
';""")

    db.manage_test(query="""CREATE OR REPLACE FUNCTION array_position (ANYARRAY, ANYARRAY)
RETURNS INTEGER
IMMUTABLE STRICT
LANGUAGE PLPGSQL
AS '
BEGIN
  for i in array_lower($1,1) .. array_upper($1,1)
  LOOP
    IF ($1[i:i] = $2)
    THEN
      RETURN i;
    END IF;
  END LOOP;
  RETURN NULL;
END;
';
""")

    out.write("Upgrading Similarity Tool\n")

    return out.getvalue()
