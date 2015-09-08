from django.contrib import admin
from notify_system_app.models import Notify
from notify_system_app.models import User_Notify

admin.site.register(Notify)
admin.site.register(User_Notify)
