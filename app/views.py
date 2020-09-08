from flask import jsonify, request
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

@app.route('/books/tags',methods=["GET"])
def testBooksByTags():
    tags = request.args.get('tags',type=str)
    tagsArray = tags.split(',')
    if(len(tagsArray) == 0):
        return jsonify({'status':3,'message':'Empty array of tags(','data':[]})
    return jsonify(Product.getAllProductsFilteredByTags(tagsArray))
#TODO:Flask login
