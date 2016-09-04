# Install

### Basic install

Install the dependencies: 

   ``` bash
pip install bleach django-ckeditor django-braces django-mqueue
git+ https://github.com/synw/django-mbase.git
   ```

Install the forum:

`pip install git+ https://github.com/synw/django-mgof.git`

Add ``"mgof",`` to INSTALLED_APPS

Add the urls: ``url('^forum/', include('mgof.urls')),``

Define the moderators groups:

   ```python
# Default is ['moderators']
MGOF_MODERATION_GROUPS = ['group1','group2']
   ```

Note: the superuser can always moderate.

### Ckeditor configuration

In settings.py:

   ```python
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
  
### Options

Set a `LOGIN_URL='/my/login/url/'`: default is `/login/`.

Pagination:

   ```python
# Default is 10
MGOF_PAGINATE_BY = 15
# Pagination for the moderation queue: default is 20
MGOF_MODERATION_PAGINATE_BY = 30
   ```

Moderation: all topics can be set manualy to be moderated or not. All threads are moderated by default. 
To change this:

   ```python
# Default is True
MGOF_DEFAULT_MODERATION = False
   ```
   
Note: you will have to run the migrations if you change this afterwards.
