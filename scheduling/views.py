import json

import django.contrib.auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
        try:
            schedule.save()
        except:
            messages.error(request, 'The schedule could not be created.')
            return HttpResponseRedirect(reverse('index'))

        messages.success(request, 'Schedule "{}" has been created!'.format(name))

        return HttpResponseRedirect(reverse('edit_schedule', args=(schedule.id,)))

    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/login/')
def edit_schedule(request, schedule_id):
    # If the user does not have permission to alter schedule objects,
    # (i.e. an instructor) redirect them to availability page.
    if not request.user.has_perm('scheduling.change_schedule'):
        return HttpResponseRedirect(reverse('availability'))

    schedule = get_object_or_404(models.Schedule, pk=schedule_id)

    context = {
        'weeks': list(range(1, 13)),
        'times': ['Morning', 'Afternoon'],
        # This is only here to prevent an error from occurring in the template.
        'sorted': {}
    }

    data = {}
    for course in models.Class.objects.all():
        for instructor in course.specialities.all():
            for availability in instructor.availability:
                time = availability[-1]
                week = availability[:2] if len(availability) == 3 else availability[:1]

                if week not in data:
                    data[week] = {}

                if time not in data[week]:
                    data[week][time] = []

                if course.type == 'FD' and not instructor.is_available_all_day(week):
                    continue

                data[week][time].append((course.to_json(), instructor.to_json()))

    context['schedule_id'] = schedule.id
    context['data'] = json.dumps(data, sort_keys=True)
    context['schedule'] = schedule.schedule

    tab_settings = models.WeekHeadingsSettings.objects.first()

    if tab_settings is None:
        tab_settings = models.WeekHeadingsSettings()
        try:
            tab_settings.save()
        except:
            messages.error(request, 'Unknown database error. Please contact the system administrator.')
            return HttpResponseRedirect(reverse('index'))

    context['tab_settings'] = {k: tab_settings.name_for_week(k) for k in range(1, 13)}

    return render(request, 'scheduling/schedule.html', context)


@login_required(login_url='/login/')
def save_schedule(request):
    # If the user does not have permission to alter schedule objects,
    # (i.e. an instructor) redirect them to availability page.
    if not request.user.has_perm('scheduling.change_schedule'):
        return HttpResponseRedirect(reverse('availability'))

    if request.POST:
        schedule = get_object_or_404(models.Schedule, pk=request.POST.get('schedule_id'))

        schedule.schedule = request.POST.get('schedule')
        try:
            schedule.save()
        except:
            messages.error(request, 'Schedule "{}" could not be saved.'.format(schedule.name))
            return HttpResponseRedirect(reverse('index'))

        messages.success(request, 'Your schedule have been saved successfully!')

    return HttpResponseRedirect(reverse('index'))


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
        try:
            request.user.instructor.save()
        except:
            messages.error(request, 'Your availability could not be saved. Please contact the system administrator.')
            return HttpResponseRedirect(reverse('index'))

        messages.success(request, 'Your schedule availability has been updated!')

    # get availabilities for current user
    # used to pre check the boxes they have selected previously.
    context['checked'] = request.user.instructor.availability

    tab_settings = models.WeekHeadingsSettings.objects.first()

    if tab_settings is None:
        tab_settings = models.WeekHeadingsSettings()
        tab_settings.save()

    context['tab_settings'] = {k: tab_settings.name_for_week(k) for k in range(1, 13)}

    return render(request, 'scheduling/availability.html', context)


@login_required(login_url='/login/')
def edit_schedule_tabs(request):
    context = {}

    # If the user does not have permission to alter schedule objects,
    # (i.e. an instructor) redirect them to availability page.
    if not request.user.has_perm('scheduling.change_schedule'):
        return HttpResponseRedirect(reverse('availability'))

    tab_settings = models.WeekHeadingsSettings.objects.first()

    if tab_settings is None:
        tab_settings = models.WeekHeadingsSettings()
        tab_settings.save()

    if request.POST:
        tab_settings.week1_title = request.POST.get('1', '')
        tab_settings.week2_title = request.POST.get('2', '')
        tab_settings.week3_title = request.POST.get('3', '')
        tab_settings.week4_title = request.POST.get('4', '')
        tab_settings.week5_title = request.POST.get('5', '')
        tab_settings.week6_title = request.POST.get('6', '')
        tab_settings.week7_title = request.POST.get('7', '')
        tab_settings.week8_title = request.POST.get('8', '')
        tab_settings.week9_title = request.POST.get('9', '')
        tab_settings.week10_title = request.POST.get('10', '')
        tab_settings.week11_title = request.POST.get('11', '')
        tab_settings.week12_title = request.POST.get('12', '')

        try:
            tab_settings.save()
        except:
            messages.error(request, 'Your settings could not be updated.')
            return HttpResponseRedirect(reverse('index'))

        messages.success(request, 'Tab settings have been successfully updated.')

    context['weeks'] = list(range(1, 13))
    context['tab_settings'] = {k: tab_settings.name_for_week(k) for k in range(1, 13)}

    return render(request, 'scheduling/tab_settings.html', context)


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
