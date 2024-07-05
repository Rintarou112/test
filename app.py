from flask import session, Flask, request, url_for, render_template, flash, redirect, abort
import sqlite3
from flask_sqlalchemy import *

from wtforms import form, IntegerField, StringField, FloatField, SubmitField
from flask_wtf import FlaskForm

from wtforms.validators import *
from sqlalchemy import *
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "GDtfD^&$%@^8tgYjD"
csrf = CSRFProtect(app)
menu = [{"name": 'Главная', "url": "index"},
        {"name": 'База данных', "url": "bazad"},
        {"name": 'Добавить фильм', "url": "vnesenie"},
        {"name": 'Добавить пользователя', "url": "users"},
        {"name": 'Авторизация', "url": "login"},
        {"name": 'Обратная связь', "url": "contact"},
        {"name": 'О сайте', "url": "about"}]


class MyForm(FlaskForm):
    name_film = StringField('Имя', validators=[DataRequired()])
    year = IntegerField('Год', validators=[DataRequired()])
    rating = FloatField('Рейтинг', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MyUsers(FlaskForm):
    name_user = StringField('Имя', validators=[DataRequired()])
    familia = StringField('Фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Film(db.Model):
    __tablename__="movies"
    id = db.Column(db.Integer, primary_key=True)
    name_film = db.Column(db.String(120))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre = db.Column(db.String(120))

    def __init__(self, name, year, rating, genre):
        self.name_film = name
        self.year = year
        self.rating = rating
        self.genre = genre

class Users(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    name_user = db.Column(db.String(100))
    familia = db.Column(db.String(100))
    age = db.Column(db.Integer)
    
    def __init__(self, name, familia, age):
        self.name_user = name
        self.familia = familia
        self.age = age
        
    #def __repr__(self):
    #    return '<User %r>' % self.username
    
@app.route("/index")
@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)

@app.route("/vnesenie", methods=['POST', 'GET'])
def vnesenie():
    print(url_for('vnesenie'))
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.data['name_film']
            year = form.data['year']
            rating = form.data['rating']
            genre = form.data['genre']
            new_film = Film(name, year, rating, genre)
            db.session.add(new_film)
            db.session.commit()
           
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
       
    return render_template('vnesenie.html', title='Добавить фильм', form=form, menu=menu)

@app.route("/users", methods=['POST', 'GET'])
def users():
    print(url_for('users'))
    form = MyUsers()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.data['name_user']
            familia = form.data['familia']
            age = form.data['age']
            new_user = Users(name, familia, age)
            db.session.add(new_user)
            db.session.commit()
    return render_template('users.html', title="Добавить пользователя",  menu=menu, form=form)

@app.route("/bazad",  methods=['POST', 'GET'])
def bazad():
    form1 = MyForm()
    if request.method == 'POST':
        if form1.validate_on_submit():
            name = form1.data['name_film']
            year = form1.data['year']
            rating = form1.data['rating']
            genre = form1.data['genre']
            new_film = Film(name, year, rating, genre)
            db.session.add(new_film)
            db.session.commit()
            
    data = Film.query.all()
    #con = sqlite3.connect('instance/movies.db')
    #cur = con.cursor()
    #res = cur.execute("SELECT * FROM movies")
    #data = res.fetchall()
    
    users = Users.query.all()
    form2 = MyUsers()
    if request.method == 'POST':
        if form2.validate_on_submit():
            name = form2.data['name_user']
            familia = form2.data['familia']
            age = form2.data['age']
            new_user = Users(name, familia, age)
            db.session.add(new_user)
            db.session.commit()
            
    #con = sqlite3.connect('instance/movies.db')
    #cur = con.cursor()
    #res = cur.execute("SELECT * FROM users")
    #users = res.fetchall()
    return render_template('bazad.html', title="База данных",  menu=menu, data=data, users=users, form1=form1, form2=form2)

@app.route("/bazad/<int:id>")
def delet(id):
    Users.query.filter_by(id=id).delete()
    Film.query.filter_by(id=id).delete()
    try:
        db.session.commit()
        return redirect(url_for('bazad'))
    except:
        return 'Ошибка'

@app.route("/bazad/<int:id>/update", methods=['POST', 'GET'])
def update(id):
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.data['id.name']
            year = form.data['year']
            rating = form.data['rating']
            genre = form.data['genre']
            new_film = Film(name, year, rating, genre)
            db.session.add(new_film)
            db.session.commit()

    return render_template('baza_update.html',  menu=menu, form=form) 
    

@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title = "О сайте", menu=menu)

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
        
    return render_template('contact.html', title = "Обратная связь", menu=menu)

@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title = "Авторизация", menu=menu)

@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Профиль пользователя: {username}"

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)

if __name__ == "__main__":
    
    app.run(debug=True)