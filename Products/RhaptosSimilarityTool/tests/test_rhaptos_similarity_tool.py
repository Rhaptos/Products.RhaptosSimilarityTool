#------------------------------------------------------------------------------#
#   test_rhaptos_similarity_tool.py                                            #
#                                                                              #
#       Authors:                                                               #
#       Rajiv Bakulesh Shah <raj@enfoldsystems.com>                            #
#                                                                              #
#           Copyright (c) 2009, Enfold Systems, Inc.                           #
#           All rights reserved.                                               #
#                                                                              #
#               This software is licensed under the Terms and Conditions       #
#               contained within the "LICENSE.txt" file that accompanied       #
#               this software.  Any inquiries concerning the scope or          #
#               enforceability of the license should be addressed to:          #
#                                                                              #
#                   Enfold Systems, Inc.                                       #
#                   4617 Montrose Blvd., Suite C215                            #
#                   Houston, Texas 77006 USA                                   #
#                   p. +1 713.942.2377 | f. +1 832.201.8856                    #
#                   www.enfoldsystems.com                                      #
#                   info@enfoldsystems.com                                     #
#------------------------------------------------------------------------------#
"""Unit tests.
$Id: $
"""


from Products.RhaptosTest import config
import Products.RhaptosSimilarityTool
config.products_to_load_zcml = [('configure.zcml', Products.RhaptosSimilarityTool),]
config.products_to_install = ['RhaptosSimilarityTool']
config.extension_profiles = ['Products.RhaptosSimilarityTool:default']

from Products.CMFCore.utils import getToolByName
from Products.RhaptosTest import base


class TestRhaptosSimilarityTool(base.RhaptosTestCase):

    def afterSetUp(self):
#        self.addProfile('Products.RhaptosSimilarityTool:default')
#        self.similarity_tool = getToolByName(self.portal, 'portal_similarity')
        pass

    def beforeTearDown(self):
        pass

    def test_similarity_tool(self):
        self.assertEqual(1, 1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRhaptosSimilarityTool))
    return suite
