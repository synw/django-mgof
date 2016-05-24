# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User


LOGIN_URL = getattr(settings, 'LOGIN_URL', '/login/')
PAGINATE_BY = getattr(settings, 'MGOF_PAGINATE_BY', 10)
MODERATION_GROUP = getattr(settings, 'MGOF_MODERATION_GROUPS', ['moderators'])
MODERATION_LEVEL = getattr(settings, 'MGOF_MODERATION_LEVEL', 0)
MODERATION_PAGINATE_BY = getattr(settings, 'MGOF_MODERATION_PAGINATE_BY', 20)
ENABLE_PRIVATE_FORUMS = getattr(settings, 'MGOF_ENABLE_PRIVATE_FORUMS', False)