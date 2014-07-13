from django.forms.extras.widgets import SelectDateWidget
from django import forms
from django.forms import ModelForm
from church.models import EventType
from church.models import Language
from church.models import ChurchEvent
from church.models import EventDocument

# Create your models here.
class EventTypeForm(ModelForm):
    class Meta:
        model = EventType
        fields = ['eventType']
    
class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ['language']

class ChurchEventForm(ModelForm):
    class Meta:
        model = ChurchEvent
        fields = ['eventType', 'presenter', 'date']
        widgets={'date': SelectDateWidget}

#class SelectChurchEventForm(forms.RadioSelect):
#    currentevents = ChurchEvent.objects.order_by(-date)[:5]
#    churcheventselectors = [(e.id, str(e)) for e in churchevents]
#    return RadioSelect(choices=churcheventselectors)

class EventDocumentForm(ModelForm):
    class Meta:
        model = EventDocument
        fields = ['churchEvent', 'language', 'title', 'filepath']

class ChurchEventDocForm(ModelForm):
    class Meta:
        model = EventDocument
        exclude = ['churchEvent']
    
