#!/usr/bin/python

"""
Test lookup functions in API

"""

from numpy.testing import assert_array_equal, assert_almost_equal, assert_equal
from cognitiveatlas.api import get_contrast_lookup
from nose.tools import assert_true, assert_false

'''Test concepts queries'''
def test_lookups():
    print "### TESTING LOOKUPS:"
    # get_concept_lookup uses get_task lookup
    concept_lookup = get_contrast_lookup()
    assert_true(len(concept_lookup)>1400)

    # Test for specific list of tasks
    task_id = [u'trm_4f244f46ebf58', u'trm_523c7a0a73cf5',
               u'trm_4ebd44cd88360', u'trm_4f24126c22011',
               u'trm_551f151f7347e']
    lookup = get_conrast_lookup(task_id=task_id)
    assert_true(len(concept_lookup)>20)
