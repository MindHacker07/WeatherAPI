''' from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
weatherstack_api_key = "003a87c533f4f9a8e434d480dd4c1c997" '''

import requests
from flask import Flask, request,render_template, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100))
    confirmpassword = db.Column(db.String(100))
    phone=db.Column(db.Integer, nullable=False)

    def __init__(self,name,email,password,confirmpassword,phone):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        self.confirmpassword =confirmpassword
        self.phone = phone


    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('/login.html')

@app.route('/register.html',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']

        phone = request.form['phone']
        
        new_user = User(name=name,email=email,password=password,confirmpassword=confirmpassword,phone=phone)
        db.session.add(new_user)
        '''db.session.commit()'''
        db.session.commit()
        return redirect('/login.html')

    return render_template('register.html')

@app.route('/login.html',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/home.html')
        else:
            return render_template('/login.html',error='Invalid user')

    return render_template('/login.html')


@app.route('/home.html')
def home():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('home.html',user=user)
    
    return redirect('/login.html') 

'''@app.route('/home.html')
def home():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('home.html',user=user) 
    
    return redirect('/login.html')'''

@app.route('/manual.html')
def manual():
    return redirect('/manual.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login.html')

if __name__ == '__main__':
    app.run(debug=True)


