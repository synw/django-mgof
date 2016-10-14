Install
=======

Basic install
-------------

Install the dependencies: 

.. highlight:: bash

::

   pip install django-mgof

Installed apps:

.. highlight:: python

::

   "ckeditor",
   "ckeditor_uploader",
   "mbase",
   "mqueue",
   "mgof",

Urls:

::

   url(r'^ckeditor/', include('ckeditor_uploader.urls')),
   url('^forum/', include('mgof.urls')),

Optional : define the moderators groups:

.. highlight:: python

::

   python
   # Default is ['moderators']
   MGOF_MODERATION_GROUPS = ['group1','group2']

Note: the superuser can always moderate.

Static files
------------

The following static files are required:

- Jquery
- Bootstrap: for templates
- `Font-awesome icons <https://fortawesome.github.io/Font-Awesome/icons/>`_: for templates

You have to load these in your main template.

Ckeditor configuration
----------------------

.. highlight:: python

::

   python
   CKEDITOR_UPLOAD_PATH = 'uploads/'
   CKEDITOR_JQUERY_URL = '/static/js/jquery-2.1.4.min.js'
   CKEDITOR_CONFIGS = {
    'public': {
        'toolbar':  [
                    ["Bold", "Italic"],
                    ['NumberedList', 'BulletedList', "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter'],
                    ["Link", "Unlink"], ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'], ['Undo', 'Redo'], ["Source", "Maximize"],
                    ],
        "removePlugins": "stylesheetparser",
    },
   }
  ```
  
Options
-------

Set a ``LOGIN_URL='/my/login/url/'``: default is ``/login/``.

Pagination:

.. highlight:: python

::

   # Default is 10
   MGOF_PAGINATE_BY = 15
   # Pagination for the moderation queue: default is 20
   MGOF_MODERATION_PAGINATE_BY = 30

Moderation: all topics can be set manualy to be moderated or not. All threads are moderated by default. 
To change this:

.. highlight:: python

::

   # Default is True
   MGOF_DEFAULT_MODERATION = False
   
Note: you will have to run the migrations if you change this afterwards.
