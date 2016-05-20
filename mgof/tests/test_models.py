# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from autofixture import AutoFixture
from mgof.models import Forum, Topic, Post

# ------------- objects factory ---------------
def create_forum():
    obj = Forum.objects.create(title='The forum')
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
        obj = create_post()
        str_output = unicode(_(u'Post')+' '+str(+obj.pk) )+': '+obj.content[:25]
        self.assertTrue(isinstance(obj, Post))
        self.assertEqual(obj.__unicode__(), str_output)
        self.assertEqual(obj.responded_to_pk, 0)
        self.assertEqual(obj.responded_to_username, '')
        self.assertEqual(obj.get_absolute_url(), reverse('forum-topic-detail', kwargs={'topic_pk':obj.topic.pk})+'?page=1#'+str(obj.pk))
        self.assertEqual(obj.get_event_object_url(), reverse('forum-topic-detail', kwargs={'topic_pk':obj.topic.pk})+'?page=1&m=1&p='+str(obj.pk)+'#'+str(obj.pk))
        return
    
    def test_obj_deletion(self):
        forum = create_forum()
        topic = create_topic(forum=forum, pk=10)
        post1 = create_post(topic=topic)
        post2 = create_post(topic=topic)
        post3 = create_post(topic=topic)
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
        self.assertEqual(forum.num_posts, 0)
        return



