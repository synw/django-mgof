# Modern good old forums for Django

An old school forum app optimized for phone devices.

This forum wants to be:

- Fast
- Simple
- Responsive

### Dependencies 

- [bleach](https://github.com/mozilla/bleach): html sanitizing
- [django-ckeditor](https://github.com/django-ckeditor): wysiwyg editor
- [django-braces](https://github.com/brack3t/django-braces): usefull mixins
- [django-mbase](https://github.com/synw/django-mbase): basic abstract models
- [django-mqueue](https://github.com/synw/django-mqueue): events queuing app used for moderation

### Static files required:

- Jquery
- Bootstrap: for templates
- [Font-awesome icons](https://fortawesome.github.io/Font-Awesome/icons/): for templates

### Install

- Clone
- `pip install bleach django-ckeditor django-braces django-mqueue` + clone mbase
- Add `mgof` to INSTALLED_APPS
- Add `url('^forum/', include('mgof.urls')),` to urls.py
- Migrate


