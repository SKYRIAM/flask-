from datetime import datetime
from flask import render_template,session,redirect,url_for,current_app

from .import main
from .forms import NameForm
from .. import db
from ..models import User
from email import *

@main.route('/',methods=['GET','POST'])
def index():
	#name=None
	form = NameForm()
	if form.validate_on_submit():#会便捷地检查该请求是否是一个 POST 请求以及是否有效。
		user = User.query.filter_by(name=form.name.data).first()
		print(user)
		if user is None:
			user = User(name=form.name.data)
			db.session.add(user)
			session['known']=False
			
			if current_app.config['FLASKY_ADMIN']:
				print(current_app.config['FLASKY_ADMIN'])
				send_email(current_app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
				
		else:
			session['known']=True
		session['name']=form.name.data
		form.name.data=''
		return redirect(url_for('.index'))
	
			
		#old_name=session.get('name')
		#if old_name is not None and old_name != form.name.data:
		#	flash('Looks like you hava changed your name')
		session['name']=form.name.data
		#return redirect(url_for('index'))
		
		#session['name']=form.name.data
		# return redirect(url_for('index'))
		#name = form.name.data
		#form.name.data=''
	return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))

'''@main.route('/',methods=['GET','POST'])

def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(name=form.name.data).first()
		print(form.name.data)
		if user is None:
			user = User(name=form.name.data)
			db.session.add(user)
			db.session.commit()
			session['known'] = False
		else:
			session['known'] = True
			session['name'] = form.name.data
			return redirect(url_for('.index'))#当前请求所在的蓝本,如果需要跨蓝本则使用带有命名空间的端点名
			
	return render_template('index.html',
							form=form,name=session.get('name'),
							known=session.get('known',False),current_time=datetime.utcnow())
'''