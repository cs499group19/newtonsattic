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

    models = map(lambda name: apps.get_model('scheduling', name), models_to_get)

    context = {'data': {}, 'DEBUG': settings.DEBUG}
    for model in models:
        context['data'][model.__name__] = serializers.serialize('json', model.objects.all())

    return render(request, 'scheduling/schedule.html', context)
