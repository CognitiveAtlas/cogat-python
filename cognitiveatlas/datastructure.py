#!/usr/bin/env python

"""

datastructure: part of the cognitive atlas package

functions for working with the cognitive atlas!


"""
from cognitiveatlas.api import get_contrast_lookup, filter_concepts, get_task_lookup, get_concept
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

# Functions to work with nodes

def make_node(node_id,name,parent,delim,file_obj):
    file_obj.writelines("%s%s%s%s%s\n" %(node_id,delim,parent,delim,name))
    if isinstance(node_id,int):
        node_id += 1
        return node_id

def init_output_file(output_file,delim="\t"):
    filey = open(output_file,"wb")
    filey.writelines("id%sparent%sname\n" %(delim,delim))
    filey.writelines("1%sNone%sBASE\n" %(delim,delim))
    return filey

"""
task_node_triples: Export a list of nodes, in triples, for a specified list of contrast ids.

contrast_ids: a list of contrast ids (e.g., ["cnt_4decfedb91973"])

OUTPUT:

  id    parent  name
  1 none BASE
  2 1   RESPONSE_INHIBITION
  3 1   RISK_SEEKING
  4 2   DS000009
  5 2   DS000008
  6 3   DS000001
  7 4   EXPLODE_4
  8 4   ACCEPT_4

"""

def task_node_triples(contrast_ids,output_file="task_node_triples.tsv",delim="\t"):
    if isinstance(contrast_ids,str):
        contrast_ids = [contrast_ids]
    contrast_lookup = get_contrast_lookup(contrast_id=contrast_ids)
    task_ids = np.unique(contrast_lookup.values()).tolist()
    task_lookup = get_task_lookup(task_id=task_ids)
    # Prepare output file
    filey = init_output_file(output_file,delim=delim)
    # Create nodes for unique tasks
    node_id = 2
    # Remember parent node ids based on taskid
    parents = dict()
    for task_id in task_ids:
        name = task_lookup[task_id]["name"]
        parents[task_id] = node_id
        node_id = make_node(node_id,name,1,delim,filey)
    # Now create a node for each contrast
    for contrast_id,task in contrast_lookup.iteritems():
        parent = parents[task]
        idx = [x for x in range(0,len(task_lookup[contrast_lookup[contrast_id]]["contrasts"])) if task_lookup[contrast_lookup[contrast_id]]["contrasts"][x]["id"] == contrast_id][0]
        name = task_lookup[contrast_lookup[contrast_id]]["contrasts"][idx]["contrast_text"]
        node_id = make_node(node_id,name,parent,delim,filey)
    filey.close()
    print "%s has been created." % output_file 


"""
concept_node_triples: Export a list of nodes, in triples

image_dict [OPTIONAL]: a dictionary of [contrast_id:image_file] pairs, eg:
                      
                           {"cnt_4decfedb91973":["image1.nii.gz","image2.nii.gz"]}

This will mean that the images in the list will be assigned to all concept nodes associated with the contrast specified. This allows for inference over the tree (for example, some relationship with concept nodes that are parents of assigned nodes) 

Specifying an image dictionary will append the images as the base nodes of the tree. No image dictionary means that the base nodes will be the lowest level concepts.

OUTPUT:

  id    parent  name
  1 none BASE                   # there is always a base node
  2 1   MEMORY                  # high level concept groups
  3 1   PERCEPTION              
  4 2   WORKING MEMORY          # concepts
  5 2   LONG TERM MEMORY
  6 4   image1.nii.gz           # associated images (discovered by way of contrasts)
  7 4   image2.nii.gz

"""

def concept_node_triples(image_dict=None,output_file="concept_node_triples.tsv",delim="\t"):
    concepts = filter_concepts()
    filey = init_output_file(output_file,delim=delim)

    # Generate a unique id for each concept
    concept_lookup = dict()
    for c in range(0,len(concepts)):
        concept_lookup[concepts[c]["id"]] = c+2
    
    # Generate tree for main concepts
    for concept in concepts:
        parents = []
        if "relationships" in concept:
            for relation in concept["relationships"]:
                if relation["direction"] == "parent":
                    if relation["id"] in concept_lookup:
                        parents.append(concept_lookup[relation["id"]])
        if not parents:
            make_node(concept_lookup[concept["id"]],concept["name"],"1",delim,filey)
        else:
            for parent in parents:    
                make_node(concept_lookup[concept["id"]],
                          concept["name"],parent,delim,filey)

    # Now add a node for each image
    if image_dict:
        node_id = max(concept_lookup.values()) + 1
        for conid, image_paths in image_dict.iteritems():
            concepts_single = get_concept(contrast_id=conid).json
            for con in concepts_single:
                for image_path in image_paths:
                    node_id = make_node(node_id,image_path,concept_lookup[concept["id"]],delim,filey)
    filey.close()
    print "%s has been created." % output_file 
