import os
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred, {
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
})

db = firestore.client()


def get_pct_from_fb() -> float:
    percentage = db.collection(u'prediction').limit(1).get()
    return float(percentage[0].to_dict()['percentage']) / 100
