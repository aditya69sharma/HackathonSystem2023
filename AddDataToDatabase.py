import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendacerealtime-f0e0e-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')
data={
    "123123":{
        "name":"Lakshmi swaroop",
        "major": "Computer Applications",
        "starting_year":2021,
        "total_attandance":1,
        "standing": "H",
        "year":3,
        "last_attandance_time":"2022-11-11 00:54:34"
    }
}

for key, value in data.items():
    ref.child(key).set(value)