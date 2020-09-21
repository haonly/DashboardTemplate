from datetime import timezone

from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from demo.models import SubmitImage
from demo.resources.image_processing import loadImage
from demo.resources.image_processing import cropRegion
from demo.resources.image_processing import mapName
from demo.resources.image_processing import mapCode
from demo.resources.image_processing import mapBday
from demo.resources.image_processing import mapAnswer
from demo.resources.image_processing import mapSex
from demo.resources.model_load import writeCSV


def index(request):
    return render(request, 'demo/index.html')

def upload(request):
    image = SubmitImage()
    image.image = request.FILES['OMR image']
    image.save()

    dst = None
    omr = loadImage(image.image.url, dst)

    ## Image Crop
    # cropName --> stdName
    w, h = 221, 344
    key = 1
    nameRegion = cropRegion(omr, 302, 397, w, h, 0, 0)
    # cropStudentCode --> stdCode
    w, h = 183, 309
    codeRegion = cropRegion(omr, 32, 353, w, h, 0, 0)
    # cropBirthday --> stdBday
    w, h = 164, 161
    birthdayRegion = cropRegion(omr, 350, 151, w, h, 0, 0)
    # ans20Region --> answerList
    w, h = 98, 627
    ans20Region = cropRegion(omr, 570, 116, w, h, 0, 0)
    ans40Region = cropRegion(omr, 711, 116, w, h, 0, 0)
    ans45Region = cropRegion(omr, 853, 116, w, 157, 0, 0)
    # sexRegion --> stdSex
    w, h = 17, 61
    sexRegion = cropRegion(omr, 250, 351, w, h, 0, 0)


    stdName = mapName(nameRegion)
    stdCode = mapCode(codeRegion)
    stdBday = mapBday(birthdayRegion)

    key = 20
    answerList = []
    answerList.extend(mapAnswer(ans20Region, key))
    key = 40
    answerList.extend(mapAnswer(ans40Region, key))
    key = 45
    answerList.extend(mapAnswer(ans45Region, key))

    missCnt = answerList.count(-1)
    stdSex = mapSex(sexRegion)

    print("stdName: ", stdName)
    print("stdSex: ", stdSex)
    print("stdCode: ", stdCode)
    print("stdBday: ", stdBday)
    print("answerList: ", answerList)
    print("answer miss(missCnt): ", missCnt)

    OMR = [stdName, stdSex, stdCode, stdBday, answerList, missCnt]

    header = ['stdName', 'stdSex', 'stdCode', 'stdBday','answerList','answer miss' ]
    writeCSV(header, OMR)

    return render(request, 'demo/upload.html', {'image': image.image, 'OMR': OMR})