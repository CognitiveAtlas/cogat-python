#!/usr/bin/env python

"""

views: part of the cognitive atlas package

functions for doing annotations, viewing data, etc.


"""

import os
import json
import string
import urllib
import urllib2
import shutil
import tempfile
import contextlib
import webbrowser
import numpy as np
import pandas as pd
import nibabel as nb
from api import merge_df, get_contrasts_dump, get_tasks_df
from template import get_template, add_string, save_text, load_text

__author__ = ["Poldracklab","Vanessa Sochat"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2015/01/23 $"
__license__ = "BSD"


'''View code in temporary browser!'''
def view(html_snippet):
  with make_tmp_folder() as tmp_dir:  
    # Write to temporary file
    tmp_file = "%s/cogannotate.html" %(tmp_dir)
    internal_view(html_snippet,tmp_file)

'''Internal view function'''
def internal_view(html_snippet,tmp_file):
  html_file = open(tmp_file,'wb')
  html_file.writelines(html_snippet)
  html_file.close()
  url = 'file://%s' %(tmp_file)
  webbrowser.open_new_tab(url)
  raw_input("Press Enter for next/to finish...")

# Make temporary directory
@contextlib.contextmanager
def make_tmp_folder():
  temp_dir = tempfile.mkdtemp()
  yield temp_dir
  shutil.rmtree(temp_dir)

'''Annotate images with concepts from cognitive atlas
there can be more than one concept per image'''
def annotate_images_concepts():
  print "TODO"

'''Produce a d3 autocomplete to embed in a django crispy form'''
def contrast_selector_django_crispy_form(django_field,include_bootstrap=True,from_file=None):

  if from_file:
    html_snippet = load_text(from_file)
  else:
    html_snippet = create_contrast_task_definition_json(filter_out_empty_contrasts=True)

  # Get template 
  template = get_template("cognitive_atlas_contrast_selector")
  django_field_div = "div_id_%s" % (django_field)
  django_field_id = "id_%s" % (django_field)
  django_field_hint = "hint_id_%s" %(django_field)
  substitutions = {"DJANGO_FIELD":django_field,
                   "DJANGO_FIELD_DIV":django_field_div,
                   "DJANGO_FIELD_ID":django_field_id,
                   "DJANGO_FIELD_HINT":django_field_hint,
                   "TASKS_DATA":html_snippet}

  template = add_string(substitutions,template)
  if not include_bootstrap: template = template[6:len(template)]
  return template

def make_contrast_lookup_table(contrasts,tasks,only_with_contrast):
  # Prepare lookup table for contrasts
  task_keys = list(tasks["UID"])
  task_names = list(tasks["NAME"]) 
  lookup = dict()
  has_contrast = []
  for task in task_keys:
    subset = contrasts[contrasts["UID"].isin([task])]
    tmp = ['{"conname":"%s","conid":"%s"}' %(item[1]["CONTRAST_TEXT"],item[1]["ID"]) for item in subset.iterrows()]
    lookup[task] = tmp # tasks without contrasts will be []
    if len(tmp) != 0: has_contrast.append(task)

  # Removed tasks without contrasts  
  if only_with_contrast == True:    
    tasks = tasks[tasks["UID"].isin(has_contrast)]
  
  task_keys = list(tasks["UID"])
  task_names = list(tasks["NAME"]) 
  task_description = [t.replace('\n','|').replace('"',"'").replace("\r","") for t in tasks["DESCRIPTION"]]
  task_list = "["
  for t in range(0,len(task_keys)):
    task_list = '%s{"name":"%s","id":"%s","description":"%s","contrasts":[%s]},\n' %(task_list,task_names[t],task_keys[t],task_description[t],",".join(lookup[task_keys[t]]))
  # The last entry is a "None" option
  task_list = '%s{"name":"None / Other","id":"None","contrasts":[{"conname":"None / Other","conid":"None"}]}]\n' %(task_list)
  return task_list

def create_contrast_task_definition_json(only_with_contrast=False):
  definitions = get_tasks_df(filters="http://www.w3.org/2004/02/skos/core#definition")
  tasks = get_tasks_df(filters="http://www.w3.org/2004/02/skos/core#prefLabel")
  contrasts = get_contrasts_dump()
  tasks = merge_df(left=definitions,right=tasks,join_column="UID")
  tasks = tasks[tasks.URL_x.notnull()]  
  tasks = tasks[["URL_x","NAME_x","UID","NAME_y"]]
  tasks.columns = ["URL","DESCRIPTION","UID","NAME"]
  task_list = make_contrast_lookup_table(contrasts,tasks,only_with_contrast=only_with_contrast) 
  return task_list

'''Annotate images with contrasts from cognitive atlas
this is intended for local annotation to produce a json from brainspell
with the article'''
def annotate_images_contrasts_json(article,image):
  task_list = create_contrast_task_definition_json()

  # Image info
  image_id = str(image["url"].replace("http://neurovault.org/images/","")[:-1])
  image_info = '{"name":"%s","file":"%s","collection_key":"%s","image_key":"%s"}' %(image["file"],image["url"],image["collection"],image_id)
  image_info = image_info.encode("utf-8")

  # Get template 
  template = get_template("annotate_images_contrasts_json")
  # Add task_list to template
  template = add_string({"CA_TASKS":task_list},template)
  # Add image_info to template
  template = add_string({"IMAGE_INFO":image_info},template)
  # Add article to template
  template = add_string({"BRAINSPELL_ARTICLE":article},template)
  view(template)
