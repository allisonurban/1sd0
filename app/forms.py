from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, Length
from app.models import User

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class EditProfileForm(Form):
    username = TextField('username', validators = [Required()])
    about = TextAreaField('about', validators = [Length(min=0, max=140)])

    def __init__(self, original_username, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_username = original_username

    def validate(self):
        if not Form.validate(self):
            return False
        if self.username.data == self.original_username:
            return True
        user = User.query.filter_by(username = self.username.data).first()
        if user != None:
            self.username.errors.append('This username is already in use. Please choose another one.')
            return False
        return True

class SentenceForm(Form):
    sentence = TextAreaField('sentence', validators = [Required()])