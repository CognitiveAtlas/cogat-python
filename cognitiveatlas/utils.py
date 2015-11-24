#!/usr/bin/env python

"""

utils: part of the cognitive atlas package

functions for working with the cognitive atlas!


"""

import os
import json
import errno
import pandas
import urllib2
from urllib2 import Request, urlopen, HTTPError

# File operations 
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def get_url(url):
    request = Request(url)
    response = urlopen(request)
    return response.read()

# Data Json (from file)
def read_json_file(file_path):
    filey = read_text_file(file_path)
    return json.loads(filey)

# Text (from file)
def read_text_file(file_path):
    filey = open(file_path,'rb')
    tmp = filey.readlines()
    filey.close()
    return "\n".join(tmp)

# Get raw json object
def get_json(url):
    return urllib2.urlopen(url).read()

# Convert json to pandas data frame
def get_df(myjson):
    try:
        df = pandas.DataFrame(myjson)
    except:
        df = []
    return df

# Load a json object
def parse_json(myjson):
    return json.loads(myjson)

# Data Json Object (from URL)
class DataJson:
  """DataJson: internal class for storing json, accessed by NeuroVault Object"""
  def __init__(self,url):
    print url
    self.url = url
    self.txt = get_json(url)
    self.json = parse_json(self.txt) 
    self.pandas = get_df(self.json)
    
  """Print json data fields"""
  def __str__(self):
    return "Result Includes:<pandas:data frame><json:dict><txt:str><url:str>"
