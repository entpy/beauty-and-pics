from django.shortcuts import render

def index(request):
    return render(request, 'website/index.html', False)

def how_it_works(request):
    return render(request, 'website/come_funziona.html', False)

def login(request):
    return render(request, 'website/login.html', False)

def forgot_password(request):
    return render(request, 'website/forgot_password.html', False)

def register(request):
    return render(request, 'website/register.html', False)

def catwalk_index(request):
    return render(request, 'website/catwalk/catwalk_index.html', False)

def catwalk_profile(request):
    return render(request, 'website/catwalk/catwalk_profile.html', False)

def help(request):
    return render(request, 'website/catwalk/help.html', False)

def report_user(request):
    return render(request, 'website/catwalk/report_user.html', False)
