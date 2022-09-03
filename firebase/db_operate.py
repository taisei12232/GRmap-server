import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

load_dotenv()

cred = credentials.Certificate("firebase/cred.json")

firebase_admin.initialize_app(
    cred,
    {
        "databaseAuthVariableOverride": {"uid": os.getenv("UID")},
    },
)

firestore = firestore.client()