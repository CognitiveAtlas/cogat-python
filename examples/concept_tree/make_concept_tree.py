#!/usr/bin/python

from cognitiveatlas.datastructure import concept_node_triples, get_concept_categories
import pandas

# EXAMPLE 2: #########################################################
# We are going to make a tree for some group of contrasts or concepts
# that we are interested in.
######################################################################

## STEP 1: GENERATE TRIPLES DATA STRUCTURE
# This is a data structure that looks like this - showing id of the node (column 1), parent id (column 2)
# and then the name

'''
  id    parent  name
  1 none BASE                   # there is always a base node
  2 1   MEMORY                  # high level concept groups
  3 1   PERCEPTION              
  4 2   WORKING MEMORY          # concepts
  5 2   LONG TERM MEMORY
  6 4   image1.nii.gz           # associated images (discovered by way of contrasts)
  7 4   image2.nii.gz
'''

# Create a data structure of tasks and contrasts for our analysis
relationship_table = concept_node_triples(save_to_file=False)

# relationship_table
# 
#                    id             parent                           name
#0                    1               None                           BASE
#1    trm_4a3fd79d096be  trm_4a3fd79d0aec1            abductive reasoning
#2    trm_4a3fd79d096e3  trm_4a3fd79d09827               abstract analogy
#3    trm_4a3fd79d096f0  trm_4a3fd79d0a746             abstract knowledge
#4    trm_4a3fd79d096fc                  1                acoustic coding
#5    trm_4a3fd79d09707  trm_4a3fd79d0b8e5              acoustic encoding
#6    trm_4a3fd79d09707  trm_4a3fd79d0b8e5              acoustic encoding
#7    trm_4a3fd79d09713  trm_4a3fd79d09ab2   acoustic phonetic processing

# Note that you can include an optional "image_dict" argument if you want to add a
# final layer of nodes (eg, a dictionary of keys (concept ids) that correspond to some final
# node of interest (in my research I used NeuroVault images). Eg:
#
# lookup = {"cnt_4e0237ba58871":[1,2,3,4]}
# concept_node_triples(output_file=output_triples_file,image_dict=lookup)
#
# and you can specify an output file, default for "save_to_file" is True 
# (this should probably be False):
#
# concept_node_triples(output_file="output_triples.tsv")
# You can also change the lookup key to be a task id instead.

# If you want to include concept categories
concept_categories = get_concept_categories()

## STEP 2: VISUALIZATION WITH PYBRAINCOMPARE
# pip install pybraincompare
from pybraincompare.template.templates import save_template
from pybraincompare.ontology.tree import named_ontology_tree_from_tsv, make_ontology_tree_d3

# First let's look at the tree structure - here is with categories
tree = named_ontology_tree_from_tsv(relationship_table,output_json=None,meta_data=concept_categories)

# And without
tree = named_ontology_tree_from_tsv(relationship_table,output_json=None)

# Now we can save the tree to file, a d3 result
html_snippet = make_ontology_tree_d3(tree)
save_template(html_snippet,"index.html")
