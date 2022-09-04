import datetime
import os
import uuid
from zoneinfo import ZoneInfo

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

from gcs import get_signed_url

load_dotenv()

cred = credentials.Certificate("firebase/cred.json")

firebase_admin.initialize_app(
    cred,
    {
        "databaseAuthVariableOverride": {"uid": os.getenv("UID")},
    },
)

db = firestore.client()


def add_review(data):
    doc_ref = db.collection("festivals").document(data.fid)
    doc = doc_ref.get().to_dict()
    rid = uuid.uuid4()
    signedurl = None
    doc["reviews"][rid] = {
        "position": data.position,
        "text": data.text,
        "shop": data.sid,
        "date": datetime.datetime.now(ZoneInfo("Asia/Tokyo")),
    }
    if data.haspicture:
        signedurl = get_signed_url.generate_upload_signed_url(
            "reviewimages", rid
        )
    return {"rid": rid, "signedurl": signedurl}


def create_festival(data):
    doc_ref = db.collection("festivals").document()
    fest = {
        "name": data.name,
        "logo": data.logo,
        "area": {
            "position_ul": [data.position_ul],
            "position_br": [data.position_br],
        },
        "reviews": {},
        "shops": {},
    }
    doc_ref.set(fest)
    return doc_ref.id


def add_shop(data):
    doc_ref = db.collection("festivals").document(data.fid)
    fest = doc_ref.get().to_dict()
    sid = uuid.uuid4()
    fest["shops"][sid] = {
        "name": data.name,
        "pamphlet": data.url,
        "position": data.position,
        "no": len(fest["shops"]) + 1,
    }
    doc_ref.set(fest)
    return sid
