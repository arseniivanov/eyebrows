from django.db import models
import uuid

# Create your models here.

def scrambleName(instance, filename):
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)


class ShowImage(models.Model):
    image = models.ImageField('Uploaded Image', upload_to=scrambleName)
    text = models.TextField(max_length=140, default='Your Perfect Eyebrows')