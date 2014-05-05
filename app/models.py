from hashlib import md5
from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(80), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	about = db.Column(db.String(140))
	last_login = db.Column(db.DateTime)
	sentences = db.relationship('Sentence', backref = 'author', lazy = 'dynamic')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

	def __repr__(self):
		return '<User %r>' % (self.username)

	@staticmethod
	def make_unique_username(username):
		if User.query.filter_by(username = username).first() == None:
			return username
		version = 2
		while True:
			new_username = username + str(version)
			if User.query.filter_by(username = new_username).first() == None:
				break
			version +=1
		return new_username

	def recent_sentences(self):
		return Sentence.query.order_by(Sentence.published_date.desc())

class Sentence(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	published_date = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body) 
