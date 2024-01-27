import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None or DATABASE_URL == "":
    raise ValueError("DATABASE_URL is not set in the environment variables")

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': DATABASE_URL
})
ref = db.reference('Students')

data = {
    "2325111": {
        "name": "Surya Pratap",
        "major": "Student",
        "starting_year": 2023,
        "total_attendance": 10,
        "year": 2,
        "last_attendance": '2023-12-03 12:15:34'
    },
    "2325120": {
        "name": "Virat Kohli",
        "major": "Cricketer",
        "starting_year": 2010,
        "total_attendance": 30,
        "year": 5,
        "last_attendance": '2023-12-03 12:15:34'
    },
    "2325051": {
        "name": "Akshay Kumar",
        "major": "Actor",
        "starting_year": 2018,
        "total_attendance": 14,
        "year": 3,
        "last_attendance": '2023-12-03 12:15:34'
    },
    "2325115": {
        "name": "Robert Downey Jr.",
        "major": "Star",
        "starting_year": 2023,
        "total_attendance": 8,
        "year": 1,
        "last_attendance": '2023-12-03 12:15:34'
    },
    "2325069": {
        "name": "Jenna Ortega",
        "major": "Student",
        "starting_year": 2021,
        "total_attendance": 14,
        "year": 2,
        "last_attendance": '2023-12-03 12:15:34'
    },
    "2325076": {
        "name": "Elon Musk",
        "major": "CEO",
        "starting_year": 2021,
        "total_attendance": 16,
        "year": 5,
        "last_attendance": '2023-12-03 12:15:34'
    },
    "2325079":{
        "name": "Nitin Goswani",
        "major": "Student",
        "starting_year": 2023,
        "total_attendance": 18,
        "year": 3,
        "last_attendance": '2024-01-10 12:15:34'
    }
}

for key, value in data.items():
    ref.child(key).set(value)
    print(f"Data added for {key}")