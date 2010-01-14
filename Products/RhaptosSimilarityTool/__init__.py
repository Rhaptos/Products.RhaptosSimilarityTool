"""
Initialize RhaptosSimilarityTool Product

Author: Brent Hendricks and Ross Reedstrom
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

import sys
from Products.CMFCore import utils
import SimilarityTool

this_module = sys.modules[ __name__ ]
product_globals = globals()
tools = ( SimilarityTool.SimilarityTool,)

def initialize(context):
    utils.ToolInit('Similarity Tool',
                    tools = tools,
                    product_name = 'RhaptosSimilarityTool',
                    icon='tool.gif' 
                    ).initialize( context )
