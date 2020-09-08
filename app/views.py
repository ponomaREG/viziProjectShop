from flask import jsonify, request
from app import app
from app import login_manager
from app.models import *
import flask_login




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

@app.route('/cart',methods=['GET'])
def testGetCartOfUser():
    user = request.args.get('userID',default=1,type=int)
    return jsonify(Cart.getCartOfUser(user))

@app.route('/flasklogin/check',methods = ['GET'])
def checkFlaskLogin():
    if flask_login.current_user.is_authenticated:
        return jsonify({'status':1})
    else:
        return jsonify({'status':0})

@app.route('/flasklogin/login',methods=['GET'])
def loginUser():
    email = request.args.get('email',type=str)
    password = request.args.get('password',type=str)
    
    userID = User.validateUserAndReturnUserID(email,password)
    if(userID != -1):
        flask_login.login_user(load_user(userID))
        return jsonify({'status':1})
    else:
        return jsonify({'status':0})

@app.route('/flasklogin/logout',methods = ["GET"])
@flask_login.login_required
def logoutUser():
    flask_login.logout_user()
    return jsonify({'status':1})

@app.route('/flasklogin/email',methods = ['GET'])
@flask_login.login_required
def checkEmail():
    return jsonify({'email':flask_login.current_user.email})

        

#TODO:Flask login
