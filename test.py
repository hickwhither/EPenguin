from werkzeug.security import generate_password_hash, check_password_hash

import firebase_admin
from firebase_admin import credentials, db, firestore
from google.cloud.firestore import FieldFilter

cred = credentials.Certificate("cktoj-users-abcxyzhehe-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
users_ref = db.collection("user")


doc = users_ref.where(filter=FieldFilter("username", "==", "khiemkrkt")).get()
#dqeifqifieqifqjiefqe
if doc:
    print(f"{doc[0].id} => {doc[0].to_dict()}")
else:
    print("No document found.")

