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

@app.route('/admin/stat',methods=['GET','POST'])
@flask_login.login_required
def adminStat():
    if(flask_login.current_user.is_admin):
        if(request.method == 'POST'):
            date_b = request.form.get('date_b')
            date_e = request.form.get('date_e')
            method = request.form.get('method',default=1,type=int)
            resultStat = None

            if(method == 3):
                resultStat=Admin.getAllIncomeByPeriod(date_b,date_e)
            elif(method == 2):
                resultStat = Admin.getRatingPopularityOfBooksByPeriod(date_b,date_e)
            elif(method == 1):
                resultStat = Admin.getAllOrdersByPeriod(date_b,date_e)
            elif(method == 4):
                resultStat = Admin.getCountOfOrderByPeriod(date_b,date_e)
            
            if resultStat is not None:
                if(resultStat['status'] == 3):
                    return render_template('admin-stat.html',date_e = date_e,date_b = date_b,message = resultStat['message'])
                elif(resultStat['status'] == 0):
                    return render_template('admin-stat.html',date_e = date_e,date_b=date_b,resultStat = resultStat)
            else:
                return render_template('admin-stat.html',date_e = date_e,date_b = date_b)

        else:
            return render_template('admin-stat.html')
    else:
        return redirect(url_for('loginUser'))

        

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
            result = Admin.insertNewBook(title,author,desc,cost_sale,cost_purchase,quantity,filename,tags)
            if(result['status'] == 0):
                return render_template('admin-add.html',message = 'Added!',productID = result['data'][0])
            else:
                return render_template('admin-add.html',message = 'No added(')
    else:
        return redirect(url_for('loginUser'))
