# -*- coding: utf-8 -*-

from django import template
from ..models import Topic


register = template.Library()
"""
@register.inclusion_tag('mgof/tags/last_post_in_forum.html')
def forums_last_posts(num_posts):
    num_posts = 10
    if num_posts:
        num_posts = int(num_posts)
    topics = Topic.objects.filter(is_public=True).select_related('topic__forum').order_by(-'last_post_date')[:num_posts]
    print "Topics = "+str(topics)
    return {
            'topics': topics,
        }
"""    
    
class LastPosts(template.Node):
    
    def __init__(self, num_posts=10):
        topics = Topic.objects.filter().select_related('forum').order_by('-last_post_date')[:num_posts]
        topics_ok = [] 
        for topic in topics:
            if topic.forum.is_public is True:
                topics_ok.append(topic)
        self.topics = topics_ok
        
    def render(self, context):
        context['topics'] = self.topics
        return ''
    
def forums_last_posts(parser, token):
    return LastPosts()

register.tag('forums_last_posts', forums_last_posts)