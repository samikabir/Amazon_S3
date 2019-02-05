from flask import Flask, render_template ,session, escape, request, Response
from flask import url_for, redirect, send_from_directory
from flask import send_file, make_response, abort
import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from aws import AWSManager

app = Flask(__name__)
app.secret_key="aws_demo_app"

app.url_map.strict_slashes = False

awsMgr = AWSManager()

@app.route('/')
def basic_pages(**kwargs):
    return make_response(open('aws.html').read())

@app.route('/getAllRegions', methods=['POST'])
def getAllRegions():
    key = request.json['key']
    secret = request.json['secret']
    return awsMgr.getRegions(key, secret), 200, {'Content-Type': 'application/json'}

@app.route('/getAllInstanceTypes', methods=['POST'])
def getAllInstanceTypes():
    return awsMgr.getInstanceTypes(), 200, {'Content-Type': 'application/json'}

@app.route('/createBuckets', methods=['POST'])
def createBuckets():
    key = request.json['key']
    secret = request.json['secret']
    location = request.json['location']
    name = request.json['name']
    return awsMgr.createBuckets(name, location, key, secret), 200, {'Content-Type': 'application/json'}

@app.route('/getAllBuckets', methods=['POST'])
def getAllBuckets():
    key = request.json['key']
    secret = request.json['secret']
    region = request.json['location']
    return awsMgr.getAllBuckets(key, secret), 200, {'Content-Type': 'application/json'}
    
@app.route('/deleteBucket', methods=['POST'])
def deleteBucket():
    key = request.json['key']
    secret = request.json['secret']
    location = request.json['location']
    name = request.json['name']
    return awsMgr.deleteBucket(name, location, key, secret), 200, {'Content-Type': 'application/json'}

@app.route('/uploadObject', methods=['POST'])
def uploadObject():
    filedata = request.files['file']
    objArr = request.form['objArr']
    jsonConvert = json.loads(objArr)
    key = jsonConvert['key']
    secret = jsonConvert['secret']
    bucketName = jsonConvert['bucketName']
    return awsMgr.uploadObject(filedata, bucketName, key, secret), 200, {'Content-Type': 'application/json'}

@app.route('/getObjectsOfBucket', methods=['POST'])
def getObjectsOfBucket():
    key = request.json['key']
    secret = request.json['secret']
    bucketName = request.json['bucketName']
    return awsMgr.getObjectsOfBucket(bucketName, key, secret), 200, {'Content-Type': 'application/json'}

@app.route('/downloadObject', methods=['POST'])
def downloadObject():
    key = request.json['key']
    secret = request.json['secret']
    bucketName = request.json['bucketName']
    filename = request.json['fileName']
    saveName = request.json['saveName']
    return awsMgr.downloadObject(filename, bucketName, saveName, key, secret), 200, {'Content-Type': 'application/json'}

@app.route('/deleteObject', methods=['POST'])
def deleteObject():
    key = request.json['key']
    secret = request.json['secret']
    bucketName = request.json['bucketName']
    filename = request.json['fileName']
    return awsMgr.deleteObject(filename, bucketName, key, secret), 200, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 5000)))
