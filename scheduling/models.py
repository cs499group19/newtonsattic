from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import date


# Create your models here.


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    year = models.IntegerField(default=date.today().year)

    # I'm assuming the version is really
    # just what they name it so it's different from the auto primary key
    name = models.CharField(max_length=255)

    # to store the JSON
    schedule = models.TextField()

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=255)
    age_group = models.CharField(max_length=10)  # Just a written '??-??'

    # Room requirements need to match the actual classrooms
    room_requirement = models.ManyToManyField(Classroom, related_name='allowed_rooms')

    def __str__(self):
        return self.name


# Will this table also be used for helpers? Or a different one?
# If we use the same, maybe we should have a boolean saying if they need to specialize at all
class Instructor(models.Model):
    name = models.CharField(max_length=255)
    age_preferences = models.IntegerField(default=0)  # I'm assuming this would just be an age number
    # that they wouldn't want to teach below... We need to ask Dawn how she wants to do it
    availability = ArrayField(
        models.CharField(max_length=5)
    )

    # Dawn was assuming specialty was just the classes they could teach
    specialty = models.ManyToManyField(Class, related_name='specialities')

    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(max_length=255)
    for_class = models.ForeignKey(Class, on_delete=models.PROTECT)

    # I'm not sure if this is right
    document = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.name
