from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from website.forms import *

# www {{{
def www_index(request):
    return render(request, 'website/www/www_index.html', False)

def www_how_it_works(request):
    return render(request, 'website/www/www_come_funziona.html', False)

def www_login(request):
    return render(request, 'website/www/www_login.html', False)

def www_forgot_password(request):
    return render(request, 'website/www/www_forgot_password.html', False)

def www_register(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
		# TODO: process the data in form.cleaned_data as required
		# ...
		# redirect to user profile
		return HttpResponseRedirect('/registrati/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    context = {
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/www/www_register.html', context)
# }}}

# catwalk {{{
def catwalk_index(request):
    return render(request, 'website/catwalk/catwalk_index.html', False)

def catwalk_profile(request):
    return render(request, 'website/catwalk/catwalk_profile.html', False)

def catwalk_help(request):
    return render(request, 'website/catwalk/catwalk_help.html', False)

def catwalk_report_user(request):
    return render(request, 'website/catwalk/catwalk_report_user.html', False)
# }}}

# private profile {{{
def profile_index(request):
    return render(request, 'website/profile/profile_index.html', False)

def profile_data(request):
    return render(request, 'website/profile/profile_data.html', False)

def profile_favorites(request):
    return render(request, 'website/profile/profile_favorites.html', False)

def profile_stats(request):
    return render(request, 'website/profile/profile_stats.html', False)

def profile_area51(request):
    return render(request, 'website/profile/profile_area51.html', False)
# }}}
