from time import sleep

import firebase_admin
from firebase_admin import credentials, firestore, db
import threading


cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
callback_done = threading.Event()


sensor_readings_collection = db.collection('sensor_readings')

def sensor_readings_onsnapshot(doc_snapshot, changes, read_time):
    global sensor_readings_docs
    sensor_readings_docs = doc_snapshot
    callback_done.set()

sensor_readings_docs = sensor_readings_collection.get()

"""
Register snhapshots
"""
sensor_readings_collection.on_snapshot(sensor_readings_onsnapshot)

def get_sensor_readings():
    global sensor_readings_docs
    return sensor_readings_docs

