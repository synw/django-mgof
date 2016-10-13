# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse
from django.http.response import Http404
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from braces.views import LoginRequiredMixin, MessageMixin, GroupRequiredMixin
from mqueue.models import MEvent
from mgof.models import Forum, Topic, Post
from mgof.forms import PublicPostForm
from mgof.utils import clean_post_data, user_is_moderator, user_can_see_forum
from mgof.conf import LOGIN_URL, PAGINATE_BY, MODERATION_PAGINATE_BY, ENABLE_PRIVATE_FORUMS


class ForumsView(TemplateView, GroupRequiredMixin):
    template_name = 'mgof/index.html'

    def get_context_data(self, **kwargs):
        context = super(ForumsView, self).get_context_data(**kwargs)
        self.public_forums = []
        self.users_forums = []
        self.groups_forums = []
        if ENABLE_PRIVATE_FORUMS is True:
            all_forums = Forum.objects.filter(is_active=True).prefetch_related('topics', 'authorized_groups')
            for forum in all_forums:
                if user_can_see_forum(forum, self.request.user) is True:
                    if forum.is_restricted_to_groups is True:
                        self.groups_forums += [forum]
                    else:
                        if forum.is_public is True:
                            self.public_forums += [forum]
                        else:
                            self.users_forums += [forum]
        else:
            self.public_forums = Forum.objects.filter(is_active=True).prefetch_related('topics')
        is_moderator = user_is_moderator(self.request.user)
        if is_moderator:
            event_classes = ['Forum post']
            model = Post
            context['num_items_in_queue'] = MEvent.objects.count_for_model(model, event_classes)
        context['public_forums'] = self.public_forums
        context['users_forums'] = self.users_forums
        context['groups_forums'] = self.groups_forums
        context['is_moderator'] = is_moderator
        return context
    
    
class ForumView(ListView):
    template_name = 'mgof/forum_detail.html'
    paginate_by = PAGINATE_BY
    context_object_name = 'topics'
    
    def dispatch(self, request, *args, **kwargs):
        if ENABLE_PRIVATE_FORUMS:
            self.forum = get_object_or_404(Forum.objects.prefetch_related('authorized_groups'), is_active=True, pk=self.kwargs['forum_pk'])
            user_can_see_forum_ = user_can_see_forum(self.forum, request.user)
            if not user_can_see_forum_:
                MEvent.objects.create(
                                      name='Forum unauthorized access: forum '+str(self.forum.pk), 
                                      instance=self.forum, 
                                      event_class="Warning",
                                      user = request.user,
                                      request = request,
                                      )
                raise Http404
        else:
            self.forum = get_object_or_404(Forum, is_active=True, pk=self.kwargs['forum_pk'])
        return super(ForumView, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        topics = Topic.objects.filter(is_active=True, forum=self.forum).order_by('-edited')
        return topics
    
    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['forum'] = self.forum
        context['is_moderator'] = user_is_moderator(self.request.user)
        return context


class TopicView(ListView, GroupRequiredMixin):
    template_name = 'mgof/topic_detail.html'
    paginate_by = PAGINATE_BY
    context_object_name = 'posts'
    
    def dispatch(self, request, *args, **kwargs):
        if ENABLE_PRIVATE_FORUMS:
            self.topic = get_object_or_404(Topic.objects.prefetch_related('forum__authorized_groups'), is_active=True, pk=self.kwargs['topic_pk'])
            self.forum = self.topic.forum
            user_can_see_forum_ = user_can_see_forum(self.forum, request.user)
            if not user_can_see_forum_:
                MEvent.objects.create(
                                      name='Forum unauthorized access: view topic', 
                                      instance=self.topic, 
                                      event_class="Warning",
                                      user = request.user,
                                      request = request,
                                      )
                raise Http404
        else:
            self.topic = get_object_or_404(Topic.objects.select_related('forum'), is_active=True, pk=self.kwargs['topic_pk'])
            self.forum = self.topic.forum
        return super(TopicView, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = Post.objects.filter(topic=self.topic, is_active=True).select_related('editor')
        #~ record view if not comes from a pagination link
        if 'v' not in self.request.GET.keys():
            self.topic.num_views = self.topic.num_views+1
        self.from_moderation = False
        self.topic.save()
        return qs
    
    def get_context_data(self, **kwargs):
        is_moderator = user_is_moderator(self.request.user)
        context = super(TopicView, self).get_context_data(**kwargs)
        #~ does it come from the moderation queue?
        if 'm' in self.request.GET.keys() and is_moderator:
            #~ get the moderated post number
            if 'p' in self.request.GET.keys():
                context['post_to_moderate_pk'] = int(self.request.GET['p']) 
                context['comes_from_moderation'] = True
        context['forum'] = self.forum
        context['topic'] = self.topic
        return context
    
    
class AddTopicView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Topic
    fields = ['title']
    template_name = 'mgof/topic/create.html'
    login_url = LOGIN_URL+'?from=/forum/'
    
    def dispatch(self, request, *args, **kwargs):
        if ENABLE_PRIVATE_FORUMS:
            self.forum = get_object_or_404(Forum.objects.prefetch_related('authorized_groups'), is_active=True, pk=self.kwargs['forum_pk'])
            user_can_see_forum_ = user_can_see_forum(self.forum, request.user)
            if not user_can_see_forum_:
                MEvent.objects.create(
                                      name='Forum unauthorized access: create topic', 
                                      instance=self.forum, 
                                      event_class="Warning",
                                      user = request.user,
                                      request = request,
                                      )
                raise Http404
        else:
            self.forum = get_object_or_404(Forum, is_active=True, pk=self.kwargs['forum_pk'])
        return super(AddTopicView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form, **kwargs):
        if self.request.method == "POST":
            obj = form.save(commit=False)
            obj.title = form.cleaned_data['title']
            obj.forum = self.forum
            # set status to orphaned until a first post is related to the topic
            #obj.is_active = False
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
    form_class = PublicPostForm
    template_name = 'mgof/post/create.html'
    login_url = LOGIN_URL+'?from=/forum/'
    
    def dispatch(self, request, *args, **kwargs):
        if ENABLE_PRIVATE_FORUMS:
            self.topic = get_object_or_404(Topic.objects.select_related('forum'), pk=self.kwargs['topic_pk'])
            if self.topic.is_closed:
                raise Http404
            self.forum = self.topic.forum
            user_can_see_forum_ = user_can_see_forum(self.forum, request.user)
            if not user_can_see_forum_:
                MEvent.objects.create(
                                      name='Forum unauthorized access: create post', 
                                      instance=self.forum, 
                                      event_class="Warning",
                                      user = request.user,
                                      request = request,
                                      )
                raise Http404
        else:
            self.topic = get_object_or_404(Topic.objects.select_related('forum'), pk=self.kwargs['topic_pk'])
            self.forum = self.topic.forum
        return super(AddPostView, self).dispatch(request, *args, **kwargs)
    
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
            if self.topic.is_closed:
                raise Http404
            topic = self.topic
            post_pk = self.kwargs['post_pk']
            #~ get posts for topic
            self.posts = Post.objects.filter(topic=self.topic, is_active=True)
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
            obj.posted_by = self.request.user
            obj.responded_to_pk = post_responded_to_pk
            obj.responded_to_username = post_responded_to_username
            obj.topic = topic
            obj.content = clean_post_data(obj.content)
            obj.is_active = True
            #~ counts for topic
            topic.num_posts = topic.num_posts+1
            topic.last_post_date = timezone.now()
            topic.last_post_username = self.request.user.username
            #topic.status = 0
            topic.save()
            #~ counts for forum
            forum = topic.forum
            forum.num_posts = forum.num_posts+1
            forum.last_post_date = timezone.now()
            forum.last_post_username = self.request.user.username
            forum.save()
            self.post = obj
            # moderation check
            if topic.is_moderated and is_moderator is False:
                obj.save()
                MEvent.objects.create(
                                model = Post, 
                                name = 'Post from forum : '+obj.topic.title,
                                instance = obj,
                                user = obj.posted_by,
                                event_class = 'Forum post',
                                request = self.request,
                                notes = obj.content
                                )
            self.messages.success(_(u'Your post has been saved'), extra_tags='save text-info fa-2x')
        else: 
            raise Http404
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
        event_classes = ['Forum post']
        model = Post
        qs = MEvent.objects.events_for_model(model, event_classes).select_related('user')
        self.num_events = qs.count()
        return qs

    def get_context_data(self, **kwargs):
        context = super(ModerationQueueView, self).get_context_data(**kwargs)
        context['num_events'] = self.num_events
        return context
    
    

@csrf_protect     
def set_topic_monitoring_level(request, topic_pk, monitoring_level):
    if request.is_ajax(): 
        if request.user.is_anonymous():
            raise Http404
        is_moderator = user_is_moderator(request.user)
        if not is_moderator:
            raise Http404     
        topic = Topic.objects.get(pk=topic_pk)
        topic.is_moderated = True
        if int(monitoring_level) == 0:
            topic.is_moderated = False
        topic.save()
        return render_to_response('mgof/topic/set_monitoring.html',
                                    {'monitoring_level': monitoring_level, 'topic': topic},
                                    content_type="application/xhtml+xml"
                                    )
    else:
        if settings.DEBUG:
            print "Not ajax request for the 'set_topic_monitoring_level' view"
        raise Http404
    
    
@csrf_protect     
def moderate_post(request, post_pk, action):
    if request.is_ajax(): 
        is_moderator = user_is_moderator(request.user)
        if not is_moderator:
            raise Http404
        #~ retrieve post
        try:     
            post = Post.objects.get(pk=post_pk) 
        except Post.ObjectDoesNotExist:
            if settings.DEBUG:
                return HttpResponse('Post not found')
            else:
                return HttpResponse('')
        #~ prepare action
        msg = ''
        predelete_post = post
        del_event = False
        if action == '0':
            del_event = True
            msg = _(u'Post rejected')
        elif action == '1':
            del_event = True
            msg = _(u'Post validated')
        #~ delete event
        if del_event:
            event = None
            events  = MEvent.objects.events_for_object(predelete_post)
            for event in events:
                if event.event_class == "Forum post":
                    event = event
                    break
            if not event:
                if settings.DEBUG:
                    return HttpResponse('Event not found '+str(events))
                else:
                    return HttpResponse('')
            event.delete()
        #~ process action
        if action == '0':
            post.delete()
        return render_to_response('mgof/post/moderate_success_actionbar.html', {'message':msg})
    else:
        raise Http404
    
@csrf_protect     
def switch_open_topic(request, topic_pk, action):
    if request.is_ajax():
        is_moderator = user_is_moderator(request.user)
        if not is_moderator:
            raise Http404
        try:
            topic=Topic.objects.get(pk=int(topic_pk))
        except:
            MEvent.objects.create(
                                  name = "Can not retrieve post ('switch_open_post' view)",
                                  event_class ="Warning",
                                  request = request,
                                  )
            return
        if int(action) == 0:
            topic.is_closed = True
        elif int(action) == 1:
            topic.is_closed = False
        topic.save()
        return render_to_response('mgof/topic/switch_open.html',
                                    {'topic': topic},
                                    content_type="application/xhtml+xml"
                                    )
    else:
        raise Http404




