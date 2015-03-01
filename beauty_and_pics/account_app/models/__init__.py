from django.contrib import admin
from website.models.accounts import Account
from website.models.favorites import Favorite
from website.models.images import Image

admin.site.register(Account)
admin.site.register(Favorite)
admin.site.register(Image)
