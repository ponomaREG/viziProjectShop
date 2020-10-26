from flask import request,redirect,url_for,render_template
from app import app
from app.admin.models.Admin import Admin
import flask_login
import os
from werkzeug.utils import secure_filename



@app.route('/admin',methods=['GET','POST'])
def loginAdmin():
    if(flask_login.current_user.is_authenticated): #Проверяем вошел ли уже пользователь
        if(flask_login.current_user.is_admin):
            return render_template('admin-page.html') #Перекидываем на страницу профиля
        else:
            return redirect(url_for('main'))
    else:
        return redirect(url_for('loginUser'))

@app.route('/admin/orders',methods=['GET','POST'])
@flask_login.login_required
def adminManageOrders():
    if(flask_login.current_user.is_admin):
         if(request.method == 'POST'):
            method = request.form.get('method',default=1,type=int)
            if(method == 1 or method == 2):
                date_b = request.form.get('date_b')
                date_e = request.form.get('date_e')
                resultStat = None

                if(method == 1):
                    resultStat = Admin.getAllOrdersByPeriod(date_b,date_e,flask_login.current_user.userID)
                elif(method == 2):
                    resultStat = Admin.getCountOfOrderByPeriod(date_b,date_e,flask_login.current_user.userID)
                else:
                    return render_template('admin-manage-orders.html',message = 'Incorrect method')
                if resultStat is not None:
                    if(resultStat['status'] == 3):
                        return render_template('admin-manage-orders.html',date_e = date_e,date_b = date_b,message = resultStat['message'])
                    elif(resultStat['status'] == 0):
                        return render_template('admin-manage-orders.html',date_e = date_e,date_b=date_b,resultOfResponse = resultStat)
                else:
                    return render_template('admin-manage-orders.html',date_e = date_e,date_b = date_b)
            elif(method == 3):
                orderID = request.form.get('orderID-3',type = int)
                resultStat = Admin.getInfoOfOrderBy(orderID,flask_login.current_user.userID)
                if(resultStat['status'] == 0):
                    return render_template('admin-manage-orders.html',resultOfResponse = resultStat)
                elif(resultStat['status'] == 3):
                    return render_template('admin-manage-orders.html',message = resultStat['message'])
            elif(method == 4):
                status = request.form.get('status',type = int)
                resultOfResponse = Admin.getOrdersByStatus(status,flask_login.current_user.userID)
                if(resultOfResponse['status'] == 0):
                    return render_template('admin-manage-orders.html',resultOfResponse = resultOfResponse)
                elif(resultOfResponse['status'] == 3):
                    return render_template('admin-manage-orders.html',message = resultOfResponse['message'])
            elif(method == 5):
                newStatus = request.form.get('newStatus',type = int)
                orderID = request.form.get('orderID-5',type=int)
                resultOfResponse = Admin.setNewStatusOfOrder(newStatus,orderID,flask_login.current_user.userID)
                return render_template('admin-manage-orders.html',resultOfResponse = resultOfResponse)


         else:
            return render_template('admin-manage-orders.html')
    else:
        return redirect(url_for('main'))

@app.route('/admin/stat',methods=['GET','POST'])
@flask_login.login_required
def adminStat():
    if(flask_login.current_user.is_admin):
        if(request.method == 'POST'):
            date_b = request.form.get('date_b')
            date_e = request.form.get('date_e')
            method = request.form.get('method',default=1,type=int)
            resultStat = None

            if(method == 1):
                resultStat=Admin.getAllIncomeByPeriod(date_b,date_e,flask_login.current_user.userID)
            elif(method == 2):
                resultStat = Admin.getRatingPopularityOfBooksByPeriod(date_b,date_e,flask_login.current_user.userID)
            else:
                return render_template('admin-stat.html',message = 'Incorrect method')
            if resultStat is not None:
                if(resultStat['status'] == 3):
                    return render_template('admin-stat.html',date_e = date_e,date_b = date_b,message = resultStat['message'])
                elif(resultStat['status'] == 0):
                    return render_template('admin-stat.html',date_e = date_e,date_b=date_b,resultOfResponse = resultStat)
            else:
                return render_template('admin-stat.html',date_e = date_e,date_b = date_b)

        else:
            return render_template('admin-stat.html')
    else:
        return redirect(url_for('loginUser'))

@app.route('/admin/product',methods=['GET','POST'])
@flask_login.login_required
def adminGetProductInfo():
     if(flask_login.current_user.is_admin):
         columnNames = Admin.getColumnsOfTable('Товар')
         if(request.method == 'GET'):
             return render_template('admin-product.html',columnNames = columnNames['data'])
         else:
             method = request.form.get('method',type=int)

             if(method == 1):
                column = request.form.get('column')
                value = request.form.get('value')
                resultOfResponseToDB = Admin.getInfoOfBookBy(column,value,flask_login.current_user.userID)
             elif(method == 2):
                quantity = request.form.get('quantity',type = int)
                productID = request.form.get('productID-2',type = int)
                resultOfResponseToDB = Admin.setNewValueBook(productID,"quantity",quantity,flask_login.current_user.userID)
             elif(method == 3):
                 desc = request.form.get('desc')
                 productID = request.form.get('productID-3',type=int)
                 resultOfResponseToDB = Admin.setNewValueBook(productID,"description",desc,flask_login.current_user.userID)
             elif(method == 4):
                 price = request.form.get('price',type=float)
                 productID = request.form.get('productID-4',type=int)
                 resultOfResponseToDB = Admin.setNewValueBook(productID,'cost_sale',price,flask_login.current_user.userID)
             elif(method == 6):
                 tags = request.form.get('tags',type=str)
                 productID = request.form.get('productID-6',type=int)
                 resultOfResponseToDB = Admin.setNewValueBook(productID,'tags',tags,flask_login.current_user.userID)
             elif(method == 5):
                 productID = request.form.get('productID-5',type=int)
                 if 'image' in request.files:
                    file = request.files['image']
                    if(file.filename != ''):
                        filename = secure_filename(file.filename)
                        filePath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                        file.save(filePath)
                        resultOfResponseToDB = Admin.setNewValueBook(productID,'imageLink',filename,flask_login.current_user.userID)
                    else:
                        return render_template('admin-product.html',columnNames = columnNames['data'],message = 'Image not uploaded 1')
                 else:
                     return render_template('admin-product.html',columnNames = columnNames['data'],message = 'Image not uploaded 2')
             else:
                 return render_template('admin-product.html',columnNames = columnNames['data'],message = 'What the fuck???Method:{}'.format(method))
             if(resultOfResponseToDB['status'] == 0):
                 return render_template('admin-product.html',resultOfResponse = resultOfResponseToDB,columnNames = columnNames['data'])
             elif(resultOfResponseToDB['status'] == 3):
                 return render_template('admin-product.html',message = 'Empty',columnNames = columnNames['data'])
             elif(resultOfResponseToDB['status'] == 130):
                 return render_template('admin-product.html',message = resultOfResponseToDB['message'],columnNames = columnNames['data'])
             


@app.route('/admin/add',methods=['GET','POST'])
@flask_login.login_required
def adminAddNew():
    if(flask_login.current_user.is_admin):
        if(request.method == 'GET'):
            return render_template('admin-add.html')
        else:
            title = request.form.get('title')
            author = request.form.get('author')
            desc = request.form.get('desc')
            cost_purchase = request.form.get('cost_purchase',type = float)
            cost_sale = request.form.get('cost_sale',type = float)
            quantity = request.form.get('quantity',type=int)
            tags = request.form.get('tags')
            filename = app.config['PLACEHOLDER_NAME']
            if 'image' in request.files:
                file = request.files['image']
                if(file.filename != ''):
                    filename = secure_filename(file.filename)
                    filePath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                    file.save(filePath)

            result = Admin.insertNewBook(title,author,desc,cost_sale,cost_purchase,quantity,filename,tags,flask_login.current_user.userID)
            if(result['status'] == 0):
                return render_template('admin-add.html',message = 'Added!',productID = result['data'][0])
            else:
                return render_template('admin-add.html',message = 'No added(')
    else:
        return redirect(url_for('loginUser'))
