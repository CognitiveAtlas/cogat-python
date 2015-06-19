#!/usr/bin/python

"""
Test core functions of Cognitive Atlas python API wrapper

"""

from numpy.testing import assert_array_equal, assert_almost_equal, assert_equal
from cognitiveatlas.api import get_concept, search, get_task, get_disorder
from nose.tools import assert_true, assert_false

'''Test concepts queries'''
def test_concepts():
    print "### TESTING CONCEPT QUERIES:"
    concept_id = "trm_5022ef7599294"
    concept_name = "anxiety"
    contrast_id = "cnt_5299143fed521"

    # concept_id
    result = get_concept(id=concept_id)
    assert_equal(result.json[0]["name"],concept_name)

    # concept_name
    result = get_concept(name=concept_name)
    assert_equal(result.json[0]["id"],concept_id)

    # contrast_id
    result = get_concept(contrast_id=contrast_id)
    assert_equal(result.json[0]["id"],concept_id)

    # concept_id and concept_name
    result = get_concept(id=concept_id,name=concept_name)
    assert_equal(result.json[0]["name"],concept_name)

    # concept_id, and contrast_id
    result = get_concept(id=concept_id,contrast_id=contrast_id)
    assert_equal(result.json[0]["name"],concept_name)

    # concept_name and contrast_id
    result = get_concept(name=concept_name,contrast_id=contrast_id)
    assert_equal(result.json[0]["id"],concept_id)
    

'''Test search query'''
def search(query):
    result = search(query="anxiety")
    assert_true(len(result.json)>20)

'''Test task queries'''
def test_task():
    print "### TESTING TASK QUERIES:"
    task_id = "trm_4cacee4a1d875"
    task_name = "mixed gambles task"

    # task_id and task_name
    result = get_task(id=task_id,name=task_name)
    assert_equal(result.json[0]["type"],"task")
    assert_equal(result.json[0]["event_stamp"],"2010-10-06 21:46:50")

    # task_id
    result = get_task(id=task_id)
    assert_equal(result.json[0]["name"],task_name)
 
    # task_name
    result = get_task(name=task_name)
    assert_equal(result.json[0]["id"],task_id)


'''Test disorder queries'''
def test_disorder():
    print "### TESTING DISORDER QUERIES:"
    disorder_id = "dso_3324"
    disorder_name = "mood disorder"

    # disorder_id and disorder_name
    result = get_disorder(id=disorder_id,name=disorder_name)
    assert_equal(result.json[0]["name"],disorder_name)
    assert_equal(result.json[0]["is_a_fulltext"],"cognitive disorder")
    assert_equal(result.json[0]["event_stamp"],"2013-11-20 15:38:27")

    # disorder_id
    result = get_disorder(id=disorder_id)
    assert_equal(result.json[0]["name"],disorder_name)
 
    # disorder_name
    result = get_disorder(name=disorder_name)
    assert_equal(result.json[0]["id"],disorder_id)
