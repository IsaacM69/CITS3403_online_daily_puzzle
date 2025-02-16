from telnetlib import GA
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Goal_words, User, Game
from werkzeug.urls import url_parse
from datetime import date

@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        u = current_user
        games = u.games.all()
        played=len(games)
        wins = 0
        losses = 0
        CStreak = 0
        MStreak = 0

        for game in games:
            if game.win == False:
                losses += 1
                if CStreak > MStreak:
                    MStreak = CStreak
                CStreak = 0
            if game.win == True:
                wins +=1
                CStreak +=1
                if CStreak > MStreak:
                    MStreak = CStreak
        
    #Check for date here, if not add new day
    return render_template('base.html', played=played, wins=wins, CStreak=CStreak, MStreak=MStreak)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login_base.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    #if current_user.is_authenticated:
    #    return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register_base.html', title='Register', form=form)



@app.route('/index/<jsdata>')
@login_required
def get_javascript_data(jsdata):
    print(jsdata)

    if jsdata == '<LOSS>':
        u = current_user
        game = Game(win=False, author=u)
        db.session.add(game)
        db.session.commit()

    if jsdata == '<WIN>':
        u = current_user
        game = Game(win=True, author=u)
        db.session.add(game)
        db.session.commit()

    return jsdata

def get_date():
    date = 'today'
    return date

def get_asia():
    city = 'perth'
    return city

def get_na():
    city = 'perth'
    return city

def get_europe():
    city = 'perth'
    return city

def get_africa():
    city = 'perth'
    return city

def get_sa():
    city = 'perth'
    return city

def get_oceania():
    city = 'perth'
    return city


def new_day():
    g = Goal_words(date = get_date(), asia = get_asia(), north_america = get_na(), europe = get_europe(), africa = get_africa(), sounth_america = get_sa(), oceania = get_oceania())
    db.session.add(g)
    db.session.commit()