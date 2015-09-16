#!/usr/bin/env python

"""

api: part of the cognitive atlas package

functions for working with the cognitive atlas!


"""
from cognitiveatlas.utils import DataJson
import cognitiveatlas.utils
import numpy as np
import urllib2
import string
import urllib
import pandas
import json
import os

__author__ = ["Poldracklab","Vanessa Sochat"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2015/01/23 $"
__license__ = "BSD"

  
apiversion = "v-alpha"

# Wrapper for the "search" query
"""
search: Search Concepts, Theories, Assertions, Tasks, Task Batteries, and Disorders for a given keyword.

query: the query to search for that will go across concepts, theories, tasks, and disorders.

"""
def search(query):
    result = DataJson("http://cognitiveatlas.org/api/%s/search?q=%s" %(apiversion,query.replace(" ","%20")))
    print result
    return result



"""
concept: return one or more concepts

id - Return the specified Concept.
name - Return the specified Concept.
contrast_id - Return all Concepts related to the specified Contrast.
[no parameters] - Return all Concepts.

Example: http://cognitiveatlas.org/api/v-alpha/concept?id=trm_4a3fd79d096be

"""
def get_concept(id=None,name=None,contrast_id=None):
    base_url = "http://cognitiveatlas.org/api/%s/concept" %(apiversion)
    parameters = {"id":id,
                  "name":name,
                  "contrast_id":contrast_id}
    url = generate_url(base_url,parameters)
    result = DataJson(url)
    print result
    return result


"""
task: return one or more tasks

id - Return the specified Task.
name - Return the specified Task.
[no parameters] - Return all Tasks with basic information only.

"""
def get_task(id=None,name=None):
    base_url = "http://cognitiveatlas.org/api/%s/task" %(apiversion)
    parameters = {"id":id,
                  "name":name}
    url = generate_url(base_url,parameters)
    result = DataJson(url)
    print result
    return result


"""
disorder: return one or more disorders

id - Return the specified Disorder.
name - Return the specified Disorder.
[no parameters] - Return all Disorders.

"""
def get_disorder(id=None,name=None):
    base_url = "http://cognitiveatlas.org/api/%s/disorder" %(apiversion)
    parameters = {"id":id,
                  "name":name}
    url = generate_url(base_url,parameters)
    result = DataJson(url)
    print result
    return result



"""
Generate a complete url from a base and list of parameters

base_url: the base url (string)
parameters: a dictionary with the keys being the parameter, values being the values of the parameter. Any values of None will not be added to the url.

"""
def generate_url(base_url,parameters):
    values = [x.replace(" ","%20") for x in parameters.values() if x]
    keys = [key for key,val in parameters.iteritems() if val]
    arguments = ["%s=%s" %(keys[i],values[i]) for i in range(len(values))]
    arguments = "&".join(arguments)
    return "%s?%s" %(base_url,arguments)


"""
filter_concepts: return concepts json

contrast_id - concepts will be obtained for specified contrast_ids
concept_id - only return particular set of concepts
[no parameters] - Return lookup with all concepts

returns list of concepts

"""
def filter_concepts(concept_id=None,contrast_id=None):
    # We can only have either or
    if concept_id and contrast_id:
        raise ValueError('You can specify contrast_id or concept_id but not both!')

    # Get concepts by contrast ids
    if contrast_id:
        if isinstance(contrast_id,str):
            contrast_id = [contrast_id]
        concepts = []
        for contrast in contrast_id:
            concepts = concepts + get_concept(contrast_id=contrast).json

    # Get concepts by concept ids
    elif concept_id:
        concepts = []
        for concept in concept_id:
            concepts = concepts + get_concept(id=concept).json

    # Build entire tree
    else:
        concepts = get_concept().json

    return concepts
    


"""Match tasks and conditions and put into a data frame based on match columns.
Tasks: seem to have tsk and trm ids, but they are unique.
""" 
def merge_df(left,right,join_column):
  return pandas.merge(left,right, on=join_column, how='right')

def filter_result(triples_df,filters,column_id):
  if isinstance(filters,str): filters = [filters]  
  return triples_df[triples_df[column_id].isin(filters)] 
