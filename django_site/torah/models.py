from django.db import models

class Word(models.Model):
    name = models.CharField(max_length=200, unique=True) # paleo hebrew
    translation = models.CharField(max_length = 200, default="") # englis translation