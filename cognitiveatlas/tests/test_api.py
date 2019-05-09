#!/usr/bin/python

"""
Test core functions of Cognitive Atlas python API wrapper
"""

import unittest
from cognitiveatlas.api import ( 
    get_concept, 
    search,
    get_task, 
    get_disorder
)

class TestAPI(unittest.TestCase):

    def test_concepts(self):
        '''Test concepts queries'''
        print("### TESTING CONCEPT QUERIES:")
        concept_id = "trm_5022ef7599294"
        concept_name = "anxiety"
        contrast_id = "cnt_5299143fed521"

        # concept_id
        result = get_concept(id=concept_id)
        self.assertEqual(result.json["name"],concept_name)

        # concept_name
        result = get_concept(name=concept_name)
        self.assertEqual(result.json["id"],concept_id)

        # contrast_id
        result = get_concept(contrast_id=contrast_id)
        self.assertTrue(any(concept_id==obj["id"] for obj in result.json))
       
        # concept_id and concept_name
        result = get_concept(id=concept_id,name=concept_name)
        self.assertEqual(result.json["name"],concept_name)

        # concept_id, and contrast_id
        result = get_concept(id=concept_id,contrast_id=contrast_id)
        self.assertEqual(result.json["name"],concept_name)

        # concept_name and contrast_id
        result = get_concept(name=concept_name,contrast_id=contrast_id)
        self.assertEqual(result.json["id"],concept_id)

    def test_search(self):
        '''Test search query'''
        result = search(query="anxiety")
        self.assertTrue(len(result.json)>20)

    def test_task(self):
        '''Test task queries'''

        print("### TESTING TASK QUERIES:")
        task_id = "trm_4cacee4a1d875"
        task_name = "mixed gambles task"

        # task_id and task_name
        result = get_task(id=task_id,name=task_name)
        self.assertEqual(result.json["type"],"task")

        # task_id
        result = get_task(id=task_id)
        self.assertEqual(result.json["name"],task_name)
 
        # task_name
        result = get_task(name=task_name)
        self.assertEqual(result.json["id"],task_id)

    def test_disorder(self):
        '''Test disorder queries'''

        print("### TESTING DISORDER QUERIES:")
        disorder_id = "dso_3324"
        disorder_name = "mood disorder"

        # disorder_id and disorder_name
        result = get_disorder(id=disorder_id,name=disorder_name)
        print(result)
        self.assertEqual(result.json["name"],disorder_name)
        print(result.json)
        self.assertEqual(result.json["type"],"disorder")

        # disorder_id
        result = get_disorder(id=disorder_id)
        self.assertEqual(result.json["name"],disorder_name)
 
        # disorder_name
        result = get_disorder(name=disorder_name)
        self.assertEqual(result.json["id"],disorder_id)

if __name__ == '__main__':
    unittest.main()
