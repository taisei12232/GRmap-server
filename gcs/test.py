import os

from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()


def list_buckets():
    """Lists all buckets."""

    storage_client = storage.Client.from_service_account_json("gcs/cred.json")
    blobs = storage_client.list_blobs(os.getenv("BUCKET_NAME"))
    for blob in blobs:
        print(blob.name)


list_buckets()
