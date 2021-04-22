import flask
from flask import Flask, render_template
app = Flask(__name__)


# set key to encrypt our sessions
app.secret_key = "@#$^kWe%^28DDgg^7@"
# Home Page, Login, register, navigation
# this is the default route,
# static folder - used to place css, js, images
# templates - used to place HTML files

@app.route('/')
def home():
    # run this route using  http://127.0.0.1:5000/
    return render_template('home.html')



# sessions management
from flask import request, redirect
from flask import session
@app.route('/login', methods = ['POST','GET']) # decorator
def login():
    # Create a login in HTML , email, password and button
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        # create a connections
        connection = pymysql.connect(host='localhost', user='root', password='1234D!@#$', database='uhai_hospital_db')
        sql = "select * from users where email = %s and password = %s"
        # create a cursor and execute above sql
        cursor = connection.cursor()
        cursor.execute(sql, (email, password))

        # check if no match found, Failure, send back a message to login template
        if cursor.rowcount < 1:
            return render_template('login.html', message = "Wrong Credentials, Try Again")

        # if 1 match is found , its a success, take user to next screen /add
        elif cursor.rowcount == 1:

            # since we have the user email, we use it as a session
            # you store the email using session['key']
            session['key'] = email
            return redirect('/search_patient')
        # here means its either a rowcount of 2 or more, means there are duplicates email
        else:
            return render_template('login.html', message="Contact Admin.")
    else:
        return render_template('login.html')


# this route is used to clear the sessions
@app.route('/logout')
def logout():
    session.pop('key',None)
    return redirect('/login')

# on chrome ctrl + shift + i
# on firefox - shift + f9


@app.route('/register')
def register():
    # do a registration page, username, email, password, confirm password,
    # location, phone, gender, dob
    # and a button
    return render_template('register.html')


@app.route('/cars')
def cars():
    return 'These are our latest cars'



# Agenda: connection between templates and your routes
# How to post data from a template to a route in python and vise versa
# Using a payroll calc.
# back end, backend receives from the from the form

from flask import request
@app.route('/payroll', methods = ['POST','GET'])
def payroll():
    if request.method == 'POST':
        basic = request.form['basic']
        allowances = request.form['allowances']
        nssf = request.form['nssf']
        nhif = request.form['nhif']

        # above we received what was posted from the form
        # get gross
        gross = float(basic) + float(allowances)

        # get net
        netpay = gross - (float(nssf) + float(nhif))

        # we return the answers to the template
        return render_template('payroll.html', gross = gross, netpay = netpay)

    else:  # the user did not click the button
        return render_template('payroll.html')




# this route will be used to add a patient to our uhai_db
from flask import request
import pymysql
@app.route("/add", methods = ['POST','GET'])
def add():
    if request.method =='POST':
        patient_id = request.form['patient_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        next_of_kin = request.form['next_of_kin']
        next_of_kin_phone = request.form['next_of_kin_phone']

        # above we captured the details from the form
        # Next we save to the database

        connection = pymysql.connect(host='localhost', user='root', password='1234D!@#$', database='uhai_hospital_db')

        # we now do an insert sql query
        sql = "insert into patients_tbl(patient_id, first_name, last_name, surname, email, phone, address, next_of_kin, next_of_kin_phone)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        # run above sql, you run sql using cursor
        cursor = connection.cursor()
        # run/execute sql and provide the values


        cursor.execute(sql, (patient_id, first_name, last_name, surname, email, phone, address, next_of_kin, next_of_kin_phone))
        connection.commit()
        return render_template('add.html', message= "Record Saved Successfully, Thank you.")

    else:
        # we pause, then we go create a template for add.html
        return render_template('add.html')



# Assignment will on saving a doctor.
# You will create a template, a route and a table.
# fields in the table will be doctor_id (PK), first_name, last_name, surname, email, phone,
# exp, kra_pin, nssf_no, hhif_no


# This route will view all patients
# this route is session protected
@app.route("/view_patients")
def view_patients():
    if 'key' in session:
        connection = pymysql.connect(host='localhost', user='root', password='1234D!@#$', database='uhai_hospital_db')
        sql = "select * from patients_tbl"
        # create cursor
        cursor = connection.cursor()

        # execute sql using the cursor
        cursor.execute(sql)

        # you check are there any  patients
        if cursor.rowcount == 0:
            return render_template('view_patients.html', message = "No patients, Please navigate to add patient page")
        else:
            # here means there are patients, fetch all
            rows = cursor.fetchall()
            return render_template('view_patients.html', rows = rows)
    else:
        return redirect('/login')






# Today:  searching records
@app.route('/search_patient', methods = ['POST','GET'])
def search_patient():
    if 'key' in session:
        if request.method == 'POST':
            patient_id = request.form['patient_id']

            connection = pymysql.connect(host='localhost', user='root', password='1234D!@#$', database='uhai_hospital_db')
            sql = "select * from patients_tbl where patient_id = %s"

            # create cursor
            cursor = connection.cursor()

            # execute sql using the cursor, provide the patient id
            cursor.execute(sql, (patient_id))
            # you check are there any  patients
            if cursor.rowcount == 0:
                return render_template('search_patient.html', message="Patient ID Does not exist")

            else:
                # here means there are patients, fetch all
                rows = cursor.fetchall()
                return render_template('search_patient.html', rows=rows)



        else:
            connection = pymysql.connect(host='localhost', user='root', password='1234D!@#$', database='uhai_hospital_db')
            sql = "select * from patients_tbl order by patient_id DESC limit 20"

            # create cursor
            cursor = connection.cursor()

            # execute sql using the cursor
            cursor.execute(sql)

            # you check are there any  patients
            if cursor.rowcount == 0:
                return render_template('search_patient.html', message="No patients, Please navigate to add patient page")

            else:
                # here means there are patients, fetch all
                rows = cursor.fetchall()
                return render_template('search_patient.html', rows=rows)

    else:
        return redirect('/login')



@app.route('/phones')
def phones():
    connection = pymysql.connect(host='localhost', user='root', password='1234D!@#$', database='uhai_hospital_db')
    sql = "select * from products"
    # create cursor
    cursor = connection.cursor()

    # execute sql using the cursor
    cursor.execute(sql)

    # you check are there any  patients
    if cursor.rowcount == 0:
        return render_template('phones.html', message = "No Products")
    else:
            # here means there are patients, fetch all
        rows = cursor.fetchall()
        return render_template('phones.html', rows = rows)



@app.route('/single_display/<product_id>')
def single_display(product_id):
    connection = pymysql.connect(host='localhost', user='root', password='1234D!@#$', database='uhai_hospital_db')
    cursor = connection.cursor()
    # execute the query using the cursor
    cursor.execute("select * from products where product_id = %s", (product_id))
    # check if no records were found
    if cursor.rowcount < 1:
        return render_template('single_display.html', message="This Product does not exist")
    else:
        # return all rows found
        rows = cursor.fetchall()
        return render_template('single_display.html', rows=rows)




@app.route("/order", methods = ['POST','GET'])
def order():
    if request.method =='POST':
        id = request.form['id']
        qtty = request.form['qtty']
        email = request.form['email']
        phone = request.form['phone']
        connection = pymysql.connect(host='localhost', user='root', password='1234D!@#$', database='uhai_hospital_db')

        # we now do an insert sql query
        sql = "insert into orders(product_id, qtty, email, phone)  VALUES(%s,%s,%s,%s)"

        # run above sql, you run sql using cursor
        cursor = connection.cursor()
        # run/execute sql and provide the values

        try:
            cursor.execute(sql, (
            id, qtty, email, phone))
            connection.commit()
            return render_template('complete.html', message="Order Made Successfully, Thank you.")
        except:
            return render_template('complete.html', message="Order Failed, Thank you.")

    else:
        # we pause, then we go create a template for add.html
        return render_template('complete.html')




# create a dummy domain/base URL
# use double underscores
if __name__  == '__main__':
    app.run()


# when you run the app, test in the browser using
# http://127.0.0.1:5000/login
# http://127.0.0.1:5000/register
# http://127.0.0.1:5000/cars
# http://127.0.0.1:5000/









