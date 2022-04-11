from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def printar_console(request):
    print(request.FILES['file_name'])
    print(request.FILES['file_name'].size/1000000, "megabytes")
    return render(request, 'index.html')
