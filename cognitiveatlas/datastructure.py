#!/usr/bin/env python

"""

datastructure: part of the cognitive atlas package

functions for working with the cognitive atlas!


"""
from cognitiveatlas.api import filter_concepts, get_concept
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
concept_node_triples: Export a list of nodes, in triples

image_dict [OPTIONAL]: a dictionary of [contrast_id:image_file] pairs, eg:
                      
                           {"cnt_4decfedb91973":["image1.nii.gz","image2.nii.gz"]}

This will mean that the images in the list will be assigned to all concept nodes associated with the contrast specified. This allows for inference over the tree (for example, some relationship with concept nodes that are parents of assigned nodes) 

Specifying an image dictionary will append the images as the base nodes of the tree. No image dictionary means that the base nodes will be the lowest level concepts.

OUTPUT:

  id    parent  name
  1 none BASE                   # there is always a base node
  trm_12345 1   MEMORY                  # high level concept groups
  trm_23456 1   PERCEPTION              
  trm_34567 trm_12345   WORKING MEMORY          # concepts
  trm_56789 trm_12345   LONG TERM MEMORY
  trm_67890 trm_34567   image1.nii.gz           # associated images (discovered by way of contrasts)
  trm_78901 trm_34567   image2.nii.gz

"""

def get_concept_categories():
    concepts = filter_concepts()
    category_lookup = {}
    for concept in concepts:
        category_lookup[concept["id"]] = {"category":str(concept["id_concept_class"])}
    return category_lookup


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
                    # We can only use "kind of" otherwise we get circular reference
                    if relation["relationship"] == "kind of":
                        if relation["id"] in concept_lookup:
                            parents.append(relation["id"])
        if not parents:
            # make_node(node_id,name,parent,delim,file_obj):
            make_node(concept["id"],concept["name"],"1",delim,filey)
        else:
            for parent in parents:    
                # make_node(node_id,name,parent,delim,file_obj):
                make_node(concept["id"],concept["name"],parent,delim,filey)

    # Now add an entry for each image / contrast, may be multiple for each image
    if image_dict:
        node_id = max(concept_lookup.values()) + 1
        for conid, image_paths in image_dict.iteritems():
            concepts_single = get_concept(contrast_id=conid).json
            for con in concepts_single: # The concept is the parent of the image
                if con:
                    for image_path in image_paths:
                        # make_node(node_id,name,parent,delim,file_obj):
                        make_node("node_%s" %node_id,image_path,con["id"],delim,filey)
                        node_id +=1
    filey.close()
    print "%s has been created." % output_file 
