from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import pymongo
import json
import time, os
import urllib.parse
from bson.json_util import dumps as bdumps
from bson.objectid import ObjectId

todo = Blueprint("todo", __name__)

MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_NAME = "trudiedo"
MONGODB_COLLECTION = "todos"
MONGODB_USER = "root"
MONGODB_PASSWORD = os.environ['TRUDB_PW']

class Todo(object):
    client = ""
    collection = ""

    def __init__(self):
        try:
            username = urllib.parse.quote_plus(MONGODB_USER)
            password = urllib.parse.quote_plus(MONGODB_PASSWORD)
            self.client = pymongo.MongoClient("mongodb://{0}:{1}@{2}".format(username, password, MONGODB_HOST), int(MONGODB_PORT))
            self.collection = self.client[MONGODB_NAME][MONGODB_COLLECTION]
            
        except Exception as err:
            self.client = "" 
    def list(self,req):
        """
        List all todos
        curl localhost:5000/todos
        """
        try:
            #if "id" in req:
            #    ob = [i for i in self.collection.find({"_id": ObjectId(req["id"])})]
            #    return bdumps(ob), 200
            ts = [x for x in self.collection.find({})]
            result = bdumps({"todos": ts})
            return result, 200
        except Exception as err:
            return json.dumps({"error": str(err)}), 500

    def is_valid(self, data):
        """ 
        Validate the request
        """
        if not type(data) is dict:
            return False
        for k in ["name", "tags"]:
            if data.get(k) == None:
                return False
        return True
    

    def create(self, req):
        """
        Create a new todo or list item
        curl -X POST -d '{"name" : "cookies", "tags": ["Trader Joes", "Winco"]}' -H "Content-Type: application/json" localhost:5000/todos
        """
        try: 
            if not req:
                return json.dumps({"status": "no data passed in"}), 200
            if self.is_valid(req):
                req["updatedAt"] = int(round(time.time() * 1000))
                id = self.collection.insert_one(req)
                return bdumps(req), 201
            else:
                return json.dumps({"invalid json" :  req}), 200
        except Exception as err:
            return json.dumps(str(err)), 500
    
    def delete(self, req):
        """
        delete a list item
        curl -X DELETE -d '{"id" : "5c231b18a2cd24713215df85"}' -H "Content-Type: application/json" localhost:5000/todos
        """
        try:
            if not req:
                return json.dumps({"status": "no data passed in"}), 200
            out = self.collection.delete_one({"_id": ObjectId(req["id"])})
            if out.deleted_count > 0:
                return json.dumps({"status": "Object with ID {} is removed".format(req['id']) }), 201
            else:
                return json.dumps({"status": "Object with ID {} was not found".format(req['id']) }), 200
            
        except Exception as err:
            return json.dumps(str(err)), 500
            
    
@todo.route("/todos", methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin()
def todo_handler():
    """
    Handle the API requests.
    """
    t = Todo()
    if request.method == 'GET':
        j, rc = t.list(request.json)
    if request.method == 'POST':
        j, rc = t.create(request.json)
    if request.method == 'DELETE':
        j, rc = t.delete(request.json)
    return jsonify(j), rc
