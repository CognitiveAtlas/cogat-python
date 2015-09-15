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
get_task_lookup: return lookup table contrast by task id

id - Return the specified Task.
[no parameters] - Return lookup with all Tasks.

"""
def get_task_lookup(task_id=None):
    if not task_id:
        tasks = get_task().json
    else:
        tasks = list()
        if isinstance(task_id,str):
            task_id = [task_id]
        for id in task_id:
            tasks.append(get_task(id=id).json[0])
    task_ids = [task["id"] for task in tasks]
    task_lookup = dict()
    for task in tasks:
        task_details = get_task(id=task["id"])
        if task_details.json[0]["contrasts"]:   
            task_lookup[task["id"]] = task_details.json[0]["contrasts"]
        else:
            task_lookup[task["id"]] = []
    return task_lookup


"""
get_contrast_lookup: return lookup table task id by contrast

id - Return the specified Task.
[no parameters] - Return lookup with all Tasks.

"""
def get_contrast_lookup(task_id=None):
    task_lookup = get_task_lookup(task_id)
    contrast_lookup = dict()
    for task,contrasts in task_lookup.iteritems():
        for contrast in contrasts:
            contrast_lookup[contrast["id"]] = task        
    return contrast_lookup


"""Match tasks and conditions and put into a data frame based on match columns.
Tasks: seem to have tsk and trm ids, but they are unique.
""" 
def merge_df(left,right,join_column):
  return pandas.merge(left,right, on=join_column, how='right')

def filter_result(triples_df,filters,column_id):
  if isinstance(filters,str): filters = [filters]  
  return triples_df[triples_df[column_id].isin(filters)] 
