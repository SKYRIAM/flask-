from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email,Required,Length,Email,Regexp,EqualTo
from flask_wtf import Form
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):   #用户登录
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(Form):   #用户注册
	email = StringField('Email',validators=[Required(),Length(1,64),Email()])
	
	name = StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must hava only letters,' 'numbers,dots or underscores')])#确保name字段只包含字母，数字，下划线，等号
	password = PasswordField('Password',validators=[Required(),EqualTo('password2',message='Password must match.')])#验证两个密码是否一致
	password2 = PasswordField('Confirm password',validators=[Required()])
	submit = SubmitField('Register')

	def validate_email(self,field):  #验证字段函数
		if User.query.filter_by(email = field.data).first():
			raise ValidationError('Email already registered')
	def validate_name(self,field):
		if User.query.filter_by(name = field.data).first():
			raise ValidationError('Username already in use')