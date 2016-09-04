# Modern good old forums for Django

An old school forum app optimized for phone devices.

This forum wants to be:

- Fast
- Simple
- Responsive

### Features:

- Forum permissions: public, authenticated users and group forums.
- Thread level moderation: each thread can be moderated or not.
- Phone friendly: responsive ckeditor interface for users to post.

### Dependencies 

- [bleach](https://github.com/mozilla/bleach): html sanitizing
- [django-ckeditor](https://github.com/django-ckeditor): wysiwyg editor
- [django-braces](https://github.com/brack3t/django-braces): usefull mixins
- [django-mbase](https://github.com/synw/django-mbase): basic abstract models
- [django-mqueue](https://github.com/synw/django-mqueue): events queuing app used for moderation

### Documentation

Check the [documentation](http://django-mgof.readthedocs.io/en/latest/) for install instructions.




