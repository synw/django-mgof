# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

default_statuses =  [
                     (0, _(u'Published')),
                     (1, _(u'Pending')),
                     (2, _(u'Unpublished')),
                     (3, _(u'Orphaned')),
                     ]

LOGIN_URL = getattr(settings, 'LOGIN_URL', '/login/')
PAGINATE_BY = getattr(settings, 'MGOF_PAGINATE_BY', 10)
MODERATION_GROUPS = getattr(settings, 'MGOF_MODERATION_GROUPS', ['moderators'])
DEFAULT_MODERATION = getattr(settings, 'MGOF_DEFAULT_MODERATION', True)
MODERATION_PAGINATE_BY = getattr(settings, 'MGOF_MODERATION_PAGINATE_BY', 20)
ENABLE_PRIVATE_FORUMS = getattr(settings, 'MGOF_ENABLE_PRIVATE_FORUMS', False)
STATUSES = getattr(settings, 'MGOF_STATUSES', default_statuses)