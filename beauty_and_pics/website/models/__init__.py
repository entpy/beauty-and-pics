from django.contrib import admin
from website.models.accounts import Account
from website.models.votes import Vote 

admin.site.register(Account)
admin.site.register(Vote)
