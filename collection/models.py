from django.db import models
# Create your models here.
import datetime
import os

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

class Item(models.Model):
    
    imageOriginal = models.ImageField(upload_to=filepath, null=True, blank=True)
    imageProcessed1 = models.ImageField(upload_to=filepath, null=True, blank=True)
    imageProcessed2 = models.ImageField(upload_to=filepath, null=True, blank=True)
    imageProcessed3 = models.ImageField(upload_to=filepath, null=True, blank=True)
    imageProcessed4 = models.ImageField(upload_to=filepath, null=True, blank=True)
    original_image_identifier = models.CharField(max_length=255, blank=True, null=True)
