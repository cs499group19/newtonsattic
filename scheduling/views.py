import pprint
import re

import django.contrib.auth
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from . import models


@login_required(login_url='/login/')
def index(request):
    # Get all available schedules from database.
    # Used to populate load select box.
    context = {'schedules': models.Schedule.objects.all()}

    # If the user does not have permission to alter schedule objects,
    # (i.e. an instructor) redirect them to availability page.
    if not request.user.has_perm('scheduling.change_schedule'):
        return HttpResponseRedirect(reverse('availability'))

    return render(request, 'scheduling/index.html', context)


@login_required(login_url='/login/')
def create_new_schedule(request):
    # We only want to process POST requests.
    if request.POST:

        # Get name from form.
        name = request.POST.get('name')

        # if the name is empty, error.
        if name is None or not name.strip():
            messages.error(request, 'Schedule name must not be blank.')

            return HttpResponseRedirect(reverse('index'))

        # Otherwise, create a schedule with specified name.
        schedule = models.Schedule(name=name)
        schedule.save()

        messages.success(request, 'Schedule "{}" has been created!'.format(name))

        return HttpResponseRedirect(reverse('edit_schedule', args=(schedule.id,)))

    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/login/')
def edit_schedule(request, schedule_id):
    schedule = get_object_or_404(models.Schedule, pk=schedule_id)

    # models_to_get = [
    #     'Class',
    #     'Classroom',
    #     'Instructor'
    # ]

    # Get all models specified above.
    # model_set = map(lambda name: apps.get_model('scheduling', name), models_to_get)

    context = {
        'data': {},
        'weeks': list(range(1, 13)),
        'times': ['Morning', 'Afternoon'],
        'sorted': {}
    }

    # for week in context['weeks']:
    #     context['sorted'][week] = {}

    # for model in model_set:
    #     # Get all records associated with a particular model and serialize them.
    #     records = model.objects.all()
    #
    #     context[model.__name__] = records
    #     context['data'][model.__name__] = serializers.serialize('json', records)

    for course in models.Class.objects.all():
        for instructor in course.specialities.all():
            for availability in instructor.availability:
                time = availability[-1]
                week = availability[:2] if len(availability) == 3 else availability[:1]

                if week not in context:
                    context[week] = {}

                if time not in context[week]:
                    context[week][time] = []

                if course.type == 'FD' and not instructor.is_available_all_day(week):
                    continue

                context[week][time].append((course, instructor))

    # for week in context['weeks']:
    #     for instructor in context['Instructor']:
    #         for a in instructor.availability:
    #             myregex = re.escape(str(week)) + "[am]"
    #             if re.match(myregex, a):
    #                 for c in instructor.specialty.all():
    #                     if c in context['sorted'][week]:
    #                         context['sorted'][week][c].append(instructor)
    #                     else:
    #                         context['sorted'][week][c] = [instructor]

    # pprint.pprint(context)

    return render(request, 'scheduling/schedule.html', context)


@login_required(login_url='/login/')
def save_schedule(request, schedule_id):
    pass


@login_required(login_url='/login/')
def instructor_availability(request):
    context = {
        'weeks': range(1, 13),
    }

    # if there is no instructor object attached to this user,
    # display a warning and return. We do not want to attempt to
    # load/store data in this case.
    if not hasattr(request.user, 'instructor'):
        messages.warning(request, 'There is no instructor associated with your user account.')
        return render(request, 'scheduling/availability.html', context)

    # If this is a POST request, we are storing data.
    if request.POST:
        # get all inputs of the form \d[am]
        times = list(filter(lambda t: t[0].isdigit() and t[-1] in 'ma', request.POST.keys()))

        # set availabilities for logged in user
        request.user.instructor.availability = times
        request.user.instructor.save()

        messages.success(request, 'Your schedule availability has been updated!')

    # get availabilities for current user
    # used to pre check the boxes they have selected previously.
    context['checked'] = request.user.instructor.availability

    return render(request, 'scheduling/availability.html', context)


def register_user(request):
    # if this is a post request, we want to create a user.
    if request.POST:
        # get values submitted from form.
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        user_name = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        # create a user in the database with supplied information
        new_user = models.User.objects.create_user(user_name, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name

        new_user.save()

        messages.success(request, 'Account created successfully!')

        return HttpResponseRedirect(reverse('login'))

    # Otherwise, display registration form.
    return render(request, 'scheduling/registration.html')


def logout(request):
    django.contrib.auth.logout(request)

    return HttpResponseRedirect(reverse('login'))
