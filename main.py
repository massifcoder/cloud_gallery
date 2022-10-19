from flask import Flask, redirect, url_for
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'what_the_fuck'


# Create the form class
class ContactForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()], render_kw={"placeholder": "Enter your email address"})
    passwords = PasswordField('password', validators=[InputRequired()],
                              render_kw={"placeholder": "Enter your password"})


class AddUser(FlaskForm):
    name = StringField('name', validators=[InputRequired()], render_kw={'placeholder': 'Users Name', 'id': 'names'})
    age = StringField('age', validators=[InputRequired()], render_kw={'placeholder': 'Users Age', 'id': 'ages'})
    email = StringField('name', validators=[InputRequired()], render_kw={'placeholder': 'Users Email', 'id': 'emails'})
    userType = StringField('name', validators=[InputRequired()],
                           render_kw={'placeholder': 'User Type', 'id': 'usertypes'})

@app.route('/', methods=['POST', 'GET'])
def home():
    form = ContactForm()
    # conn = sqlite3.connect('users.db')
    # c = conn.cursor()
    # c.execute("""CREATE TABLE users(name TEXT,age INTEGER,email TEXT PRIMARY KEY ,usertype TEXT)""")
    # conn.execute()
    if form.validate_on_submit():
        return redirect(url_for('classes'))
    return render_template('Login_Page/index.html', form=form)


@app.route('/item')
def classes():
    return render_template("Image_Gallery/index.html")


@app.route('/administrator',methods=["POST", "GET"])
def administrator():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    d = c.execute("""SELECT * FROM users""")
    # for i in range(len(list(d))
    d = list(d)
    ll = len(d)
    return render_template("Administrator/index.html", users=d, length=ll)
    # return 'hi'

@app.route('/add_user', methods=["POST", "GET"])
def addUser():
    form = AddUser()
    if form.validate_on_submit():
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        name = form.name.data
        email = form.email.data
        usertype = form.userType.data
        age = form.age.data
        c.execute(f"""
                INSERT INTO users(name,age,email,usertype) VALUES('{name}','{age}','{email}','{usertype}')
                """)
        conn.commit()
        conn.close()
        return redirect(url_for('administrator'))
    return render_template('AddUser/index.html', form=form)


app.run(debug=True)