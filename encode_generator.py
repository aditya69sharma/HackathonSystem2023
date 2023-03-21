import cv2, face_recognition, pickle, os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendacerealtime-f0e0e-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendacerealtime-f0e0e.appspot.com"
})


folderPath = "images"
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentID = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))

    studentID.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    # print(path)
    # print(os.path.splitext(path)[0])
print(studentID)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("encoding started...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithid = [encodeListKnown,studentID]
print("encoding complete")

# print(encodeListKnown)

file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithid, file)
file.close()
print("file saved")
