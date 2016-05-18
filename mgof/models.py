# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group 
from ckeditor.fields import RichTextField
from mbase.models import MetaBaseModel, MetaBaseContentModel, MetaBaseShortTitleModel, MetaBasePostedByModel, MetaBaseStatusModel
from mgof.conf import PAGINATE_BY

class Forum(MetaBaseModel, MetaBaseShortTitleModel, MetaBaseStatusModel):
    num_topics = models.IntegerField(default=0, verbose_name=_(u'Topics in forum'))
    num_posts = models.IntegerField(default=0, verbose_name=_(u'Posts in forum'))
    last_post_date = models.DateTimeField(editable=False, null=True, blank=True)
    last_post_username = models.CharField(max_length=120, editable=False, blank=True)
    is_public = models.BooleanField(default=True, verbose_name=_(u'Opened to anonymous users'))
    authorized_groups = models.ManyToManyField(Group, blank=True, verbose_name=_(u'Reserved to groups')) 
    
    class Meta:
        verbose_name=_(u'Forum')
        verbose_name_plural = _(u'Forums')

    def __unicode__(self):
        return unicode(self.title)
    
    def get_absolute_url(self):
        return reverse('forum-detail', kwargs={'forum_pk':self.pk})


class Topic(MetaBaseModel, MetaBaseShortTitleModel, MetaBasePostedByModel, MetaBaseStatusModel):
    forum = models.ForeignKey(Forum, related_name="topics", verbose_name = _(u'Forum'))
    num_posts = models.IntegerField(default=0, verbose_name=_(u'Number of posts'))
    num_views = models.IntegerField(default=0, verbose_name=_(u'Number of views'))
    last_post_date = models.DateTimeField(editable=False, null=True, blank=True)
    last_post_username = models.CharField(max_length=120, editable=False, blank=True)
    is_closed = models.BooleanField(default=False, verbose_name=_(u'Topic closed'))
    is_moderated = models.BooleanField(default=True, verbose_name=_(u'Topic is moderated'))
    
    class Meta:
        verbose_name=_(u'Topic')
        verbose_name_plural = _(u'Topics')

    def __unicode__(self):
        return unicode(self.title)
    
    def get_absolute_url(self):
        return reverse('forum-topic-detail', kwargs={'topic_pk':self.pk})
        

class Post(MetaBaseModel, MetaBasePostedByModel, MetaBaseContentModel, MetaBaseStatusModel):
    topic = models.ForeignKey(Topic, related_name="posts", verbose_name = _(u'Topic'))
    responded_to_pk = models.PositiveIntegerField(default=0, blank=True) 
    responded_to_username = models.CharField(max_length=120, default='', blank=True)
    
    class Meta:
        verbose_name=_(u'Post')
        verbose_name_plural = _(u'Post')

    def __unicode__(self):
        return unicode(_(u'Post')+' '+str(+self.pk) )+': '+self.content[:25]
        
    def delete(self, *args, **kwargs):
        #~ get topic an forum
        if 'topic' in kwargs.keys():
            topic = kwargs['topic']
        else:
            topic = self.topic
        if 'forum' in kwargs.keys():
            forum = kwargs['forum']
        else:
            forum = self.topic.forum
        #~ check if topic has posts or delete it
        posts = topic.posts
        if not posts:
            topic.delete()
        else:
            #~ update topic an forum info
            topic.num_posts = topic.num_posts+1
            # TODO: update for last post info
            topic.save()
            forum.num_posts = forum.num_posts+1
            forum.save()
        super(Post, self).delete(*args, **kwargs)
    
    def get_absolute_url(self):
        posts = Post.objects.filter(topic=self.topic, status=0)
        page_num = 1
        if posts:
            paginator = Paginator(posts, PAGINATE_BY)
            page_num = paginator.num_pages
        return reverse('forum-topic-detail', kwargs={'topic_pk':self.topic.pk})+'?page='+str(page_num)+'#'+str(self.pk)
         
    def get_event_object_url(self):
        posts = Post.objects.filter(topic=self.topic, status=0)
        page_num = 1
        if posts:
            paginator = Paginator(posts, PAGINATE_BY)
            page_num = paginator.num_pages
        return reverse('forum-topic-detail', kwargs={'topic_pk':self.topic.pk})+'?page='+str(page_num)+'&m=1&p='+str(self.pk)+'#'+str(self.pk)
        









