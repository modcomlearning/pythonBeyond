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
    return 'This my nice login...'


@app.route('/register')
def register():
    # do a registration page, username, email, password, confirm password,
    # location, phone, gender, dob
    # and a button
    return 'Here is our good registration route'


@app.route('/cars')
def cars():
    return 'These are our latest cars'




# create a dummy domain/base URL
# use double underscores
if __name__  == '__main__':
    app.run()


# when you run the app, test in the browser using
# http://127.0.0.1:5000/login
# http://127.0.0.1:5000/register
# http://127.0.0.1:5000/cars
# http://127.0.0.1:5000/









