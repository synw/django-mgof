from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

class MgofConfig(AppConfig):
    name = "mgof"
    verbose_name = _(u"Forums")
    
    def ready(self):
        pass