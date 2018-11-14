from . import mail
from flask import render_template,current_app
from flask_mail import Message
from threading import Thread

def send_async_email(app,msg):
	with app.app_context():   #激活应用上下文
		mail.send(msg)
		
def send_email(to,subject,template,**kwargs):#收件人地址，主题，渲染邮件正文模块和关键字参数列表
	app = current_app._get_current_object()
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
	sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])  
	msg.body = render_template(template+'.txt',**kwargs)
	msg.html = render_template(template+'.html',**kwargs) #将发送函数移到后台进程
	thr = Thread(target=send_async_email,args=[app,msg])
	thr.start()
	return thr