import datetime
import os

from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()
print("GCS_CRED:")
print(str(os.getenv("GCS_CRED")))
with open("gcs/cred.json", "w") as f:
    f.write(str(os.getenv("GCS_CRED")))


def generate_upload_signed_url(path, id):
    storage_client = storage.Client.from_service_account_json("gcs/cred.json")
    bucket = storage_client.bucket(os.getenv("BUCKET_NAME"))
    blob = bucket.blob(path + "/" + id + ".png")
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=1),
        method="PUT",
        content_type="application/octet-stream",
    )

    return url


os.remove("gcs/cred.json")
