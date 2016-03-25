from django.db import models

# Create your models here.


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name
