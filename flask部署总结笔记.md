

## flask部署总结笔记



### 处理虚拟环境

建立虚拟环境

```
virtualenv -p /usr/bin/python3 venv
```

激活虚拟环境

```
source venv/bin/activate
```

安装依赖

```
pip install -r requirements.txt
```

ps.   requirements.txt的生成方式

```
pip freeze > requirements.txt
```



### 处理gunicorn

撰写配置文件（此处比较简略 如要查看完成的配置文件样例 请参阅官方配置样例）位于项目根目录下

https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

```python
# gunicorn.py

bind = '127.0.0.1:5001'  # 绑定ip和端口号

workers = 1  # 进程数
threads = 2  # 指定每个进程开启的线程数
loglevel = 'debug'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
daemon = True  # 守护进程
accesslog = "/home/ubuntu/questionnaire/log/gunicorn_access.log"  # 访问日志文件
errorlog = "/home/ubuntu/questionnaire/log/gunicorn_error.log"  # 错误日志文件
```

进入服务器虚拟环境 安装gunicorn

```
pip install gunicorn
```

运行app 左边的manage是你的py文件名 右边的app是你的文件里的app名

```
gunicorn -c gunicorn.py manage:app
```



### 处理nginx

撰写配置文件 位于项目根目录下

```nginx
server {
    listen       80;
    server_name  api.yuzzl.top;
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_redirect off;
        proxy_set_header Host $host:80;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

寻找nginx安装目录 修改nginx.conf  定位到此处 添加一项

```nginx
	##
	# Virtual Host Configs
	##

	include /etc/nginx/conf.d/*.conf;
	include /etc/nginx/sites-enabled/*;
	//下面就是你要添加的 来自你的项目目录
	include /home/ubuntu/questionnaire/questionnaire.conf; 
```

执行命令

停止nginx服务

```
service nginx stop
```

开启nginx服务
```
service nginx stop
```



### 附

杀死gunicorn

输出进程树

```
pstree -ap | grep gunicorn
```

找到对应的pid 执行

```
kill -9 pid
```



yuzhanglong

记于2020年2月6日00:31:21