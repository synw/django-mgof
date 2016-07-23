# -*- coding: utf-8 -*-
from mgof.models import Forum, Topic, Post

# ------------- objects factory ---------------
def create_forum(is_public=True):
    obj = Forum.objects.create(title='The forum', is_public=is_public)
    return obj
    
def create_topic(forum=None, pk=None):
    if forum is None:
        forum = create_forum()
    if pk is None:
        obj = Topic.objects.create(title='The topic', forum=forum)
    else:
        obj = Topic.objects.create(pk=pk, title='The topic', forum=forum)
    return obj

def create_post(topic=None):
    if topic is None:
        topic = create_topic()
    obj = Post.objects.create(topic=topic, content="Lorem ipsum")
    return obj