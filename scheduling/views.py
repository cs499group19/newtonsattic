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
        'weeks': list(range(1, 13)),
        'times': ['Morning', 'Afternoon'],
        'sorted': {}
    }

    for week in context['weeks']:
        context['sorted'][week] = []

    for model in models:
        # Get all records associated with a particular model and serialize them.
        records = model.objects.all()

        context[model.__name__] = records
        context['data'][model.__name__] = serializers.serialize('json', records)

    import random
    import pprint
    random.seed(15)
    for c in context['Class']:
        for week in context['weeks']:
            if random.random() > 0.51:
                context['sorted'][week].append(c)

    pprint.pprint(context['sorted'])

    # return render(request, 'scheduling/schedule.html', context)
    return render(request, 'scheduling/index.html', context)


@login_required(login_url='/login/')
def create_new_schedule(request):
    pass


@login_required(login_url='/login/')
def load_schedule(request, schedule_id):
    return


@login_required(login_url='/login/')
def instructor_availability(request):
    return render(request, 'scheduling/availability.html', {'weeks': range(1, 13)})
