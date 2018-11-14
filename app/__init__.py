from flask import Flask ,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
#******登录
login_manager = LoginManager()
login_manager.session_protection = 'strong'#设置安全等级
login_manager.login_view = 'auth.login' #设置登录视图名称

#工厂函数,config.from_object,init_app
def create_app(config_name):   #调用的时候才会创建实例，想创建多少就调用多少，每次调用都可以配置不同参数
	app = Flask(__name__)
	app.config.from_object(config[config_name])  #导入配置信息
	config[config_name].init_app(app)  #调用init_app静态方法
	
	bootstrap.init_app(app)   #Flasky自带的初始化方法
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	#*****注册蓝本
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	
	#*****注册附加蓝本
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint,url_prefix='/auth')
	#url_prefix 注册后蓝本中的路由都会加上指定的前缀，/login -> /auth/login

	return app

	