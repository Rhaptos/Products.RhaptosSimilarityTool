from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from DateTime import DateTime
import string
from ZODB.Transaction import get_transaction

def recalc(self):
    """Upgrade the installed tool"""
    out = StringIO()

    # get the tool
    sim = getToolByName(self, 'portal_similarity')

    #get All objects
    objs=self.content.searchRepositoryByDate(DateTime(1970,1,1), end=DateTime(2010,1,1))
    
    num = len(objs)
    print "%s objects" % num
    for n,o in zip(range(len(objs)),objs):
        print 'Recalc sim for %(objectId)s(%(version)s)' % o
	sim.deleteSimilarity(o.objectId,o.version)
	sim._storeSimilarity(self.content.getRhaptosObject(o.objectId)[o.version])
	if not(n%10):
          get_transaction().commit()
	  print "%s%% done" % ((n*100.0)/num)

    get_transaction().commit()
    out.write("Recalc Similarities Complete\n")

    return out.getvalue()

if __name__ == '__main__':
    recalc(app.plone)
