from flask import Blueprint
#实例化对象，创造蓝本
main = Blueprint('main',__name__)#蓝本的名字和蓝本所在的包或模块

from.import views,errors#导入模块将路由和错误处理联系起来
