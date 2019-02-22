### SQL 审计系统

仓库地址:

```
https://gitlab.***.com/devops/DevOpsPlatForm.git
```



配置文件

```
DevOpsPlatForm/audit/settings.py
```



rabbit MQ

```
BROKER_URL = 'amqp://root:root@172.16.130.207:5672/sql'


```



mysql 配置

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'audit',
        'USER': 'sqlaudit',
        'PASSWORD': 'Fs9006',
        'HOST': '172.16.130.207',
        'PORT': '13306',
    },
}
```





目前最新的docker images

 仓库里面有ci 文件， 提交后会自动构建image

 ```
registry.boyait.9fwealth.com:1443/devops/devopsplatform:77e36
 ```

启动

```
docker run -d -p 8000:8000 \
registry.boyait.9fwealth.com:1443/devops/devopsplatform:77e36
```



注意事项

* 不适用于mycat.
* 不适用于myisam表



使用流程:

* 添加目标数据库
* 添加业务板块
* 新建用户，分配权限

默认审核流程

```mermaid
graph LR
A[普通开发] -->B(开发组长)

    B --> C{判断影响行数}

    C -->|>200行| D[流程审核通过]

    C -->|<200行| E[副总审核]
```

