# -*- coding: utf-8 -*-

import bleach
from django.conf import settings
from mgof.conf import MODERATION_GROUP
from mqueue.models import MEvent


def clean_post_data(html_str):
    tags = ['a', 'p','ul','li']
    attr = {
            '*': ['style'],
            'a': ['href'],
            'img': ['src','alt'],
            }
    styles = ['font-weight','font-style', 'text-align']
    strip = True
    return bleach.clean(html_str,
                        tags=tags,
                        attributes=attr,
                        styles=styles,
                        strip=strip)
    

def user_is_moderator(user, superuser_too=True):
    is_moderator = False
    if not user.is_anonymous():
        if superuser_too:
            if user.is_superuser:
                is_moderator = True
        else:
            is_moderator = user.groups.filter(name=MODERATION_GROUP).exists()
    return is_moderator


def user_can_see_forum(forum, user, superuser_too=True):
    user_groups = user.groups.all()
    if forum.is_public:
        return True
    if superuser_too:
        if user.is_superuser:
            return True
    else:
        forum_groups = forum.authorized_groups.all()
        for allowed_group in forum_groups:
            if allowed_group in user_groups:
                return True
    return False


