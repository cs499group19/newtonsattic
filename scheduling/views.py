from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.core import serializers
from django.conf import settings

# Create your views here.


@login_required(login_url='/login/')
def index(request):
    models_to_get = [
        'Class',
        'Classroom',
        'Instructor',
        'Schedule'
    ]

    # Get all models specified above.
    models = map(lambda name: apps.get_model('scheduling', name), models_to_get)

    context = {
        'data': {},
        'weeks': range(1, 13),
        'times': ['Morning', 'Afternoon'],
        'DEBUG': settings.DEBUG
    }

    for model in models:
        # Get all records associated with a particular model and serialize them.
        records = model.objects.all()

        context[model.__name__] = records
        context['data'][model.__name__] = serializers.serialize('json', records)

    return render(request, 'scheduling/schedule.html', context)


@login_required(login_url='/login/')
def instructor_availability(request):
    return render(request, 'scheduling/availability.html', {'weeks': range(1, 13)})
