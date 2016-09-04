# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from mqueue.models import MEvent
from mgof.models import Post


def mpost_save(sender, instance, created, **kwargs):
    if created:
        #~ record for moderation if the topic is monitored
        if instance.topic.is_moderated:
            MEvent.objects.create(
                            model = Post, 
                            name = 'Post from forum : '+instance.topic.title,
                            instance = instance,
                            user = instance.posted_by,
                            event_class = 'Forum post',
                            )
    return   


post_save.connect(mpost_save, Post)




    