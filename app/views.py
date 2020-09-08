from flask import jsonify
from app import app
from app.models import *



@app.route('/',methods=["GET"])
def test():
    return jsonify({"status":"1"})

@app.route('/user',methods=["GET"])
def userTEsT():
    return jsonify(User.getInfo(1))

@app.route('/books/<int:page>',methods=["GET"])
def testBooks(page):
    return jsonify(Product.getAllProfuctsFilteredByRate(page))
#TODO:Flask login
