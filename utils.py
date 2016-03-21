# -*- coding: utf-8 -*-

import bleach
from mgof.conf import MODERATION_GROUP


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





