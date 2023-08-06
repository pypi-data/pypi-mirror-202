from django.db import models

class Model1(models.Model):
    name = models.CharField(max_length=100)
    image1 = models.ImageField(null=True)

    def __str__(self):
        return self.name

