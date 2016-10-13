from django.conf.urls import url
from mgof.views import ForumsView, ForumView, TopicView, AddPostView, AddTopicView, set_topic_monitoring_level, ModerationQueueView, moderate_post, switch_open_topic


urlpatterns = [
    url(r'^post/add/(?P<forum_pk>[0-9]+)/(?P<topic_pk>[0-9]+)/(?P<post_pk>[0-9]+)/$', AddPostView.as_view(), name="forum-post-create"),
    url(r'^topic/add/(?P<forum_pk>[0-9]+)/$', AddTopicView.as_view(), name="forum-topic-create"),
    url(r'^topic/monitor/(?P<topic_pk>[0-9]+)/(?P<monitoring_level>[0-9]+)/$', set_topic_monitoring_level, name="forum-topic-set_monitoring"),
    url(r'^topic/switch/(?P<topic_pk>[0-9]+)/(?P<action>[0-9]+)/$', switch_open_topic, name="forum-topic-switch-open"),
    url(r'^moderate/(?P<post_pk>[0-9]+)/(?P<action>[0-9]+)/$', moderate_post, name="forum-post-moderate"),
    url(r'^topic/(?P<topic_pk>[0-9]+)/$', TopicView.as_view(), name="forum-topic-detail"),
    url(r'^(?P<forum_pk>[0-9]+)/$', ForumView.as_view(), name="forum-detail"),
    url(r'^moderation_queue/$', ModerationQueueView.as_view(), name="forum-moderation-queue"),
    url(r'^', ForumsView.as_view(), name="forums-index"),
    ]