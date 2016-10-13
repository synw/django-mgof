# -*- coding: utf-8 -*-

from django import forms
from ckeditor.widgets import CKEditorWidget
from mgof.models import Post, Topic, Forum


class PublicPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='public'))
    content.label = ''
    
    class Meta:
        model = Post
        fields = ['content']

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'is_active', 'is_moderated', 'is_public', "is_restricted_to_groups", 'authorized_groups']
        

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'forum', 'is_moderated', 'is_closed', 'is_active', 'posted_by']
       
        
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    content.label = ''
    
    class Meta:
        model = Post
        fields = ['topic', 'content', 'is_active', 'posted_by']



