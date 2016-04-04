# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from mqueue.models import MEvent
from mqueue.conf import bcolors
from mgof.models import Forum, Topic, Post

    
def mmessage_save(sender, instance, created, **kwargs):
    has_monitoring_level=getattr(instance, 'monitoring_level', None)
    if has_monitoring_level:
        create_event = False
        event_class = ''
        classname = instance.__class__.__name__
        if created:
            if instance.monitoring_level >= 1:
                create_event = True
                event_class = classname+' created'
        else:
            if instance.monitoring_level == 2:
                create_event = True
                event_class = classname+' edited'
        if create_event:
            #~ create event
            #admin_url = reverse('admin:%s_%s_change' %(instance._meta.app_label,  instance._meta.model_name),  args=[instance.id] )
            title = str(instance.pk)
            try:
                title = instance.title
            except:
                pass
            MEvent.objects.create(
                        model = instance.__class__, 
                        name = classname+': '+title, 
                        obj_pk = instance.pk, 
                        user = instance.posted_by,
                        #admin_url = admin_url,
                        event_class = event_class,
                        )
        if settings.DEBUG:
            print bcolors.SUCCESS+'Event'+bcolors.ENDC+' : '+event_class      
    return    


post_save.connect(mmessage_save, Topic)
post_save.connect(mmessage_save, Post)




    