from threading import currentThread
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app, session_options={"autoflush": False})
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    invite_code = db.Column(db.String(80))
    number_of_members = db.Column(db.Integer)
    users = db.relationship('User', backref='_team')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))
    team = db.Column(db.Integer, db.ForeignKey('team.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class RegisterForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class RegisterTeam(FlaskForm):
    name = StringField('name')
    invite_code = StringField('invite_code')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('index.html')
    
    return render_template('signup.html', form=form)

def check_invite_code(hashed_invite_code, input):
    if check_password_hash(hashed_invite_code, input):
        teams = Team.query.all()
        for team in teams:
            print("-")
            if check_password_hash(team.invite_code, input):
                print(hashed_invite_code)
                print(team.invite_code)
                team.number_of_members += 1
                current_user.team = team 
        pass
    pass

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    form = RegisterTeam()
    hashed_invite_code = generate_password_hash(form.invite_code.data, method='sha256')
    teams = Team.query.all()

    if "new_team" in request.form: 
        teams = Team.query.all()
        for team in teams:
            if team.name == form.name.data:
                return ('This team name is already taken!')

        hashed_invite_code = generate_password_hash(form.invite_code.data, method='sha256')
        new_team = Team(name=form.name.data, invite_code=hashed_invite_code, number_of_members=1, users=[current_user])
        current_user.team = new_team
        db.session.add(new_team)
        db.session.commit()
        teams = Team.query.all()

    if "join_team" in request.form:
        check_invite_code(hashed_invite_code, form.invite_code.data)

    if "leave_team" in request.form:
        db.session.delete(db.session.query(User).filter(current_user.team==User.team).first())
        db.session.commit()

    return render_template('dashboard.html', user=current_user, form=form, teams=teams)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
