from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import login_required
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


'''#保护路由只让认证用户访问
@app.route('/secret')
@login_required
def secret():
		return 'Only authenticated users are allowed!'
'''
	
class Role(db.Model):
	__tablename__ = 'roles'     #表名
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique = True)
	users = db.relationship('User',backref = 'role')
	#db.relationship()用于在两个表之间建立一对多关系。例如书中 roles 表中一个 User 角色，可以对应 users 表中多个实际的普通用户
	#。实现这种关系时，要在“多”这一侧加入一个外键，指向“一”这一侧联接的记录。
	#backref 定义反向关系
	def __repr__(self):
		return '<Role %s>' % self.name  #返回一个字符表示模型
	
class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key=True)
	#email = db.Column(db.String(64),unique=True,index=True)
	#name = db.Column(db.String(64),unique = True,index=True)#不允许出现重复的值，并为这列添加索引
	email = db.Column(db.String(64),index=True)
	name = db.Column(db.String(64),index=True)
	password_hash=db.Column(db.String(128))
	confirmed = db.Column(db.Boolean,default = False)  #判断是否认证
	role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))  #建立和role表的关系
	@property   #定义password类属性方法
	def password(self):  
		raise AttributeError('password is not a readable attribute')   #?
		
		
	@password.setter   #对password进行赋值
	def password(self,password):
		self.password_hash = generate_password_hash(password)#输出密码的散列值
		
	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)#验证用户输入的密码和散列值
		
	def __repr__(self):
		return '<User %s>' % self.name
		
	# 确认用户 
	#加密
	def generate_confirmation_token(self,expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'],expiration)
		return s.dumps({'confirm':self.id}) #使用confirm存储self.id，生成加密签名
	#解密，认证
	def confirm(self,token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		if data.get('confirm') != self.id:   #验证加密签名
			return False
		self.confirmed = True
		db.session.add(self)
		return True
		
#要使用Flask-Login扩展，你必须在数据库模型文件(models.py)中提供一个回调函数user_loader，
#这个回调函数用于从会话中存储的用户ID重新加载用户对象。它应该接受一个用户的id作为输入，返回相应的用户对象。
@login_manager.user_loader
def load_user(user_id):
	try:
		return User.query.get(int(user_id))
	except:
		return None