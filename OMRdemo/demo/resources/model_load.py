import joblib
import csv

def loadModel(modelName):
    file_name = 'C:/Users/khaye/edu-ai/data/OMR/' + modelName
    model = joblib.load(file_name)
    return model

def writeCSV(header, stdInfo):
    with open("omr_result.csv", "w", encoding='utf-8-sig') as f_new:
        writer = csv.writer(f_new, delimiter=",", quotechar='"')
        writer.writerow(header)
        writer.writerow(map(lambda x:x, stdInfo))
        print(lambda x:x, stdInfo)
        writer.writerow(["If answer miss is not 0, please check"])