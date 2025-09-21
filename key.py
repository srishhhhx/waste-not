import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud-key.json"
from google.cloud import vision

client = vision.ImageAnnotatorClient()
print(client)
