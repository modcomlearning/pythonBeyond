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


@app.route('/login') # decorator
def login():
    # Create a login in HTML , email, password and button
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


















# create a dummy domain/base URL
# use double underscores
if __name__  == '__main__':
    app.run()


# when you run the app, test in the browser using
# http://127.0.0.1:5000/login
# http://127.0.0.1:5000/register
# http://127.0.0.1:5000/cars
# http://127.0.0.1:5000/









