from django.db import models

class Word(models.Model):
    book = models.IntegerField()
    chapter = models.IntegerField()
    line = models.IntegerField()
    position = models.IntegerField()
    token = models.CharField(max_length=50)
    meaning = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.book} {self.line}:{self.chapter} {self.token}({self.meaning})'



