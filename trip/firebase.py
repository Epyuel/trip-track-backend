import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import base64
import json


load_dotenv()

firebase_credentials_base64 = os.getenv("FIREBASE_CREDENTIALS")
firebase_credentials_json = base64.b64decode(firebase_credentials_base64).decode('utf-8')

# Convert the JSON string back to a dictionary
firebase_credentials = json.loads(firebase_credentials_json)



# Initialize the Firebase Admin SDK
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://trip-track-67466-default-rtdb.firebaseio.com/'
})

# Reference to the Realtime Database
database_ref = db.reference()

def create_log(logEntry,date):
    log_ref = database_ref.child('log').push({
        'date': date,
        'logEntry': logEntry
    })
    return log_ref.key  

def read_logs():
    users = database_ref.child('log').get()
    return users if users else {}

def read_log_by_date(date):
    logs = database_ref.child('log').order_by_child('date').equal_to(date).get()
    return logs if logs else None

def read_logs_by_date_range(start_date, end_date):
    logs_snapshot = database_ref.child('log') \
        .order_by_child('date') \
        .start_at(start_date) \
        .end_at(end_date) \
        .get()

    return logs_snapshot if logs_snapshot else None

def update_log_fb(log_id, logEntry):
    user_ref = database_ref.child(f'log/{log_id}')
    updates = {}
    if logEntry:
        updates['logEntry'] = logEntry
    if updates:
        user_ref.update(updates)
        return True
    return False

def delete_log_fb(log_id):
    database_ref.child(f'log/{log_id}').delete()
    return True
