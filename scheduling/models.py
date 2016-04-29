from datetime import date

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)

    def json_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'capacity': self.capacity
        }

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
    HALF_DAY = 'HD'
    FULL_DAY = 'FD'

    TYPE_CHOICES = (
        (HALF_DAY, 'Half Day'),
        (FULL_DAY, 'Full Day')
    )

    name = models.CharField(max_length=255)

    age_group = models.CharField(max_length=10)

    type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=HALF_DAY)

    # Room requirements need to match the actual classrooms
    room_requirement = models.ManyToManyField(Classroom, related_name='allowed_rooms')

    def __str__(self):
        return self.name


# Will this table also be used for helpers? Or a different one?
# If we use the same, maybe we should have a boolean saying if they need to specialize at all
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    availability = ArrayField(
        models.CharField(max_length=5)
    )

    # Dawn was assuming specialty was just the classes they could teach
    specialty = models.ManyToManyField(Class, related_name='specialities')

    def __str__(self):
        return self.user.username


class Document(models.Model):
    name = models.CharField(max_length=255)
    for_class = models.ForeignKey(Class, on_delete=models.PROTECT)

    # I'm not sure if this is right
    document = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.name
