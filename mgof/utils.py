# -*- coding: utf-8 -*-

import bleach
from mgof.conf import MODERATION_GROUPS
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
            is_moderator = user.groups.filter(name__in=MODERATION_GROUPS).exists()
    return is_moderator

def user_can_see_forum(forum, user, superuser_too=True):
    # superuser bypasses all
    if superuser_too:
        if user.is_superuser:
            return True
    # check vs public / private forum
    if forum.is_public is True:
        return True
    else:
        # check vs forum reserved to groups
        if forum.is_restricted_to_groups is True:
            print "* Group"
            authorized_groups = forum.authorized_groups.all()
            user_groups = user.groups.all()
            print str(authorized_groups)+' - '+str(user_groups)
            for group in user_groups:
                print str(group)
                if group in authorized_groups:
                    return True
        else:
            print "* user forum"
            if user.is_authenticated():
                print "Is auth"
                return True
    return False


