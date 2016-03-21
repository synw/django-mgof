# -*- coding: utf-8 -*-

from django import forms
from ckeditor.widgets import CKEditorWidget
from mgof.models import Post, Topic


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='public'))
    content.label = ''
    
    class Meta:
        model = Post
        fields = ['content']
        



