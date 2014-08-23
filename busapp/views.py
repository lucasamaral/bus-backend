from django.shortcuts import render

def index(request):
    return render(request, 'busapp/index.html', {})