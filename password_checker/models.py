from django.db import models

# Create your models here.

class Password(models.Model):
    hash = models.CharField(max_length=40, unique=True) 

    def __str__(self):
        return self.hash
