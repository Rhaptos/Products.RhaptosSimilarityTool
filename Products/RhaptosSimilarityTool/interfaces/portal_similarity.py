# Copyright (c) 2004 The Connexions Project, All Rights Reserved
# Written by Brent Hendricks

""" File system import interface"""

from Interface import Attribute
try:
    from Interface import Interface
except ImportError:
    # for Zope versions before 2.6.0
    from Interface import Similarity as Interface

class portal_similarity(Interface):
    """Defines an interface for a tool that measures and stores
       'similarity' between content objects in the RhaptosRepository"""

    id = Attribute('id','Must be set to "portal_similarity"')

    def getSimilarContent(object):
        """
        Find content that is 'similar' to the given object
        
        Returns a list of (content, score) tuples where content is
        the similar object, score is some measure of similarity.
        The list will be sorted in order of descending score.
        """

    def storeSimilarity(object):
        """Calculate and store similarity for the specified object"""

    def deleteSimilarity(objectId, version):
        """Delete similarity for the specified object id, one or all versions"""

