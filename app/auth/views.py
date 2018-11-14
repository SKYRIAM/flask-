from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from . import auth
from ..models import User
from .forms import LoginForm,RegistrationForm
from .. import db
from ..email import *
#捕捉没有确认的用户,#用户已经登录
@auth.before_app_request
def before_request():
    if current_user.is_authenticated() \
            and not current_user.confirmed \
            and request.endpoint \
            and not request.endpoint.startswith('auth.') \
            and request.endpoint != 'static':
        #print('current_user.is_anonymous',bool(current_user.is_anonymous),type(current_user.is_anonymous))
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    print('unconfirmed',current_user.confirmed)
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

	
#绑定视图函数
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is not None and user.verify_password(form.password.data):
            
            login_user(user, form.remember_me.data)
            return redirect( url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
	
@auth.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	print(form.data['email'])
	if form.validate_on_submit():
		user = User( email=form.data['email'],name=form.data['name'],password=form.data['password'])
		db.session.add(user)
		db.session.commit()#提交后才能确定ID
		token = user.generate_confirmation_token()
		send_email(user.email,'Confirm Your Account','auth/email/confirm', user=user,token=token) #发送邮件
		flash('Yon can now login')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html',form=form)

#验证用户视图，用户点击了邮箱里的链接后就跳转到main/index界面
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	print('confirm!')
	if current_user.confirmed:  #防止从邮箱多次验证
		#print('已经验证过',current_user.confirmed)
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		db.session.commit()
		flash("You hava comfirmed your account ,Thinks")
		#print('进行了验证然后通过',current_user.confirmed)
	else:
		flash('The confirmation link is invaild or has expored')
		#print('没验证过',current_user.confirmed)
	return redirect(url_for('main.index'))
	

	
#重新发送账户确认邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email,'Confirm your Account','auth/email/confirm',user=current_user,token=token)
	flash('A new confirmation email has been sent to your email.')
	return redirect(url_for('main.index'))