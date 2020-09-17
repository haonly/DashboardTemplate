from datetime import timezone

from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, 'demo/index.html')

def upload(request):
    return render(request, 'demo/upload.html')


def info(request):
    img_fName = 'none'
    if request.method == "POST":
        img_fName = request.POST.get("img_fName")


    # img_fName으로 csv 파일 찾아서 바로 읽기
    # 위에서는 csv로 떨구는 것까지 processing
    return render(request, 'demo/upload.html', img_fName)

def upload_image(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = UploadForm()
    return render(request, 'demo/upload.html', {
        'form': form
    })
