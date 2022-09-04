import os
from zoneinfo import ZoneInfo
import json
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
    print(data)
    for review in data[]
    with open('firebase/backup.json', 'w') as f:
        json.dump(data, f, indent=4,ensure_ascii=False)
    break

