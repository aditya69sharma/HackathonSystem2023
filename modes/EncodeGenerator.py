import cv2
import face_recognition
import pickle
import os

folderPath = 'facerecog/modes'
PathList = os.listdir(folderPath)
print(PathList)
imageList = []
studentIds = []
for path in PathList:
    imageList.append(cv2.imread(os.path.join(folderPath, path)))

    studentIds.append(os.path.join(folderPath, path))
    print(path)
    print(os.path.splitext(path)[0])
print(len(imageList))
