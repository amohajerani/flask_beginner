'''
Users collection: 
- _id
- username
- email

s3:
    thegagali
        username1
            resume.csv
            ...

Files collection
- _id
- filepath
- username
- private


'''
from pymongo.mongo_client import MongoClient
from dotenv import find_dotenv, load_dotenv
from os import environ as env


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
MONGO_URL = env.get("MONGO_URI")
client = MongoClient(MONGO_URL)
db = client.thegagali
Users = db.Users
Files = db.files
Events = db.Events


def create_username(email):
    username = email.split("@")[0]
    username = ''.join(e for e in username if e.isalnum())
    num = 0
    while Users.find_one({'username': username}):
        username = username+str(num)
        num += 1
    return username


def get_username(email):
    user_obj = Users.find_one({'email': email})
    if not user_obj:
        username = create_username(email)
        Users.insert_one({'email': email, 'username': username})
    else:
        username = user_obj['username']
    return username


def file_exists(username, filename):
    filepath = username+'/'+filename
    res = Files.find_one({'filepath': filepath})
    if res:
        return True
    else:
        return False


def insert_file_doc(username, filename, private):
    filepath = username+'/'+filename
    Files.insert_one(
        {'filepath': filepath, 'private': private, 'username': username})


def get_file_doc(filepath):
    return Files.find_one({'filepath': filepath})


def mongo_delete_doc(filepath):
    Files.delete_one({'filepath': filepath})


def mongo_update_file(filepath, update_obj):
    filter = {'filepath': filepath}
    file_obj = Files.find_one(filter)
    newvalues = {"$set": update_obj}
    Files.update_one(filter, newvalues)


def get_events(filepath):
    events = list(Events.find({filepath: filepath}))
    sorted(events, key=lambda k: k['time'], reverse=True)
    return events[:100]


def insert_event(event):
    Events.insert_one(event)
