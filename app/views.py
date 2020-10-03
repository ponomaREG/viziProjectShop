from flask import jsonify, request, redirect, url_for, render_template
from app import app
from app import login_manager
from app.model import load_user
from app.models.User import User
from app.models.Product import Product
from app.models.Cart import Cart
from app.models.Order import Order
from app.admin.models import *
from app.admin.views import *
from utils import pageHelper
import flask_login
from utils import sqlQueryHelper, tagsHelper
from werkzeug.utils import secure_filename
import os



@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('loginUser'))
    
    
@app.route("/",methods=['GET'])
def main():
    return redirect(url_for('showBooksDefault'))

@app.route('/search')
def searchAdvanced():
    availableTags = Product.getAvailableTags()
    return render_template('advanced-search.html',user=flask_login.current_user,tags = availableTags['data'])

@app.route('/checkout',methods=['GET'])
def checkout():
        cart = Cart.getCartOfUser(flask_login.current_user.userID) #TODO: CHECK STATUS
        if(cart['status'] == 0):
            return render_template('checkout.html',
            user = flask_login.current_user,
            productsInCart=cart['data'])
        elif(cart['status'] == 2):
            return render_template('checkout.htlm',
            user = flask_login.current_user,
            error = cart['message']
            )
        

@app.route('/order/<int:orderID>')
@flask_login.login_required
def showDetailsOfOrder(orderID):
    orderDetails = Order.getDetailsOfOrder(flask_login.current_user.userID,orderID)
    if(orderDetails['status'] == 0):
        return render_template('order-page.html',
        orderInfo = orderDetails['info'],
        user = flask_login.current_user,
        data = orderDetails['data'],
        address = orderDetails['address'])
    elif(orderDetails['status'] == 3 or orderDetails['status'] == 40):
        return redirect(url_for('main'))
    else:
        return render_template('order-page.html',
        user = flask_login.current_user,
        error = orderDetails['message'],
        orderDetails = orderDetails)

@app.route('/user/orders',methods=['GET'])
@flask_login.login_required
def showOrders():
    orders = Order.getOrdersOfUser(flask_login.current_user.userID)
    if(orders['status'] == 0):
        return render_template('orders-page.html',ordersList = orders['data'],user = flask_login.current_user)
    else:
        return render_template('orders-page.html',error = orders['message'],user = flask_login.current_user)

@app.route('/order/new',methods=['GET','POST'])
@flask_login.login_required
def newOrder():
        if(request.method == 'POST'):
            district = request.form.get('district')
            street = request.form.get('street')
            flat = request.form.get('flat',type=str,default = '')
            floor = request.form.get('floor',type=str,default = '')
            porch = request.form.get('porch',type=str,default = '')
            house = request.form.get('house')
            email = request.form.get('email',type=str,default='')

            newOrder = Order.addNewOrder(flask_login.current_user.userID,district,
            flat,house,floor,street,porch,email=email)
            if(newOrder['status'] == 0):
                return render_template('order.html',user = flask_login.current_user,data = newOrder['data']['data'])
            else:
                return render_template('order.html',user = flask_login.current_user,error = newOrder['message'])
        else:
            return redirect(url_for('main'))

@app.route('/cart',methods=['GET'])
@flask_login.login_required
def cart():
        cart = Cart.getCartOfUser(flask_login.current_user.userID) #TODO: CHECK STATUS
        if(cart['status'] == 0):
            print('len ' + str(len(cart['data'])))
            return render_template('shoping-cart.html',
            user = flask_login.current_user,
            productsInCart = cart['data'])
        else:
            return render_template('shoping-cart.html',
            user = flask_login.current_user,
            error = cart['message'])


@app.route("/login",methods = ['GET','POST'])
def loginUser():
    if(flask_login.current_user.is_authenticated): #Проверяем вошел ли уже пользователь
        return redirect(url_for('userInfo')) #Перекидываем на страницу профиля
    if(request.method == 'POST'): # Если метод обращения к url POST
        email = request.form.get('email',type=str) # Получаем введенный email 
        password = request.form.get('password',type=str) # Получаем введенный пароль
        userID = User.validateUserAndReturnUserID(email,password) #Получаем ID пользователя по введенному email и паролю
        if(userID != -1):# Если пользователь найден
            flask_login.login_user(load_user(userID),remember=True)#Логиним пользователя в системе
            return redirect(url_for('showBooks',page=1))# Перекидываем на страницу книг
        else:
            return render_template('login.html',error = "Not found")#Выводим страницу логина с ошибкой
    else:
        return render_template('login.html')# Если метод обращения не POST , то выводим html страницу логина

@app.route('/registration',methods=['GET','POST'])
def registrationUser():
    if(flask_login.current_user.is_authenticated):
        return redirect(url_for('userInfo'))
    if(request.method == 'POST'):
        email = request.form.get('email',type=str) # Получаем введенный email пользователя
        pswd = request.form.get('pswd',type=str) # Получаем введенный пароль пользователя
        pswd2 = request.form.get('pswd2',type=str) # Получаем введенный 2 пароль пользователя
        first_name = request.form.get('firstName',type=str) # Получаем введенныое имя пользователя
        last_name = request.form.get('lastName',type=str) # Получаем введенную фамилию пользователя
        birthdate = request.form.get('birthDate') # Получаем введенную дата рождения пользователя
        if(pswd != pswd2):
            return render_template('registration.html',error = 'Password mismatch') # Возвращаем html с ошибкой
        resultRegisterOperation = User.registerUser(email,pswd,last_name,first_name,birthdate) # Создаем пользователя
        if(resultRegisterOperation["status"] == 8):
            return render_template('registration.html',error = 'User already exists') # Возвращаем html с ошибкой
        elif(resultRegisterOperation['status'] == 7):
            return render_template('registration.html',error = 'Incorrect email') # Возвращаем html с ошибкой
        flask_login.login_user(load_user(resultRegisterOperation["userID"]),remember=True) # Авторизируем пользователя
        return redirect(url_for('userInfo'))
    else:
        return render_template('registration.html')# Возвращаем html с формой


@app.route('/user',methods=['GET'])
@flask_login.login_required # Пример декоратора
def userInfo():
        return render_template('user-profile.html',user = flask_login.current_user)

@app.route('/logout',methods=['GET'])
@flask_login.login_required
def logoutUser():
    flask_login.logout_user()
    return redirect(url_for('main'))

@app.route('/books',methods = ['GET'])
def showBooksDefault():
    return showBooks(1)

@app.route('/books/<int:page>',methods=["GET"])
def showBooks(page):
    if(page < 1):
        return render_template('books.html',error = 'Incorrect page',user = flask_login.current_user)
    OFFSET = 5
    userQuerySearch = request.args.get('q',default=None,type=str)
    tagsFilter = request.args.getlist('tags')
    tagsFilterStr = None
    if(userQuerySearch is not None):
        result = Product.getAllProfuctsFilteredByQuery(userQuerySearch,page,OFFSET)
        countOfRows = Product.getQuantityOfRowsInTable(
            'select * from Товар where title like "%{0}% " \
            or author like "%{0}%" order by rate;'.format(userQuerySearch))['count']
    elif(tagsFilter):
        countOfRows = Product.getQuantityOfRowsInTable(sqlQueryHelper.buildSqlQueryByTags('select * from Товар',tagsFilter))['count']
        result = Product.getAllProductsFilteredByTags(tagsFilter,page,OFFSET)
        tagsFilterStr = tagsHelper.makeArrayOfTagsToStr(tagsFilter)
    else:
        countOfRows = Product.getQuantityOfRowsInTable('select * from Товар order by rate;')['count']
        result = Product.getAllProfuctsFilteredByRate(page,OFFSET)
    if(result['status'] == 0):
        countOfPages = countOfRows // OFFSET
        if(countOfRows % OFFSET > 0):
            countOfPages += 1
        countOfPagesRange = pageHelper.getRangeOfPages(countOfPages,page)
        return render_template(
            'books.html', #TODO : IF STATUS
            products = result['data'],
            countOfPagesRange = countOfPagesRange,
            user = flask_login.current_user,
            q = userQuerySearch,
            currentPage=page,
            tagsAlreadySearched = tagsFilterStr)
    elif(result['status'] == 2):
        return render_template('books.html',
        error = 'Not found',
        user = flask_login.current_user,
        q = userQuerySearch,
        tagsAlreadySearched = tagsFilterStr)
    elif(result['status'] == 1):
        return render_template('books.html',
        error = 'SQL runtime error',
        user = flask_login.current_user)
    return render_template('books.html',error='ERROR',user = flask_login.current_user)


@app.route('/books/details/<int:productID>')
def showDetailsOfBook(productID):
    details = Product.getDetailsOfProduct(productID)
    if(details['status'] == 0):
        if(flask_login.current_user.is_authenticated):
            return render_template('shop-details.html',
            user = flask_login.current_user,
            details = details['data'][0],
            quantityInCart = Cart.getQuantityOfProductInCart(flask_login.current_user.userID,productID))
        else:
            return render_template('shop-details.html',
            user = flask_login.current_user,
            details = details['data'][0])
    elif(details['status'] == 2):
        return render_template('shop-details.html',
        user = flask_login.current_user,error = details['message'])
    elif(details['status'] == 1): #TODO: ERROR
        return render_template('shop-details.html',
        user = flask_login.current_user,error = details['message'])
    else:
        return redirect(url_for('showBooks',page=1))







