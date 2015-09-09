from django.contrib import admin
from account_app.models.accounts import Account
from account_app.models.favorites import Favorite
from account_app.models.images import Book

admin.site.register(Account)
admin.site.register(Favorite)
admin.site.register(Book)
