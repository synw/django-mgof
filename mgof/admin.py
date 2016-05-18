# -*- coding: utf-8 -*-

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from mgof.models import Forum, Topic, Post


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'status', 'is_public','authorized_groups']
        widgets = {'status': forms.RadioSelect}
        

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'forum', 'is_moderated', 'is_closed', 'status', 'posted_by']
        widgets = {
                   'status': forms.RadioSelect,
                   }
       
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['topic', 'content', 'status', 'posted_by']
        widgets = {'status': forms.RadioSelect}
        

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    form = ForumForm
    date_hierarchy = 'edited'
    readonly_fields = [ 'num_topics', 'num_posts', 'editor', 'edited', 'created' ]
    list_display = ['title', 'num_topics', 'num_posts', 'is_public', 'status', 'edited']
    list_filter = ['status']
    search_fields = ['title', 'editor__username']
    
    def save_model(self, request, obj, form, change):
        obj.editor = request.user
        super(ForumAdmin, self).save_model(request, obj, form, change)
    

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    form = TopicForm
    date_hierarchy = 'edited'
    readonly_fields = [ 'num_posts', 'num_views', 'editor', 'edited', 'created' ]
    list_display = ['title', 'forum', 'num_posts', 'num_views', 'status', 'is_moderated', 'is_closed', 'edited']
    list_filter = ['status']
    search_fields = ['title', 'editor__username']
    
    def save_model(self, request, obj, form, change):
        obj.editor = request.user
        super(TopicAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    date_hierarchy = 'edited'
    readonly_fields = [ 'editor', 'edited', 'created' ]
    list_display = ['topic', 'pk', 'posted_by', 'status', 'edited']
    list_filter = ['status', 'topic__title']
    search_fields = ['title', 'editor__username', 'posted_by__username', 'topic__title']
    list_select_related = ['posted_by', 'topic']
    
    def save_model(self, request, obj, form, change):
        obj.editor = request.user
        obj.save()
        super(PostAdmin, self).save_model(request, obj, form, change)
        
        
        
        
        
