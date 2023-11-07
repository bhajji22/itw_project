from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class filedata(models.Model):
    Title = models.CharField(max_length=200)
    File = models.FileField(upload_to='shop')
    filechoices = [("image","image"),("video","video"),("audio","audio"),("text","text"),("others","others")]
    File_type = models.CharField(max_length=6,choices=filechoices)
    File_description = models.CharField(max_length=300)
    date_added = models.DateField()
    file_owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default='')
    file_access = models.ManyToManyField(User,related_name="access")

