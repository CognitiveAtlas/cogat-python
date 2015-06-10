# Cognitive Atlas Python API

*in development*

This API will allow python access to the RESTful API in the cognitive atlas. The current code is working with RDF, and this will be updated to use the new RESTful API (alpha) promptly. Functions include:

- tasks
- concepts
- disorders
- collections
- contrasts (soon)

as well as tools to annotate data, and integrate with brain imaging databases (NeuroVault) as well as annotation platforms (brainspell).  For example, [this workflow](examples/annotate_nv_images.py) shows doing the following:

- grab contrasts and tasks from the cognitive atlas (the ontology)
- grab images we want to label from NeuroVault (the data)
- grab the metadata for the image from brainspell (the data structure)
- open up interactive web interface to search and do tagging
- click save button to output modified data structure

A demo of the annotation interface that pops up is [available here](http://www.vbmis.com/bmi/project/cogatlas/annotate.html)
A demo of the crispy form (django) integration is [available here](http://vbmis.com/bmi/share/cogatlas/cogatlas.html)


