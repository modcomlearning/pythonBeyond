import flask
from flask import Flask, render_template
app = Flask(__name__)

# Home Page, Login, register, navigation
# this is the default route,
# static folder - used to place css, js, images
# templates - used to place HTML files


@app.route('/')
def home():
    # run this route using  http://127.0.0.1:5000/
    return render_template('home.html')




from flask import request, redirect
@app.route('/login', methods = ['POST','GET']) # decorator
def login():
    # Create a login in HTML , email, password and button
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        # create a connections
        connection = pymysql.connect(host='localhost', user='root', password='', database='uhai_hospital_db')

        sql = "select * from users where email = %s and password = %s"

        # create a cursor and execute above sql
        cursor = connection.cursor()
        cursor.execute(sql, (email, password))

        # check if no match found, Failure, send back a message to login template
        if cursor.rowcount < 1:
            return render_template('login.html', message = "Wrong Credentials, Try Again")

        # if 1 match is found , its a success, take user to next screen /add
        elif cursor.rowcount == 1:
            return redirect('/add')
        # here means its either a rowcount of 2, means there are duplicates email
        else:
            return render_template('login.html', message="Contact Admin.")
    else:
        return render_template('login.html')








    return render_template('login.html')










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
@app.route("/view_patients")
def view_patients():
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



# Today:  searching records
@app.route('/search_patient', methods = ['POST','GET'])
def search_patient():
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





# create a dummy domain/base URL
# use double underscores
if __name__  == '__main__':
    app.run()


# when you run the app, test in the browser using
# http://127.0.0.1:5000/login
# http://127.0.0.1:5000/register
# http://127.0.0.1:5000/cars
# http://127.0.0.1:5000/









