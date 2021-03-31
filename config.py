from flask import Flask
import pymongo
from pymongo import MongoClient

# Making Flask Application
makeconfig = Flask(__name__) 

def connect():
    cluster = MongoClient("mongodb+srv://suchit:director1613@userdata.n9oyo.mongodb.net/flasktest?retryWrites=true&w=majority")
    db = cluster["flasktest"]
    return  db["newuser"]


# def connect(database):
#     cluster = MongoClient("mongodb+srv://suchit:director1613@userdata.n9oyo.mongodb.net/flasktest?retryWrites=true&w=majority")
#     db = cluster["flasktest"]
#     if database == "users":
#          return  db["users"]
#     elif database == "teacher":
#          return  db["teacher"] 