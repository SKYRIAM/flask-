
import unittest

from flask import current_app
from app import create_app,db
from app.models import User

class BasicsTestCase(unittest.TestCase): #从unittest.TestCase集成的class就是一个测试案例
#setUp()该测试用例执行前的设置工作、 
#tearDown()该测试用例执行后的清理工作、
	def setUp(self):
		self.app=create_app('testing')  #配置测试环境的数据库  #没有懂self.app
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()
	
	def test_app_exists(self):   #测试案例
		self.assertFalse(current_app is None)
		
	def test_app_is_testing(self):
		self.assertTrue(current_app.config['TESTING'])
		


 
		
		