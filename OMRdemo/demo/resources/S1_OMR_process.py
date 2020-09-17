import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os, sys
import glob
import cv2
from sklearn.svm import SVC
import unicode #한글 자모 결합 오픈소스
import csv


# When needed checking
def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


def loadImage(base_dir, fileNM, dst):
    base_dir = base_dir
    fileNM = fileNM
    image = cv2.imread(base_dir + fileNM + '.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dst = cv2.resize(gray, dsize=(1000, 800), interpolation=cv2.INTER_AREA)
    # _, dst = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)
    plt.imshow(dst)
    plt.show()

    # x,y 좌표 찍기
    cv2.imshow('ddir', dst)
    cv2.setMouseCallback('ddir', onMouse)
    cv2.waitKey()
    cv2.destroyAllWindows()

    return dst