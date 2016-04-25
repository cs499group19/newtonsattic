from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Classroom
from .models import Schedule
from .models import Class
from .models import Instructor
# from .models import Document


class SchedulingAdmin(AdminSite):
    site_header = 'Newton\'s Attic Administration'
    site_title = 'Newton\'s Attic Admin'


admin_site = SchedulingAdmin(name='scheduling_admin')
# Register your models here.


admin_site.register(Classroom)
admin_site.register(Schedule)
admin_site.register(Class)
admin_site.register(Instructor)
# admin.site.register(Document)
