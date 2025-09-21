import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\skand\Downloads\dk\gcloud-key.json"
from google.cloud import vision
client = vision.ImageAnnotatorClient()
print(client)