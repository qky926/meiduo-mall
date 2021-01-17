#4.设置任务
# 1.任务本质是一个函数
# 2.这个函数必须要被celery的实列对象的task装饰器装饰
# 3.必须调用celery实例对象的自动检测来检测任务
from celery_tasks.main import app
from libs.yuntongxun.sms import CCP

@app.task
def send_sms_code(mobile,smscode):
    CCP().send_template_sms(mobile, [smscode, 5], 1)  # 发送验证码

