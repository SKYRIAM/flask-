from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from . import auth
from ..models import User
from .forms import LoginForm,RegistrationForm,ChangePasswordForm,PasswordResetRequestForm,PasswordResetForm,ChangeEmailForm
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
	#print(form.data['email'])
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
	#print('confirm!')
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
	
#修改密码功能
@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('invaild password')
    return render_template('auth/change_password.html',form=form)
		
#忘记密码
@auth.route('/reset',methods=['GET','POST'])	
def  password_reset_request():    #发送邮件
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()  #查看邮箱是否存在
        if user:
            token = user.generate_reset_token() #生成验证链接
            send_email(user.email,'Confirm Your Account','auth/email/reset_password', user=user,token=token) #发送邮件
            flash('An email with instructions to reset your password has been '
              'sent to you.')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

#更换密码
@auth.route('/reset/<token>',methods=['GET','POST'])  
def password_reset(token):
    if not current_user.is_anonymous():
        print('asasas')
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if  User.reset_password(token,form.password.data):
            db.session.commit()  #向数据库提交数据
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)
    
#修改邮箱功能
@auth.route('/change_email',methods=['GET','POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():   #验证验证器
        if current_user.verify_password(form.password.data):  #验证密码
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)  #生成token
            send_email(new_email,'Confirm your new email ','auth/email/change_email',user=current_user,token=token)#发送邮件
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))  #返回主界面
        else:
            flash('invaild password or email')
    return render_template("auth/change_email.html", form=form)  #感觉有问题
    
#生成新邮箱验证地址
@auth.route('/change_email/<token>')    
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
        
	