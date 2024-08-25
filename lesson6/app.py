import requests
from flask import render_template, Flask, request, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = '123456789'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    password = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return self.email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/register_ok')
def register_ok():
    return '<h1>Register ok</h1>'


@app.route('/login_ok')
def login_ok():
    return '<h1>Login ok</h1>'


@app.route('/logout_ok')
def logout_ok():
    return '<h1>Logout ok</h1>'


@app.route('/protected')
@login_required
def protected():
    return '<h1>PROTECTED PAGE</h1>'


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        new_user = User(first_name=first_name, last_name=last_name, email=email,
                        password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('register_ok'))
    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return '<h1>User is not valid</h1>'
        login_user(user)
        return redirect(url_for('login_ok'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('logout_ok'))


@app.route('/weather')
@login_required
def weather():
    try:
        result = requests.get('https://api.openweathermap.org/data/2.5/weather',
                              params={'q': 'Tartu', 'appid': '', 'lang': 'ee',
                                      'units': 'metric'})
        data = result.json()

        condition = data['weather'][0]['description']
        temp = data['main']['temp']
        return render_template('weather.html', condition=condition, temp=temp)
    except:
        return 'exeption'


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
