from django.db import models

# Create your models here.
#class used for uploadind apks
class apkUpload(models.Model):
	docfile = models.FileField(upload_to='apks')