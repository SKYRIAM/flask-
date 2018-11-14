import os
basedir = os.path.abspath(os.path.dirname(__file__))   #获取目录的绝对路径

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
	MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
	MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() in \
		['true', 'on', '1']
	MAIL_USERNAME = 'putdowncat@163.com'#
	MAIL_PASSWORD = '123456aa'
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'putdowncat@163.com'
	FLASKY_ADMIN = 'putdowncat@163.com'
	DEFAULT_FROM_EMAIL='putdowncat@163.com'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	'''
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flaksy]'
	FLASKY_MAIL_SENDER = 'putdowncat@163.com'
	FLASKY_ADMIN = 'putdowncat@163.com'
	DEBUG = True
	Mail_SERVER = 'smtp.163.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'putdowncat@163.com'#os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD ='123456aa' #os.environ.get('MAIL_PASSWORD')'''
	
	@staticmethod  #静态方法
	def init_app(app):
		pass
	
class DevelopmentConfig(Config):
	
	SQLALCHEMY_DATABASE_URI =os.environ.get('DEV_DATABASE_URI') or \
		'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')#指定文件位置和文件名
		
class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI =os.environ.get('TEST_DATABASE_URI') or \
		'sqlite:///'+os.path.join(basedir,'data-test.sqlite')#指定文件位置和文件名
		
class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URI') or \
		'sqlite:///'+os.path.join(basedir,'data.sqlite')#指定文件位置和文件名
		
#config字典

config = {
		'development': DevelopmentConfig,
		'testing':TestingConfig,
		'production':ProductionConfig,
		'default':DevelopmentConfig
		}
	