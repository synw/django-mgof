# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.http.response import Http404
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from braces.views import LoginRequiredMixin, MessageMixin
from mqueue.models import MEvent
from mgof.models import Forum, Topic, Post
from mgof.forms import PostForm
from mgof.utils import clean_post_data, user_is_moderator
from mgof.conf import LOGIN_URL, PAGINATE_BY, MODERATION_GROUP, MODERATION_LEVEL, MODERATION_PAGINATE_BY


class ForumsView(TemplateView):
    template_name = 'mgof/index.html'

    def get_context_data(self, **kwargs):
        context = super(ForumsView, self).get_context_data(**kwargs)
        forums = Forum.objects.filter(status=0).prefetch_related('topics')
        is_moderator = user_is_moderator(self.request.user)
        if is_moderator:
            event_classes = ['Object created', 'Object deleted']
            model = Post
            context['num_items_in_queue'] = MEvent.objects.count_for_model(model, event_classes)
        context['forums'] = forums
        context['is_moderator'] = is_moderator
        return context
    
    
class ForumView(ListView):
    template_name = 'mgof/forum_detail.html'
    paginate_by = PAGINATE_BY
    context_object_name = 'topics'
    
    def get_queryset(self):
        self.forum = get_object_or_404(Forum, status=0, pk=self.kwargs['forum_pk'])
        topics = Topic.objects.filter(status=0, forum=self.forum).order_by('-edited')
        return topics
    
    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['forum'] = self.forum
        context['is_moderator'] = user_is_moderator(self.request.user)
        return context


class TopicView(ListView):
    template_name = 'mgof/topic_detail.html'
    paginate_by = PAGINATE_BY
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.topic = get_object_or_404(Topic.objects.select_related('forum'), status=0, pk=self.kwargs['topic_pk'])
        self.forum = self.topic.forum
        qs = Post.objects.filter(topic=self.topic, status=0).select_related('editor')
        #~ record view if not comes from a pagination link
        if 'v' not in self.request.GET.keys():
            self.topic.num_views = self.topic.num_views+1
        self.topic.save()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(TopicView, self).get_context_data(**kwargs)
        context['forum'] = self.forum
        context['topic'] = self.topic
        return context
    
    
class AddTopicView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Topic
    fields = ['title']
    template_name = 'mgof/topic/create.html'
    login_url = LOGIN_URL+'?from=/forum/'
    
    def form_valid(self, form, **kwargs):
        self.forum = get_object_or_404(Forum, status=0, pk=self.kwargs['forum_pk'])
        if self.request.method == "POST":
            obj = form.save(commit=False)
            obj.title = form.cleaned_data['title']
            obj.forum = self.forum
            obj.monitoring_level = MODERATION_LEVEL
            obj.status = 1
        else: 
            raise Http404
        self.topic = obj
        #~ update forum counter
        self.forum.num_topics = self.forum.num_topics+1
        self.forum.save()
        return super(AddTopicView, self).form_valid(form)
            
    def get_success_url(self):
        return "%s?t=1" % reverse('forum-post-create', kwargs={'forum_pk': self.forum.pk, 'topic_pk': self.topic.pk, 'post_pk': 0})


class AddPostView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'mgof/post/create.html'
    login_url = LOGIN_URL+'?from=/forum/'
    
    def get_context_data(self, **kwargs):
            context = super(AddPostView, self).get_context_data(**kwargs)
            from_topic = None
            if 't' in self.request.GET.keys():
                from_topic = 1
            context['from_topic'] = from_topic
            return context
        
    def form_valid(self, form, **kwargs):
        is_moderator = user_is_moderator(self.request.user)
        if self.request.method == "POST":
            topic_pk = self.kwargs['topic_pk']
            post_pk = self.kwargs['post_pk']
            #~ get topic
            self.topic = topic = get_object_or_404(Topic.objects.select_related('forum'), pk=topic_pk)
            #~ get posts for topic
            self.posts = Post.objects.filter(topic=self.topic, status=0)
            #~ get related post information
            try:
                post_responded_to = self.posts.filter(pk=post_pk)[0]
                post_responded_to_username = post_responded_to.posted_by.username
                post_responded_to_pk = post_responded_to.posted_by.pk
            except:
                post_responded_to_username = ''
                post_responded_to_pk = 0
            obj = form.save(commit=False)
            #~ handle meta info
            obj.editor = self.request.user
            obj.responded_to_pk = post_responded_to_pk
            obj.responded_to_username = post_responded_to_username
            obj.topic = topic
            obj.content = clean_post_data(obj.content)
            #~ set monitoring level for post
            if not is_moderator:
                obj.monitoring_level = topic.monitoring_level
            else:
                obj.monitoring_level = 0
            obj.status = 0
            #~ counts for topic
            topic.num_posts = topic.num_posts+1
            topic.last_post_date = timezone.now()
            topic.last_post_username = self.request.user.username
            topic.status = 0
            topic.save()
            #~ counts for forum
            forum = topic.forum
            forum.num_posts = forum.num_posts+1
            forum.last_post_date = timezone.now()
            forum.last_post_username = self.request.user.username
            forum.save()
            self.messages.success(_(u'Your post has been saved'), extra_tags='save text-info fa-2x')
        else: 
            raise Http404
        self.post = obj
        return super(AddPostView, self).form_valid(form)

    def get_success_url(self):
        posts = self.posts
        page_num = 1
        if posts:
            paginator = Paginator(posts, PAGINATE_BY)
            page_num = paginator.num_pages
        return reverse('forum-topic-detail', kwargs={'topic_pk':self.topic.pk})+'?page='+str(page_num)+'#'+str(self.post.pk)


class ModerationQueueView(ListView):
    template_name = 'mgof/moderation_queue.html'
    paginate_by = MODERATION_PAGINATE_BY
    context_object_name = 'events'
    
    def get_queryset(self):
        is_moderator = user_is_moderator(self.request.user)
        if not is_moderator:
            raise Http404
        event_classes = ['Object created', 'Object deleted']
        model = Post
        qs = MEvent.objects.events_for_model(model, event_classes).select_related('user')
        return qs
    

@csrf_protect     
def set_topic_monitoring_level(request, topic_pk, monitoring_level):
    if request.is_ajax(): 
        if request.user.is_anonymous():
            raise Http404
        if request.user.is_superuser:
            is_moderator = True
        else:
            is_moderator = request.user.groups.filter(name=MODERATION_GROUP).exists()
        if not is_moderator:
            raise Http404     
        try:
            topic = Topic.objects.get(pk=topic_pk)
            topic.monitoring_level = int(monitoring_level)
            topic.save()
        except:
            pass
        return render_to_response('mgof/topic/set_monitoring.html',
                                    {'monitoring_level': monitoring_level, 'topic': topic},
                                    content_type="application/xhtml+xml"
                                    )
    else:
        if settings.DEBUG:
            print "Not ajax request for the 'set_topic_monitoring_level' view"
        raise Http404

