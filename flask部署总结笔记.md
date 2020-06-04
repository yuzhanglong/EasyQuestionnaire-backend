# flask部署总结笔记

## 旧的部署方法不推荐了!!!因为略显麻烦，且一不小心容易出错，强烈建议使用docker，轻松、快速、幸福地部署本项目，满满的幸福感～
## PS.学习docker可以前往docker官网，或者【菜鸟教程】网站，附链接:https://www.runoob.com/docker/docker-tutorial.html



## 在docker上部署项目


**安装docker**

**docker**的安装十分简单，你只需要执行一行命令：

```sh
sudo yum install docker
```



**构建镜像**

通过本地的dockerfile**构建一个镜像**，请进入(CD到)**项目主目录**，执行：

```sh
docker build -t questionnaire:1.0
```

其中，【questionnaire】为**项目镜像名**，1.0为**项目版本号**，可以自行设置



**运行容器**

```shell
docker run -p 8080:5001 questionnaire:1.0
```

项目将myschool **容器内**暴露出的端口（**5001**）映射到**本地服务器**端口（**8080**）上



**测试部署**

访问服务器的**8080**端口，如果返回以下信息，说明部署完成：

```json
{
    "errorCode": 0,
    "message": "Your project is running successfully!"
}
```



附：下面是本项目的**dockerfile**文件，在**项目根目录**下，可以将项目打包成镜像，**一般不需要修改**:

```dockerfile
FROM python:3.8
COPY . .
WORKDIR .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["gunicorn", "-c", "gunicorn.py", "manage:app"]
EXPOSE 5001
```



下面是本项目的**gunicorn**配置文件，在**项目根目录**下:

```python
bind = '127.0.0.1:5001'  # 绑定ip和端口号

workers = 1  # 进程数
threads = 2  # 指定每个进程开启的线程数
loglevel = 'debug'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
accesslog = "/home/ubuntu/questionnaire/log/gunicorn_access.log"  # 访问日志文件
errorlog = "/home/ubuntu/questionnaire/log/gunicorn_error.log"  # 错误日志文件
```



## 设置转发

进行如上操作后，项目部署在了docker容器的**5001**端口，然后映射到服务器的**8080**端口
之后你可以利用nginx进行转发：

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



## 以下是一般方法（不推荐）

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
daemon = True  # 守护进程，这里如果你是使用docker部署的，请不要添加
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



### 设置转发

请参阅上方docker部署的【设置转发】条目。



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

更新于2020年6月5日00:27