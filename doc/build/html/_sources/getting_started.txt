Getting Started
===============

Installation
------------
::

	pip install cognitiveatlas


Development Version

::

	git clone https://github.com/CognitiveAtlas/cogat-python
        cd cogat-python
        python setup.py install



Dependencies:

* pandas


Overview
-----

The Cognitive Atlas is an ontology, or a description of concepts, disorders, task paradigms, and associated contrasts and conditions known in cognitive neuroscience. A concept can be any kind of cognitive process related to emotion, language, executive control, action, attention, learning and memory, perception, social function, reasoning or decision making, or motivation.  A "task" is any kind of behavioral paradigm (assessment, survey, fMRI scanner task, etc.) that can be used to measure a concept. Associated with tasks are conditions (components that make up the task that may induce different cognitive processes) and contrasts (operations on conditions to summarize one or more conditions for the purposes of analyses, such as summing up a particular set of questions for an assessment to come up with a final score.) Finally, a disorder is a manifestation of symptoms that negatively impact daily functioning. We place "tasks," "concepts," and "disorders" together in the Cognitive Atlas because our (current) standard definition of disorders (the Diagnostic and Statistical Manual of Mental Disorders, or DSM-V) defines disorders based on abberrant cognitive processes and behaviors, which can be described by concepts in the atlas, and measured by tasks.


Functions
---------

The most basic functions are to search, and get concepts, tasks, and disorders.

- search
- get_concept
- get_task
- get_disorder


Each function returns a "cognitiveatlas.DataJson" object with the following fields:

- result.json: a list of dictionaries, each representing a single json result    
- result.pandas: a pandas data frame of the results 
- result.txt: a text version of the json, for printing to file     
- result.url: the RESTful API call (a url) to retrieve the result


See the "search" function below for an example of each of the above. The get functions follow.


Search
------

Search Concepts, Theories, Assertions, Tasks, Task Batteries, and Disorders for a given keyword.

Parameters
++++++++++

- query: the query to search for that will go across concepts, theories, tasks, and disorders


Output
++++++

- id: the unique id of the item
- link: the url to append to the base of "http://www.cognitiveatlas.org" to see the webpage for the item
- type: one of "concept," "task," "disorder," "task_definition," "concept_definition," or "assertion."


Example
++++++++

::

	> from cognitiveatlas.api import search
        > result = search(query="anxiety")      
        http://cognitiveatlas.org/api/v-alpha/search?q=anxiety
        Result Includes:<pandas:data frame><json:dict><txt:str><url:str>

We can look at the result as a data frame

::

	> result.pandas
	                   id                             link                type
	0   trm_5022ef7599294    /concept/id/trm_5022ef7599294             concept
	1   trm_50aff037c389f    /concept/id/trm_50aff037c389f             concept
	2   trm_523ca7e778c50    /concept/id/trm_523ca7e778c50             concept
	3   trm_4b7c27094a093    /concept/id/trm_4b7c27094a093  concept_definition
	4   trm_50aff037c389f    /concept/id/trm_50aff037c389f  concept_definition
	5   trm_523ca7e778c50    /concept/id/trm_523ca7e778c50  concept_definition
	6   trm_523e0419ec219    /concept/id/trm_523e0419ec219  concept_definition
	7   tsk_4a57abb949dfe       /task/id/tsk_4a57abb949dfe                task
	8   tsk_4a57abb949dfe       /task/id/tsk_4a57abb949dfe     task_definition
	9   trm_5208fe678c652       /task/id/trm_5208fe678c652     task_definition
	...

raw json text

::

	> result.txt
	'[{"type":"concept","id":"trm_5022ef7599294","link":"\\/concept\\/id\\/trm_5022ef7599294"},{"type":"concept","id":"trm_50aff037c389f","link":"\\/concept\\/id\\/trm_50aff037c389f"},{"type":"concept","id":"trm_523ca7e778c50","link":"\\/concept\\/id\\/trm_523ca7e778c50"},{"type":"concept_definition","id":"trm_4b7c27094a093","link":"\\/concept\\/id\\/trm_4b7c27094a093"},{"type":"concept_definition","id":"trm_50aff037c389f","link":"\\/concept\\/id\\/trm_50aff037c389f"},...


json (dictionary)


::

	> len(result.json)
	22
	> result.json[0]
	{u'id': u'trm_5022ef7599294',
	 u'link': u'/concept/id/trm_5022ef7599294',
	 u'type': u'concept'}


And finally, we can see the original url call:

::

	> result.url
	'http://cognitiveatlas.org/api/v-alpha/search?q=anxiety'




get_concept
-----------

Return one or more concepts


Parameters
++++++++++

- concept_id - Return the specified Concept.
- concept_name - Return the specified Concept.
- contrast_id - Return all Concepts related to the specified Contrast.
- [no parameters] - Return all Concepts.


Output
++++++++++

- concept_class: A category that the concept belongs in, one of
    - action
    - attention
    - emotion
    - executive-cognitive control
    - language
    - learning and memory
    - perception
    - reasoning and decision making
    - social function
    - motivation
- def_event_stamp: the creation date and time of the definition (e.g., 2012-08-08 23:00:05)
- def_id: a unique identifier for the definition
- def_id_user: the user id that generated the definition
- definition_text: the concept definition
- id_concept_class: a unique identifier for the concept class
- id_term: the concept term unique id
- relationships: a list of ontological relationships
    - direction: the direction of the relationship in the ontology tree, either "parent" or "child"
    - id: the unique identifier of the related term
    - relationship: the kind of relationship, either "kind of" or "part of"
- term_alias: an alias for the concept
- term_text: the name of the concept
- trm_event_stamp: the creation date and time of the concept
- trm_id: the unique id for the concept
- trm_id_user: the unique id for the user that created the concept

Example
++++++++

::

    from cognitiveatlas.api import get_concept

    concept_id = "trm_5022ef7599294"
    concept_name = "anxiety"
    contrast_id = "cnt_5299143fed521"

    # concept_id
    > result = get_concept(concept_id=concept_id)
    http://cognitiveatlas.org/api/v-alpha/concept?concept_id=trm_5022ef7599294
    Result Includes:<pandas:data frame><json:dict><txt:str><url:str>


An example of the json output:

::
	
	> result.json[0]
	{u'concept_class': u'',
	 u'def_event_stamp': u'2013-06-14 04:19:52',
	 u'def_id': u'def_51ba99e738d7c',
	 u'def_id_user': u'usr_51ba954cf0abe',
	 u'definition_text': u'An aversive psychophysiological state characterized by fear, worry, or concern associated with current or impending threat often elicited by general and specific interoceptive or exteroceptive cues.',
	 u'id_concept_class': u'ctp_C8',
	 u'id_term': u'trm_5022ef7599294',
	 u'relationships': [{u'direction': u'parent',
	   u'id': u'trm_4a3fd79d0a17f',
	   u'relationship': u'kind of'}],
	 u'term_alias': u'',
	 u'term_text': u'anxiety',
	 u'term_type': u'concept',
	 u'trm_event_stamp': u'2012-08-08 23:00:05',
	 u'trm_id': u'trm_5022ef7599294',
	 u'trm_id_user': u'usr_4f177506dde77'}


get_task
--------

Return one or more tasks


Parameters
++++++++++

- task_id - Return the specified Task.
- task_name - Return the specified Task.
- [no parameters] - Return all Tasks with basic information only.

Output
++++++

- citation: a list of citations associated with the task, each including the following:
    - citation_authors
    - citation_comment
    - citation_desc: the title of the publication
    - citation_pmid: the pubmed id
    - citation_pubdate: date of publicatoin
    - citation_pubname: journal title
    - citation_source: where the information was parsed from
    - citation_type: a unique identifier for the citation type
    - citation_url
    - event_stamp: date and time when citation was added
    - id: a unique identifier for the citation
    - id_user: the unique id of the user that added the citation
- citation_matches
- concept_class: if the task belongs under one of:
    - action
    - attention
    - emotion
    - executive-cognitive control
    - language
    - learning and memory
    - perception
    - reasoning and decision making
    - social function
    - motivation
- concepts: a list of concept unique identifiers associated with the task. Each has:
    - concept_id: a unique identifier for the concept
    - contrast_id: one or more contrasts used to measure the concept defined under the task
- conclass
- conditions: a list of conditions defined for the task. Each has:
    - condition_description: a longer description of the condition
    - condition_text: the shorter name of the condition
    - event_stamp
    - id: a unique identifier for the condition
    - id_term: the task unique identifier
    - id_user: the unique id of the user that created the condition
- def_event_stamp: the creation date and time for the definition
- def_id: a unique identifier for the definition
- def_id_user: the unique identifier of the user that defined the task
- def_id: a unique identifier of the definition
- definition_text: the task definition
- discussion: user discussion
- disorders: disorders associated with the task
- external_datasets: external datasets associated with the task. Each has:
    - dataset_name
    - dataset_url
    - event_stamp
    - id
    - id_term: the task unique id
    - id_user: the unique id of the user that added the dataset
    - history: includes all (historical) versions of the fields already listed.
- id_concept_class
- id_term: the task unique id
- implementations: a list of implementations of the task
- indicators: a list of indicators for the task
- term_alias
- term_text: the name of the task
- term_type: should be "task" or "task_definition"
- trm_event_stamp:
- trm_id: the unique id of the task
- trm_id_user: the unique id of the user that generated the task
- umark: the username that created the task
- umarkdef: the username that created the definition

Example
+++++++

::

	from cognitiveatlas.api import get_task
	task_id = "trm_4cacee4a1d875"
	task_name = "mixed gambles task"

	# task_id and task_name
	> result = get_task(task_id=task_id,task_name=task_name)
	http://cognitiveatlas.org/api/v-alpha/task?task_name=mixed%20gambles%20task&task_id=trm_4cacee4a1d875
	Result Includes:<pandas:data frame><json:dict><txt:str><url:str>
 

get_disorder
--------

Return one or more disorders


Parameters
++++++++++

- disorder: return one or more disorders
- disorder_id - Return the specified Disorder.
- disorder_name - Return the specified Disorder.
- [no parameters] - Return all Disorders.


Output
++++++


Example
+++++++

::

	from cognitiveatlas.api import get_task


   disorder_id = "dso_3324"
    disorder_name = "mood disorder"

    # disorder_id and disorder_name
    result = get_disorder(disorder_id=disorder_id,disorder_name=disorder_name)
    assert_equal(result.json[0]["name"],disorder_name)
    assert_equal(result.json[0]["is_a_fulltext"],"cognitive disorder")
    assert_equal(result.json[0]["event_stamp"],"2013-11-20 15:38:27")

    # disorder_id
    result = get_disorder(disorder_id=disorder_id)
    assert_equal(result.json[0]["name"],disorder_name)
 
    # disorder_name
    result = get_disorder(disorder_name=disorder_name)
    assert_equal(result.json[0]["id"],disorder_id)
