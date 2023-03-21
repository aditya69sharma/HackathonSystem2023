import cv2, os, pickle
import numpy as np
import cvzone
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendacerealtime-f0e0e-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendacerealtime-f0e0e.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("images/image cv.png")
folderModePath = "modes"
modePathList = os.listdir(folderModePath)
imageModeList = []
imgStudent = []
for path in modePathList:
    imageModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(modePathList))

# load encode file
print("encode loading file....")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown,studentID = encodeListKnownWithIds
print("encode loaded")
# print(studentID)

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS  = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[70:70 + 535, 850:850 + 352] = imageModeList[modeType]


    for encodeFace, faceLOC in zip(encodeCurFrame,faceCurFrame):

        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print("matches", matches)
        # print("faceDis", faceDis)
        matchIndex = np.argmin(faceDis)
        # print("Match index",matchIndex)

        if matches[matchIndex]:
            # print("known face dedected")
            # print(studentID[matchIndex])
            y1, x2, y2, x1 = faceLOC
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55 + x1, 162+y1, x2-x1,  y2-y1
            imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
            id = studentID[matchIndex]

            if counter ==0:
                counter = 1
                modeType =1

    if counter !=0:
        if counter == 1:
            studentsInfo = db.reference(f'Students/{id}').get()
            print(studentsInfo)

            #get image from storage
            blob = bucket.get_blob(f'Students/{id}.jpg')
            #array = np.frombuffer(blob.download_as_string())
            #imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)



        cv2.putText(imgBackground,str(studentsInfo['total_attandance']), (800,800),
                     cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),1)

        cv2.putText(imgBackground,str(studentsInfo['name']), (890,410),
                            cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)

        cv2.putText(imgBackground, str(id), (1002, 451),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(imgBackground, str(studentsInfo['standing']), (1006, 500),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
        cv2.putText(imgBackground, str(studentsInfo['year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
        cv2.putText(imgBackground, str(studentsInfo['starting_year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
        cv2.putText(imgBackground, str(studentsInfo['major']), (700,800),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
        #imgBackground[175:175+246, 909:909+549] = imgStudent
        counter = counter + 1
# cv2.imshow('face', img)
    cv2.imshow('back', imgBackground)
    cv2.waitKey(3)
