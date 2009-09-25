from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
import string

def install(self):
    """Add the tool"""
    out = StringIO()

    # Add the tool
    urltool = getToolByName(self, 'portal_url')
    portal = urltool.getPortalObject();
    try:
        portal.manage_delObjects('portal_similarity')
        out.write("Removed old portal_similarity tool\n")
    except:
        pass  # we don't care if it fails
    portal.manage_addProduct['RhaptosSimilarityTool'].manage_addTool('Similarity Tool', None)

    # Register skins
    
    
    out.write("Adding Similarity Tool\n")

    return out.getvalue()
