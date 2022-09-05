import json
import os
from zoneinfo import ZoneInfo
import datetime
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

from gcs import get_signed_url

load_dotenv()
with open("firebase/cred.json", "w") as f:
    f.write(str(os.getenv("FIREBASE_CRED")))

cred = credentials.Certificate("firebase/cred.json")

firebase_admin.initialize_app(
    cred,
    {
        "databaseAuthVariableOverride": {"uid": os.getenv("AUTH_ID")},
    },
)

db = firestore.client()

docs = db.collection("festivals").stream()
for doc in docs:
    data = {
        "festivals":{
            doc.id:{
                **doc.to_dict()
            }
        }
    }
    #print(data)
    for rid,review in doc.to_dict()["reviews"].items():
        data["festivals"][doc.id]["reviews"][rid]["date"] = datetime.datetime.fromtimestamp(review["date"].timestamp()).strftime('%Y年%m月%d日 %H時%M分')
    with open('firebase/backup.json', 'w') as f:
        json.dump(data, f, indent=4,ensure_ascii=False)
    break

