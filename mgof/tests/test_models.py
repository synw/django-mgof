# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from autofixture import AutoFixture
from mqueue.models import MEvent
from mgof.models import Forum, Topic, Post
from mgof.tests.factory import create_forum, create_topic, create_post

# ------------- tests ---------------
class ForumTest(TestCase):
    
    def test_obj_creation(self):
        obj = create_forum()
        self.assertTrue(isinstance(obj, Forum))
        self.assertEqual(obj.title, "The forum")
        self.assertEqual(obj.__unicode__(), "The forum")
        self.assertEqual(obj.num_topics, 0)
        self.assertEqual(obj.num_posts, 0)
        self.assertTrue(obj.is_public)
        self.assertEqual(list(obj.authorized_groups.all()), [])
        self.assertEqual(obj.get_absolute_url(), reverse('forum-detail', kwargs={'forum_pk':obj.pk}))
        return
    
    
class TopicTest(TestCase):
    
    def test_obj_creation(self):
        obj = create_topic()
        self.assertTrue(isinstance(obj, Topic))
        self.assertEqual(obj.title, "The topic")
        self.assertEqual(obj.__unicode__(), "The topic")
        self.assertEqual(obj.num_views, 0)
        self.assertEqual(obj.num_posts, 0)
        self.assertTrue(obj.is_moderated)
        self.assertFalse(obj.is_closed)
        self.assertEqual(obj.get_absolute_url(), reverse('forum-topic-detail', kwargs={'topic_pk':obj.pk}))
        return
    

class PostTest(TestCase):
    
    def test_obj_creation(self):
        topic = create_topic()
        obj = create_post(topic)
        str_output = unicode(_(u'Post')+' '+str(obj.pk) )+': '+obj.content[:25]
        self.assertTrue(isinstance(obj, Post))
        self.assertEqual(obj.__unicode__(), str_output)
        self.assertEqual(obj.responded_to_pk, 0)
        self.assertEqual(obj.responded_to_username, '')
        self.assertEqual(obj.get_absolute_url(), reverse('forum-topic-detail', kwargs={'topic_pk':obj.topic.pk})+'?page=1#'+str(obj.pk))
        self.assertEqual(obj.get_event_object_url(), reverse('forum-topic-detail', kwargs={'topic_pk':obj.topic.pk})+'?page=1&m=1&p='+str(obj.pk)+'#'+str(obj.pk))
        self.assertTrue(topic.is_moderated)
        self.assertFalse(topic.is_closed)
        self.assertEqual(topic.num_views, 0)
        return
    
    def test_obj_deletion(self):
        forum = create_forum()
        topic = create_topic(forum=forum, pk=10)
        post1 = create_post(topic=topic)
        post2 = create_post(topic=topic)
        post3 = create_post(topic=topic)
        # fake these (handled in the create view)
        topic.num_posts = 3
        forum.num_posts = 3
        topic.save()
        forum.save()
        post3.delete()
        # check counters
        self.assertEqual(topic.num_posts, 2)
        self.assertEqual(forum.num_posts, 2)
        # topic should be deleted with his last post
        post2.delete()
        post1.delete()
        self.assertFalse(Topic.objects.filter(pk=10).exists())
        self.assertEqual(len(forum.topics.all()), 0)
        self.assertEqual(forum.num_posts, 0)
        
        return



