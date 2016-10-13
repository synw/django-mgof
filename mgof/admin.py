# -*- coding: utf-8 -*-

from django.contrib import admin
from mgof.models import Forum, Topic, Post
from mgof.forms import ForumForm, TopicForm, PostForm
        

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    form = ForumForm
    date_hierarchy = 'edited'
    readonly_fields = [ 'num_topics', 'num_posts', 'editor', 'edited', 'created' ]
    list_display = ['title', 'num_topics', 'num_posts', "is_public", "is_restricted_to_groups", 'is_active', 'is_moderated', 'edited']
    list_filter = ['is_active']
    search_fields = ['title', 'editor__username']
    filter_horizontal = ('authorized_groups',)
    
    def save_model(self, request, obj, form, change):
        obj.editor = request.user
        super(ForumAdmin, self).save_model(request, obj, form, change)
    

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    form = TopicForm
    date_hierarchy = 'edited'
    readonly_fields = [ 'num_posts', 'num_views', 'editor', 'edited', 'created' ]
    list_display = ['title', 'forum', 'num_posts', 'num_views', 'is_active', 'is_moderated', 'is_closed', 'edited']
    list_filter = ['is_active']
    search_fields = ['title', 'editor__username']
    
    def save_model(self, request, obj, form, change):
        obj.editor = request.user
        super(TopicAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    date_hierarchy = 'edited'
    readonly_fields = [ 'editor', 'edited', 'created' ]
    list_display = ['topic', 'pk', 'posted_by', 'is_active', 'edited']
    list_filter = ['is_active', 'topic__title']
    search_fields = ['title', 'editor__username', 'posted_by__username', 'topic__title']
    list_select_related = ['posted_by', 'topic']
    
    def save_model(self, request, obj, form, change):
        obj.editor = request.user
        obj.save()
        super(PostAdmin, self).save_model(request, obj, form, change)
