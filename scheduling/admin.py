from django.contrib import admin

from .models import Classroom
from .models import Schedule
from .models import Class
from .models import Instructor
from .models import Document

# Register your models here.

admin.site.register(Classroom)
admin.site.register(Schedule)
admin.site.register(Class)
admin.site.register(Instructor)
admin.site.register(Document)
