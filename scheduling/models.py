from datetime import date

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


def user_to_json(user: User):
    return {
        'id': user.id,
        'full_name': user.get_full_name()
    }


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)

    def to_json(self):
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

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'schedule': self.schedule
        }

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

    def to_json(self):
        rooms = [room.to_json() for room in self.room_requirement.all()]

        return {
            'id': self.id,
            'name': self.name,
            'age_group': self.age_group,
            'type': self.type,
            'room_requirement': rooms
        }

    def __str__(self):
        return self.name


# Will this table also be used for helpers? Or a different one?
# If we use the same, maybe we should have a boolean saying if they need to specialize at all
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    availability = ArrayField(
        models.CharField(max_length=5),
        default=list,
        blank=True,
        null=True
    )

    # Dawn was assuming specialty was just the classes they could teach
    specialty = models.ManyToManyField(Class, related_name='specialities')

    def is_available_in_morning(self, week):
        week_morning = '{}m'.format(week)

        return week_morning in self.availability

    def is_available_in_afternoon(self, week):
        week_afternoon = '{}a'.format(week)

        return week_afternoon in self.availability

    def is_available(self, week):
        return self.is_available_in_morning(week) or self.is_available_in_afternoon(week)

    def is_available_all_day(self, week):
        return self.is_available_in_afternoon(week) and self.is_available_in_afternoon(week)

    def to_json(self):
        specialties = [specialty.id for specialty in self.specialty.all()]

        return {
            'id': self.id,
            'user': user_to_json(self.user),
            'availability': self.availability,
            'specialty': specialties
        }

    def __str__(self):
        return self.user.username


class Document(models.Model):
    name = models.CharField(max_length=255)
    for_class = models.ForeignKey(Class, on_delete=models.PROTECT)

    # I'm not sure if this is right
    document = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.name


class WeekHeadingsSettings(models.Model):
    week1_title = models.CharField(max_length=255, default='Week 1')
    week2_title = models.CharField(max_length=255, default='Week 2')
    week3_title = models.CharField(max_length=255, default='Week 3')
    week4_title = models.CharField(max_length=255, default='Week 4')
    week5_title = models.CharField(max_length=255, default='Week 5')
    week6_title = models.CharField(max_length=255, default='Week 6')
    week7_title = models.CharField(max_length=255, default='Week 7')
    week8_title = models.CharField(max_length=255, default='Week 8')
    week9_title = models.CharField(max_length=255, default='Week 9')
    week10_title = models.CharField(max_length=255, default='Week 10')
    week11_title = models.CharField(max_length=255, default='Week 11')
    week12_title = models.CharField(max_length=255, default='Week 12')

    def name_for_week(self, week):
        return {
            '1': self.week1_title,
            '2': self.week2_title,
            '3': self.week3_title,
            '4': self.week4_title,
            '5': self.week5_title,
            '6': self.week6_title,
            '7': self.week7_title,
            '8': self.week8_title,
            '9': self.week9_title,
            '10': self.week10_title,
            '11': self.week11_title,
            '12': self.week12_title,
        }.get(str(week), '')

    def __str__(self):
        return 'Week Heading Settings'

