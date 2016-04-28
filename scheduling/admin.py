from django.contrib.admin import AdminSite

from .models import Class
from .models import Classroom
from .models import Instructor
from .models import Schedule


class SchedulingAdmin(AdminSite):
    site_header = 'Newton\'s Attic Administration'
    site_title = 'Newton\'s Attic Admin'


admin_site = SchedulingAdmin(name='scheduling_admin')

admin_site.register(Classroom)
admin_site.register(Schedule)
admin_site.register(Class)
admin_site.register(Instructor)
# admin.site.register(Document)
