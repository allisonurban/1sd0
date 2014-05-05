from datetime import datetime, date
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, EditForm, SentenceForm
from models import User, Sentence
from config import POSTS_PER_PAGE
import re

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_login = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/')
@app.route('/feed/<int:page>')
# @login_required
def index(page = 1):
	if g.user.is_authenticated():
		sentences = g.user.recent_sentences().paginate(page, POSTS_PER_PAGE, False)
		last_wrote = g.user.sentences.first().published_date
		return render_template('feed.html', 
			title = 'Feed', 
			sentences = sentences,
			last_wrote = last_wrote,
			go_write = last_wrote.date() < date.today())
	else:
		return render_template('index.html')

@app.route('/write', methods = ['GET', 'POST'])
@login_required
def write():
	form = SentenceForm()
	if form.validate_on_submit():
		sentence = Sentence(body = form.sentence.data, published_date = datetime.utcnow(), author = g.user)
		db.session.add(sentence)
		db.session.commit()
		flash('Success! Your sentence has been posted.')
		return redirect(url_for('index'))
	return render_template('write.html', 
		title = 'Write', 
		form = form,
		today = datetime.now())

@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
@login_required
def user(username, page = 1):
	user = User.query.filter_by(username = username).first()
	if user == None:
		flash('User ' + username + ' not found.')
		return redirect(url_for('index'))
	sentences = user.sentences.paginate(page, POSTS_PER_PAGE, False)
	return render_template('user.html',
		user = user,
		sentences = sentences)

@app.route('/sentence/<int:id>')
def sentence(id, page = 1):
    sentence = Sentence.query.filter_by(id = id).first()
    if sentence == None:
        flash('Sentence not found.')
        return redirect(url_for('index'))
    return render_template('sentence.html',
    	sentence = sentence)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.username)
	if form.validate_on_submit():
		g.user.username = form.username.data
		g.user.about = form.about.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('user', username = g.user.username))
	else:
		form.username.data = g.user.username
		form.about.data = g.user.about
	return render_template('edit.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
	return render_template('login.html',
		title = 'Sign In',
		form = form,
		providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	user = User.query.filter_by(email = resp.email).first()
	if user is None:
		username = resp.nickname
		if username is None or username == "":
			username = resp.email.split('@')[0]
		user = User(username = username, email = resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out. See you tomorrow!')
    return redirect(url_for('index'))
