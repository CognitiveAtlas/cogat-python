#/usr/bin/python

# Here we will get a task --> definition data frame, and convert to json
from cognitiveatlas import views,template

cogat_json = "/home/vanessa/Desktop/cognitiveatlas_tasks.json"
task_list = views.create_contrast_task_definition_json() # default will include tasks with no contrasts defined
task_list = views.create_contrast_task_definition_json(only_with_contrast=True) # only include tasks with contrasts defined
template.save_text(task_list,cogat_json)

# Now we will generate an html snippet (eg, to embed into a django crispy form)
django_field = "contrast_definition_cogatlas"
html_snippet = views.contrast_selector_django_crispy_form(django_field=django_field,include_bootstrap=False,from_file=cogat_json)    
