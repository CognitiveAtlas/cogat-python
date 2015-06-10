#!/usr/bin/env python

"""

brainspell: part of the cognitive atlas package

functions for working with brainspell.org


"""

import os
import json
import string
import urllib
import urllib2
import numpy as np
import pandas as pd
import nibabel as nb
import numpy as np
from utils import DataJson

__author__ = ["Poldracklab","Vanessa Sochat"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2015/01/23 $"
__license__ = "BSD"

def get_article(pmid):
   """Get brainspell article"""
   try:
     return DataJson("http://brainspell.org/json/pmid/%s" %(pmid))
   except:
     print "ERROR %s is not in the brainspell database!" %(pmid) 

def article_from_json(file_path):
   """Read in from json directly"""
   
