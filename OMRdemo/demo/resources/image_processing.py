import cv2
from demo.resources.model_load import loadModel
from demo.resources import unicode


def loadImage(fileNM, dst):
    image = cv2.imread('demo/' + fileNM)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dst = cv2.resize(gray, dsize=(1000, 800), interpolation=cv2.INTER_AREA)
    # _, dst = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)
    #plt.imshow(dst)
    #plt.show()

    return dst


def cropRegion(omr, x, y, w, h, cropX, cropY):
    roiRegion = omr[y:y + h, x:x + w]
    img = roiRegion.copy()
    if cropX > 0 and cropY > 0:
        img = cv2.resize(img, dsize=(cropX, cropY), interpolation=cv2.INTER_AREA)
    _, img = cv2.threshold(img, 170, 255, cv2.THRESH_BINARY)

    return img


def mapName(regionImg):
    # s2(한국교육과정평가원), 이름모델 --> S2_0_Name, S2_1_Name, S2_2_Name
    nameDict0 = {0: 'ㄱ', 1: 'ㄲ', 2: 'ㄴ', 3: 'ㄷ', 4: 'ㄸ', 5: 'ㄹ', 6: 'ㅁ', 7: 'ㅂ', 8: 'ㅃ', 9: 'ㅅ', 10: 'ㅆ', \
                 11: 'ㅇ', 12: 'ㅈ', 13: 'ㅉ', 14: 'ㅊ', 15: 'ㅋ', 16: 'ㅌ', 17: 'ㅍ', 18: 'ㅎ', -1: 'none'}
    nameDict1 = {0: 'ㅏ', 1: 'ㅐ', 2: 'ㅑ', 3: 'ㅒ', 4: 'ㅓ', 5: 'ㅔ', 6: 'ㅕ', 7: 'ㅖ', 8: 'ㅗ', 9: 'ㅘ', 10: 'ㅙ', \
                 11: 'ㅚ', 12: 'ㅛ', 13: 'ㅜ', 14: 'ㅝ', 15: 'ㅞ', 16: 'ㅟ', 17: 'ㅠ', 18: 'ㅡ', 19: 'ㅢ', 20: 'ㅣ', -1: 'none'}
    nameDict2 = {0: 'ㄱ', 1: 'ㄲ', 2: 'ㄴ', 3: 'ㄶ', 4: 'ㄷ', 5: 'ㄹ', 6: 'ㄺ', 7: 'ㄻ', 8: 'ㄼ', 9: 'ㅀ', 10: 'ㅁ', \
                 11: 'ㅂ', 12: 'ㅅ', 13: 'ㅆ', 14: 'ㅇ', 15: 'ㅈ', 16: 'ㅊ', 17: 'ㅋ', 18: 'ㅌ', 19: 'ㅍ', 20: 'ㅎ', -1: 'none'}
    name = []
    nameX, nameY = 60, 1200
    longNameY = 1300
    key = 0

    name0Model = loadModel('S2_0_Name_SVM.pkl')
    name1Model = loadModel('S2_1_Name_SVM.pkl')
    name2Model = loadModel('S2_2_Name_SVM.pkl')

    name00Region = cropRegion(regionImg, 4, 8, 14, 299, nameX, nameY)
    name01Region = cropRegion(regionImg, 22, 8, 14, 331, nameX, longNameY)
    name02Region = cropRegion(regionImg, 40, 8, 14, 331, nameX, longNameY)

    name10Region = cropRegion(regionImg, 60, 8, 14, 299, nameX, nameY)
    name11Region = cropRegion(regionImg, 77, 8, 14, 331, nameX, longNameY)
    name12Region = cropRegion(regionImg, 94, 8, 14, 331, nameX, longNameY)

    name20Region = cropRegion(regionImg, 113, 8, 14, 299, nameX, nameY)
    name21Region = cropRegion(regionImg, 131, 8, 14, 331, nameX, longNameY)
    name22Region = cropRegion(regionImg, 150, 8, 14, 331, nameX, longNameY)

    name30Region = cropRegion(regionImg, 169, 8, 14, 299, nameX, nameY)
    name31Region = cropRegion(regionImg, 186, 8, 14, 331, nameX, longNameY)
    name32Region = cropRegion(regionImg, 205, 8, 14, 331, nameX, longNameY)

    # name0
    name.append(nameDict0[int(name0Model.predict(name00Region.flatten().reshape(1, -1)))])
    name.append(nameDict1[int(name1Model.predict(name01Region.flatten().reshape(1, -1)))])
    name.append(nameDict2[int(name2Model.predict(name02Region.flatten().reshape(1, -1)))])

    # name1
    name.append(nameDict0[int(name0Model.predict(name10Region.flatten().reshape(1, -1)))])
    name.append(nameDict1[int(name1Model.predict(name11Region.flatten().reshape(1, -1)))])
    name.append(nameDict2[int(name2Model.predict(name12Region.flatten().reshape(1, -1)))])

    # name2
    name.append(nameDict0[int(name0Model.predict(name20Region.flatten().reshape(1, -1)))])
    name.append(nameDict1[int(name1Model.predict(name21Region.flatten().reshape(1, -1)))])
    name.append(nameDict2[int(name2Model.predict(name22Region.flatten().reshape(1, -1)))])

    # name3
    name.append(nameDict0[int(name0Model.predict(name30Region.flatten().reshape(1, -1)))])
    name.append(nameDict1[int(name1Model.predict(name31Region.flatten().reshape(1, -1)))])
    name.append(nameDict2[int(name2Model.predict(name32Region.flatten().reshape(1, -1)))])

    print("name before processing:", name)

    while 'none' in name:
        name.remove('none')
    name = unicode.join_jamos("".join(name))
    return name


def mapCode(regionImg):
    # s2(한국교육과정평가원), 수험번호 모델: S2_CASE1_SVM.pkl, S2_CASE2_SVM.pkl
    # case1: 1~4, case2:0~9
    # case1: cv2.resize(gray, dsize = (30,550), interpolation=cv2.INTER_AREA)
    # case2: cv2.resize(gray, dsize = (30,550), interpolation=cv2.INTER_AREA)

    codeX, codeY = 30, 550
    ## 월요일에 할것:
    ## 각 영역별 x, y, w, h 구해서 위에 이름 했던 것처럼 코드 돌리기
    y, w, h = 0, 18, 310
    key = 0
    idx0Model = loadModel('S2_CASE1_SVM.pkl')
    idxRestModel = loadModel('S2_CASE2_SVM.pkl')

    code = []
    idx0Region = cropRegion(regionImg, 0, y, w, h, codeX, codeY)
    idx1Region = cropRegion(regionImg, 18, y, w, h, codeX, codeY)
    idx2Region = cropRegion(regionImg, 36, y, w, h, codeX, codeY)
    idx3Region = cropRegion(regionImg, 54, y, w, h, codeX, codeY)
    idx4Region = cropRegion(regionImg, 72, y, w, h, codeX, codeY)

    idx5Region = cropRegion(regionImg, 108, y, w, h, codeX, codeY)
    idx6Region = cropRegion(regionImg, 126, y, w, h, codeX, codeY)
    idx7Region = cropRegion(regionImg, 144, y, w, h, codeX, codeY)
    idx8Region = cropRegion(regionImg, 162, y, w, h, codeX, codeY)

    # mapping
    code.append(int(idx0Model.predict(idx0Region.flatten().reshape(1, -1))))
    code.append(int(idxRestModel.predict(idx1Region.flatten().reshape(1, -1))))
    code.append(int(idxRestModel.predict(idx2Region.flatten().reshape(1, -1))))
    code.append(int(idxRestModel.predict(idx3Region.flatten().reshape(1, -1))))
    code.append(int(idxRestModel.predict(idx4Region.flatten().reshape(1, -1))))

    # 구분..
    code.append('-')

    code.append(int(idxRestModel.predict(idx5Region.flatten().reshape(1, -1))))
    code.append(int(idxRestModel.predict(idx6Region.flatten().reshape(1, -1))))
    code.append(int(idxRestModel.predict(idx7Region.flatten().reshape(1, -1))))
    code.append(int(idxRestModel.predict(idx8Region.flatten().reshape(1, -1))))

    print(code, type(code))
    code = "".join([str(_) for _ in code])

    return code


def mapBday(regionImg):
    # s2(한국교육과정평가원), 생일모델: S2_CASE3_SVM, S2_CASE4_SVM, S2_CASE5_SVM

    codeX, codeY = 30, 550
    y, h = 0, 160
    case3Model = loadModel('S2_CASE3_SVM.pkl')
    case4Model = loadModel('S2_CASE4_SVM.pkl')
    case5Model = loadModel('S2_CASE5_SVM.pkl')

    bday = []

    yy0 = cropRegion(regionImg, 0, y, 26, h, codeX, codeY)
    yy1 = cropRegion(regionImg, 25, y, 30, h, codeX, codeY)
    mm0 = cropRegion(regionImg, 54, y, 28, h, codeX, codeY)
    mm1 = cropRegion(regionImg, 81, y, 28, h, codeX, codeY)
    dd0 = cropRegion(regionImg, 109, y, 28, h, codeX, codeY)
    dd1 = cropRegion(regionImg, 136, y, 27, h, codeX, codeY)

    # mapping
    bday.append(int(case3Model.predict(yy0.flatten().reshape(1, -1))))
    bday.append(int(case4Model.predict(yy1.flatten().reshape(1, -1))))
    bday.append(int(case5Model.predict(mm0.flatten().reshape(1, -1))))
    bday.append(int(case4Model.predict(mm1.flatten().reshape(1, -1))))
    bday.append(int(case3Model.predict(dd0.flatten().reshape(1, -1))))
    bday.append(int(case4Model.predict(dd1.flatten().reshape(1, -1))))
    # code.append(int(idxRestModel.predict(idx4Region.flatten().reshape(1,-1))))
    print(bday)
    bday = "".join([str(_) for _ in bday])
    return bday


def mapAnswer(regionImg, key):
    # s2(한국교육과정평가원), 답안모델1-20, 21-40: S2_CASE6_SVM

    codeX, codeY = 240, 75
    x, y, w, h = 0, 3, 96, 31
    answerModel = loadModel('S2_CASE6_SVM.pkl')

    answer = []
    # answerImg = []
    if key <= 40:
        for i in range(20):
            answerImg = cropRegion(regionImg, x, y, w, h, codeX, codeY)
            answer.append(int(answerModel.predict(answerImg.flatten().reshape(1, -1))))
            y += 31
            if i == 15:
                y += 2
    elif key == 45:
        for i in range(5):
            answerImg = cropRegion(regionImg, x, y, w, h, codeX, codeY)
            answer.append(int(answerModel.predict(answerImg.flatten().reshape(1, -1))))
            y += 31
    print(answer)
    return answer


def mapSex(regionImg):
    # s2(한국교육과정평가원),성별모델: S2_Sex_SVM

    cropX, cropY = 30, 60
    sexModel = loadModel('S2_Sex_SVM.pkl')

    # sex = 1 : male
    # sex = 2 : female
    sex = -1

    img = cv2.resize(regionImg, dsize=(cropX, cropY), interpolation=cv2.INTER_AREA)

    # mapping
    sex = int(sexModel.predict(img.flatten().reshape(1, -1)))
    if sex == 1:
        sex = '남'
    if sex == 2:
        sex = '여'

    return sex