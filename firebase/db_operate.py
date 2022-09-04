import datetime
import os
import random
import uuid
from zoneinfo import ZoneInfo

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


def add_review(data):
    doc_ref = db.collection("festivals").document(data.fid)
    doc = doc_ref.get().to_dict()
    rid = str(uuid.uuid4())
    signedurl = None
    print(doc)
    doc["reviews"][rid] = {
        "position": data.position,
        "text": data.text,
        "shop": data.sid,
        "date": datetime.datetime.now(ZoneInfo("Asia/Tokyo")),
        "color": doc["shops"][data.sid]["color"],
        "pictuire": "https://storage.googleapis.com"
        + "/gourmap_bucket/reviewimages/"
        + rid
        + ".png",
    }
    doc_ref.set(doc)
    if data.haspicture:
        signedurl = get_signed_url.generate_upload_signed_url(
            "reviewimages", rid
        )
    return {"signedurl": signedurl}


def add_review_image(data):
    doc_ref = db.collection("festivals").document(data.fid)
    doc = doc_ref.get().to_dict()
    doc["reviews"][data.rid]["picture"] = data.url
    doc_ref.set(doc)


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
    sid = str(uuid.uuid4())
    fest["shops"][sid] = {
        "name": data.name,
        "pamphlet": data.url,
        "position": data.position,
        "no": len(fest["shops"]) + 1,
        "color": "#"
        + ("0" + str(hex(random.randint(0, 255))[2:]))[-2:]
        + ("0" + str(hex(random.randint(0, 255))[2:]))[-2:]
        + ("0" + str(hex(random.randint(0, 255))[2:]))[-2:],
    }
    doc_ref.set(fest)
    return sid


def search_fest(lat, lng):
    docs = db.collection("festivals").stream()
    today = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    print(today.today())
    for doc in docs:
        data = doc.to_dict()
        if (
            data["area"]["position_ul"][0] >= lat
            and data["area"]["position_br"][0] <= lat
            and data["area"]["position_ul"][1] <= lng
            and data["area"]["position_br"][1] >= lng
        ):
            if str(today.date()) not in data["accesses"]:
                data["accesses"][str(today.date())] = [0] * 24
            data["accesses"][str(today.date())][today.hour] += 1
            db.collection("festivals").document(doc.id).set(data)
            reviewpositions = list(
                map(
                    lambda review: {
                        "position": review["position"],
                        "color": data["shops"][review["shop"]]["color"],
                    },
                    data["reviews"].values(),
                )
            )
            return {
                "fid": doc.id,
                "logo": data["logo"],
                "area": [
                    data["area"]["position_ul"],
                    data["area"]["position_br"],
                ],
                "shops": data["shops"],
                "reviewpositions": reviewpositions,
                "accesses": data["accesses"][str(today.date())],
            }
    return None


def get_reviews(fid):
    doc_ref = db.collection("festivals").document(fid)
    fest = doc_ref.get().to_dict()
    reviews = {
        "shoplist": list(
            map(
                lambda shop: {"value": shop[0], "label": shop[1]["name"]},
                fest["shops"].items(),
            )
        ),
        "reviews": list(
            map(
                lambda review: {
                    "rid": review[0],
                    "sid": review[1]["shop"],
                    "text": review[1]["text"],
                    "picture": review[1]["picture"],
                    "shopno": fest["shops"][review[1]["shop"]]["no"],
                    "shopname": fest["shops"][review[1]["shop"]]["name"],
                    "shopcolor": fest["shops"][review[1]["shop"]]["color"],
                },
                fest["reviews"].items(),
            )
        ),
        "pamphlets": dict(
            zip(
                fest["shops"].keys(),
                list(
                    map(lambda shop: shop["pamphlet"], fest["shops"].values())
                ),
            )
        ),
    }
    return reviews
