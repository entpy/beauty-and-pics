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
