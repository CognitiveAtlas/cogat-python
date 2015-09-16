#!/usr/bin/python

"""
Test lookup functions in API

"""

from numpy.testing import assert_array_equal, assert_almost_equal, assert_equal
from cognitiveatlas.api import get_task_lookup
from nose.tools import assert_true, assert_false, raises

'''Test concepts queries'''
def test_lookups():
    print "### TESTING LOOKUPS:"

    # Test for specific list of tasks
    task_id = [u'trm_4f244f46ebf58', u'trm_523c7a0a73cf5',
               u'trm_4ebd44cd88360', u'trm_4f24126c22011',
               u'trm_551f151f7347e']
    lookup = get_contrast_lookup(task_id=task_id)
    assert_true(len(lookup)>20)

    # Test for specific contrasts
    contrast_ids = [u'cnt_523c7cf0ea7b4',u'cnt_553a64ea67841',
                    u'cnt_553a664f97104',u'cnt_553a647ca67ed',
                    u'cnt_553a64d23c393',u'cnt_523c7d0de6735']
    lookup = get_contrast_lookup(contrast_id=contrast_ids)
    assert_true(len(lookup)==6)
    

@raises(ValueError)
def test_raises_type_error():
    # Test for specific list of tasks
    task_id = [u'trm_4f244f46ebf58', u'trm_523c7a0a73cf5',
               u'trm_4ebd44cd88360', u'trm_4f24126c22011',
               u'trm_551f151f7347e']

    contrast_ids = [u'cnt_523c7cf0ea7b4',u'cnt_553a64ea67841',
                    u'cnt_553a664f97104',u'cnt_553a647ca67ed',
                    u'cnt_553a64d23c393',u'cnt_523c7d0de6735']

    lookup = get_contrast_lookup(task_id=task_id,contrast_id=contrast_ids)
