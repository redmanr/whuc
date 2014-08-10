from django.db import models
from datetime import date

# Create your models here.
class EventType(models.Model):
    """
    A list of event types that will be associated with
    public documents.  This will be used to create a picklist 
    for ChurchEvents.
    """
    eventType = models.CharField(max_length=30)

    def __unicode__(self):
        """
        Event type
        """
        return self.eventType
    
class Language(models.Model):
    """
    A list of languages that will be associated with
    public documents.  This will be used to create a picklist 
    for ChurchEvents.
    """
    language = models.CharField(max_length=20)
    
    def __unicode__(self):
        """
        Language name, in unicode so can use proper characterset.
        """
        return self.language

class ChurchEvent(models.Model):
    """
    Church events are associated with documents that will be 
    uploaded through a password-protected admin page to 
    MEDIA_ROOT and will then be available for public download.
    """
    eventType = models.ForeignKey(EventType) 
    presenter = models.CharField(max_length=50)
    date = models.DateTimeField()
    
    class Meta:
        ordering = ['date']
    
    def __unicode__(self):
        """
        Unicode string representation of the sermon,
        which will be abbreviated at first.
        """
        return '\n'.join([
            'Presenter: ' + self.presenter,
            'Date: ' + date(self.date).isoformat()])

class EventDocument(models.Model):
    """
    A list of  public documentsassociated with a ChurchEvent.
    """
    churchEvent = models.ForeignKey('ChurchEvent')
    language = models.ForeignKey(Language)
    title = models.CharField(max_length=200)
    filepath = models.FileField(upload_to='upload')

    def __unicode__(self):
        """
        Unicode string representation of the sermon,
        which will be abbreviated at first.
        """
        return '\n'.join([
            'Title: ' + self.title])
    