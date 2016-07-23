# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from mgof.tests.factory import create_forum, create_topic, create_post


class ForumViewsTest(TestCase):
    
    @override_settings(MGOF_ENABLE_PRIVATE_FORUMS=True)
    def test_ForumsView(self):
        self.assertEqual(settings.MGOF_ENABLE_PRIVATE_FORUMS, True)
        #from mgof import conf
        #self.assertEqual(conf.ENABLE_PRIVATE_FORUMS, True)
        forum1 = create_forum()
        forum2 = create_forum(is_public=False)
        response = self.client.get(reverse('forums-index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['forums']), [forum1, forum2])
        self.assertTemplateUsed(response, 'mgof/index.html')
        self.assertFalse(response.context['is_moderator'])
        #self.assertEqual(response.context['forums'], [forum1])
        return