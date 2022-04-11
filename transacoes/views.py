from django.shortcuts import render
from django.http import FileResponse


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

    elif request.method == 'POST':
        print(request.FILES['file_name'])
        print(request.FILES['file_name'].size/1000000, "megabytes")
        file_h = FileResponse(request.FILES['file_name'])
        for file in file_h:
            print(file.decode("utf-8"))
        request.method = 'GET'
        return render(request, 'index.html')
