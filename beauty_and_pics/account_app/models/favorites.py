from django.db import models
from django.contrib.auth.models import User
from account_app.models import Account

class Favorite(models.Model):
    id_favorite = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user')
    favorite_user = models.ForeignKey(User, related_name='favorite_user')

    class Meta:
        app_label = 'account_app'

    def add_favorite(self, user_id=None, favorite_user_id=None):
        """Function to add a new favorite user"""
        return_var = False

        if user_id and favorite_user_id:
            # if favorite not exists for this account, than add it
            if not self.check_if_favorite_exists(user_id=user_id, favorite_user_id=favorite_user_id):
                # retrieve user and favorite user obj
                account_obj = Account()
                user_obj = account_obj.get_user_about_id(user_id=user_id)
                favorite_user_obj = account_obj.get_user_about_id(user_id=favorite_user_id)

                favorite_obj = Favorite()
                favorite_obj.user = user_obj
                favorite_obj.favorite_user = favorite_user_obj
                favorite_obj.save()
                return_var = True

        return return_var

    def check_if_favorite_exists(self, user_id=None, favorite_user_id=None):
        """Function check if favorite already exists for this account"""
        return_var = False

        if user_id and favorite_user_id:
            # check if favorite already exists for this account 
            try:
                Favorite.objects.get(user__id=user_id, favorite_user__id=favorite_user_id)
                return_var = True
            except Favorite.DoesNotExist:
                pass

        return return_var

    def remove_favorite(self, user_id=None, favorite_user_id=None):
        """Function to remove favorite user"""
        return_var = False
            if user_id and favorite_user_id:
                try:
                    favorite_obj = Favorite.objects.get(user__id=user_id, favorite_user__id=favorite_user_id)
                    return_var = True
                except Favorite.DoesNotExist:
                    pass
                else:
                    favorite_obj.delete()
                    return_var = True

        return return_var
