import unittest
import time
from app.models import User
from app import create_app,db

class UserModelTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		
		
	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()
		
	def test_password_setter(self):
		u = User(password = 'cat')
		self.assertTrue(u.password_hash is not None)
	def test_no_password_getter(self):
		u = User(password = 'cat')
		with self.assertRaises(AttributeError):  #访问不可访问的属性时，验证抛出的异常是否是定义好的
			u.password
	
	def test_password_verification(self):
		u = User(password='cat')
		self.assertTrue(u.verify_password('cat'))
		self.assertFalse(u.verify_password('dog'))
	
	def test_password_salts_are_randow(self):
		u = User(password='cat')
		u2 = User(password='cat')
		self.assertTrue(u.password_hash != u2.password_hash)
	
	#测试验证成功
	def test_valid_confirmation_token(self):
		u = User(password='cat')
		db.session.add(u)
		db.session.commit()
		token = u.generate_confirmation_token()
		self.assertTrue(u.confirm(token))
		
	#测试验证错误
	def test_invaild_confirmation_token(self):
		u1 = User(password='ccc')
		u2 = User(password = 'ccc')
		token1 = u1.generate_confirmation_token()
		token2 = u2.generate_confirmation_token()
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		self.assertFalse(u1.confirm(token2))
	#验证时效性	
	def test_expired_confirmation_token(self):
		u = User(password='cat')
		db.session.add(u)
		db.session.commit()
		token = u.generate_confirmation_token(1)
		time.sleep(2)
		self.assertFalse(u.confirm(token))
		
	
	