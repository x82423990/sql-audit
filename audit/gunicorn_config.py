# 配置服务器的监听ip和端口
bind = '0.0.0.0:8000'
# 以守护进程方式运行
daemon = True
# worker数量
workers = 2
# 错误日志路径
errorlog = '/var/log/gun_error.log'
# 访问日志路径
accesslog = '/var/log/gun_access.log'
