#!/usr/bin/env python

"""

api: part of the cognitive atlas package

functions for working with the cognitive atlas!


"""
from cognitiveatlas.utils import DataJson
import cognitiveatlas.utils
import string
import pandas
import json
import os

__author__ = ["Poldracklab","Vanessa Sochat"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2015/01/23 $"
__license__ = "BSD"

  
apiversion = "v-alpha"

# Wrapper for the "search" query
def search(query,silent=False):
    '''search 
    Search Concepts, Theories, Assertions, Tasks, Task Batteries, and Disorders for a given keyword.

    :param query: str
        the query to search for that will go across concepts, theories, tasks, and disorders.

    '''

    result = DataJson("http://cognitiveatlas.org/api/%s/search?q=%s" %(apiversion,query.replace(" ","%20")),silent=silent)
    if not silent:
        print(result)
    return result



def get_concept(id=None,name=None,contrast_id=None,silent=False):
    '''get_concept
    return one or more concepts

    :param id: Return the specified Concept.
    :param name name: Return the specified Concept.
    :param contrast_id: Return all Concepts related to the specified Contrast.
    
    [no parameters] - Return all Concepts.

    :Example:

        http://cognitiveatlas.org/api/v-alpha/concept?id=trm_4a3fd79d096be

    '''

    base_url = "http://cognitiveatlas.org/api/%s/concept" %(apiversion)
    parameters = {"id":id,
                  "name":name,
                  "contrast_id":contrast_id}
    url = generate_url(base_url,parameters)
    result = DataJson(url,silent=silent)
    if not silent:
        print(result)
    return result


def get_task(id=None,name=None,silent=False):
    '''get_task
    return one or more tasks

    :param id: Return the specified Task.
    :param name name: Return the specified Task.
    
    [no parameters] - Return all Tasks with basic information only.

    :Example:

        http://cognitiveatlas.org/api/v-alpha/task?id=trm_4f244f46ebf58

    '''

    base_url = "http://cognitiveatlas.org/api/%s/task" %(apiversion)
    parameters = {"id":id,
                  "name":name}
    url = generate_url(base_url,parameters)
    result = DataJson(url,silent=silent)
    if not silent:
        print(result)
    return result


def get_disorder(id=None,name=None,silent=False):
    '''get_disorder
    return one or more disorders

    :param id: Return the specified Disorder.
    :param name name: Return the specified Disorder.
    
    [no parameters] - Return all Tasks with basic information only.

    '''

    base_url = "http://cognitiveatlas.org/api/%s/disorder" %(apiversion)
    parameters = {"id":id,
                  "name":name}
    url = generate_url(base_url,parameters)
    result = DataJson(url,silent=silent)
    if not silent:
        print(result)
    return result



def generate_url(base_url,parameters):
    '''
    Generate a complete url from a base and list of parameters

    :param base_url: the base url (string)
    :param parameters: a dictionary with the keys being the parameter, values being the values of the parameter. Any values of None will not be added to the url.

    '''

    values = [x.replace(" ","%20") for x in parameters.values() if x]
    #keys = [key for key,val in parameters.iteritems() if val]
    keys = [key for (key, value) in parameters.items() if value]
    arguments = ["%s=%s" %(keys[i],values[i]) for i in range(len(values))]
    arguments = "&".join(arguments)
    return "%s?%s" %(base_url,arguments)


def filter_concepts(concept_id=None,contrast_id=None):
    '''filter_concepts
    return concepts json

    :param contrast_id - concepts will be obtained for specified contrast_ids
    :param concept_id - only return particular set of concepts
    [no parameters] - Return lookup with all concepts

    returns list of concepts

    '''

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
    

def merge_df(left,right,join_column):
    '''Match tasks and conditions and put into a data frame based on match columns.
    '''
    return pandas.merge(left,right, on=join_column, how='right')

def filter_result(triples_df,filters,column_id):
    if isinstance(filters,str): filters = [filters]  
    return triples_df[triples_df[column_id].isin(filters)] 
