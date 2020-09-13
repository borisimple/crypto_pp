import os
import re
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred, {
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
})

db = firestore.client()


def get_pct_from_fb() -> int:
    percentage = db.collection(u'prediction').limit(1).get()
    return int(percentage[0].to_dict()['percentage'])
