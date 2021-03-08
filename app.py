from flask_login import LoginManager,login_user,current_user,login_required,logout_user
from userclass import DbUser
import urllib.request, json


from main import app, engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
from flask import request, jsonify,render_template,redirect,flash,url_for
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Session
from flask_cors import CORS, cross_origin
import os
CORS(app, support_credentials=True)
Base = automap_base()
Base.prepare(engine, reflect=True)
User=Base.classes.users

login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    print("userid")
    print(user_id)
    user = session.query(User).filter(or_(User.userid == user_id)
                                          ).first()
    return DbUser(user)

# @login_manager.user_loader
# def get_user(ident):
#     print(ident)
#     user=session.query(User).filter(or_(User.userid == ident) ).first()
#     print(user)
#     return user


session = Session(engine)
metadata = MetaData(engine)


@app.route('/index')
@app.route('/',methods=['POST','GET'])
@login_required
def index():
    if request.method=="POST":
        ingredents=request.form.get('ingredients')
        apiurl="http://www.recipepuppy.com/api/?i={}".format(ingredents)
        with urllib.request.urlopen(apiurl) as url:
            data = json.loads(url.read().decode())
            recips = data['results']
        return render_template('index.html',recipes=recips)
    recips=[]
    with urllib.request.urlopen("http://www.recipepuppy.com/api/") as url:
        data = json.loads(url.read().decode())
        recips=data['results']
    return render_template('index.html',recipes=recips)





@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method=="POST":
        email = request.form.get('email')
        user = session.query(User).filter(or_(User.email == email)
                                          ).first()
        print(user)
        if user:
            print("ok")
            flash("This email Already Exist")
            return redirect(url_for('register'))
        name = request.form.get('name')
        password = request.form.get('password')
        password_hash = password
        account = Table('users', metadata, autoload=True)

        engine.execute(account.insert(), email=email,
                       fullname=name, password=password_hash)
        #engine.dispose()
        session.close()
        return redirect(url_for('login'))
     #engine.dispose()
        session.close()

    return render_template("signup.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method=="POST":
        engine.dispose()
        session.close()
        email= request.form.get('email')
        password_entered = request.form.get('password')
        user = session.query(User).filter(or_(User.email == email)
                                              ).first()
        if user is not None and user.password==password_entered:
            user.password=password_entered
            if login_user(DbUser(user)):
                flash('You are now logged in')
                return redirect(url_for('index'))
        flash('Email or password Wrong')
        return redirect(url_for('login'))
    return render_template("login.html")


@app.route('/update', methods=["GET", "POST"])
def update():
    session.close()
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    about=request.form.get('about')
    password_hash = generate_password_hash(password)
    print(password_hash)
    account = Table('users', metadata, autoload=True)
    user = current_user.get_user()
    engine.execute(account.update().where(account.c.userid==user.userid), email=email,
                   fullname=name, password=password_hash,about=about)
    return redirect(url_for('profile'))


@login_required
@app.route('/profile', methods=["GET", "POST"])
def profile():
    user=current_user.get_user()
    return render_template("profile.html",current_user=user)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add_book', methods=["GET", "POST"])
def add_book():
    isbn = request.args.get('isbn')
    book_title = request.args.get('book_title')
    book_author = request.args.get('book_author')
    publication_year = request.args.get('publication_year')
    image_url = request.args.get('image_url')
    price = request.args.get('price')
    books = Table('books', metadata, autoload=True)
    engine.execute(books.insert(), isbn=isbn,
                   book_title=book_title, book_author=book_author, publication_year=publication_year,
                   image_url=image_url, price=price)
    return jsonify({'book_added': True})




if __name__=='__main__':
    app.run()
