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
        context['sorted'][week] = {}

    for model in models:
        # Get all records associated with a particular model and serialize them.
        records = model.objects.all()

        context[model.__name__] = records
        context['data'][model.__name__] = serializers.serialize('json', records)

    '''import random
    import pprint
    random.seed(15)
    for c in context['Class']:
        for week in context['weeks']:
            if random.random() > 0.51:
                context['sorted'][week].append(c)

    pprint.pprint(context['sorted'])'''

    import pprint
    import re
    from scheduling.models import Instructor

    for week in context['weeks']:
        for instructor in Instructor.objects.all():
            for a in instructor.availability:
                myregex = re.escape(str(week))+"[am]"
                if (re.match(myregex, a)):
                    for c in instructor.specialty.all():
                        if c in context['sorted'][week]:
                            context['sorted'][week][c].append(instructor)
                        else:
                            context['sorted'][week][c] = [instructor]
    pprint.pprint(context['sorted'])

    return render(request, 'scheduling/schedule.html', context)


@login_required(login_url='/login/')
def instructor_availability(request):
    return render(request, 'scheduling/availability.html', {'weeks': range(1, 13)})
