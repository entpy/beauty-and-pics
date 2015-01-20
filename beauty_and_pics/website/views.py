from django.shortcuts import render

def index(request):
    return render(request, 'website/index.html', False)

def come_funziona(request):
    return render(request, 'website/come_funziona.html', False)
