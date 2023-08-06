# Basic Configuration

## Add `dj_docs` to the `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # ...
    'dj_docs',
]
```
Your `settings.py` file should now include `dj_docs` in the `INSTALLED_APPS` list. 
This will enable the dj_docs app in your Django project.


## Configuration for `DOC_STRING_MODULES`

The `DOC_STRING_MODULES` setting in Django's `settings.py` file allows you to define documentation strings for your 
project's modules, classes, and functions.

To configure `DOC_STRING_MODULES`, add the following code to your `settings.py` file:
```python
DOC_STRING_MODULES = [
  {
      "section": "enter title",
      "modules": [
          {
              "module_name": "module",
              "class": "module.class",
              "function": "module.function",
              "synopsis": "Description"
          },
      ]
  },
]
```
Replace `"enter title"` with the title of the page you want to add, 
`"module"` with the name of the module you want to document, `"module.class"` with the name of the class you want to 
document, `"module.function"` with the name of the function you want to document, and `"Description"` with the 
description of the module, class, or function.

You can add as many sections and modules as you need to document your project.


## Adding the Documentation URL Path

To access the documentation for this Django app, you'll need to add a URL path to your `urls.py` file that includes the `dj_docs` app's URLs. Follow these steps:


```python
from django.urls import include # Import the `include` function from Django's `urls` module

urlpatterns = [
    # ...
    path('docs/', include('dj_docs.urls')), # add url for documentation url to django application
]
```