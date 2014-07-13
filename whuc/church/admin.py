from django.contrib import admin
from church.models import EventType
from church.models import Language
from church.models import ChurchEvent
from church.models import EventDocument

# Register your models here.
admin.site.register(EventType)
admin.site.register(Language)
admin.site.register(ChurchEvent)
admin.site.register(EventDocument)
