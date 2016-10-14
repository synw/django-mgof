# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group 
from mbase.models import MetaBaseModel, MetaBaseContentModel, MetaBaseShortTitleModel, MetaBasePostedByModel
from mgof.conf import PAGINATE_BY, DEFAULT_MODERATION
from mqueue.models import MEvent

class Forum(MetaBaseModel, MetaBaseShortTitleModel):
    num_topics = models.IntegerField(default=0, verbose_name=_(u'Topics in forum'))
    num_posts = models.IntegerField(default=0, verbose_name=_(u'Posts in forum'))
    last_post_date = models.DateTimeField(editable=False, null=True, blank=True)
    last_post_username = models.CharField(max_length=120, editable=False, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_(u'Is Active'))
    is_public = models.BooleanField(default=True, verbose_name=_(u'Opened to anonymous users'), help_text=_(u'Anonymous users will be able to see this forum'))
    is_moderated = models.BooleanField(default=DEFAULT_MODERATION, verbose_name=_(u'Is moderated'))
    is_restricted_to_groups = models.BooleanField(default=False, verbose_name=_(u'Restricted to groups'), help_text=_(u'You must check this in order to restrict the forum to groups'))
    authorized_groups = models.ManyToManyField(Group, blank=True, verbose_name=_(u'Groups that can access the forum')) 
    
    class Meta:
        verbose_name=_(u'Forum')
        verbose_name_plural = _(u'Forums')

    def __unicode__(self):
        return unicode(self.title)
    
    def get_absolute_url(self):
        return reverse('forum-detail', kwargs={'forum_pk':self.pk})


class Topic(MetaBaseModel, MetaBaseShortTitleModel, MetaBasePostedByModel):
    forum = models.ForeignKey(Forum, related_name="topics", verbose_name = _(u'Forum'))
    num_posts = models.IntegerField(default=0, verbose_name=_(u'Number of posts'))
    num_views = models.IntegerField(default=0, verbose_name=_(u'Number of views'))
    last_post_date = models.DateTimeField(editable=False, null=True, blank=True)
    last_post_username = models.CharField(max_length=120, editable=False, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_(u'Is Active'))
    is_closed = models.BooleanField(default=False, verbose_name=_(u'Topic closed'))
    is_moderated = models.BooleanField(default=DEFAULT_MODERATION, verbose_name=_(u'Topic is moderated'))
    
    class Meta:
        verbose_name=_(u'Topic')
        verbose_name_plural = _(u'Topics')

    def __unicode__(self):
        return unicode(self.title)
    
    def get_absolute_url(self):
        return reverse('forum-topic-detail', kwargs={'topic_pk':self.pk})
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_moderated = self.forum.is_moderated
        return super(Topic, self).save(*args, **kwargs)
        

class Post(MetaBaseModel, MetaBasePostedByModel, MetaBaseContentModel):
    topic = models.ForeignKey(Topic, related_name="posts", verbose_name = _(u'Topic'))
    responded_to_pk = models.PositiveIntegerField(default=0, blank=True) 
    responded_to_username = models.CharField(max_length=120, default='', blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_(u'Is Active'))
    
    class Meta:
        verbose_name=_(u'Post')
        verbose_name_plural = _(u'Post')

    def __unicode__(self):
        try:
            return unicode(_(u'Post')+' '+str(+self.pk) )+': '+self.content[:25]
        except:
            return unicode(_(u'Post'))
        
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
        posts = topic.posts.all()
        if len(posts) == 1:
            topic.delete()
        else:
            #~ update topic an forum info
            topic.num_posts = topic.num_posts-1
            # TODO: update for last post info
            topic.save()
        forum.num_posts = forum.num_posts-1
        forum.save()
        # clean moderation queue
        try:
            event = MEvent.objects.get(model=Post, event_class='forum_post')
            event.delete()
        except:
            pass
        super(Post, self).delete(*args, **kwargs)
    
    def get_absolute_url(self):
        posts = Post.objects.filter(topic=self.topic, is_active=True)
        page_num = 1
        if posts:
            paginator = Paginator(posts, PAGINATE_BY)
            page_num = paginator.num_pages
        return reverse('forum-topic-detail', kwargs={'topic_pk':self.topic.pk})+'?page='+str(page_num)+'#'+str(self.pk)
         
    def get_event_object_url(self):
        posts = Post.objects.filter(topic=self.topic, is_active=True)
        page_num = 1
        if posts:
            paginator = Paginator(posts, PAGINATE_BY)
            page_num = paginator.num_pages
        return reverse('forum-topic-detail', kwargs={'topic_pk':self.topic.pk})+'?page='+str(page_num)+'&m=1&p='+str(self.pk)+'#'+str(self.pk)
