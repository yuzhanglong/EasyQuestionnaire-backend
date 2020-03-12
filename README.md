# EasyQuestionnaire-backend

#### 此项目是问卷调查平台的后端项目 基于Python的flask框架



#### 前端项目请移步：

##### (web端) https://github.com/yuzhanglong/EasyQuestionnaire-web
##### (小程序端) 正在做



## 项目结构
```
questionnaire-back
├─ .gitignore
├─ README.md
├─ app
│  ├─ api  // 接口相关
│  │  ├─ utilsApi.py
│  │  ├─ v1
│  │  │  ├─ users.py
│  │  │  ├─ utils.py
│  │  │  ├─ __init__.py
│  │  │  ├─ analysis.py
│  │  │  ├─ completes.py
│  │  │  └─ questionnaires.py
│  │  ├─ error   // 全局错误处理
│  │  │  ├─ exceptions.py
│  │  │  ├─ baseHandler.py
│  │  │  └─ errorHandler.py
│  ├─ utils   // 工具相关
│  │  ├─ emailtools.py
│  │  ├─ placeFinder.py
│  │  ├─ templateMaker
│  │  │  ├─ spiders
│  │  │  │  ├─ spider.py
│  │  │  │  └─ wenjuanwang.py
│  │  │  └─ templateMaker.py
│  │  ├─ auth
│  │  │  ├─ auth.py
│  │  │  └─ authHelp.py
│  │  ├─ betterPrint
│  │  │  └─ betterPrint.py
│  │  ├─ timeHelper
│  │  │  └─ timeHelper.py
│  │  ├─ qrCode.py
│  │  └─ dataCalculate.py
│  ├─ static   // 静态资源
│  ├─ config   // 配置相关
│  │  ├─ database.py
│  │  └─ baseConfig.py
│  ├─ models   // 模型
│  │  ├─ user.py
│  │  ├─ problem.py
│  │  ├─ complete.py
│  │  ├─ resolution.py
│  │  ├─ questionnaire.py
│  │  └─ basicInfo.py
│  ├─ validators  // 表单验证相关
│  │  ├─ base.py
│  │  ├─ forms.py
│  │  └─ completeForm.py
│  ├─ __init__.py
│  └─ extensions.py   // flask扩展
├─ requirements.txt
├─ gunicorn.py
├─ questionnaire.conf
├─ flask部署总结笔记.md
├─ manage.py
```



## 安装（开发环境）

### 进入安装目录
```
cd /安装目录
```

### clone项目

```
git clone https://github.com/yuzhanglong/EasyQuestionnaire-backend.git
```

### 进入程序目录
```
cd /程序目录
```

### 创建虚拟环境
```
virtualenv venv
```

### 进入虚拟环境
```
source venv/bin/activate
```

### 安装依赖
```
pip install -r requirements.txt
```



## 部署

##### 请参考本项目下的 [flask部署总结笔记.md]([https://github.com/yuzhanglong/questionnaire-back/blob/master/flask%E9%83%A8%E7%BD%B2%E6%80%BB%E7%BB%93%E7%AC%94%E8%AE%B0.md](https://github.com/yuzhanglong/questionnaire-back/blob/master/flask部署总结笔记.md))



## 常见问题

##### 如果开发环境下开启了flask的debug模式 可能无法运行定时任务



## 其他

#### 当前功能：

##### 1.登录注册 邮箱验证 等用户的基本操作

##### 2.创建问卷以供填报（支持题型：单选题 多选题 填空题 下拉题）

##### 3.对你当前所拥有的问卷进行增删改  支持问卷模板一键生成问卷

##### 4.问卷发布功能（基本的发布/停止发布功能 设置问卷密码 限制ip或者设备重复访问）

##### 5.问卷数据分析 对某个问卷收集的数据进行数据可视化分析
