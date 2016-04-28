import pprint
import re

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
    context = {'schedules': models.Schedule.objects.all()}

    return render(request, 'scheduling/index.html', context)


@login_required(login_url='/login/')
def create_new_schedule(request):
    name = request.POST.get('name')

    if name is None or not name.strip():
        messages.error(request, 'Schedule name must not be blank.')

        return HttpResponseRedirect(reverse('index'))

    schedule = models.Schedule(name=name)
    schedule.save()

    messages.success(request, 'Schedule "{}" has been created!'.format(name))

    return HttpResponseRedirect(reverse('edit_schedule', args=(schedule.id,)))


@login_required(login_url='/login/')
def edit_schedule(request, schedule_id):
    schedule = get_object_or_404(models.Schedule, pk=schedule_id)

    models_to_get = [
        'Class',
        'Classroom',
        'Instructor'
    ]

    # Get all models specified above.
    model_set = map(lambda name: apps.get_model('scheduling', name), models_to_get)

    context = {
        'data': {},
        'weeks': list(range(1, 13)),
        'times': ['Morning', 'Afternoon'],
        'sorted': {}
    }

    for week in context['weeks']:
        context['sorted'][week] = {}

    for model in model_set:
        # Get all records associated with a particular model and serialize them.
        records = model.objects.all()

        context[model.__name__] = records
        context['data'][model.__name__] = serializers.serialize('json', records)

    for week in context['weeks']:
        for instructor in context['Instructor']:
            for a in instructor.availability:
                myregex = re.escape(str(week)) + "[am]"
                if re.match(myregex, a):
                    for c in instructor.specialty.all():
                        if c in context['sorted'][week]:
                            context['sorted'][week][c].append(instructor)
                        else:
                            context['sorted'][week][c] = [instructor]

    pprint.pprint(context['sorted'])

    return render(request, 'scheduling/schedule.html', context)


@login_required(login_url='/login/')
def instructor_availability(request):
    if request.POST:
        messages.success(request, 'Your schedule availability has been updated!')
        times = filter(lambda t: t[0].isdigit() and t[-1] in 'ma', request.POST.keys())

    return render(request, 'scheduling/availability.html', {'weeks': range(1, 13)})
