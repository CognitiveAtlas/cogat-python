#!/usr/bin/python

"""
Test import of cognitive atlas package
"""

from numpy.testing import assert_array_equal, assert_almost_equal, assert_equal
from nose.tools import assert_true, assert_false

'''Test that API dataframe object created successfully'''
def test_import():
    from cognitiveatlas import api

    print "Initial test of tests working!"
