import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context
from church.models import EventDocument
from church.models import EventType
from church.models import ChurchEvent
from church.models import Language
from church.forms import LanguageForm
from church.forms import EventTypeForm
from church.forms import EventDocumentForm
from church.forms import ChurchEventDocForm
from church.forms import ChurchEventForm

# Create your views here.
def index(request):
    userauth = request.user.is_authenticated()
    return render(request, 'church/home.html', 
                      {'userauth': userauth})

def action(request, action=''):
    userauth = request.user.is_authenticated()
    if action == 'where/':
        return render(request, 'church/where.html', 
                      {'userauth': userauth})
    elif action == 'contact/':
        return render(request, 'church/contact.html', 
                      {'userauth': userauth})
    elif action == 'mission/':
        return render(request, 'church/mission.html', 
                      {'userauth': userauth})
    elif action == 'services/':
        services = ChurchEvent.objects.filter(eventType__eventType="service")
        services.exclude(date__gte=(datetime.date.today()-datetime.timedelta(35)))
        services.order_by("-date")        
        services.select_related()
        return render(request, 'church/services.html', 
                      {'services': services,
                       'userauth': userauth})
    else:
        return render(request, 'church/home.html', 
                      {'userauth': userauth})

@login_required
def staff(request, action=''):
    """
    Staff pages manage the contents of the website
    """
    logger = logging.getLogger('whuc')
    userauth = request.user.is_authenticated()
    
    if action == 'language/':
        if request.method == 'POST': # If the form has been submitted...
            languageForm = LanguageForm(request.POST)
            if languageForm.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                languageForm.save()
        
        languages = Language.objects.all()
        languageForm = LanguageForm()    
        return render(request, 'church/language.html', 
                                  {'languages': languages,
                                   'form': languageForm,
                                   'userauth': userauth})
    
    elif action == 'eventtype/':
        if request.method == 'POST': # If the form has been submitted...
            eventtypeForm = EventTypeForm(request.POST)
            if eventtypeForm.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                eventtypeForm.save()
            
        eventtypes = EventType.objects.all()
        eventtypeForm = EventTypeForm()    
        return render(request, 'church/eventtype.html', 
                                  {'eventtypes': eventtypes,
                                   'form': eventtypeForm,
                                   'userauth': userauth})
    
    elif action == 'churchevent/': 
        try:
            churchevent = ChurchEvent.objects.latest('date')
        except:
            churchevent = None
        
        if request.method == 'POST': # If the form has been submitted...
            # churcheventselection = SelectChurchEventForm(request=POST)
            newevent = ChurchEventForm(request.POST)

            if newevent.is_valid():
                logger.info('valid event')

                thiseventType = newevent.cleaned_data['eventType']
                thispresenter = newevent.cleaned_data['presenter']
                thisdate = newevent.cleaned_data['date']
                
                try:
                    churchevent = ChurchEvent.objects.get(
                                            eventType=thiseventType,
                                            presenter=thispresenter,
                                            date=thisdate)
                                    
                except:
                    logger.info('could not find this event')
                    churchevent = newevent.save()

            else:
                thiseventType = request.POST['eventType']
                thispresenter = request.POST['presenter']
                thisdate = datetime.date(int(request.POST['date_year']),
                                         int(request.POST['date_month']),
                                         int(request.POST['date_day']))

                try:
                    churchevent = ChurchEvent.objects.get(
                                            eventType=thiseventType,
                                            presenter=thispresenter,
                                            date=thisdate)
                                    
                except:
                    logger.info('could not find this event')
                    churchevent = ChurchEvent.objects.latest('date')
                
            # elif churcheventselection.is_valid():
            #     key = int(churcheventselection.cleaned_data['value'])
            #     churchevent = ChurchEvents.objects.filter(pk=key)
            
            eventdoc = EventDocument(churchEvent=churchevent)
            churcheventdocForm = ChurchEventDocForm(request.POST,
                                                    request.FILES,
                                                    instance=eventdoc)
            if churcheventdocForm.is_valid():
                churcheventdocForm.save()
                
        # selectchurcheventForm = SelectChurchEventForm(instance=churchevent)
        churcheventForm = ChurchEventForm(instance=churchevent)
        churcheventdocForm = ChurchEventDocForm()
        eventdocs = EventDocument.objects.filter(churchEvent=churchevent)
        
        return render(request, 'church/churchevent.html', 
                                  {'churcheventform': churcheventForm,
                                   'eventdocform': churcheventdocForm,
                                   'eventdocs': eventdocs,
                                   'userauth': userauth})
