import os, json
import firebase_admin
from firebase_admin import credentials, firestore

cert = {
    "type": "service_account",
    "token_uri": "https://oauth2.googleapis.com/token",
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL')
}

cred = credentials.Certificate(cert=cert)
firebase_admin.initialize_app(cred, {
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
})

db = firestore.client()


def get_pct_from_fb() -> float:
    percentage = db.collection(u'prediction').limit(1).get()
    return float(percentage[0].to_dict()['percentage']) / 100
