# 1.让celery加载工程中的配置文件
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')
# 2.创建celery对象，参数一般采用工程名
from celery import Celery
app = Celery('meiduo_mall')
# 3.让celery设置broker队列,参数为配置文件的路径
app.config_from_object('celery_tasks.config')
#4.设置任务
# 1.任务本质是一个函数
# 2.这个函数必须要被celery的实列对象的tsak装饰器装饰
# 3.必须调用celery实例对象的自动检测来检测任务

# 5.让celery自动检测任务，参数是列表，列表元素为任务的包的路径
app.autodiscover_tasks(['celery_tasks.sms'])

#6.设置消费者（worker）,celery -A celery实例对象文件 worker -l info
# celery -A celery_tasks.main worker -l info