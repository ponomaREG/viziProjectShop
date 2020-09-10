from flask import jsonify, request, redirect, url_for, render_template
from app import app
from app import login_manager
from app.model import *
from app.models.User import User
from app.models.Product import Product
from app.models.Cart import Cart
from app.models.Order import Order
import flask_login


    
    

@app.route("/login",methods = ['GET','POST'])
def loginUser():
    if(flask_login.current_user.is_authenticated):
        return redirect(url_for('userInfo'))
    if(request.method == 'POST'):
        email = request.form.get('email',type=str)
        password = request.form.get('password',type=str)
        userID = User.validateUserAndReturnUserID(email,password)
        if(userID != -1):
            flask_login.login_user(load_user(userID),remember=True)
            return redirect(url_for('userInfo'))
        else:
            return render_template('login.html',error = "Not found")
    else:
        return render_template('login.html')

@app.route('/registration',methods=['GET','POST'])
def registrationUser():
    if(flask_login.current_user.is_authenticated):
        return redirect(url_for('userInfo'))
    if(request.method == 'POST'):
        email = request.form.get('email',type=str)
        pswd = request.form.get('pswd',type=str)
        pswd2 = request.form.get('pswd2',type=str)
        first_name = request.form.get('firstName',type=str)
        last_name = request.form.get('lastName',type=str)
        birthdate = request.form.get('birthDate')
        if(pswd != pswd2):
            return render_template('registration.html',error = 'Password mismatch')
        resultRegisterOperation = User.registerUser(email,pswd,last_name,first_name,birthdate)
        if(resultRegisterOperation["status"] == 1):
            return render_template('registration.html',error = 'User already exists')
        flask_login.login_user(load_user(resultRegisterOperation["userID"]),remember=True)
        return redirect(url_for('userInfo'))
    else:
        return render_template('registration.html')


@app.route('/user',methods=['GET'])
@flask_login.login_required
def userInfo():
    return render_template('check.html',user = flask_login.current_user)

@app.route('/logout',methods=['GET'])
@flask_login.login_required
def logoutUser():
    flask_login.logout_user()
    return redirect(url_for('loginUser'))