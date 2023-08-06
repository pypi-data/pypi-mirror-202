from django.db import models
from django.contrib import admin

# Create your models here.
class Model1(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


admin.site.register(Model1)