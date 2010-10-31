"""
Tool for finding Rhaptos objects that are similar

Author: Brent Hendricks and Ross Reedstrom
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from zope.interface import implements

import zLOG
import AccessControl
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore.permissions import View, ManagePortal
from Products.RhaptosModuleStorage.ZSQLFile import ZSQLFile
from Products.ZCTextIndex.ParseTree import ParseError

from interfaces.portal_similarity import portal_similarity as ISimilarityTool


class SimilarityError(Exception):
    pass

class SimilarityTool(UniqueObject, SimpleItem):

    implements(ISimilarityTool)

    id = 'portal_similarity'
    meta_type = 'Similarity Tool'
    security = AccessControl.ClassSecurityInfo()

    sqlInsertSimilar = ZSQLFile('sql/insertSimilar', globals(), __name__='sqlInsertSimilar')
    sqlDeleteSimilar = ZSQLFile('sql/deleteSimilar', globals(), __name__='sqlDeleteSimilar')
    sqlInsertSimilarList = ZSQLFile('sql/insertSimilarList', globals(), __name__='sqlInsertSimilarList')
    sqlGetSimilar = ZSQLFile('sql/getSimilar', globals(), __name__='sqlGetSimilar')
    sqlGetSimilarList = ZSQLFile('sql/getSimilarList', globals(), __name__='sqlGetSimilarList')
    sqlUpdateSimilarList = ZSQLFile('sql/updateSimilarList', globals(), __name__='sqlUpdateSimilarList')
    sqlCalcSimilarityByModule = ZSQLFile('sql/calcSimilarityByModule', globals(), __name__='sqlCalcSimilarityByModule')
    sqlCalcSimilarityByMetadata = ZSQLFile('sql/calcSimilarityByMetadata', globals(), __name__='sqlCalcSimilarityByMetadata')


    manage_options=(( {'label':'Overview', 'action':'manage_overview'},
                      {'label':'Configure', 'action':'manage_configure'},
                      )
                    + SimpleItem.manage_options
                    )

    ##   ZMI methods
    security.declareProtected(ManagePortal, 'manage_overview')
    manage_overview = PageTemplateFile('zpt/explainSimilarityTool', globals() )

    security.declareProtected(ManagePortal, 'manage_configure')
    manage_configure = PageTemplateFile('zpt/editSimilarityTool', globals() )

    def __init__(self, db=None):
        self.db = db

    def manage_afterAdd(self, object, container):
        if not self.db:
            # Default to first SQL connection we find if none specified
            try:
                self.db = container.SQLConnectionIDs()[0][0]
            except IndexError:
                raise Exception, "No SQL Database connections found"
                 
    security.declareProtected(ManagePortal, 'manage_editSimilarityTool')
    def manage_editSimilarityTool(self, connection, REQUEST=None):
        """Edit the SimilarityTool parameters"""

        self.db = connection
        
        if REQUEST:
            return self.manage_configure(manage_tabs_message="SimilarityTool updated")

    # ISimilarityTool Interface fulfillment 
    def getSimilarContent(self, object, threshold=0, repository=None):
        """Return a list of  content that is 'similar' to the given object"""

        try:
            if repository:
                return self.sqlGetSimilar(objectId=object.objectId, version=object.version)[0].simobjs(repository)
            else:
                return self.sqlGetSimilar(objectId=object.objectId, version=object.version)[0].similarities()
        except IndexError:
            return []


    def storeSimilarity(self, object):
        """Calculate and store similarity for the specified object"""
        import os
        from Globals import package_home

        cmd =  os.path.join(INSTANCE_HOME, 'bin', 'zopectl')
        script = os.path.join(package_home(globals()), 'Extensions', 'storeSimilarity.py')
        os.spawnlp(os.P_NOWAIT, cmd, 'zopectl', 'run', script, object.objectId, object.version)

        
    def _storeSimilarity(self, object, replace=False):
        """Calculate and store similarity for the specified object"""

        # What is this object similar to
        similarities = self._calculateSimilarity(object)

        # Delete similarites to older versions of this object
        if similarities:
            # Filter out older versions
            filtered = []
            for objectId, versions in similarities.items():
                latest = reduce(lambda x, y: (x.revised > y.revised) and x or y, versions.values() )
                filtered.append( (objectId, latest.version, int(latest.weight)) )
            # Sort by weight
            filtered.sort(lambda x,y: cmp(y[2], x[2]))

            if replace:
                self.sqlUpdateSimilarList(similar=[(object.objectId, object.version, filtered)])
            else:
                self.sqlInsertSimilar(objectId=object.objectId, version=object.version, similar=filtered)

            # Now get similar content and update their references to this one
            others = self.sqlGetSimilarList(objects=similarities)
            for r in others:
                sim = r.similarities()
                weight = int(similarities[r.objectId][r.version].weight)

                # Replace the similarity to this object with the new version and weight
                for index in range(len(sim)):
                    if sim[index][0] == object.objectId:
                        sim[index] = (object.objectId, object.version, weight)
                        break
                else:
                    # The other object didn't use to be similar.  Now it is
                    sim.append( (object.objectId, object.version, weight) )

                # Re-sort on weight since we've changed one
                sim.sort(lambda x,y: cmp(y[2], x[2]))
                # Store this update in the DB
                self.sqlUpdateSimilarList(similar=[(r.objectId, r.version, sim)])

                # Flag this one as "done" by removing it from similarities
                del similarities[r.objectId][r.version]

            # Handle other objects that didn't use to be similar to
            # anything: if there are any entries left in 'similarities'
            # (not in others), they need to be inserted
            for objectId, versions in similarities.items():
                for version, o in versions.items():
                    self.sqlInsertSimilar(objectId=objectId,version=version,similar =  [(object.objectId, object.version, int(o.weight))])
            
    def deleteSimilarity(self, objectId,version=None):
        """Delete similarity for the specified object"""
        #do this all in the SQL now
        if version:
            self.sqlDeleteSimilar(objectId=objectId,version=version)
        else:
            self.sqlDeleteSimilar(objectId=objectId)


    def _calculateSimilarity(self, object):
        results = self._getModuleSimilarity(object)
        results.update(self._getCourseSimilarity(object))

        return results


    def _getModuleSimilarity(self, object):

        if object.portal_type == 'Module':
            results = self.sqlCalcSimilarityByModule(objectId=object.objectId, version=object.version)
        else:
            kw,uncook = self.content.module_version_storage.cookSearchTerms(object.keywords)
            title,uncook = self.content.module_version_storage.cookSearchTerms([object.Title()])
            results = self.sqlCalcSimilarityByMetadata(keywords=kw, title=title)

        sim = {}
        for r in results:
            sim.setdefault(r.objectId, {})[r.version] = r

        return sim


    def _getCourseSimilarity(self, object):

        forward = self._forwardCourseSimilarity(object)
        reverse = self._reverseCourseSimilarity(object)

        # Combine forward and reverse similarity lookups
        courses = forward
        for objectId, versions in reverse.items():
            for version, ob in versions.items():
                r = courses.setdefault(objectId, {})
                try:
                    r[version].weight += ob.weight
                except KeyError:
                    r[version] = ob

        return courses
                             

    def _forwardCourseSimilarity(self, object):
        """Find courses that match the object's keywords"""

        catalog = self.content.catalog
        courses = {}

        query,uncook = self.content.version_folder_storage.cookSearchTerms(object.keywords)
        for w in query:
            #cs = catalog(abstract=w)
            #for c in cs:
            #    c.weight = 0
            #    courses.setdefault(c.objectId, {}).setdefault(c.version, c).weight += 1

            cs = catalog(keywords=w, portal_type='Collection')
            for c in cs:
                c.weight = 0                
                courses.setdefault(c.objectId, {}).setdefault(c.version, c).weight += 10

            cs = catalog(Title='"'+w+'"', portal_type='Collection')
            for c in cs:
                c.weight = 0
                courses.setdefault(c.objectId, {}).setdefault(c.version, c).weight += 100

        # Filter out courses with the same id
        try:
            del courses[object.objectId]
        except KeyError:
            pass

        return courses


    def _reverseCourseSimilarity(self, object):
        """Find courses whose keywords match the object"""
        
        catalog = self.content.catalog
        courses = {}

        if object.portal_type == 'Module':
            query,uncook = self.content.version_folder_storage.cookSearchTerms(object.SearchableText().split())
            for w in query:
                for c in catalog(keywords=w, portal_type='Collection'):
                    c.weight = 0                
                    courses.setdefault(c.objectId, {}).setdefault(c.version, c).weight += 1

            # Filter out courses with a score of only 1
            for id, versions in courses.items():
                for v, ob in versions.items():
                    if ob.weight <= 1:
                        del versions[v]
                if not len(versions):
                    del courses[id]

        #for w in object.abstract.split():
        #    for c in catalog(keywords=w):
        #        c.weight = 0                
        #        courses.setdefault(c.objectId, {}).setdefault(c.version, c).weight += 1

        query,uncook = self.content.version_folder_storage.cookSearchTerms(object.keywords)
        for w in query:
            cs = catalog(keywords=w, portal_type='Collection')
            for c in cs:
                c.weight = 0                
                courses.setdefault(c.objectId, {}).setdefault(c.version, c).weight += 10

        query,uncook = self.content.version_folder_storage.cookSearchTerms(object.Title().split())
        for w in query:
            cs = catalog(keywords=w, portal_type='Collection')
            for c in cs:
                c.weight = 0                
                courses.setdefault(c.objectId, {}).setdefault(c.version, c).weight += 100

        # Filter out courses with the same id
        try:
            del courses[object.objectId]
        except KeyError:
            pass

        return courses
    

                
InitializeClass(SimilarityTool)


# Convenience functions

