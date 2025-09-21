from flask import Flask, render_template, request, redirect, flash
from flask_moment import Moment
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os
app_path = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(app_path, '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)
moment = Moment(app)
app.secret_key = os.environ.get("SECRETKEY")

connectionString = os.environ.get("MONGOSTRING")

cluster = pymongo.MongoClient(connectionString)

database = cluster["mydatabase"]    

collection = database["contacts"]


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        allcontacts = list(collection.find({}))
        return render_template("index.html", allcontacts = allcontacts)
    if request.method == "POST":
        name = request.form["name"]
        number = request.form["number"]
        record = {"name" : name, "number" : number}
        collection.insert_one(record)
        return redirect("/")

@app.route("/delete")
def delete():
    noteid = request.args["contactid"]
    collection.delete_one({"_id" : ObjectId(noteid)})
    return redirect("/")

@app.route("/edit", methods = ["GET", "POST"])
def edit():
    if request.method == "GET":
        noteid = request.args["contactid"]
        contact = collection.find_one({"_id" : ObjectId(noteid)})
        return render_template("edit.html", contact = contact)
    if request.method == "POST":
        name = request.form["name"]
        number = request.form["number"]
        noteid = request.args["contactid"]
        collection.update_one({"_id":ObjectId(noteid)}, {"$set": {"name" : name, "number" : number}})
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)