from datetime import timezone

from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from demo.models import SubmitImage


def index(request):
    return render(request, 'demo/index.html')

def upload(request):
    image = SubmitImage()
    image.image = request.FILES['OMR image']
    image.save()
    print("----------------------------------------", image.image)
    return render(request, 'demo/upload.html', {'image': image.image})